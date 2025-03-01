from sqlmodel import Field, SQLModel

class Tickets(SQLModel, table=True):
    ticket_id: int = Field(default=None, primary_key=True)
    surname: str  = Field(max_length=30)
    firstname: str = Field(max_length=30)

    chosen_train_code: str | None = Field(default=None, foreign_key="trains.train_code")

