# Change Log

All notable changes to the "ssm-admin" will be documented in this file.

## [0.2.0] - 2023-09-04

### Added

- Added a new command `list-commands` to list available command IDs in a table with creation dates.
- The table includes two columns: "Command ID" and "Creation Date."
- The `rich` package is now used to format and display tables with rich formatting.
- Improved user-friendliness and readability throughout the code.

### Changed

- Modified the `list_commands()` function to display directories in reverse order of creation, with the latest directory created first.

### Deprecated

- None.

### Removed

- None.

## [0.1.0] - 2023-09-01

### Added

- Initial version of the CLI tool.
- Includes commands to view agent logs and command execution logs.
- Supports specifying log directories and viewing logs via a pager.

### Changed

- None.

### Deprecated

- None.

### Removed

- None.
