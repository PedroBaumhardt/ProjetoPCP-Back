from abc import ABC

from fastapi.responses import JSONResponse

class BaseView(ABC):
    def __init__(self, message: str, status_code: int = 200, error: bool = False, message_type: int = 0, **kwargs):
        self.status_code = status_code
        self.content = kwargs
        self.content["info"] = {
            "message": message,
            "type": message_type,
        }
        self.content["error"] = error

    def to_response(self):
        return JSONResponse(
            content=self.content,
            status_code=self.status_code
        )