from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select
from models.train import Trains
from models.ticket import Tickets


# url to file
sqlite_url = "sqlite:///TrainDB.db"

# this will manage our sessions and connects the api to database
engine = create_engine(sqlite_url)

# drop existing tables
SQLModel.metadata.drop_all(engine) 

# this will create the tables
SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# sample data
train_1 = Trains(train_code="RE9210", train_type="Regio Express", departure_station="Pitesti", destination_station="Bucuresti Nord")
train_2 = Trains(train_code="RE9213", train_type="Regio Express", departure_station="Bucuresti Nord", destination_station="Pitesti")
train_3 = Trains(train_code="R8010", train_type="Regio", departure_station="Constanta", destination_station="Bucuresti Nord")
train_4 = Trains(train_code="IR1883", train_type="Inter Regio", departure_station="Bucuresti Nord", destination_station="Constanta")

ticket_1 = Tickets(surname="Zarnoianu", firstname="Adrian", chosen_train_code="RE9210")

with Session(engine) as session:
    session.add(train_1)
    session.add(train_2)
    session.add(train_3)
    session.add(train_4)
    session.add(ticket_1)
    session.commit()

# turn on app
app = FastAPI()


# this is the main page
@app.get("/")
async def home_page():
    return {"message":"Train app"}

# retrieves all the available trains and other info 
@app.get("/trains")
async def select_trains(session: SessionDep) -> list[Trains]:
    trains = session.exec(select(Trains)).all()
    return trains

# creates a new ticket
@app.put("/tickets")
async def create_ticket(ticket: Tickets, session: SessionDep) -> Tickets:
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket

# deletes ticket bought for a certain train
@app.delete("/deleteTicket/{ticket_id}")
async def delete_ticket(ticket_id: int, session: SessionDep):
    ticket = session.get(Tickets, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="The ticket doesn't seem to exist...")
    session.delete(ticket)
    session.commit()

# changes the train code in a ticket
@app.post("/updateTicket/{ticket_id}")
async def update_ticket(new_code: str, ticket_id: int, session: SessionDep):
    chosen_ticket = session.get(Tickets, ticket_id)
    if not chosen_ticket:
        raise HTTPException(status_code=404, detail="The ticket doesn't seem to exist..." )
    chosen_ticket.chosen_train_code = new_code
    session.add(chosen_ticket)
    session.commit()
    session.refresh(chosen_ticket)
    return chosen_ticket

    

