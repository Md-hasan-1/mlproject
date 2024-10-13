import sys
from src.logger import logging


def get_mssg(mssg, error_details:sys):
    _, _, exc_traceback = error_details.exc_info()
    file_path = exc_traceback.tb_frame.f_code.co_filename
    file_name = file_path.split("/")[-1]
    line_no = exc_traceback.tb_lineno
    detail_mssg = f"Error occured !!!! \n\nfile name: {file_name} \nfile location: {file_path} \nline: {line_no} \nmessage: {mssg}"

    return detail_mssg



class CustomException(Exception):

    def __init__(self, mssg, details:sys):
        super().__init__(mssg)
        self.mssg = get_mssg(mssg, details)

    def __str__(self) -> str:
        return self.mssg
