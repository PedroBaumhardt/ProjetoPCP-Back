from pydantic import BaseModel, field_validator

PRIORITIES: list[str] = ["baixa", "média", "alta"]

class PrioritySchema(BaseModel):
    priority: int

    def to_priority(self) -> str:
        return PRIORITIES[self.priority]

    @staticmethod
    def number_to_priority(number: int) -> str:
        if number < 0 or number > 2:
            raise ValueError("Priority must be between 0 and 2")
        return PRIORITIES[number]

    @field_validator("priority")
    @classmethod
    def _validate_priority(cls, priority: int) -> int:
        if priority < 0 or priority > 2:
            raise ValueError("Priority must be between 0 and 2")
        return priority