import streamlit as st
import plotly.express as px

from helpers.api import get_competitions, get_seasons, get_teams, get_team_players, get_player_physical


def main():
    st.title("CSV Data Viewer")
    competition_df = get_competitions()
    comp_list = competition_df.name.unique()
    selected_competition = st.selectbox('Select competition', comp_list, index=0, key='competition-select')

    comp_id = competition_df.query(f'name=="{selected_competition}"').squeeze().id

    seasons_df = get_seasons(competition_id=comp_id)
    season_list = seasons_df.season_name.unique()
    selected_season = st.selectbox('Select season', season_list, index=0, key='season-select')

    season_id = seasons_df.query(f'season_name=="{selected_season}"').squeeze().season_id

    teams_df = get_teams(competition_id=comp_id, season_id=season_id)
    teams_list = teams_df.name.unique()
    selected_team = st.selectbox('Select team', teams_list, index=0, key='team-select')
    team_id = teams_df.query(f'name=="{selected_team}"').squeeze().id

    players_df = get_team_players(competition_id=comp_id, season_id=season_id, team_id=team_id)
    players_list = players_df.short_name.unique()
    selected_player = st.selectbox('Select player', players_list, index=0, key='player-select')

    player_id = players_df.query(f'short_name=="{selected_player}"').squeeze().id

    player_physical_df = get_player_physical(player_id=player_id, team_id=team_id, season_id=season_id)

    st.subheader("Data Table")
    st.write(player_physical_df)

    # COLS2LOOK = [
    #     'Distance', 'Sprinting Distance', 'HSR Distance', 'Running Distance', 'Count Medium Acceleration', 'Count Medium Deceleration'
    # ]
    # Options for chart x, y & hover values.
    columns = player_physical_df.select_dtypes(include='number').columns.tolist()
    x_axis = st.selectbox("Select X-axis", options=columns)
    y_axis = st.selectbox("Select Y-axis", options=columns)

    hover_name = st.selectbox("Select Third Column for Hover Data (Optional)", options=["None"] + columns, index=0)
    # Chart plotting.
    if st.button("Plot Chart"):
        if hover_name != "None":
            fig = px.scatter(player_physical_df, x=x_axis, y=y_axis, hover_name=hover_name)
        else:
            fig = px.scatter(player_physical_df, x=x_axis, y=y_axis)
        st.plotly_chart(fig)


if __name__ == "__main__":
    main()
