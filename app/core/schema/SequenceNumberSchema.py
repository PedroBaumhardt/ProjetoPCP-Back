from pydantic import BaseModel, field_validator


class SequenceNumberSchema(BaseModel):
    sequence_number: int

    @field_validator("sequence_number")
    @classmethod
    def validate_sequence_number(cls, value):
        if value < 0:
            raise ValueError("Sequence number must be a positive integer")
        return value