import streamlit as st
from helpers.api import get_teams
from helpers.helpers import find_element_position
from helpers.plotting import plot_ranking_table, plot_scatter, plot_violin
from helpers.utils import authenticate, sidebar_selections, add_page_logo, add_sidebar_logo, filter_by_suffix, \
    format_select_labels
from settings import METRIC_LABELS


def main():
    st.title('Team analysis')
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
    select_metric = st.selectbox(
        'Select metric', metric_values, index=0,
        format_func=format_select_labels, key='metric-select'
    )

    top10_df = league_df.sort_values(select_metric, ascending=False).iloc[:10]
    try:
        top10_df['plot_label'] = top10_df.player_name + ' | ' + top10_df['position_group']
    except KeyError:
        top10_df['plot_label'] = top10_df.player_name
    plot_ranking_table(top10_df, metric=select_metric)
    # ---------------------
    x_axis = st.selectbox(
        'Select X-axis', options=metric_values, index=find_element_position(list(metric_values), select_metric),
        format_func=format_select_labels, key='x-axis-select'
    )
    y_axis = st.selectbox(
        'Select Y-axis', options=metric_values, index=find_element_position(list(metric_values), select_metric)+1,
        format_func=format_select_labels, key='y-axis-select'
    )
    plot_scatter(league_df, data_point_id='team_name', selected_id=selected_team, x_metric=x_axis, y_metric=y_axis)
    # -----------------------
    violin_x_axis = st.selectbox(
        'Select X-axis', options=metric_values, index=find_element_position(list(metric_values), select_metric),
        format_func=format_select_labels, key='violin-axis-select'
    )
    team_players = league_df[league_df.team_id == team_id].player_id.unique()
    plot_violin(
        league_df, data_point_id='player_id', x_metric=violin_x_axis, y_metric=position_column,
        highlight_list=team_players
    )

if __name__ == "__main__":
    add_page_logo()
    add_sidebar_logo()
    authenticate()
    if st.session_state['authentication_status']:
        main()
