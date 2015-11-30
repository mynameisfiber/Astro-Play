require './command_generator'
require 'socket'
require 'json'

single_cmd_input = File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json'
single_cmd_output = File.dirname(__FILE__) + '/json_samples/1_command/5-robot_input-1cmd.json'
square_cmd_input = File.dirname(__FILE__) + '/json_samples/square_command/3-translator_output-square.json'
square_cmd_output  = File.dirname(__FILE__) + '/json_samples/square_command/5-robot_input-square.json'
while_cmd_input = File.dirname(__FILE__) + '/json_samples/while_command/3-translator_output-while.json'
while_cmd_output = File.dirname(__FILE__) + '/json_samples/while_command/5-robot_input-while.json'
fizzbuzz_input = File.dirname(__FILE__) + '/json_samples/fizz_buzz/3-translator_output-fizzbuzz.json'
fizzbuzz_output = File.dirname(__FILE__) + '/json_samples/fizz_buzz/5-robot_input-fizzbuzz.json'

describe 'CommandGenerator' do 

  let( :command_generator_single ) { CommandGenerator.new( single_cmd_input ) }

  it 'translates single command scenario input into expected Astrobot JSON object' do
    command_generator = CommandGenerator.new( single_cmd_input )
    expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( single_cmd_output ).read ) )
  end

  it 'translates square command scenario input into expected Astrobot JSON object' do
    command_generator = CommandGenerator.new( square_cmd_input )
    expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( square_cmd_output ).read ) )
  end

  it 'translates while command scenario input into expected Astrobot JSON object' do
    command_generator = CommandGenerator.new( while_cmd_input )
    expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( while_cmd_output ).read ) )
  end

  it 'translates fizzbuzz command scenario input into expected Astrobot JSON object' do
    command_generator = CommandGenerator.new( fizzbuzz_input )
    expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( fizzbuzz_output ).read ) )
  end

end