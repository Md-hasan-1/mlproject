import sys


def get_mssg(error_message:str, sys:sys):
    """
    returns: detiled message
    """
    _, _, tb = sys.exc_info()
    file_name = tb.tb_frame.f_code.co_filename
    file_name = file_name.split("\\")[-1]
    line_no = tb.tb_lineno
    detailed_message = f"""
"file_name":{file_name}
"line_no":{line_no}
"message":{error_message}
"""
    return detailed_message


class CustomException(Exception):
    def __init__(self, error_message:str, sys:sys) -> None:
        super().__init__(error_message)
        self.error_message = get_mssg(error_message, sys)
        return None

    def __str__(self) -> str:
        return self.error_message
