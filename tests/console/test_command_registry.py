from pulseco.console.commands import Command
from pulseco.console.command_registry import CommandRegistry
import pytest
from unittest import mock

mock_command_1 = Command(
    name="mock",
    description="Mock command",
    usage="mock",
    function=lambda: print("Mock command executed."),
)

mock_command_2 = Command(
    name="mock2",
    description="Mock command 2",
    usage="mock2",
    function=lambda: print("Mock command 2 executed."),
)


@pytest.fixture(autouse=True)
def reset_singleton():
    """
    Reset the singleton instance of the CommandRegistry class before each test.
    So that the tests are independent of each other and the application itself.
    """
    instance = CommandRegistry()
    instance.reset_instance()


def test_singleton_instance():
    """
    Test that the CommandRegistry class is a singleton.
    """
    instance1 = CommandRegistry()
    instance2 = CommandRegistry()
    assert instance1 is instance2


def test_register_command():
    """
    Test that a command can be registered.
    """
    registry = CommandRegistry()
    registry.register(mock_command_1)
    assert mock_command_1 in registry.get_commands()


def test_register_multiple_commands():
    """
    Test that multiple commands can be registered.
    """
    registry = CommandRegistry()
    registry.register(mock_command_1)
    registry.register(mock_command_2)
    commands = registry.get_commands()
    assert len(commands) == 2
    assert mock_command_1 in commands
    assert mock_command_2 in commands


def test_register_same_command_multiple_times():
    """
    Test that the same command cannot be registered multiple times.
    """
    registry = CommandRegistry()
    registry.register(mock_command_1)
    registry.register(mock_command_1)
    commands = registry.get_commands()
    assert len(commands) == 1
    assert commands.count(mock_command_1) == 1


def test_reset_instance_on_non_unit_test_raises_error():
    # This test will pass if my_function raises RuntimeError
    with mock.patch("inspect.stack") as mock_stack:
        mock_stack.return_value = [
            mock.Mock(filename="some_other_script.py"),
            mock.Mock(filename="main_script.py"),
        ]

        instance = CommandRegistry()

        instance.register(mock_command_1)
        assert instance.get_commands() == [mock_command_1]
        assert len(instance.get_commands()) == 1

        with pytest.raises(
            RuntimeError,
            match="This method is only allowed to be called from unit tests.",
        ):
            instance.reset_instance()

        assert len(instance.get_commands()) == 1
        assert instance.get_commands() == [mock_command_1]


def test_reset_instance_on_unit_test():
    instance = CommandRegistry()
    instance.register(mock_command_1)
    assert instance.get_commands() == [mock_command_1]
    instance.reset_instance()
    assert instance.get_commands() == []
