import logging
import os
from datetime import datetime

# LOG_FILE: A String Representing The Log File's Name, Which Includes The Current Date And Time
# The strftime Function Is A Method In Python's Datetime Module That Stands For "String Format Time." It Is Used To Format A Datetime Object Into A String Representation Based On A Specified Format

# logs_path: The Directory Path For Storing Log Files, Created By Joining The Current Working Directory With A "Logs" Subdirectory
# os.getcwd(): This Function Returns The Current Working Directory
# The os.path.join Function Is Used To Join One Or More Path Components Intelligently
# "logs": This Is A String Representing The Name Of The Subdirectory That Will Be Created To Store The Log Files

"""
import os

directory = "/path/to/directory"
filename = "example.txt"

full_path = os.path.join(directory, filename)

print(full_path)

"""
# In This Example, Full_Path Will Be "/path/to/directory/example.txt"

# os.makedirs(logs_path, exist_ok=True): Creating The "Logs" Directory If It Doesn't Exist
# LOG_FILE_PATH: The Complete Path To The Log File, Including The Directory And File Name


LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
