import os
import shutil
import logging


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), "manager.log")),  # Log to a file
        logging.StreamHandler()  # Also log to console
    ]
)


def move_all_files(source_folder, destination_folder, overwrite=True):
    # Ensure destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Walk through all files and subfolders in the source folder
    for root, _, files in os.walk(source_folder):
        for filename in files:
            source_path = os.path.join(root, filename)
            destination_path = os.path.join(destination_folder, filename)

            # If a file with the same name exists in the destination, add a suffix to avoid overwriting
            if (os.path.exists(destination_path)) & (overwrite == False):
                base, ext = os.path.splitext(filename)
                destination_path = os.path.join(destination_folder, f"{base}_copy{ext}")
            
            # Move the file
            shutil.copy2(source_path, destination_path)
            logging.info(f"Copied: {source_path} -> {destination_path}")


if __name__ == "__main__":
    DAGS_UPDATE = True
    DAGS_ORIGIN_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dags")
    DAGS_TARGET_FOLDER = os.path.expanduser("~/airflow/dags")    
    
    if DAGS_UPDATE:
        move_all_files(DAGS_ORIGIN_FOLDER, DAGS_TARGET_FOLDER)
