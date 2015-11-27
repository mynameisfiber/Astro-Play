require './command_generator'
require 'json'

@singlecmd = JSON.parse open(File.dirname(__FILE__) + '/json_samples/1_command/3-translator_output-1cmd.json').read

describe 'interpreter' do 

  it 'converts single command string for robot' do
    print @singlecmd
  end

end