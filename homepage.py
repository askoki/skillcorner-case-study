import streamlit as st
from helpers.api import get_teams, get_team_players
from helpers.helpers import find_element_position
from helpers.plotting import plot_ranking_table, plot_distance_scatter, plot_radar
from helpers.utils import authenticate, sidebar_selections, add_page_logo, add_sidebar_logo


def main():
    st.title('CSV Data Viewer')
    league_df, selection_dict = sidebar_selections()

    psv99_top10_df = league_df.sort_values('psv99', ascending=False).iloc[:10]
    psv99_top10_df['plot_label'] = psv99_top10_df['player_short_name'] + ' | ' + psv99_top10_df['position_group']

    plot_ranking_table(psv99_top10_df)
    # ------------------------------
    teams_df = get_teams(competition_id=selection_dict['competition']['id'], season_id=selection_dict['season']['id'])
    teams_list = teams_df.name.unique()
    selected_team = st.selectbox('Select team', teams_list, index=0, key='team-select')
    team_id = teams_df.query(f'name=="{selected_team}"').squeeze().id

    x_axis = st.selectbox("Select X-axis", options=selection_dict['metrics'],
                          index=find_element_position(selection_dict['metrics'], 'total_distance_per_90'))
    y_axis = st.selectbox("Select Y-axis", options=selection_dict['metrics'], index=find_element_position(selection_dict['metrics'], 'hi_distance_per_90'))
    plot_distance_scatter(league_df, team_name=selected_team, x_metric=x_axis, y_metric=y_axis)
    # -----------------------

    players_df = get_team_players(competition_id=selection_dict['competition']['id'], season_id=selection_dict['season']['id'], team_id=team_id)
    players_list = players_df.short_name.unique()
    selected_player = st.selectbox('Select player', players_list, index=0, key='player-select')

    player_id = players_df.query(f'short_name=="{selected_player}"').squeeze().id

    plot_metrics = {
        'meters_per_minute_tip': 'Meters Per Minute TIP',
        'meters_per_minute_otip': 'Meters Per Minute OTIP',
        'highaccel_count_per_60_bip': 'Number Of High Accels Per 60 BIP',
        'highdecel_count_per_60_bip': 'Number Of High Decels Per 60 BIP',
        'sprint_count_per_60_bip': 'Number Sprints Per 60 BIP',
        'psv99': 'Peak Sprint Velocity 99th Percentile'
    }
    player_position = league_df.query(f'player_id=={player_id}').squeeze().position_group
    if len(player_position) < 1:
        st.warning('Player does not have enough matches for radar plot.')
    else:
        position_physical_df = league_df[league_df.position_group == player_position]
        plot_radar(
            position_physical_df,
            f'Running Profile | {selected_player}',
            player_id,
            metrics=[key for key in plot_metrics.keys()],
            metrics_labels=plot_metrics,
            position_label=player_position,
            competition_label=selection_dict['competition']['selected'],
            season_label=selection_dict['season']['selected']
        )


if __name__ == "__main__":
    add_page_logo()
    add_sidebar_logo()
    authenticate()
    if st.session_state['authentication_status']:
        main()
