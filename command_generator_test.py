# import command_generator
import unittest
import json
from command_generator import CommandGenerator


def assert_dict_equal(A, B):
    """
    Check that two dictionaries, A and B, have the same keys and values
    """
    assert len(A) == len(B), \
        "Dictionaries are not the same size"
    N = len(A)
    assert len(set(A.keys()) & set(B.keys())) == N, \
        "Dictionaries have different keys"
    assert all(v == B[k] for k,v in A.items()), \
        "Dictionaries have different values"


def process(input_file, output_file):
    """
    Given an input_file and outut_file, check that running the CommandGenerator
    on the input_file results in the same data as what is represented in
    output_file
    """
    with open(output_file) as fd:
        output_data = json.load(fd)
    with open(input_file) as fd:
        input_raw = fd.read()
    processed_data = CommandGenerator(input_raw).output
    assert_dict_equal(processed_data, output_data)


class TestCommandGenerator(unittest.TestCase):
    def test_command(self):
        process(
            './json_samples/1_command/3-translator_output-1cmd.json',
            './json_samples/1_command/5-robot_input-1cmd.json'
        )

    def test_square(self):
        process(
            './json_samples/square_command/3-translator_output-square.json',
            './json_samples/square_command/5-robot_input-square.json'
        )

    def test_while(self):
        process(
            './json_samples/while_command/3-translator_output-while.json',
            './json_samples/while_command/5-robot_input-while.json'
        )

    def test_fizzbuzz(self):
        process(
            './json_samples/fizz_buzz/3-translator_output-fizzbuzz.json',
            './json_samples/fizz_buzz/5-robot_input-fizzbuzz.json'
        )



if __name__ == '__main__':
    unittest.main()
