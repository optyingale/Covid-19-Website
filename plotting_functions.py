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
                      height=650,
                      hovermode='x')

    fig.update_xaxes(tickangle=-45)

    return plotly.offline.plot(fig, output_type='div')


def daily_bar(deaths, ma=3):
    df = deaths
    daily_deaths = []

    for i in range(df.shape[0]):
        if i == 0:
            daily_deaths.append(0)
        else:
            daily_deaths.append(df.iloc[i]['India'] - df.iloc[i - 1]['India'])

    df.insert(2, "Daily Deaths", daily_deaths, True)

    df['MA'] = df['Daily Deaths'].rolling(ma).mean()
    df['MA'].fillna(0, inplace=True)

    fig = go.Figure([go.Bar(x=df['Date'], y=df['Daily Deaths'], name='Daily Deaths')])
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA'], mode='lines', name=f'moving average of {ma}'))
    fig.update_layout(height=700,
                      title={'x': 0.5, 'xanchor': 'center'},
                      hovermode='x',
                      template='plotly_dark',
                      title_text='Daily Deaths (India)')

    return plotly.offline.plot(fig, output_type='div')


def pie_chart(df, x, y, category):
    title = f'{x} and {y} ' + category

    other = ['other']
    for column in df.columns[1:]:
        other.append(df.loc[21:][column].sum())

    df = df.drop(df.index[21:])
    df.loc[df.index.max()+1] = other

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
                      height=700,
                      hovermode='x')
    return plotly.offline.plot(fig, output_type='div')
