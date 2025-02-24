from typing import Tuple

import pandas as pd
import requests
import streamlit as st
from requests.auth import HTTPBasicAuth
from skillcorner.client import SkillcornerClient
from skillcornerviz.utils import skillcorner_physical_utils as p_utils
from skillcornerviz.utils import skillcorner_game_intelligence_utils as gi_utils
from helpers.helpers import urljoin
from settings import RUNS

server_address = st.secrets.API.base_url
username = st.secrets.API.username
password = st.secrets.API.password

client = SkillcornerClient(username=username, password=password)


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


def get_player_physical(player_id: int, team_id: int, season_id: int) -> pd.DataFrame:
    response = requests.get(
        urljoin(server_address, 'physical/') + f'?player={player_id}&team={team_id}&season={season_id}',
        auth=HTTPBasicAuth(username, password)
    )
    if response.status_code == 200:
        return pd.json_normalize(response.json(), sep='_')

    raise Exception('Teams could not be fetched.')


@st.cache_resource
def get_league_physical(competition_id: int, season_id: int) -> Tuple[pd.DataFrame, list]:
    data = client.get_physical(params={
        'competition': competition_id, 'season': season_id,
        'group_by': 'player,team,competition,season,group',
        'possession': 'all,tip,otip',
        'playing_time__gte': 60,
        'count_match__gte': 8,
        'data_version': '3'
    })
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(), []
    metrics = p_utils.add_standard_metrics(df)
    return df, metrics


@st.cache_resource
def get_league_off_ball_runs(competition_id: int, season_id: int) -> Tuple[pd.DataFrame, list]:
    data = client.get_in_possession_off_ball_runs(params={
        'competition': competition_id, 'season': season_id,
        'group_by': 'player,competition,team,group',
        'average_per': '30_min_tip',
        'playing_time__gte': 60,
        'count_match__gte': 8,
        'run_type': 'all,run_in_behind,run_ahead_of_the_ball,'
                    'support_run,pulling_wide_run,coming_short_run,'
                    'underlap_run,overlap_run,dropping_off_run,'
                    'pulling_half_space_run,cross_receiver_run'
    })
    df = pd.DataFrame(data)
    if df.empty:
        return pd.DataFrame(), []
    # metrics is empty in this case, workaround with RUNS dict
    metrics = gi_utils.add_run_normalisations(df)
    return df, RUNS.keys()
