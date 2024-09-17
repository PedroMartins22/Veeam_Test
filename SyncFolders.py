import os
import shutil
import time
import hashlib
import argparse
import logging
import sys

def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica, log):
    for root, dirs, files in os.walk(source):
        # Create corresponding directories in the replica folder
        rel_path = os.path.relpath(root, source)
        replica_dir = os.path.join(replica, rel_path)
        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            log.info(f"Directory created: {replica_dir}")

        # Sync files
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(replica_dir, file)

            if not os.path.exists(replica_file):
                shutil.copy2(source_file, replica_file)
                log.info(f"File copied: {source_file} -> {replica_file}")
            else:
                # Compare files by MD5 hash or modification time
                if get_file_md5(source_file) != get_file_md5(replica_file):
                    shutil.copy2(source_file, replica_file)
                    log.info(f"File updated: {source_file} -> {replica_file}")

    # Remove files and directories that are no longer in the source folder
    for root, dirs, files in os.walk(replica, topdown=False):
        rel_path = os.path.relpath(root, replica)
        source_dir = os.path.join(source, rel_path)

        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_dir, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                log.info(f"File removed: {replica_file}")

        for dir in dirs:
            replica_dir = os.path.join(root, dir)
            source_dir = os.path.join(source, dir)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                log.info(f"Directory removed: {replica_dir}")

def setup_logging(log_file):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    return log

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    
    args = parser.parse_args()

    # Setup logging
    log = setup_logging(args.log_file)

    # Run the synchronization periodically
    while True:
        log.info("Starting synchronization...")
        sync_folders(args.source, args.replica, log)
        log.info("Synchronization complete. Waiting for next interval...")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
