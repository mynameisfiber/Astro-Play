import json
import re
from operator import itemgetter
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
STRUCTURES = re.compile(r'({})'.format('|'.join(STRUCTURES_STR)))



class InvalidCommand(Exception):
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
            translator_output = json.loads(data)
            commands = self._parse_commands(translator_output)
            structures = self._parse_structure(commands)
            output = self._evaluate(structures)
        except Exception as e:
            print(e)
            output = self._evaluate(self.FAIL)
        finally:
            self.output = self._parse_output(output)
        print("OUTPUT: ", self.output)

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
        structures = {}
        leftover = commands
        for match in STRUCTURES.finditer(commands):
            start, end = match.span(0)
            structures[start] = match.group(0).strip()
            leftover = leftover[:start] + '#' * (end-start) + leftover[end:]
        leftover = leftover.strip("# ")
        if leftover:
            raise InvalidCommand(leftover)
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
            command = command.replace("elsif", "elif")  # pseudocode to python
            # append collon at end of control structures
            if command[:2].isalpha():
                command += ":"
            elif any(command.startswith(f + ' ') for f in 'fblr'):
                command = "{}({})".format(command[0], command[1:])
            if command.startswith('end'):
                depth -= 1
                # we skip the rest of the loop to skip adding this to the
                # structure list
                continue
            elif any(command.startswith(f) for f in ('else', 'elif')):
                depth -= 1
            structure.append("\t"*depth + command)
            if any(command.startswith(f) for f in ('if', 'while', 'for', 'else', 'elif')):
                depth += 1
        return structure

    def _evaluate(self, structures):
        structures = self._translate_structures(structures)
        output = []
        eval_globals = {
            'f': lambda x: output.append('f ' + str(x)),
            'l': lambda x: output.append('l ' + str(x)),
            'r': lambda x: output.append('r ' + str(x)),
            'b': lambda x: output.append('b ' + str(x)),
        }
        exec("\n".join(structures), eval_globals, {})
        return output

    def _parse_output(self, output):
        output_dict = {'cmd'+str(i): cmd for i, cmd in enumerate(output)}
        return json.dumps(output_dict)



if __name__ == "__main__":
    test = open("json_samples/fizz_buzz/3-translator_output-fizzbuzz.json").read()
    CommandGenerator(test)




