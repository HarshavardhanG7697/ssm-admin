# SSM ADMIN CLI TOOL

A tool to perform multiple tasks (which I have not yet thought about but currently only to view logs) related to Amazon SSM agent via the command line.
## WHY?
Because I am lazy. I do not want to spend time trying to `cd` into the correct directory or type a loooooooooooonnnnnnnnnnnggggg directory path only to view a log file.

## INSTALLATION
Make sure you have **Python3.7** or higher installed on your system.

Switch to **root user** and then just use `$ pip install ssm-admin` or `$pip3 install ssm-admin` (if you are using a macbook).

## HOW TO USE?
The intention of this tool is that you can either view the logs right on the instance or you can download the logs to a different machine and use the tool to view them. 

- IF you are viewing logs present in the instance itself, switch to root user `$ sudo su -`. If not, skip this.
- `ssm-admin agent-logs` directly opens up the latest amazon-ssm-agent.log file.
- `ssm-admin command-logs` needs a mandatory option `--command-id`. Specify the command ID of which you want to view the `stdout` file and it will open it for you.

**NOTE**:
For all the above commands, if you are using the tool on another instance or in your local machine, then you need to specify the `--log-dir` option.
- If you are viewing the agent logs, then you need to provide the path to the directory which contains the `amazon-ssm-agent.log` file. This will be in `/var/log/amazon/ssm/` directory in an EC2 instance. 
For example, if you have downloaded just the agent logs and the path is `~/Downloads/amazon-ssm-agent.log` then the command will look like `$ ssm-admin agent-logs --log-dir ~/Downloads`.

- For command logs, the `--log-dir` should point to the directory that is equivalent to `/var/lib/amazon/ssm/Instance-Id/document/orchestration/` directory in the instance.

## ROADMAP
This is very basic. Does not do much. However, there are lot of features that I am planning to add and you too can contribute:
1. Implement time contraint to view the agent logs. Currently, the tools simply opens the latest agent log file. All the past log files should be combined and then we should be able to view the agent logs only withing a specified time frame.
2. Implement log filtering so that we can only view logs that are `ERROR` or `WARNING`
3. Add a new command to enable debug logs for the agent. Example: `$ ssm-admin enable-debug` should modify the seelog.xml file and restart the ssm agent.