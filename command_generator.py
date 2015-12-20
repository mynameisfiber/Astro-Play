import json
import re
from operator import itemgetter
import http.server
import http.client
import itertools as IT


STRUCTURES_STR = [
    # catches for, while, and if through a number 0-9 inclusive with optional
    # modulo with arithmatic and subsequent comparison
    r'((while|for|if|elsif) (x|y) (>|<|>=|<=|==|%|\+|-|\*|\/|\*\*) [0-9]+ (== ([0-9]+|(x|y)))?)',

    # catches assignments of x/y to a single number 0-9 including x = x + 1
    # format
    r'(((x =)|(y =)) [0-9]+)|(((x =)|(y =)) ... [0-9]+)',

    # catches robot commands, units only in tens
    r'((f|b|l|r) (- )?(10|20|30|40|50|60|70|80|90))',

    # catches 'end' and 'else', any and all use cases
    r'(end)|(else)',
]

# Now we take all the regexs defined in STRUCTURES_STR and combine them into
# one compiled regex that can match for all the structures
STRUCTURES = re.compile(r'({})'.format('|'.join(STRUCTURES_STR)))


class InvalidCommand(Exception):
    """
    Exception for invalid commands in the command generator
    """
    def __init__(self, command, line=None):
        self.command = command
        self.line = line

    def __str__(self):
        if self.line:
            return "Invalid command on line {}: {}".format(
                self.line, self.command
            )
        return "Invalid command: {}".format(self.command)


class CommandGenerator(object):
    # Command string to be formatted and passed to robot in the event of
    # non-executable input
    FAIL = "r(10) l(10) r(10) l(10)".split(' ')

    def __init__(self, data):
        try:
            data_json = json.loads(data)
            commands = self._parse_commands(data_json)
            structures = self._parse_structure(commands)
            output = self._evaluate(structures)
        except Exception as e:
            print(e)
            output = self._evaluate(self.FAIL)
        finally:
            self.output = self._parse_output(output)

    def _parse_commands(self, translator_output):
        # sort translator output by the key value
        sorted_commands = sorted(
            translator_output.items(), 
            key=lambda item: int(item[0])
        )
        # extract the commands and filter out false-ish values
        commands_raw = filter(None, map(itemgetter(1), sorted_commands))
        # group sequences of numbers in the commands
        commands = []
        for is_numbers, command_group in IT.groupby(commands_raw, str.isdigit):
            if is_numbers:
                commands.append("".join(command_group))
            else:
                commands.extend(command_group)
        return " ".join(commands)

    def _parse_structure(self, commands):
        # structures start as a mapping from "start index of structure" =>
        # "structure code"
        structures = {}
        # leftovers will get re-written with '#' to mark sections we have
        # already found
        leftover = commands
        # use the STRUCTURES regex to find all structures in the inputted
        # command
        for match in STRUCTURES.finditer(commands):
            start, end = match.span(0)
            structures[start] = match.group(0).strip()
            leftover = leftover[:start] + '#' * (end-start) + leftover[end:]
        # if leftovers is only # and spaces then it only contains valid
        # structures
        leftover = leftover.strip("# ")
        if leftover:
            raise InvalidCommand(leftover)
        # sort the structures on their starting indexes from the original
        # commands string
        structures_sorted = sorted(structures.items(), key=itemgetter(0))
        return map(itemgetter(1), structures_sorted)

    def _translate_structures(self, commands):
        """
        The following is terrible code that only god can forgive us for.  It
        translate the pseudo-code recived from the translator into python.
        """
        structure = []
        depth = 0
        for i, command in enumerate(commands):
            # in python, 'elsif' is 'elif'
            command = command.replace("elsif", "elif")
            if command[:2].isalpha():
                # append collon at end of control structures
                command += ":"
            elif any(command.startswith(f + ' ') for f in 'fblr'):
                # turn calls to f,b,l and r into actual function calls
                command = "{}({})".format(command[0], command[1:])
            if command.startswith('end'):
                # 'end' structure decreases the python depth
                depth -= 1
                # we skip the rest of the loop to skip adding this to the
                # structure list
                continue
            elif any(command.startswith(f) for f in ('else', 'elif')):
                # 'else' and 'elif' structure decreases the python depth
                depth -= 1
            # add the current command at the correct depth
            structure.append("\t"*depth + command)
            if any(command.startswith(f) for f in
                    ('if', 'while', 'for', 'else', 'elif')):
                # anything after a 'if', 'while', 'for', 'else' or 'elif'
                # should be at an increased depth
                depth += 1
        return structure

    def _evaluate(self, structures):
        # translate structures into python
        structures = self._translate_structures(structures)
        # create an output array and pin calls to f/l/r/b into appends in this
        # output array
        output = []
        eval_globals = {
            'f': lambda x: output.append('f ' + str(x)),
            'l': lambda x: output.append('l ' + str(x)),
            'r': lambda x: output.append('r ' + str(x)),
            'b': lambda x: output.append('b ' + str(x)),
        }
        # execute the structures in a controlled environment that only contains
        # our patched f/l/r/b functions
        exec("\n".join(structures), eval_globals, {})
        return output

    def _parse_output(self, output):
        return {'cmd'+str(i): cmd for i, cmd in enumerate(output, 1)}

    def __str__(self):
        return json.dumps(self.output)


class HTTPHandler(http.server.BaseHTTPRequestHandler):
    output_server = None

    def do_POST(s):
        """
        Read the data from the post request (in UTF-8 encoding) and pushes the
        result to the server given by the 'output_server' class variable
        """
        print("Processing request")
        data_length = int(s.headers['Content-Length'])
        data = s.rfile.read(data_length).decode("utf-8")
        commands = CommandGenerator(data)

        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()

        conn = http.client.HTTPConnection(*s.output_server)
        conn.request("PUT", "/update", str(commands))
        conn.close()


if __name__ == "__main__":
    input_server = ("127.0.0.1", 9999)
    output_server = ("127.0.0.1", 8081)

    HTTPHandler.output_server = output_server
    httpd = http.server.HTTPServer(input_server, HTTPHandler)
    print("Command Generator active.")
    print("Address = http://{}:{}".format(*input_server))
    httpd.serve_forever()
