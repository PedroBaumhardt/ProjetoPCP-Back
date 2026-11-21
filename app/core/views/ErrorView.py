from app.core.views.BaseView import BaseView

class ErrorView(BaseView):
    def __init__(self, message: str, status_code: int = 400, **kwargs):
        super().__init__(message, status_code, error=True, **kwargs)