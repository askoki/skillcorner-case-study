import pandas as pd
import streamlit as st
from skillcornerviz.standard_plots import scatter_plot as scatter
from skillcornerviz.standard_plots import radar_plot as radar

from skillcornerviz.standard_plots import bar_plot as bar

from helpers.utils import format_select_labels


def plot_ranking_table(df: pd.DataFrame, metric: str):
    fig, ax = bar.plot_bar_chart(
        df=df,
        metric=metric,
        label=format_select_labels(metric),
        # unit='km/h',
        primary_highlight_group=df.iloc[:3].player_id.values,
        add_bar_values=True,
        data_point_id='player_id',
        data_point_label='plot_label'
    )
    st.pyplot(fig)


def plot_scatter(df: pd.DataFrame, team_name: str, x_metric: str, y_metric: str):
    fig, ax = scatter.plot_scatter(
        df=df,
        x_metric=x_metric,
        y_metric=y_metric,
        data_point_id='team_name',
        data_point_label='player_name',
        # x_unit='m',
        # y_unit='m',
        x_label=format_select_labels(x_metric),
        y_label=format_select_labels(y_metric),
        primary_highlight_group=[team_name]
    )
    st.pyplot(fig)


def plot_radar(position_df: pd.DataFrame, plot_title: str, player_id: int, metrics: list, metrics_labels: list,
               position_label: str, competition_label: str, season_label: str):
    fig, ax = radar.plot_radar(df=position_df,
                               data_point_id='player_id',
                               label=player_id,
                               plot_title=plot_title,
                               metrics=metrics,
                               metric_labels=metrics_labels,
                               percentiles_precalculated=False,
                               positions=position_label,
                               matches=8,
                               minutes=60,
                               competitions=competition_label,
                               seasons=season_label,
                               add_sample_info=True)
    st.pyplot(fig)
