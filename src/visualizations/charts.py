import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

class ChartBuilder:
    @staticmethod
    def create_bar_chart(data, x_col, y_col, title=""):
        """Create a basic bar chart"""
        if isinstance(data, list):
            data = pd.DataFrame(data)
        fig = px.bar(data, x=x_col, y=y_col, title=title)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_time_series(data, date_col, value_col, title=""):
        """Create a time series line chart"""
        if isinstance(data, list):
            data = pd.DataFrame(data)
        data[date_col] = pd.to_datetime(data[date_col])
        fig = px.line(data, x=date_col, y=value_col, title=title)
        return fig
    
    @staticmethod
    def create_pie_chart(data, names_col, values_col, title=""):
        """Create a pie chart"""
        fig = px.pie(data, names=names_col, values=values_col, title=title)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        return fig
    
    @staticmethod
    def create_scatter_plot(data, x_col, y_col, color_col=None, title=""):
        """Create a scatter plot"""
        fig = px.scatter(data, x=x_col, y=y_col, color=color_col, title=title)
        fig.update_traces(marker=dict(size=12, line=dict(width=2)))
        return fig