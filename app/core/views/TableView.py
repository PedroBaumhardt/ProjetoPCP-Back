from app.core.schema.TableSchema import Table
from app.core.views.SuccessView import SuccessView


class TableView(SuccessView):
    table: Table

    def __init__(self, message: str, table: Table):
        super().__init__(message)
        self.table = table

    #todo implement