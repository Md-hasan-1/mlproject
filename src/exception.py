import sys


def get_mssg(mssg, error_details:sys):
    _, _, exc_traceback = error_details.exc_info()
    file_path = exc_traceback.tb_frame.f_code.co_filename
    file_name = file_path.split("/")[-1]
    line_no = exc_traceback.tb_lineno
    detail_mssg = f"Error occured !!!! \n\n\t- file name: {file_name} \n\t- file location: {file_path} \n\t- line: {line_no} \n\t- message: {mssg}"

    return detail_mssg


class CustomException(Exception):
    def __init__(self, mssg, details:sys):
        super().__init__(mssg)
        self.mssg = get_mssg(mssg, details)

    def __str__(self) -> str:
        return self.mssg


if __name__=="__main__":
    try:
        1/0
    except Exception as e:
        raise CustomException(e, sys)
    
