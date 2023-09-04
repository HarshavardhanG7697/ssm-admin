# SSM ADMIN CLI TOOL

![ssm-admin logs](https://github.com/HarshavardhanG7697/ssm-admin/assets/84803301/5ad0f2b1-1d57-4f78-8b00-66525839886d)

A tool to perform multiple tasks (which I have not yet thought about but currently only to view logs) related to Amazon SSM agent via the command line.
## WHY?
Because I am lazy. I do not want to spend time trying to `cd` into the correct directory or type a loooooooooooonnnnnnnnnnnggggg directory path only to view a log file.

## INSTALLATION
Make sure you have **Python3.7** or higher installed on your system.

Switch to **root user** and then just use `$ pip install ssm-admin` or `$pip3 install ssm-admin` (if you are using a macbook).

## HOW TO USE?

### Within The Instance
The intention of this tool is that you can either view the logs right on the instance or you can download the logs to a different machine and use the tool to view them. All the information can be viewed using the `--help` option.
Example:
```
# ssm-admin --help
# ssm-admin command-logs --help
```
The tool currently consists of 3 commands. They are as follows:
1. `agent-logs`: This is to view the ssm agent logs. 
2. `command-logs`: This is to view the logs of SSM Command Invocations. It takes an argument `command-id`. Currently, this only supports logs from Run-Command and Patch operations.
3. `list-commands`: This will output a table of command IDs and their respective time of creation. The latest command invocation will be at the top.

### Outside The Instance
If you have collected the ssm related logs and downloaded them to your local machine for further investigation, then you can use the option `--log-dir` for all the sub-commands mentioned above. 
1. `agent-logs`: The path specified must be the path to a directory which contains `amazon-ssm-agent.log` file.
2. `command-logs`: The path specified must be path to a directory which contains the `orchestration` directory
3. `list-commands`: The path specified must be path to a directory which contains the `orchestration` directory

## ROADMAP
This is very basic. Does not do much. However, there are lot of features that I am planning to add and you too can contribute:
1. Implement time contraint to view the agent logs. Currently, the tools simply opens the latest agent log file. All the past log files should be combined and then we should be able to view the agent logs only withing a specified time frame.
2. Implement log filtering so that we can only view logs that are `ERROR` or `WARNING`
3. Add a new command to enable debug logs for the agent. Example: `$ ssm-admin enable-debug` should modify the seelog.xml file and restart the ssm agent.