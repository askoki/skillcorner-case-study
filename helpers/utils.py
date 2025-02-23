from typing import Tuple

import pandas as pd
import streamlit as st

from streamlit_authenticator import Authenticate

from helpers.api import get_competitions, get_seasons, get_league_physical, get_league_off_ball_runs


def authenticate():
    credentials = {
        'usernames': {}
    }
    for user in st.secrets.auth.users:
        single_cred_dict: dict = {}
        single_cred_dict[user['username']] = {
            'email': user['email'],
            'name': user['name'],
            'password': user['password']
        }
        credentials['usernames'].update(single_cred_dict)

    authenticator = Authenticate(
        credentials,
        st.secrets.auth.cookie['name'],
        st.secrets.auth.cookie['key'],
        st.secrets.auth.cookie['expiry_days'],
    )
    authenticator.login()

    if st.session_state['authentication_status']:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')


def sidebar_selections() -> Tuple[pd.DataFrame, list, int, int]:
    with st.sidebar:
        competition_df = get_competitions()
        comp_list = competition_df.name.unique()
        selected_competition = st.selectbox('Select competition', comp_list, index=0, key='competition-select')

        comp_id = competition_df.query(f'name == \"{selected_competition}\"').squeeze().id

        seasons_df = get_seasons(competition_id=comp_id)
        season_list = seasons_df.season_name.unique()
        selected_season = st.selectbox('Select season', season_list, index=0, key='season-select')

        season_id = seasons_df.query(f'season_name == \"{selected_season}\"').squeeze().season_id

        selected_data_source = st.selectbox('Select data source', ['Physical', 'Off ball runs'], index=0,
                                            key='data-source-select')

    if selected_data_source == 'Physical':
        df, metrics = get_league_physical(competition_id=comp_id, season_id=season_id)
    else:
        df, metrics = get_league_off_ball_runs(competition_id=comp_id, season_id=season_id)
    return df, metrics, comp_id, season_id
