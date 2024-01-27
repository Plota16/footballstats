
from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    playerID: int = Field(default=None, primary_key=True)
    name: str
    description: str
    imageURL: str
    age: int
    height: float
    citizenship: str
    position: str
    foot: str
    shirtNumber: int
    club_id: str
    marketValue: float


class CompetitionStats(SQLModel, table=True):
    playerID: int = Field(default=None, primary_key=True)
    clubID: int = Field(default=None, primary_key=True)
    seasonID: str = Field(default=None, primary_key=True)
    competitionID: int = Field(default=None, primary_key=True)
    competitionName: str
    appearances: int
    goals: int
    assists: int
    yellowCards: int
    minutesPlayed: int

