# Presentation for Seminar 2

### Requests on a database using FastAPI and SQLModel

### Part 1: Database Presentation

For this small project, I decided to make a small database with 2 tables:

- **Trains** with:
  - `train_id`: INTEGER, and the primary key of the table
  - `train_code`: VARCHAR(8), it's the "name" of the train, following the CFR Calatori standards (e.g: RE9210)
  - `train_type`: VARCHAR, it's the type of train, which in reality indicate how many stations the train stops to before it reaches the final destination (e.g.: Regio is a "personal" train, it stops at every station possible)
  - `departure_station`: VARCHAR, it represents the station from where the train departs
  - `destination_station`: VARCHAR, the destination of the train
  
- **Tickets** with:
  - `ticket_id`: INTEGER, the primary key
  - `surname`: VARCHAR(30), the surname of the client that buys the ticket
  - `firstname`: VARCHAR(30), the first name of the client
  - `chosen_train_code`: VARCHAR, is the foreign key that "binds" the two tables by using the train code

 
### Relationship:
 
**Trains --< Tickets**

One or more tickets can be assigned to the same train.\
One ticket is assigned to a single train.


### Part 2: The Requests

In this program, I have implemented one of each type of request, GET, POST, PUT and DELETE.
Those can be tested by following the `http://127.0.0.1:8000/docs` link.

After populating the tables with dummy data and creating a session through which the program sends queries, we have:  

### GET - Select all available trains

```
@app.get("/trains")
async def select_trains(session: SessionDep) -> list[Trains]:
    trains = session.exec(select(Trains)).all()
    return trains
```

This code sends the following query (`SELECT * FROM Trains`) to the database and retrieves a JSON containing all available trains.
	
Response body: 

```
[
  {
    "departure_station": "Pitesti",
    "destination_station": "Bucuresti Nord",
    "train_id": 1,
    "train_code": "RE9210",
    "train_type": "Regio Express"
  },
  {
    "departure_station": "Bucuresti Nord",
    "destination_station": "Pitesti",
    "train_id": 2,
    "train_code": "RE9213",
    "train_type": "Regio Express"
  },
  {
    "departure_station": "Constanta",
    "destination_station": "Bucuresti Nord",
    "train_id": 3,
    "train_code": "R8010",
    "train_type": "Regio"
  },
  {
    "departure_station": "Bucuresti Nord",
    "destination_station": "Constanta",
    "train_id": 4,
    "train_code": "IR1883",
    "train_type": "Inter Regio"
  }
]
```

### PUT - Create a new Ticket

```
@app.put("/tickets")
async def create_ticket(ticket: Tickets, session: SessionDep) -> Tickets:
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket
```

The PUT request needs some data in order to create a new entry in table Tickets. The data will be "sent" through the request body which will contain the `surname`, `firstname` and `train_code` inputs:

**Example of a request body that is valid in our case:**
```
{
  "surname": "Cranga",
  "firstname": "Teea",
  "chosen_train_code": "RE9210"
}
```

If the data is valid, the program will return the response body that is similar to our request one, but with `ticket_id` automatically added.

###DELETE - Delete a Ticket

```
@app.delete("/deleteTicket/{ticket_id}")
async def delete_ticket(ticket_id: int, session: SessionDep):
    ticket = session.get(Tickets, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="The ticket doesn't seem to exist...")
    session.delete(ticket)
    session.commit()
```

The async function will retrieve the ticket that needs to be deleted by using `ticket_id`. If no such ticket is found, an exception is rasied. Otherwise, the process runs normally and the entry is deleted from the database.

###POST - Change the train from a specific ticket

```
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
```

This one was a bit tricky to figure out, but after a few YouTube tutorials I managed to do a decent request. Similarly to the DELETE request, it used `ticket_id` to find the ticket we want to delete. If found, we update the `chosen_train_code` value of the selected ticket with `new_code`, the URL query parameter. 


