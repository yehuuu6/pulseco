from pulseco.console.classes import Command
from io import StringIO
from contextlib import redirect_stdout

def mock_function():
    print('Test command executed.')

def test_command_init():
    """
    Test the initialization of a Command object.
    """
    test_class = Command(
        name='test',
        description='Test command',
        usage='test',
        function=mock_function)
    assert test_class.name == 'test'
    assert test_class.description == 'Test command'
    assert test_class.usage == 'test'
    assert test_class.function == mock_function

def test_command_repr():
    """
    Test the __repr__ method of a Command object.
    """
    test_class = Command(
        name='test',
        description='Test command',
        usage='test',
        function=mock_function)
    assert repr(test_class) == 'Command(name=test, description=Test command, usage=test)'

def test_command_execute():
    """
    Test the execute method of a Command object.
    """
    test_class = Command(
        name='test',
        description='Test command',
        usage='test',
        function=mock_function)
    test_class.execute()

def test_command_to_raise_type_error_on_missing_args():
    """
    Test the execute method of a Command object with arguments.
    """
    def test_function_with_args(arg1: str, arg2: str):
        print(f'Test command needs these args: {arg1} and {arg2}.')

    test_class = Command(
        name='test',
        description='Test command',
        usage='Usage: test <arg1> <arg2>',
        function=test_function_with_args
    )
    
    argv = ['pulse.py', 'test', 'arg1'] # Missing the second argument

    # Capture the output using a context manager
    captured_output = StringIO()
    with redirect_stdout(captured_output):
        # Execute the command with insufficient arguments
        test_class.execute(*argv[2:])

    # Check if the usage message was printed
    assert captured_output.getvalue().strip() == 'Usage: test <arg1> <arg2>'