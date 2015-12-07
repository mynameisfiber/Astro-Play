"""

  Module receives JSON output from interpreter, converts series of commands into 
  executable instructions for robot. 

  built in Ruby version 2.1.3p242 ( 2014-09-19 revision 47630 ) [ x86_64-darwin13.0 ]
  requires only standard libraries.

"""

# library for access to the underlying operating system socket implementations; included in standard Ruby library
import socket
# library for JSON implementation; included in standard Ruby library
import json
# library for regular expressions
import re

# Class defined for compartmentalization
class CommandGenerator( object ):

  # Stardard initialization as part of generating class object; requires JSON file to be interpreted for object creation
  def __init__( self, file ):
    # Assign the opened and parsed JSON object to @object instance variable
    self.object = open( file ) 
    # Collection of Regexp structures for parsing; any added structures will need to be added in least common to most common order
    # to prevent more common structures from being plucked out of the middle of less common structures
    self.structures = [  re.compile('((while|for|if|elsif) (x|y) (>|<|>=|<=|==|%|\+|-|\*|\/|\*\*) [0-9]+ (== ([0-9]+|(x|y)))?)'),
                        # catches for, while, and if through a number 0-9 inclusive with optional modulo with arithmatic and subsequent comparison
                    re.compile('(((x =)|(y =)) [0-9]+)|(((x =)|(y =)) ... [0-9]+)'),
                        # catches assignments of x/y to a single number 0-9 including x = x + 1 format
                    re.compile('/((f|b|l|r) (- )?(10|20|30|40|50|60|70|80|90))'),
                        # catches robot commands, units only in tens
                    re.compile('/(end)|(else)') ]
                        # catches 'end' and 'else', any and all use cases 
    # Command string to be formatted and passed to robot in the event of non-executable input
    self.rescue = "output.push( 'r 10' ); output.push( 'l 10' ); output.push( 'r 10' ); output.push( 'l 10' )"
    # Adds flow control method to the end of initilazation to begin command parsing and generation
    self.parse_to_astrobot
  

  # Flow control
  def parse_to_astrobot(self):
    # Pull pertinent data from JSON input ( details in function below )
    self.pull_commands(self)
    # Break command string into lines ( details in function below )
    self.parse_string(self)
    # Reassemble and eval command string for output commands ( details in function below )
    self.eval_string(self)
    # Format into output JSON object ( details in function below )
    self.json_formatter(self)
    # Send final formatted JSON object to robot ( details in function below )
    # Pending
    # self.send_to_astro_bot
  

  # Pull pertinent data from JSON input; puts all tokens into @raw_command_string
  def pull_commands(self):
    # Create instance variable to hold a raw string of commands
    self.raw_command_string = ""
    # Go through the JSON object, and for each of the token_values
    for token in self.object[ 'token_values' ]:
      # Check to see if the last character added to the @raw_command_string instance variable was part of a multi-digit number
      if re.match('[0-9]', self.raw_command_string[ -2 ] ) and re.match('[0-9]', ( token[ 'token' ] ) )
        # Remove the extra space at the end
        self.raw_command_string = self.raw_command_string[ 0 ... -1 ]
      # ... add the value to the @raw_command_string instance variable
      self.raw_command_string << "#{ token[ 'token' ] } " if  token[ 'token' ] != nil
    end
  

  # Break command string into lines
  def parse_string(self):
    # Local array ( multidimensional ) to hold code structures
    parse_string_holder = []
    # Loop through each of the regular expressions in the @structures instance variable array
    @structures.each do | structure |
      # Check to see if the structure can be found in the @raw_command_string created in the previous method call
      if structure.match( @raw_command_string )
        # If any were found, loop through the found objects
        @raw_command_string.scan( structure ).each do | caught |
          # Pull out the longest array element corresponding to the whole found string
          # this is necessary due to the way Ruby handles results from a regex search; creating a MatchData
          # object which can be read and treated as an array
          found = caught.to_a.compact.max_by( &:length )
          # Find the starting point in the @raw_command_string instance variabl array using the found string as the
          # basis for a new regex.
          start = /#{ Regexp.quote( found ) }/.match( @raw_command_string ).begin( 0 )
          # Holder for substitution string
          substitute = ""
          # Create substitution string using least common character I could think of, if it proves necessary, this can
          # be swapped out for any other single character in the event "~" is needed down the road
          found.length.times { substitute << "~" }
          # Replace the structure in the original string ( ! = dustructive, meaning it changes the orignal object ) 
          # with the substitute string to prevent duplication
          @raw_command_string.sub!( structure,  substitute )
          # Add subarray to holder array consisting of the starting point ( for sorting ) and the found string
          parse_string_holder << [ start, found ]
        end
      end
    end
    # Assign to new instance variable a sorted multidimensional array consisting of all found command structures in 
    # order of execution
    @parsed_command_string = parse_string_holder.sort
  

  # Reassemble and eval command string for output commands
  def eval_string(self):
    # Local holder for executable code strings
    eval_string_holder = []
    # Local holder for final JSON output code
    output = []
    # Go through the @parsed_command_string instance variable created above
    @parsed_command_string.each do | subcommand |
      # Checks to see if the commands are intended for the robot
      if subcommand[ 1 ].match( /((f|b|l|r) (10|20|30|40|50|60|70|80|90))/ )
        # Adds internal code to enable robot instructions to be inserted and appropriately formatted into the local output
        # holder array
        subcommand[ 1 ] = "output.push( '#{ subcommand[ 1 ] }' )"
      end
      # Adds code strings to be executed to local holder array
      eval_string_holder << subcommand[ 1 ]
    end
    # Combines the disparate bits of code with ";" line separation character
    executable = eval_string_holder.join( "; " )
    # Rescue loop
   begin
      # Execute code string
      eval( executable )
    # If there's an error...
   rescue Exception => exc
      # Execute the @rescue string instead ( defined in initilazation )
     eval( @rescue )
   end
    # Assign the contents of the output holder array ( formatted robot commands )to new @command_array 
    # instance variable for access below
    @command_array = output
  

  # Format into output JSON object
  def json_formatter(self):
    # Create hash formatted to robot's API for final output with empty "command_values" array
    json_output = { "robot_commands" => @command_array.length, "command_values" => [] }
    # Loop through the @command_array instance variable created above
    command_body = @command_array.each do | command |
      # Add a hash to the "command_values" array in the json_output hash for each robot instruction
      json_output[ "command_values" ] << { "line" => "#{ @command_array.index( command ) }", "value" => "#{ command }" } 
      # Set the array element to empty string so that the proper index is set above when it comes back around
      # in the event of duplicate instructions
      @command_array[ @command_array.index( command ) ] = ""
    end 
    # Convert json_output hash to JSON object, and assign to @output new instance variable
    @output = json_output.to_json
  

  # Output to robot
  def send_to_astro_bot(self):
    # Pending

# class AstroBotServer
#
#   # Socket to listen on port 9999
#   @server = TCPServer.open( 9999 )
#   # Servers run forever
#   loop {
#     Thread.start( @server.accept ) do | client |
#       # Read complete response
#       file = socket.read
#       @command_generator = CommandGenerator.new( file )
#       client.print( @command_generator.instance_variable_get( :@output ) )
#       # Disconnect from the client
#       client.close
#     end
#   }
#
# end