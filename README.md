# Internal Development in QA Team

This is a command-line utility that synchronizes two folders: a source folder and a replica folder. It ensures that the replica folder contains an exact copy of the source folder, updating it periodically to match any changes. The synchronization process logs all actions (file creation, modification, deletion) to both the console and a log file.

## Features
- **One-way synchronization**: The replica folder is updated to match the source folder, but not vice versa.
- **File and folder operations**: New files are copied, modified files are updated, and deleted files/folders are removed from the replica.
- **Logging**: Logs all synchronization activities to a specified log file and the console.
- **Periodic execution**: The tool runs at a user-specified interval.

## Requirements
- Python 3.6 or higher

## How to Use

### 1. Clone the Repository
```bash
git clone https://github.com/PedroMartins22/Veeam_Test.git
cd Veeam_Test
```

### 2. Run the program
```bash
python .\SyncFolders.py "soureFolder" "replicaFolder" intervalBetweenSyncs(in secs) "pathOfLogFile"
```
