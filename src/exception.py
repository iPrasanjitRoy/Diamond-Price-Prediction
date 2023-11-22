import sys
from src.logger import logging

# A Function That Takes An Error Message And Sys Information, Extracts The File Name, Line Number, And Generates An Error Message String With This Information
# The Sys Module Provides Functions And Variables Used To Manipulate Different Parts Of The Python Runtime Environment
# sys.exit() Is Used To Exit From The Python Script
# sys.version Provides A String Containing The Python Version
# The Function Error_Message_Detail Is Function That Takes An Error And Additional Information From The Sys Module To Generate A Detailed Error Message


# _, _, exc_tb = error_detail.exc_info(): This Line Retrieves Information About The Current Exception Using sys.exc_info()
# The exc_tb Variable Holds The Traceback Object
# file_name = exc_tb.tb_frame.f_code.co_filename: Extracts The File Name From The Code Object Associated With The Traceback

# The error_message Line Formats A String Using The Obtained Information, Including The File Name, Line Number And The String Representation Of The Error


def error_message_detail(error, error_detail: sys):
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error Occured In Python Script Name [{0}] Line Number [{1}] Error Message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


# This Is The Constructor Method For The Custom Exception Class.
# It Takes Three Parameters: Self (Representing The Instance Of The Class), Error_message (The Error Message You Want To Associate With The Exception), And Error_detail (Information About The Error, Likely Obtained From Sys.exc_info())
# super().__init__(error_message): Calls The Constructor Of The Parent Class (Which Is Likely The Built-In Exception Class) And Passes The Error_Message To It


class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    logging.info("Logging Has Started")

    try:
        a = 1 / 0
    except Exception as e:
        logging.info("Division By Zero")
        raise CustomException(e, sys)
