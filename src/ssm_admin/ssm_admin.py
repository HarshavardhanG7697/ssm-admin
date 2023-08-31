import typer
import os
from rich import print
from typing_extensions import Annotated
from botocore.utils import IMDSFetcher
import structlog

# command logs format
# /var/lib/amazon/ssm/Instance-Id/document/orchestration/Command-Id/awsrunShellScript/PatchLinux/stdout
# /var/lib/amazon/ssm/Instance-Id/document/orchestration/Command-Id/awsrunShellScript/0.awsrunShellScript/stdout

app = typer.Typer()
logger = structlog.get_logger()

LOG_DIRS = {"agent_logs": "amazon-ssm-agent.log", "command_logs": "awsrunShellScript"}


@app.command("agent-logs")
def view_agent_logs(
    log_dir: Annotated[
        str,
        typer.Option(
            help="The path to directory that is equivalent of the /var/log/amazon/ssm directory which contains the amazon-ssm-agent.log file."
        ),
    ] = None,
):
    if log_dir is None:
        log_dir = os.path.join("/var/log/amazon/ssm/", LOG_DIRS["agent_logs"])
    else:
        log_dir = os.path.join(log_dir, LOG_DIRS["agent_logs"])
    if os.path.exists(log_dir):
        logger.info(f"Amazon SSM Agent logs found in {log_dir}.]")
        with open(log_dir, "r") as agent_logs:
            logger.info("showing agent logs now!")
            typer.echo_via_pager(agent_logs.read())
    else:
        logger.error(
            f"Unable to locate {LOG_DIRS['agent_logs']} in {log_dir}. Please specify the directory that contains 'amazon-ssm-agent.log' file."
        )


@app.command("command-logs")
def view_command_logs(
    command_id: Annotated[
        str,
        typer.Option(
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
    if log_dir is None:
        instance_id = (
            IMDSFetcher()
            ._get_request(
                "/latest/meta-data/instance-id",
                None,
                token=IMDSFetcher()._fetch_metadata_token(),
            )
            .text
        )
        log_dir = os.path.join(
            "/var/lib/amazon/ssm/", instance_id, "document/orchestration/", command_id
        )
    else:
        log_dir = os.path.join(log_dir, command_id)

    logger.info(f"Logs for command: {command_id} found in {log_dir}.]")
    try:
        with open(
            os.path.join(log_dir, LOG_DIRS["command_logs"], "PatchLinux/stdout"), "r"
        ) as command_logs:
            logger.info(f"The command: {command_id} is a Patch Operation.")
            typer.echo_via_pager(command_logs.read())
    except FileNotFoundError:
        try:
            with open(
                os.path.join(
                    log_dir, LOG_DIRS["command_logs"], "0.awsrunShellScript/stdout"
                ),
                "r",
            ) as command_logs:
                logger.info(f"The command: {command_id} is a Run Command.")
                typer.echo_via_pager(command_logs.read())
        except FileNotFoundError:
            logger.error(
                f"Unable to locate {LOG_DIRS['command_logs']} in {log_dir}. Please specify the directory that contains 'awsrunShellScript' file."
            )


if __name__ == "__main__":
    app()
