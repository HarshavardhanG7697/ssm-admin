# ====================================
# This is not yet working as expected
# ====================================


import pytest
import os
from typer.testing import CliRunner
from ssm_admin import (
    app,
    view_agent_logs,
    view_command_logs,
    list_commands,
    set_log_path,
    get_instance_id,
)

# Initialize the test runner
runner = CliRunner()

# Mocked instance ID for testing
MOCK_INSTANCE_ID = "i-1234567890abcdef0"

# Mocked log directory paths
MOCK_AGENT_LOGS_DIR = "/var/log/amazon/ssm/"
MOCK_COMMAND_LOGS_DIR = (
    f"/var/lib/amazon/ssm/{MOCK_INSTANCE_ID}/document/orchestration/"
)

# Mocked log file paths
MOCK_AGENT_LOG_FILE = os.path.join(MOCK_AGENT_LOGS_DIR, "amazon-ssm-agent.log")
MOCK_COMMAND_LOG_FILE_1 = os.path.join(
    MOCK_COMMAND_LOGS_DIR, "command-1/awsrunShellScript/stdout"
)
MOCK_COMMAND_LOG_FILE_2 = os.path.join(
    MOCK_COMMAND_LOGS_DIR, "command-2/awsrunShellScript/stdout"
)


@pytest.fixture
def mocked_get_instance_id(monkeypatch):
    def mock_get_instance_id():
        return MOCK_INSTANCE_ID

    monkeypatch.setattr("ssm_admin.get_instance_id", mock_get_instance_id)


@pytest.fixture
def mocked_os_path_exists(monkeypatch):
    def mock_os_path_exists(path):
        return True  # Mocking that the log directory or file exists

    monkeypatch.setattr(os.path, "exists", mock_os_path_exists)


@pytest.fixture
def mocked_os_listdir(monkeypatch):
    def mock_os_listdir(path):
        if path == MOCK_COMMAND_LOGS_DIR:
            return ["command-1", "command-2"]
        return []

    monkeypatch.setattr(os, "listdir", mock_os_listdir)


def test_set_log_path():
    # Test the default log path for command logs
    assert set_log_path() == MOCK_COMMAND_LOGS_DIR

    # Test specifying a custom log directory
    custom_log_dir = "/custom/log/directory"
    assert set_log_path(custom_log_dir) == os.path.join(
        custom_log_dir, "orchestration/"
    )

    # Test setting the log path for agent logs
    assert set_log_path(log_type="agent-logs") == MOCK_AGENT_LOGS_DIR


def test_get_instance_id(mocked_get_instance_id):
    assert get_instance_id() == MOCK_INSTANCE_ID


def test_view_agent_logs(mocked_os_path_exists, caplog):
    result = runner.invoke(view_agent_logs)
    assert result.exit_code == 0
    assert f"Amazon SSM Agent logs found in {MOCK_AGENT_LOGS_DIR}." in caplog.text


def test_view_command_logs(mocked_os_path_exists, caplog):
    result = runner.invoke(view_command_logs, ["--command-id", "command-1"])
    assert result.exit_code == 0
    assert (
        f"Logs for command: command-1 found in {MOCK_COMMAND_LOGS_DIR}." in caplog.text
    )


def test_list_commands(mocked_os_listdir, capsys):
    result = runner.invoke(list_commands)
    assert result.exit_code == 0
    captured = capsys.readouterr()
    assert "Command IDs and Creation Dates" in captured.out
    assert "command-1" in captured.out
    assert "command-2" in captured.out
