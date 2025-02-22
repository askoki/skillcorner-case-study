import streamlit as st
from helpers.api import get_competitions, get_seasons, get_teams, get_team_players, get_player_physical, \
    get_league_physical
from helpers.helpers import find_element_position
from helpers.plotting import plot_spv99_table, plot_distance_scatter, plot_radar


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

    phy_league_df, metrics = get_league_physical(competition_id=comp_id, season_id=season_id)
    psv99_top10_df = phy_league_df.sort_values('psv99', ascending=False).iloc[:10]
    psv99_top10_df['plot_label'] = psv99_top10_df['player_short_name'] + ' | ' + psv99_top10_df['position_group']

    plot_spv99_table(psv99_top10_df)
    # ------------------------------
    teams_df = get_teams(competition_id=comp_id, season_id=season_id)
    teams_list = teams_df.name.unique()
    selected_team = st.selectbox('Select team', teams_list, index=0, key='team-select')
    team_id = teams_df.query(f'name=="{selected_team}"').squeeze().id

    x_axis = st.selectbox("Select X-axis", options=metrics,
                          index=find_element_position(metrics, 'total_distance_per_90'))
    y_axis = st.selectbox("Select Y-axis", options=metrics, index=find_element_position(metrics, 'hi_distance_per_90'))
    plot_distance_scatter(phy_league_df, team_name=selected_team, x_metric=x_axis, y_metric=y_axis)
    # -----------------------

    players_df = get_team_players(competition_id=comp_id, season_id=season_id, team_id=team_id)
    players_list = players_df.short_name.unique()
    selected_player = st.selectbox('Select player', players_list, index=0, key='player-select')

    player_id = players_df.query(f'short_name=="{selected_player}"').squeeze().id

    player_physical_df = get_player_physical(player_id=player_id, team_id=team_id, season_id=season_id)

    plot_metrics = {
        'meters_per_minute_tip': 'Meters Per Minute TIP',
        'meters_per_minute_otip': 'Meters Per Minute OTIP',
        'highaccel_count_per_60_bip': 'Number Of High Accels Per 60 BIP',
        'highdecel_count_per_60_bip': 'Number Of High Decels Per 60 BIP',
        'sprint_count_per_60_bip': 'Number Sprints Per 60 BIP',
        'psv99': 'Peak Sprint Velocity 99th Percentile'
    }
    player_position = phy_league_df.query(f'player_id=={player_id}').squeeze().position_group
    if len(player_position) < 1:
        st.warning('Player does not have enough matches for radar plot.')
    else:
        position_physical_df = phy_league_df[phy_league_df.position_group == player_position]
        plot_radar(
            position_physical_df,
            f'Running Profile | {selected_player}',
            player_id,
            metrics=[key for key in plot_metrics.keys()],
            metrics_labels=plot_metrics,
            position_label=player_position,
            competition_label=selected_competition,
            season_label=selected_season
        )


if __name__ == "__main__":
    main()
