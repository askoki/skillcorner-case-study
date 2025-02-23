import pandas as pd
import streamlit as st
from PIL import Image
from typing import Tuple
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


def add_page_logo():
    img = Image.open('skillcorner_logo.jpeg')
    st.set_page_config(
        page_title="Skillcorner Case Study",
        page_icon=img
    )


def add_sidebar_logo():
    img = Image.open('skillcorner.png')
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )
    st.sidebar.image(image=img)
    st.sidebar.title('Skillcorner Case Study')


def sidebar_selections() -> Tuple[pd.DataFrame, dict]:
    with st.sidebar:
        competition_df = get_competitions()
        comp_list = competition_df.name.unique()
        selected_competition = st.selectbox('Select competition', comp_list, index=0, key='competition-select')

        comp_id = competition_df.query(f'name == \"{selected_competition}\"').squeeze().id

        seasons_df = get_seasons(competition_id=comp_id)
        season_list = seasons_df.season_name.unique()
        selected_season = st.selectbox('Select season', season_list, index=0, key='season-select')

        season_id = seasons_df.query(f'season_name == \"{selected_season}\"').squeeze().season_id

        selected_data_source = st.selectbox('Select data source', ['Physical', 'Off ball runs'], index=1,
                                            key='data-source-select')
    is_physical = False
    if selected_data_source == 'Physical':
        df, metrics = get_league_physical(competition_id=comp_id, season_id=season_id)
        is_physical = True
    else:
        df, metrics = get_league_off_ball_runs(competition_id=comp_id, season_id=season_id)
    return_dict = {
        'is_physical': is_physical,
        'metrics': metrics,
        'competition': {
            'selected': selected_competition,
            'id': comp_id,
        },
        'season': {
            'selected': selected_season,
            'id': season_id,
        }
    }
    return df, return_dict


def filter_by_suffix(items: list, suffix: str) -> list:
    series = pd.Series(items)
    return series[series.str.endswith(suffix)].tolist()


def format_select_labels(r):
    return r.replace('_', ' ').capitalize()
