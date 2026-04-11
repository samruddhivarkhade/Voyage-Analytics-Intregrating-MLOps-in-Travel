from pydantic import BaseModel, field_validator


VALID_FLIGHT_TYPES = {"economic", "firstClass", "premium"}
VALID_AGENCIES = {"Rainbow", "CloudFy", "FlyingDrops"}
VALID_GENDERS = {"male", "female"}


class FlightPriceRequest(BaseModel):
    flightType: str
    agency: str
    gender: str
    distance: float
    time: float
    age: int

    @field_validator("flightType")
    @classmethod
    def validate_flight_type(cls, value: str) -> str:
        if value not in VALID_FLIGHT_TYPES:
            raise ValueError(
                f"Invalid flightType '{value}'. Must be one of {sorted(VALID_FLIGHT_TYPES)}."
            )
        return value

    @field_validator("agency")
    @classmethod
    def validate_agency(cls, value: str) -> str:
        if value not in VALID_AGENCIES:
            raise ValueError(
                f"Invalid agency '{value}'. Must be one of {sorted(VALID_AGENCIES)}."
            )
        return value

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        if value not in VALID_GENDERS:
            raise ValueError(
                f"Invalid gender '{value}'. Must be one of {sorted(VALID_GENDERS)}."
            )
        return value


class FlightPriceResponse(BaseModel):
    predicted_price: float
