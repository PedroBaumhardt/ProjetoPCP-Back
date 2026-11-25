import datetime

from pydantic import BaseModel, field_validator

from app.core.schema.PrioritySchema import PrioritySchema


class ProductionOrderSchema(BaseModel):
    code: str
    product: str # produto_codigo
    priority: int
    quantity: int
    estimated_start: datetime.date
    observation: str | None = None

    def priority_str(self) -> str:
        return PrioritySchema.number_to_priority(self.priority)

    @field_validator("priority")
    @classmethod
    def _validate_priority(cls, priority: int) -> int:
        if priority < 0 or priority > 2:
            raise ValueError("Priority must be between 0 and 2")
        return priority

    @field_validator("estimated_start")
    @classmethod
    def _validate_estimated_start(cls, estimated_start: datetime.date) -> datetime.date:
        if datetime.date.today() > estimated_start:
            raise ValueError("Estimated start date cannot be in the past")
        return estimated_start