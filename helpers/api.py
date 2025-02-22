import pandas as pd
import requests
import streamlit as st
from requests.auth import HTTPBasicAuth

from helpers.helpers import urljoin

server_address = st.secrets.API.base_url
username = st.secrets.API.username
password = st.secrets.API.password


def get_competitions() -> pd.DataFrame:
    response = requests.get(
        urljoin(server_address, 'competitions/') + '?gender=male&age_group=adult&component_permission_for=all',
        auth=HTTPBasicAuth(username, password)
    )
    if response.status_code == 200:
        return pd.DataFrame(response.json()['results'])

    raise Exception('Competitions could not be fetched.')


def get_seasons(competition_id: int) -> pd.DataFrame:
    response = requests.get(
        urljoin(server_address, f'competitions/{competition_id}/editions/') + '?component_permission_for=all',
        auth=HTTPBasicAuth(username, password)
    )
    if response.status_code == 200:
        return pd.json_normalize(response.json()['results'], sep='_')

    raise Exception('Seasons could not be fetched.')


# def get_matches(competition_id: int, season_id: int) -> pd.DataFrame:
#     response = requests.get(
#         urljoin(server_address, 'matches/') + f'?competition={competition_id}&season={season_id}',
#         auth=HTTPBasicAuth(username, password)
#     )
#     if response.status_code == 200:
#         pd.json_normalize(response.json()['results'], sep='_')
#
#     raise Exception('Matches could not be fetched.')

def get_teams(competition_id: int, season_id: int) -> pd.DataFrame:
    response = requests.get(
        urljoin(server_address, 'teams/') + f'?competition={competition_id}&season={season_id}',
        auth=HTTPBasicAuth(username, password)
    )
    if response.status_code == 200:
        return pd.json_normalize(response.json()['results'], sep='_')

    raise Exception('Teams could not be fetched.')

def get_team_players(competition_id: int, season_id: int, team_id: int) -> pd.DataFrame:
    response = requests.get(
        urljoin(server_address, 'players/') + f'?competition={competition_id}&season={season_id}&team={team_id}',
        auth=HTTPBasicAuth(username, password)
    )
    if response.status_code == 200:
        return pd.json_normalize(response.json()['results'], sep='_')

    raise Exception('Teams could not be fetched.')


# def get_match(match_id: int) -> pd.DataFrame:
#     response = requests.get(
#         urljoin(server_address, f'match/{match_id}'),
#         auth=HTTPBasicAuth(username, password)
#     )
#     if response.status_code == 200:
#         import pdb;
#         pdb.set_trace()
#         return pd.DataFrame(response.json()['results'])
#
#     raise Exception('Matches could not be fetched.')

def get_player_physical(player_id: int, team_id: int, season_id: int) -> pd.DataFrame:
    response = requests.get(
        urljoin(server_address, 'physical/') + f'?player={player_id}&team={team_id}&season={season_id}',
        auth=HTTPBasicAuth(username, password)
    )
    if response.status_code == 200:
        return pd.json_normalize(response.json(), sep='_')

    raise Exception('Teams could not be fetched.')
