=begin

  Module receives JSON output from interpreter, converts series of commands into 
  executable instructions for robot. 

=end

require 'socket'
require 'json'

# Flow control
def parse_to_astrobot( file )
  raw_json_string( file )
  pull_commands
  parse_string
  eval_string
  json_formatter
end

# Temp holder values
@object = ""
@raw_command_string = ""
@parsed_command_string = []
@output = ""

# Access JSON object input
def raw_json_string( file )
  @object = JSON.parse( open( file ).read )
end

# Pull pertinent data from JSON input
def pull_commands
  string = ""
  @object[ 'token_values' ].each do | token |
    string << "#{ token[ 'token' ] } " if token[ 'token' ] != 'blank'
  end
  @raw_command_string = string[ 0 .. -2 ]
end

# Break command string into lines
def parse_string
  holder = []
  structures = [  /((while|for|if) ... [0-9])/,
                  /(((x =)|(y =)) [0-9])|(((x =)|(y =)) ... [0-9])/,
                  /((f|b|l|r) (10|20|30|40|50|60|70|80|90))/,
                  /(end)/ ]
  structures.each do | structure |
    if structure.match( @raw_command_string )
      @raw_command_string.scan( structure ).each do | caught |
        found = caught.to_a.compact.max_by( &:length )
        start = /#{ Regexp.quote( found ) }/.match( @raw_command_string ).begin( 0 )
        substitute = []
        found.length.times { substitute << "~" }
        @raw_command_string.sub!( structure,  substitute.join )
        holder << [ start, found ]
      end
    end
  end
  @parsed_command_string = holder.sort
end

# Reassemble and eval command string for output commands
def eval_string
  holder = []
  output = []
  @parsed_command_string.each do | subcommand |
    if subcommand[ 1 ].match( /((f|b|l|r) (10|20|30|40|50|60|70|80|90))/ )
      subcommand[ 1 ] = "output.push( '#{ subcommand[ 1 ] }' )"
    end
    holder << subcommand[ 1 ]
  end
  executable = holder.join( "; " )
  eval( executable )
  print output
end

# Format into output JSON object
def json_formatter

end

# Output to robot
def send_to_astro_bot

end