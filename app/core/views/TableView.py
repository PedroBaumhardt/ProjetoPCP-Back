import typing

from starlette.responses import JSONResponse

from app.core.schema.TableSchema import Table
from app.core.views.SuccessView import SuccessView


class TableView(SuccessView):
    table: Table

    def __init__(self, message: str, data: list[dict[str, typing.Any]]):
        super().__init__(message)
        self.table = Table.from_dict_list(data)

    def to_response(self):
        content = self.content.copy()
        content.update(self.table.table_dump())
        return JSONResponse(
            content=content,
            status_code=self.status_code
        )