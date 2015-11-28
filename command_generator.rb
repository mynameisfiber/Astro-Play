=begin

  Module receives JSON output from interpreter, converts series of commands into 
  executable instructions for robot. 

=end

require 'socket'
require 'json'

class CommandGenerator

  def initialize( file )
    @object = JSON.parse( open( file ).read )
    @structures = [  /((while|for|if) ... [0-9])/,
                    /(((x =)|(y =)) [0-9])|(((x =)|(y =)) ... [0-9])/,
                    /((f|b|l|r) (10|20|30|40|50|60|70|80|90))/,
                    /(end)/ ]
    parse_to_astrobot
  end

  # Flow control
  def parse_to_astrobot
    pull_commands
    parse_string
    eval_string
    json_formatter
  end

  # Pull pertinent data from JSON input
  def pull_commands
    @raw_command_string = ""
    @object[ 'token_values' ].each do | token |
      @raw_command_string << "#{ token[ 'token' ] } " if  token[ 'token' ] != nil
    end
  end

  # Break command string into lines
  def parse_string
    holder = []
    @structures.each do | structure |
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
    @command_array = output
  end

  # Format into output JSON object
  def json_formatter
    json_output = { "robot_commands" => @command_array.length, "command_values" => [] }
    command_body = @command_array.each do | command |
      json_output[ "command_values" ] << { "line" => "#{ @command_array.index( command ) }", "value" => "#{ command }" } 
      @command_array[ @command_array.index( command ) ] = ""
    end 
    @output = json_output.to_json
  end

  # Output to robot
  def send_to_astro_bot

  end

end

# class AstroBotServer

#   @server = TCPServer.open( 9999 )      # Socket to listen on port 9999

#   loop {                                # Servers run forever
#     Thread.start( @server.accept ) do | client |
#       file = socket.read                # Read complete response
#       @command_generator = CommandGenerator.new( file )
#       client.print( @command_generator.instance_variable_get( :@output ) )
#       client.close                      # Disconnect from the client
#     end
#   }

# end