import sys
from logger import get_logger


logger = get_logger("flask-model")

def get_error_details(error: Exception, error_detail: sys) -> dict:
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
    else:
        file_name = "Unknown"
        line_number = "Unknown"

    return {
        "error_type": type(error).__name__,
        "error_message": str(error),
        "file_name": file_name,
        "line_number": line_number
    }


class CustomException(Exception):
    def __init__(self, error: Exception, error_detail: sys):
        self.error_details = get_error_details(error, error_detail)
        self.error_message = (
            f"Error Type: "
            f"{self.error_details['error_type']} | "

            f"Message: "
            f"{self.error_details['error_message']} | "

            f"File: "
            f"{self.error_details['file_name']} | "

            f"Line: "
            f"{self.error_details['line_number']}"
        )

        logger.exception(self.error_message)

        super().__init__(self.error_message)

    def __str__(self):
        return self.error_message