import matplotlib.pyplot as plt
import plotly
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def bar_chart(df, x, y, category):
    title = f'{x}({y}) ' + category

    fig = px.bar(df, x=df.columns[0], y=df[x],
                 title=title,
                 color=df[y],
                 text=df[y],
                 template='plotly_dark')
                 
    fig.update_traces(textposition='outside')

    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'},
                      height=650)

    fig.update_xaxes(tickangle=-45)

    return plotly.offline.plot(fig, output_type='div')


def pie_chart(df, x, y, category):
    title = f'{x} and {y} ' + category

    fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
    fig.add_trace(go.Pie(labels=df[df.columns[0]], values=df[x], name=x),
                  1, 1)
    fig.add_trace(go.Pie(labels=df[df.columns[0]], values=df[y], name=y),
                  1, 2)

    fig.update_traces(hole=0.3, textposition='inside', textinfo='percent+label', showlegend=True)
    fig.update_layout(title={'x': 0.5,
                             'xanchor': 'center'},
                      template='plotly_dark',
                      title_text=title,
                      annotations=[dict(text=x, x=0.2, y=0.5, font_size=13, showarrow=False),
                                   dict(text=y, x=0.825, y=0.5, font_size=15, showarrow=False)],
                      height=650)

    return plotly.offline.plot(fig, output_type='div')


def table(df):
    df3 = ff.create_table(df)
    # return df3
    return plotly.offline.plot(df3, output_type='div')


def time_series(confirmed, deaths, recovered):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=confirmed['Date'], y=confirmed['India'], mode='lines', name='Confirmed'))
    fig.add_trace(go.Scatter(x=deaths['Date'], y=deaths['India'], mode='lines', name='Deaths'))
    fig.add_trace(go.Scatter(x=recovered['Date'], y=recovered['India'], mode='lines', name='Recovered'))

    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(title={'x': 0.5, 'xanchor': 'center'},
                      title_text='Time Series for confirmed, deaths and recovered',
                      template='plotly_dark',
                      height=700)
    return plotly.offline.plot(fig, output_type='div')
