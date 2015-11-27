=begin

  Module receives JSON output from interpreter, converts series of commands into 
  executable instructions for robot. 

=end

require 'socket'

# Config
@port = 9999

# Listener
server = TCPServer.new( @port )

# loop do

#   Thread.start( server.accept ) do | client |
#     client.astro_translate
#     client.close
#   end

# end

# Gooey bits
def astro_translate()

end