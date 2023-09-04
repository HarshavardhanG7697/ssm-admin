import typer
import os
import structlog
from typing_extensions import Annotated
from typing import Optional
from botocore.utils import IMDSFetcher
from rich import print
from rich.table import Table
from datetime import datetime

# Initialize the logger
logger = structlog.get_logger()

LOG_DIRS = {"agent_logs": "amazon-ssm-agent.log", "command_logs": "awsrunShellScript"}

app = typer.Typer()


def set_log_path(
    log_dir: Optional[str] = None,
    log_type: str = "command-logs",
) -> str:
    """
    Set the log path based on log_dir and log_type.

    :param log_dir: The directory containing logs.
    :param log_type: Type of logs ('command-logs' or 'agent-logs').
    :return: The log location.
    """
    if log_dir is None:
        instance_id = get_instance_id()

        if log_type == "command-logs":
            log_location = os.path.join(
                "/var/lib/amazon/ssm/", instance_id, "document/orchestration/"
            )
        elif log_type == "agent-logs":
            log_location = "/var/log/amazon/ssm/"
    else:
        if log_type == "command-logs":
            log_location = os.path.join(log_dir, "orchestration/")
        elif log_type == "agent-logs":
            log_location = log_dir

    return log_location


def get_instance_id() -> str:
    """Retrieve the EC2 instance ID using the AWS IMDS."""
    try:
        instance_id = (
            IMDSFetcher()
            ._get_request(
                "/latest/meta-data/instance-id",
                None,
                token=IMDSFetcher()._fetch_metadata_token(),
            )
            .text
        )
        return instance_id
    except Exception as e:
        logger.error(f"Failed to retrieve EC2 instance ID: {e}")
        raise typer.Abort()


@app.command("agent-logs")
def view_agent_logs(
    log_dir: Annotated[
        str,
        typer.Option(
            help="The path to directory that is equivalent of the /var/log/amazon/ssm directory which contains the amazon-ssm-agent.log file."
        ),
    ] = None
):
    """
    View Amazon SSM Agent logs.

    :param log_dir: The directory containing agent logs.
    """
    log_dir = set_log_path(log_dir, log_type="agent-logs")

    if not os.path.exists(log_dir):
        logger.error(
            f"Unable to locate {LOG_DIRS['agent_logs']} in {log_dir}. "
            "Please specify the directory that contains 'amazon-ssm-agent.log' file."
        )
        raise typer.Abort()

    logger.info(f"Amazon SSM Agent logs found in {log_dir}.")

    log_file_path = os.path.join(log_dir, LOG_DIRS["agent_logs"])
    with open(log_file_path, "r") as agent_logs:
        logger.info("Showing agent logs now!")
        typer.echo_via_pager(agent_logs.read())


@app.command("command-logs")
def view_command_logs(
    command_id: Annotated[
        str,
        typer.Argument(
            help="The command id that you want to view the execution logs for."
        ),
    ],
    log_dir: Annotated[
        str,
        typer.Option(
            help="The path to directory that is equivalent of the /var/lib/amazon/ssm/Instance-Id/document/orchestration/ which contains all the commands' execution logs."
        ),
    ] = None,
):
    """
    View execution logs for a specific command.

    :param command_id: The command ID.
    :param log_dir: The directory containing command logs.
    """
    log_dir = set_log_path(log_dir, log_type="command-logs")

    logger.info(f"Logs for command: {command_id} found in {log_dir}.")

    try:
        log_file_path = os.path.join(
            log_dir, command_id, LOG_DIRS["command_logs"], "PatchLinux/stdout"
        )
        log_type = "Patch Operation"

        if not os.path.exists(log_file_path):
            log_file_path = os.path.join(
                log_dir,
                command_id,
                LOG_DIRS["command_logs"],
                "0.awsrunShellScript/stdout",
            )
            log_type = "Run Command"

        with open(log_file_path, "r") as command_logs:
            logger.info(f"The command: {command_id} is a {log_type}.")
            typer.echo_via_pager(command_logs.read())
    except FileNotFoundError:
        logger.error(
            f"Unable to locate {LOG_DIRS['command_logs']} in {log_file_path}. "
            "This can either mean that the directory specified is incorrect or the command is neither patch operation nor run-command operation."
        )
        raise typer.Abort()


@app.command("list-commands")
def list_commands(
    log_dir: Optional[str] = None,
):
    """
    List available command IDs in a table with creation dates.

    :param log_dir: The directory containing command logs.
    """
    log_dir = set_log_path(log_dir, log_type="command-logs")

    try:
        # Get a list of command directories and sort them by creation time in reverse order
        command_dirs = sorted(
            os.listdir(log_dir),
            key=lambda x: os.path.getctime(os.path.join(log_dir, x)),
            reverse=True,
        )

        table = Table(title="Command IDs and Creation Dates")
        table.add_column("Command ID", style="bold")
        table.add_column("Creation Date", style="bold")

        for dir in command_dirs:
            creation_date = datetime.fromtimestamp(
                os.path.getctime(os.path.join(log_dir, dir))
            ).strftime("%Y-%m-%d %H:%M:%S")
            table.add_row(dir, creation_date)

        print(table)
    except FileNotFoundError:
        logger.error(f"Unable to locate any commands in {log_dir}.")
        raise typer.Abort()


if __name__ == "__main__":
    app()
