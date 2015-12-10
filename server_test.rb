require 'net/http'
require 'uri'
require 'socket'
# library for JSON implementation; included in standard Ruby library
require 'json'

def post
  url = "http://" + @host_out + ":" + @port_out + "/" + @path_out
  uri = URI.parse( url )
  http = Net::HTTP.new( uri.host, uri.port )

  payload = open( File.dirname( __FILE__ ) + '/json_samples/1_command/3-translator_output-1cmd.json' ).read
  
  request = Net::HTTP::Post.new( uri.request_uri, initheader = { 'Content-Type' => 'application/json' } )
  request.body = payload
  resp = http.request( request )
end

post