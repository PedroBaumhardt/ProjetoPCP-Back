from app.core.views.BaseView import BaseView

class SuccessView(BaseView):
    def __init__(self, message: str, status_code: int = 200, **kwargs):
        super().__init__(message, status_code, error=False, **kwargs)