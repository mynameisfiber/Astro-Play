=begin

  Module receives JSON output from interpreter, converts series of commands into 
  executable instructions for robot. 

  built in Ruby version 2.1.3p242 ( 2014-09-19 revision 47630 ) [ x86_64-darwin13.0 ]
  requires only standard libraries.

=end

# Libraries for access to the underlying operating system http implementations; included in standard Ruby library
require 'net/http'
require 'uri'
require 'socket'
# library for JSON implementation; included in standard Ruby library
require 'json'

# Class defined for compartmentalization
class CommandGenerator

  # Stardard initialization as part of generating class object; requires JSON file to be interpreted for object creation
  def initialize( data )
    # Assign the opened and parsed JSON object to @object instance variable
    @object = JSON.parse( data )
    # Uncomment for test suite
    # @object = JSON.parse( open( data ).read )
    # Collection of Regexp structures for parsing; any added structures will need to be added in least common to most common order
    # to prevent more common structures from being plucked out of the middle of less common structures
    @structures = [  /((while|for|if|elsif) (x|y) (>|<|>=|<=|==|%|\+|-|\*|\/|\*\*) [0-9]+ (== ([0-9]+|(x|y)))?)/,
                        # catches for, while, and if through a number 0-9 inclusive with optional modulo with arithmatic and subsequent comparison
                    /(((x =)|(y =)) [0-9]+)|(((x =)|(y =)) ... [0-9]+)/,
                        # catches assignments of x/y to a single number 0-9 including x = x + 1 format
                    /((f|b|l|r) (- )?(10|20|30|40|50|60|70|80|90))/,
                        # catches robot commands, units only in tens
                    /(end)|(else)/ ]
                        # catches 'end' and 'else', any and all use cases 
    # Command string to be formatted and passed to robot in the event of non-executable input
    @rescue = "output.push( 'r 10' ); output.push( 'l 10' ); output.push( 'r 10' ); output.push( 'l 10' )"
    # Adds flow control method to the end of initilazation to begin command parsing and generation
    parse_to_astrobot
  end

  # Flow control
  def parse_to_astrobot
    # Pull pertinent data from JSON input ( details in function below )
    pull_commands
    # Break command string into lines ( details in function below )
    parse_string
    # Reassemble and eval command string for output commands ( details in function below )
    eval_string
    # Format into output JSON object ( details in function below )
    json_formatter
  end

  # Pull pertinent data from JSON input; puts all tokens into @raw_command_string
  def pull_commands
    # Array to hold/sort hash values
    hash_holder = []
    # Create instance variable to hold a raw string of commands
    @raw_command_string = ""
    # Go through the JSON object, and for each of the token_values
    @object.each do | key, token |
      # Check to see if the last character added to the @raw_command_string instance variable was part of a multi-digit number
      if hash_holder[ -1 ] && /[0-9]/.match( hash_holder[ -1 ][ 1 ] ) != nil && /[0-9]/.match( token ) != nil
        # Combine last two numbers
        token = "#{ hash_holder[ -1 ][1] }#{ token }"
        # Delete redundant number
        hash_holder.delete_at( -1 )
      end
      # ... add the value to the @raw_command_string instance variable
      hash_holder << [ key, token ] if  token != nil || token != ""
    end
    # Sort array by key
    hash_holder.sort { | a, b| a[ 0 ] <=> b[ 0 ] }.each do | pair |
      # Delete index from final array
      pair.delete_at( 0 )
    end
    # Convert array to formatted string
    @raw_command_string = hash_holder.flatten.join( " " )
  end

  # Break command string into lines
  def parse_string
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
    # Check for non-valid structures, throw error
    if @raw_command_string.gsub( /~/, "" ).gsub( / /, "" ).length > 0
      # If there are any uncaught ( invalid ) block structures, set to false for error handling
      @parsed_command_string = false
    else
      # Assign to new instance variable a sorted multidimensional array consisting of all found command structures in 
      # order of execution
      @parsed_command_string = parse_string_holder.sort
    end
  end

  # Reassemble and eval command string for output commands
  def eval_string
    # Local holder for executable code strings
    eval_string_holder = []
    # Local holder for final JSON output code
    output = []
    # Check for invalid command sequence from above
    if @parsed_command_string
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
   else
    # Beep
    print "\a"
    # Rescue sequence
    eval( @rescue )
  end
    # Assign the contents of the output holder array ( formatted robot commands )to new @command_array 
    # instance variable for access below
    @command_array = output
  end

  # Format into output JSON object
  def json_formatter
    # Create hash formatted to robot's API for final output with empty "command_values" array
    # json_output = { "robot_commands" => @command_array.length, "command_values" => [] }
    json_output = { }
    # Loop through the @command_array instance variable created above
    command_body = @command_array.each do | command |
      # Add a hash to the "command_values" array in the json_output hash for each robot instruction
      # json_output[ "command_values" ] << { "line" => "#{ @command_array.index( command ) }", "value" => "#{ command }" } 
      json_output[ "cmd#{ @command_array.index( command ) + 1 }" ] = "#{ command }" 
      # Set the array element to empty string so that the proper index is set above when it comes back around
      # in the event of duplicate instructions
      @command_array[ @command_array.index( command ) ] = ""
    end 
    # Convert json_output hash to JSON object, and assign to @output new instance variable
    @output = json_output.to_json
  end

end

class AstroBotServer


  IP_address_in = "192.168.43.153"
  port_in = 9999
  IP_address_out = "192.168.43.36"
  port_out = 8081

  server = TCPServer.new( IP_address_in, port_in )
  # server = TCPServer.new( "10.2.108.1", 9999 )
  STDERR.puts "Command Generator active."
  STDERR.puts "Address = http://#{IP_address_in}:#{port_in}"

  # Servers run forever
  loop {
    Thread.start( server.accept ) do | client |
      # Receive section
      # In this case, method = "POST" and path = "/"
      method, path = client.gets.split
      headers = {}
      # Collect HTTP headers
      while line = client.gets.split( ' ', 2 )
        # Blank line means no more headers
        break if line[ 0 ] == ""
        # Hash headers by type
        headers[ line[ 0 ].chop ] = line[ 1 ].strip
      end
      # Read the POST data as specified in the header
      data = client.read( headers[ "Content-Length" ].to_i )
      STDERR.puts "Connection received."
      STDERR.puts "Input @#{Time.now}:"
      STDERR.puts data
      response = "HTTP/1.1 200 OK\r\nContent-type: application/json\r\n\r\n"
      client.puts response
      client.close
      # Send section

      url1 = "http://#{IP_address_out}:#{port_out}/update"
      uri1 = URI.parse( url1 )
      http = Net::HTTP.new( uri1.host, uri1.port )
      payload = CommandGenerator.new( data ).instance_variable_get( :@output )
      request = Net::HTTP::Post.new( uri1.request_uri, initheader = { 'Content-Type' => 'application/json' } )
      request.body = payload
      resp = http.request( request )
      STDERR.puts "Output @#{Time.now}:"
      STDERR.puts payload
    end
  }
end

AstroBotServer.new()