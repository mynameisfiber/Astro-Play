require './command_generator'
require 'socket'
require 'json'

# @singlecmd = JSON.parse( open(File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json').read )
singlecmd = File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json'
squarecmd = File.dirname(__FILE__) + '/json_samples/square_command/3-translator_output-square.json'
whilecmd = File.dirname(__FILE__) + '/json_samples/while_command/3-translator_output-while.json'

describe 'interpreter' do 

  it 'converts single command string for parsing' do
    parse_to_astrobot( singlecmd )
    expect( @commands ).to eq( 'f 10' )
  end

  it 'converts square command string for parsing' do
    parse_to_astrobot( squarecmd )
    expect( @commands ).to eq( 'f 10 r 90 f 10 r 90 f 10 r 90 f 10 r 90' )
  end

  it 'converts while command string for parsing' do
    parse_to_astrobot( whilecmd )
    expect( @commands ).to eq( 'x = 1 while x < 4 f 10 r 90 x = x + 1 end' )
  end

  it 'test' do
    parse_to_astrobot( whilecmd )
    expect( @output ).to eq( "f 10 r 90 \nf 10 r 90 \nf 10 r 90 \nf 10 r 90" )
  end

end