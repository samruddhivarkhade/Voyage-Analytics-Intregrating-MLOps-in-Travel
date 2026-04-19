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







class GenderRequest(BaseModel):
    flight_count: int
    total_price: float
    total_distance: float
    total_hotel_spend: float
    total_days: int
    age: int


class GenderResponse(BaseModel):
    predicted_gender: str


# Hotel Recommendation Schemas
VALID_GENDERS_HOTEL = {"male", "female", "unknown"}
VALID_BUDGETS = {"budget", "mid", "luxury"}
VALID_COMPANIES = {"4You", "Acme Factory", "Monsters CYA", "Umbrella LTDA", "Wonka Company"}


class HotelRecommendationRequest(BaseModel):
    days: int
    month: int
    age: int
    gender: str
    budget: str
    company: str
    top_n: int = 5

    @field_validator("gender")
    @classmethod
    def validate_gender(cls, value: str) -> str:
        if value not in VALID_GENDERS_HOTEL:
            raise ValueError(
                f"Invalid gender '{value}'. Must be one of {sorted(VALID_GENDERS_HOTEL)}."
            )
        return value

    @field_validator("budget")
    @classmethod
    def validate_budget(cls, value: str) -> str:
        if value not in VALID_BUDGETS:
            raise ValueError(
                f"Invalid budget '{value}'. Must be one of {sorted(VALID_BUDGETS)}."
            )
        return value

    @field_validator("company")
    @classmethod
    def validate_company(cls, value: str) -> str:
        if value not in VALID_COMPANIES:
            raise ValueError(
                f"Invalid company '{value}'. Must be one of {sorted(VALID_COMPANIES)}."
            )
        return value

    @field_validator("days")
    @classmethod
    def validate_days(cls, value: int) -> int:
        if value < 1 or value > 30:
            raise ValueError("Days must be between 1 and 30")
        return value

    @field_validator("month")
    @classmethod
    def validate_month(cls, value: int) -> int:
        if value < 1 or value > 12:
            raise ValueError("Month must be between 1 and 12")
        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int) -> int:
        if value < 18 or value > 100:
            raise ValueError("Age must be between 18 and 100")
        return value


class HotelRecommendation(BaseModel):
    rank: int
    hotel: str
    match_score: float


class HotelRecommendationResponse(BaseModel):
    recommendations: list[HotelRecommendation]
    total_recommendations: int


# User Stats Schema
class UserStats(BaseModel):
    total_predictions: int
    flight_predictions: int
    gender_predictions: int
    avg_prediction_time_ms: float = 0.0
    last_prediction: str | None = None