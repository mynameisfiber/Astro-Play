require './command_generator'
require 'socket'
require 'json'

# @singlecmd = JSON.parse( open(File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json').read )
single_cmd_input = File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json'
single_cmd_output = File.dirname(__FILE__) + '/json_samples/1_command/5-robot_input-1cmd.json'
square_cmd_input = File.dirname(__FILE__) + '/json_samples/square_command/3-translator_output-square.json'
square_cmd_output  = File.dirname(__FILE__) + '/json_samples/square_command/5-robot_input-square.json'
while_cmd_input = File.dirname(__FILE__) + '/json_samples/while_command/3-translator_output-while.json'
while_cmd_output = File.dirname(__FILE__) + '/json_samples/while_command/5-robot_input-while.json'

describe 'command parser' do 

  it 'translates single command scenario input into expected Astrobot JSON object' do
    parse_to_astrobot( single_cmd_input )
    expect( @output ).to eq( JSON.parse( open( single_cmd_output ).read ) )
  end

  it 'translates square command scenario input into expected Astrobot JSON object' do
    parse_to_astrobot( square_cmd_input )
    expect( @output ).to eq( JSON.parse( open( square_cmd_output ).read ) )
  end

  it 'translates while command scenario input into expected Astrobot JSON object' do
    parse_to_astrobot( while_cmd_input )
    expect( @output ).to eq( JSON.parse( open( while_cmd_output ).read ) )
  end

  

end