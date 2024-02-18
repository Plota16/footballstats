import json

import requests

from src.model import Player, CompetitionStats


class TransfermarktAPI:

    def __init__(self):
        self._url = 'https://transfermarkt-api.vercel.app/'

    def get_club_id_by_name(self, club_name: str):
        club_name = club_name.replace(' ', '%20')
        response = requests.get(f'{self._url}/clubs/search/{club_name}')
        if response.status_code != 200:
            print('Error', 'get_club_id_by_name')
        response_test = json.loads(response.text)
        return response_test['results'][0]['id']

    def get_club_players(self, club_id: int):
        response = requests.get(f'{self._url}/clubs/{club_id}/players')
        if response.status_code != 200:
            print('Error', 'get_club_players')
        response_test = json.loads(response.text)
        player_ids = []
        for player in response_test['players']:
            player_ids.append(player['id'])
        return player_ids

    def get_player_id_by_name(self, player_name: str):
        player_name = player_name.replace(' ', '%20')
        response = requests.get(f'{self._url}/players/search/{player_name}')
        if response.status_code != 200:
            print('Error', 'get_player_id_by_name')
        response_test = json.loads(response.text)
        return response_test['results'][0]['id']

    def get_player_bio_by_id(self, player_id: int):
        response = requests.get(f'{self._url}/players/{player_id}/profile')
        if response.status_code != 200:
            print('Error', 'get_player_bio_by_id')
        response_test = json.loads(response.text)

        try:
            height = float(response_test['height'][:-1].replace(',', '.'))
        except KeyError:
            height = 0

        try:
            imageURL = response_test['imageURL']
        except KeyError:
            imageURL = ''

        try:
            foot = response_test['foot']
        except KeyError:
            foot = ''


        return Player(
            playerID=response_test['id'],
            name=response_test['description'].split(',')[0],
            description=response_test['description'],
            imageURL=imageURL,
            age=response_test['age'],
            height=height,
            citizenship=response_test['citizenship'][0],
            position=response_test['position']['main'],
            foot=foot,
            shirtNumber=int(response_test['shirtNumber'].replace('#', '')),
            club_id=response_test['club']['id'],
            marketValue=(
                response_test['marketValue']
                .replace('€', '')
                .replace('.', '')
                .replace('m', '000000')
                .replace('k', '000')
            )
        )


    def get_player_stats_by_id(self, player_id):
        response = requests.get(f'{self._url}/players/{player_id}/stats')
        if response.status_code != 200:
            print('Error', 'get_player_stats_by_id')
        response_test = json.loads(response.text)
        stats = []
        for competition in response_test['stats']:
            try:
                assists = competition['assists']
            except KeyError:
                assists = 0

            try:
                goals = competition['goals']
            except KeyError:
                goals = 0

            try:
                yellowCards = competition['yellowCards']
            except KeyError:
                yellowCards = 0

            try:
                appearances = competition['appearances']
            except KeyError:
                appearances = 0

            try:
                minutesPlayed = competition['minutesPlayed']
                minutesPlayed = minutesPlayed.replace('.', '').replace("'", '')
            except KeyError:
                minutesPlayed = 0

            stats.append(CompetitionStats(
                playerID=response_test['id'],
                clubID=competition['clubID'],
                seasonID=competition['seasonID'],
                competitionID=competition['competitionID'],
                competitionName=competition['competitionName'],
                appearances=int(appearances),
                goals=int(goals),
                assists=int(assists),
                yellowCards=int(yellowCards),
                minutesPlayed=int(minutesPlayed)
            ))

        return stats


