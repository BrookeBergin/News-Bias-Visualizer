import plotly.graph_objs as go
from plotly.offline import plot
from plotly.utils import PlotlyJSONEncoder
import json

def create_plot(data_by_source):
    fig = go.Figure()
    for source, points in data_by_source.items():
        # filter out None
        points = [(date, sentiment) for date, sentiment in points if sentiment is not None]
        if not points:
            continue

        points.sort()  # Sort by date
        dates = [p[0] for p in points]
        sentiments = [p[1] for p in points]
        fig.add_trace(go.Scatter(
            x=dates,
            y=sentiments,
            mode='lines+markers',
            name=source,
            hovertemplate = f'Date: %{{x}}<br>Sentiment: %{{y:.2f}}<extra>{source}</extra>'
        ))

    fig.update_layout(
        title="Sentiment Over Time",
        xaxis_title="Published Date",
        yaxis_title="Sentiment Score",
        hovermode="closest"
    )

    graphJSON = json.dumps(fig, cls=PlotlyJSONEncoder)
    return graphJSON
