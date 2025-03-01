from sqlmodel import Field, SQLModel

class Trains(SQLModel, table=True):
    train_id: int = Field(default=None, primary_key=True)
    train_code: str = Field(max_length=8, unique=True)
    train_type: str
    departure_station: str
    destination_station: str 
