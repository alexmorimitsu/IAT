import pandas as pd
import plotly.graph_objs as go


def compute_histogram(filtered_df):
    classes = filtered_df['manual_label'].value_counts().to_dict()

    print()
    labels = [l + ' (' + str(c) + ')' for l, c in zip(classes.keys(), classes.values())]
    total = 0
    for v in classes.values():
        total += v

    fig = go.Figure([go.Bar(x=labels, y=list(classes.values()))])
    fig.update_layout(
        title=str(total) + ' images selected.',
        margin=dict(l=0, r=0, t=30, b=0),
    )
    return fig