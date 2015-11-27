=begin

  Module receives JSON output from interpreter, converts series of commands into 
  executable instructions for robot. 

=end

require 'socket'
require 'json'

@object = ""
@commands = ""
@output = ""

def parse_to_astrobot( file )
  raw_json_string( file )
  pull_commands
  convert
end

def raw_json_string( file )
  @object = JSON.parse( open( file ).read )
end

def pull_commands
  string = ""
  @object[ 'token_values' ].each do | token |
    string << "#{ token[ 'token' ] } " if token[ 'token' ] != 'blank'
  end
  @commands = string[ 0 .. -2 ]
end

def convert
  holder = []
  eval("x = 0; while x < 4; holder.push( 'f 10 r 90' ); x = x + 1; end")
  @output = holder.join(" \n")
end