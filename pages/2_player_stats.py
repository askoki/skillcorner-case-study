import streamlit as st
from helpers.api import get_teams, get_team_players
from helpers.helpers import find_element_position
from helpers.plotting import plot_scatter, plot_radar, plot_violin
from helpers.utils import authenticate, sidebar_selections, add_page_logo, add_sidebar_logo, filter_by_suffix, \
    format_select_labels
from settings import METRIC_LABELS


def main():
    st.title('Player analysis')
    league_df, selection_dict = sidebar_selections()
    if league_df.empty:
        st.warning('No data found')
        return
    # ------------------------------
    teams_df = get_teams(competition_id=selection_dict['competition']['id'], season_id=selection_dict['season']['id'])
    teams_list = teams_df.name.unique()
    selected_team = st.selectbox('Select team', teams_list, index=0, key='team-select')
    team_id = teams_df.query(f'name=="{selected_team}"').squeeze().id

    position_column = 'group'
    if selection_dict['is_physical']:
        position_column = 'position_group'
        select_metric_type = st.selectbox(
            'Select metric type', METRIC_LABELS.keys(), index=0, format_func=lambda r: METRIC_LABELS[r],
            key='metric-type-select'
        )
        metric_values = filter_by_suffix(selection_dict['metrics'], select_metric_type)
    else:
        metric_values = selection_dict['metrics']

    players_df = get_team_players(
        competition_id=selection_dict['competition']['id'], season_id=selection_dict['season']['id'], team_id=team_id
    )
    players_df.loc[:, 'player_name'] = players_df.first_name + ' ' + players_df.last_name
    players2keep = league_df[league_df.team_id == team_id].player_name.unique()
    # filter out players with lower playing time
    players_df = players_df[players_df.player_name.isin(players2keep)]
    players_list = players_df.short_name.unique()
    selected_player = st.selectbox('Select player', players_list, index=0, key='player-select')
    player_id = players_df.query(f'short_name=="{selected_player}"').squeeze().id

    positions = league_df[position_column].unique().tolist()
    player_position = league_df.query(f'player_id=={player_id}').squeeze()[position_column]
    selected_position = st.selectbox(
        'Playing Position', positions, index=find_element_position(positions, player_position),
        key='player-position-select', disabled=True
    )

    # ---------------------
    x_axis = st.selectbox(
        'Select X-axis', options=metric_values, index=0,
        format_func=format_select_labels, key='x-axis-select'
    )
    y_axis = st.selectbox(
        'Select Y-axis', options=metric_values, index=1,
        format_func=format_select_labels, key='y-axis-select'
    )
    position_df = league_df[league_df[position_column] == player_position]
    plot_scatter(position_df, data_point_id='player_id', selected_id=player_id, x_metric=x_axis, y_metric=y_axis)
    # -----------------------

    radar_options = st.multiselect(
        'Select radar attributes', metric_values, default=list(metric_values)[:8],
        max_selections=10,
        format_func=format_select_labels, key='radar-multiselect'
    )
    plot_radar(
        position_df,
        f'Running Profile | {selected_player}',
        player_id,
        metrics=radar_options,
        position_label=player_position,
        competition_label=selection_dict['competition']['selected'],
        season_label=selection_dict['season']['selected']
    )

    violin_x_axis = st.selectbox(
        'Select X-axis', options=metric_values, index=find_element_position(list(metric_values), x_axis),
        format_func=format_select_labels, key='violin-axis-select'
    )

    plot_violin(
        position_df, data_point_id='player_id', x_metric=violin_x_axis, y_metric=position_column,
        highlight_list=[player_id]
    )


if __name__ == "__main__":
    add_page_logo()
    add_sidebar_logo()
    authenticate()
    if st.session_state['authentication_status']:
        main()
