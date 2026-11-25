import typing

from pydantic import BaseModel, field_serializer, model_validator


def _get_type_name(value: typing.Any) -> str:
    return type(value).__name__

class TableField(BaseModel):
    value:  typing.Any
    type:   str | None = None

    @field_serializer("type")
    def _serialize_type(self, type: str | None) -> str:
        if type is not None: return type
        return _get_type_name(type)

class TableColumn(BaseModel):
    name:   str
    label:  str | None = None
    type:   str | None = None
    hidden: bool = False
    values: list[TableField]

    @field_serializer("label")
    def _serialize_label(self, label: str | None) -> str:
        if label is None:
            return self.name.replace("_", " ").title()
        return label

    @field_serializer("type")
    def _serialize_type(self, ctype: str | None) -> str:
        if ctype is not None: return ctype
        return typing.cast(str, self.values[0].type)

    @model_validator(mode="after")
    def _validate_values(self) -> "TableColumn":
        if len(self.values) == 0:
            raise ValueError("Table column must have at least one value")

        expected_type = self.values[0].type
        for value in self.values:
            if value.type != expected_type:
                raise ValueError("All values in a column must have the same type")

        return self

    def append(self, value: typing.Any):
        self.values.append(TableField(value=value))

class Table(BaseModel):
    columns: dict[str, TableColumn]

    @classmethod
    def from_dict_list(cls, data: list[dict[str, typing.Any]]) -> "Table":  # Exameple [{ "name": "John", "age": "18" }, { "name": "David", "age": "19" }]
        temp_columns = {}
        for key, value in data[0].items():
            temp_columns[key] = TableColumn(name=key, values=[TableField(value=value)])

        data.pop(0)

        for entry in data:
            for key, value in entry.items():
                temp_columns[key].append(value)

        return cls(columns=temp_columns)

    def table_dump(self) -> dict:
        dump = self.model_dump()

        tbl = {"headers": {}, "table": {}}

        for key, column in dump["columns"].items():
            tbl["headers"][key] =  {
                "type": column.type,
                "label": column.label,
                "hidden": column.hidden,
            }
            tbl["table"][key] = column.values

        return tbl