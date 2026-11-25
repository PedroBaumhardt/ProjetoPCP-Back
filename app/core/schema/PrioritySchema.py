from pydantic import BaseModel, field_validator, ValidationError

PRIORITIES: list[str] = ["baixa", "média", "alta"]

class PrioritySchema(BaseModel):
    priority: int

    def to_priority(self) -> str:
        return PRIORITIES[self.priority]

    @field_validator("priority")
    @classmethod
    def _validate_priority(cls, priority: int) -> int:
        if priority < 0 or priority > 2:
            raise ValidationError("Priority must be between 0 and 2")
        return priority