from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select

from api import TransfermarktAPI
import pandas as pd

from model import Player, CompetitionStats


class UpdateDBService:

    def __init__(self, reference_club: str, traitors: list):
        self._api = TransfermarktAPI()
        self._club_id = self._api.get_club_id_by_name(reference_club)
        self._traitors = traitors

        sqlite_file_name = "./database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        SQLModel.metadata.drop_all(self.engine)
        SQLModel.metadata.create_all(self.engine)

    def update_traitors(self):
        with Session(self.engine) as session:
            for triator in self._traitors:
                bio, stats = self._get_player_info(player_name=triator)
                print(bio.name)
                session.add(bio)
                session.add_all(stats)
            session.commit()

    def update_club(self):
        with Session(self.engine) as session:
            for player_id in self._api.get_club_players(self._club_id):
                bio, stats = self._get_player_info(player_id=player_id)
                print(bio.name)
                session.add(bio)
                session.add_all(stats)
            session.commit()

    def update_all(self):
        self.update_traitors()
        self.update_club()

    def _get_player_info(self, player_name: str = None, player_id: int = None):

        if player_id is None:
            self._player_id = self._api.get_player_id_by_name(player_name)
        else:
            self._player_id = player_id
        bio = self._api.get_player_bio_by_id(self._player_id)
        cmp_stats = self._api.get_player_stats_by_id(self._player_id)

        return bio, cmp_stats


class FootballService:

    def __init__(self):
        sqlite_file_name = "./database.db"
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        self.engine = create_engine(sqlite_url, echo=True)
        self.bio_df = self._get_bio_from_db()
        self.stats_df = self._get_stats_from_db()

    def _get_bio_from_db(self):
        with Session(self.engine) as session:
            players = session.exec(select(Player)).all()
            players = [i.dict() for i in players]
            return pd.DataFrame.from_records(players)

    def _get_stats_from_db(self):
        with Session(self.engine) as session:
            stats = session.exec(select(CompetitionStats)).all()
            stats = [i.dict() for i in stats]
            return pd.DataFrame.from_records(stats)

    def get_data(self):
        df = self.stats_df[self.stats_df['seasonID'] == '23/24']
        df = df[df['competitionID'].str.contains('21') == 0]
        df['GA'] = df.apply(lambda row: row.goals + row.assists, axis=1)
        df['assists_p90'] = df.apply(
            lambda row: row.goals / row.minutesPlayed * 90 if row.minutesPlayed > 0 else 0, axis=1
        )
        df['goals_p90'] = df.apply(
            lambda row: row.assists / row.minutesPlayed * 90 if row.minutesPlayed > 0 else 0, axis=1
        )
        df['GA_p90'] = df.apply(
            lambda row: (row.goals + row.assists) / row.minutesPlayed * 90 if row.minutesPlayed > 0 else 0, axis=1
        )
        return df

    def get_data_for_league(self):
        df = self.get_data()
        df = df[df['competitionID'].str.endswith('1')]
        return df

    def get_bio(self):
        return self.bio_df

    def get_data_agg(self):
        df = self.get_data()
        df = df.groupby(['seasonID', 'clubID', 'playerID'], as_index=False).agg({
            'goals': 'sum',
            'assists': 'sum',
            'appearances': 'sum',
            'yellowCards': 'sum',
            'minutesPlayed': 'sum',
            'GA': 'sum',

        })
        df['assists_p90'] = df.apply(
            lambda row: row.goals / row.minutesPlayed * 90 if row.minutesPlayed > 0 else 0, axis=1
        )
        df['goals_p90'] = df.apply(
            lambda row: row.assists / row.minutesPlayed * 90 if row.minutesPlayed > 0 else 0, axis=1
        )
        df['GA_p90'] = df.apply(
            lambda row: (row.goals + row.assists) / row.minutesPlayed * 90 if row.minutesPlayed > 0 else 0, axis=1
        )
        df['competitionID'] = 'ALL'
        df['competitionName'] = 'All competitions'
        return df
