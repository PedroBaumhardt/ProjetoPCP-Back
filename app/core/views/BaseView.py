from abc import ABC

from fastapi.responses import JSONResponse


class BaseView(ABC):
    def _init_(self, message: str, status_code: int = 200, error: bool = False, **kwargs):
        self.status_code = status_code
        self.content = kwargs
        self.content["message"] = message
        self.content["error"] = error

    def to_response(self):
        return JSONResponse(
            content=self.content,
            status_code=self.status_code
        )