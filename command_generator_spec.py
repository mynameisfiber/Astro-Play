# import command_generator
import unittest
import json
from command_generator import parse_to_astrobot

# single_cmd_input = File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json'
with open('./json_samples/1_command/3-translator_output-1cmd.json') as data_file:
    single_cmd_input = json.load(data_file)
# single_cmd_output = File.dirname(__FILE__) + '/json_samples/1_command/5-robot_input-1cmd.json'
with open('./json_samples/1_command/5-robot_input-1cmd.json') as data_file:
    single_cmd_output = json.load(data_file)
# square_cmd_input = File.dirname(__FILE__) + '/json_samples/square_command/3-translator_output-square.json'
with open('./json_samples/square_command/3-translator_output-square.json') as data_file:
    square_cmd_input = json.load(data_file)
# square_cmd_output  = File.dirname(__FILE__) + '/json_samples/square_command/5-robot_input-square.json'
with open('./json_samples/square_command/5-robot_input-square.json') as data_file:
    square_cmd_output = json.load(data_file)
# while_cmd_input = File.dirname(__FILE__) + '/json_samples/while_command/3-translator_output-while.json'
with open('./json_samples/while_command/3-translator_output-while.json') as data_file:
    while_cmd_input = json.load(data_file)
# while_cmd_output = File.dirname(__FILE__) + '/json_samples/while_command/5-robot_input-while.json'
with open('./json_samples/while_command/5-robot_input-while.json') as data_file:
    while_cmd_output = json.load(data_file)
# fizzbuzz_input = File.dirname(__FILE__) + '/json_samples/fizz_buzz/3-translator_output-fizzbuzz.json'
with open('./json_samples/fizz_buzz/3-translator_output-fizzbuzz.json') as data_file:
    fizzbuzz_input = json.load(data_file)
# fizzbuzz_output = File.dirname(__FILE__) + '/json_samples/fizz_buzz/5-robot_input-fizzbuzz.json'
with open('./json_samples/fizz_buzz/5-robot_input-fizzbuzz.json') as data_file:
    fizzbuzz_output = json.load(data_file)

class TestCommandGenerator(unittest.TestCase):

  def test_translates_single_command_scenario_input_into_expected_Astrobot_JSON_object(self):
    command_generator = CommandGenerator.new( single_cmd_input )
    self.assertEqual(command_generator, single_cmd_output)

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

if __name__ == '__main__':
    unittest.main()





  # JSON.load( command_generator.instance_variable_get( :@output ) ), JSON.load( open( single_cmd_output ).read ) )
  

  # it 'translates square command scenario input into expected Astrobot JSON object' do
  #   command_generator = CommandGenerator.new( square_cmd_input )
  #   expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( square_cmd_output ).read ) )
  # end

  # it 'translates while command scenario input into expected Astrobot JSON object' do
  #   command_generator = CommandGenerator.new( while_cmd_input )
  #   expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( while_cmd_output ).read ) )
  # end

  # it 'translates fizzbuzz command scenario input into expected Astrobot JSON object' do
  #   command_generator = CommandGenerator.new( fizzbuzz_input )
  #   expect( JSON.parse( command_generator.instance_variable_get( :@output ) ) ).to eq( JSON.parse( open( fizzbuzz_output ).read ) )
  # end