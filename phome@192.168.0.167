import os
import shutil
from datetime import datetime


def backup_files(pull_folder, backup_folder):
    if not os.path.exists(pull_folder):
        return None

    timestamp = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
    backup_path = os.path.join(backup_folder, f"backup_{timestamp}")

    try:
        shutil.copytree(pull_folder, backup_folder)
        print(f"Backup successful to {backup_path}")
    except Exception as e:
        print(f"Backup failed: {e}")


# Configuration
pull_folder = '/home/phome/'
backup_folder = '/home/phome/backup'
