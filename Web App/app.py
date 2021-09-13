# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from raceplotly.plots import barplot


#	external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [ #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We',
        'crossorigin': 'anonymous'
    }
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

#BARCHART RACE CODE
top50 = pd.read_csv('Data/top50.csv')

colors = {'Western Europe': 'rgb(5, 169, 230)',
          'North America and ANZ': 'rgb(20, 73, 190)',
          'Middle East and North Africa': 'rgb(145,90,142)',
          'Latin America and Caribbean': 'rgb(222, 188, 196)',
          'Southeast Asia': 'rgb(252,185,8)',
          'Central and Eastern Europe': 'rgb(230,26,41)',
          'East Asia': 'rgb(248,124,4)',
          'Commonwealth of Independent States': 'rgb(99, 192, 159)',
          'Sub-Saharan Africa': 'rgb(57, 240, 119)'}

# my_raceplot = barplot(top50,  item_column='country', value_column='happiness_score', time_column='year', item_color=colors)

writeupbar= "     For the past 6 years, Western Europe produces the happiest countries " \
            "in the world and the majority of the top " \
            "50 also come from western countries or those of the developed countries"
top50['color'] = top50['region'].map(colors)

counts = []
counts_list = ["10", "25", "50"]
for i in counts_list:
    counts.append({
        "label": i,
        "value": i
    })

my_raceplot = barplot(
    top50,
    item_column='country',
    value_column='happiness_score',
    category_column='region',
    rank_column='rank',
    time_column='year',
    top_entries=25,
    item_color=colors)

top50race = my_raceplot.plot(title='Top 25 Happiest Countries (2015-2020)', item_label='Countries',
                             value_label='Happiness Score',
                             time_label='Year: ',
                             frame_duration=800)

top50race.update_layout(
    autosize=False,
    width=1300,
    height=900,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="rgb(223, 226, 219)",
)

# CHOROPLETH
whrdf = pd.read_csv('Data/choropleth.csv')

whrdf['year'] = whrdf['year'].fillna(2015)
whrdf['year'] = whrdf['year'].astype(int)

choro_happy = px.choropleth(whrdf,
                            locations="iso_a3",
                            color="happiness_score",
                            hover_name="country",
                            animation_frame="year",
                            projection="kavrayskiy7",
                            range_color=[whrdf['happiness_score'].min(), whrdf['happiness_score'].max()])

choro_happy.update_layout(autosize=False,
                          width=1000,
                          height=650,
                          margin={"r":0,"t":0,"l":0,"b":0},
                          paper_bgcolor="rgb(246, 250, 239)",
                          plot_bgcolor="rgb(246, 250, 239)")

factors = []
factors.append({"label": "Influence of GDP on Happiness Score", "value": "gdp_hscore"})
factors.append({"label": "Influence of Life Expectancy on Happiness Score", "value": "lifeexp_hscore"})
factors.append({"label": "Influence of Freedom on Happiness Score", "value": "freedom_hscore"})
factors.append({"label": "Influence of Generosity on Happiness Score", "value": "generosity_hscore"})
factors.append({"label": "Influence of Corruption on Happiness Score", "value": "corruption_hscore"})
factors.append({"label": "Actual Crime Rate", "value": "actual_crime"}),
factors.append({"label": "Actual GDP", "value": "actual_gdp"}),
factors.append({"label": "Actual Life Expectancy", "value": "actual_lifeexp"})


choro_factor = px.choropleth(whrdf,
                             locations="iso_a3",
                             color="gdp_hscore",
                             hover_name="country",
                             animation_frame="year",
                             projection="kavrayskiy7",
                             range_color=[whrdf['gdp_hscore'].min(), whrdf['gdp_hscore'].max()])

choro_factor.update_layout(autosize=True,
                           margin={"r":0,"t":0,"l":0,"b":0,"pad":4,"autoexpand":True},
                           paper_bgcolor="rgb(246, 250, 239)")

categories = ['GDP','Life Expectancy','Freedom',
              'Generosity', 'Corruption', 'GDP']

radardf     = whrdf[['year', 'country', 'region', 'gdp_hscore', 'lifeexp_hscore',
                     'freedom_hscore', 'generosity_hscore', 'corruption_hscore']]

radardf2015 = radardf[radardf['year'] == 2015].groupby(by=["region"]).mean()
radardf2016 = radardf[radardf['year'] == 2016].groupby(by=["region"]).mean()
radardf2017 = radardf[radardf['year'] == 2017].groupby(by=["region"]).mean()
radardf2018 = radardf[radardf['year'] == 2018].groupby(by=["region"]).mean()
radardf2019 = radardf[radardf['year'] == 2019].groupby(by=["region"]).mean()
radardf2020 = radardf[radardf['year'] == 2020].groupby(by=["region"]).mean()

radardflist = radardf[['region', 'gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                       'generosity_hscore', 'corruption_hscore']].groupby(by=["region"]).mean()
print(radardflist.head(10))

# df = pd.DataFrame(products, columns= ['Product', 'Price'])

radarlist   = radardflist[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()
radar2015   = radardf2015[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()
radar2016   = radardf2016[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()
radar2017   = radardf2017[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()
radar2018   = radardf2018[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()
radar2019   = radardf2019[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()
radar2020   = radardf2020[['gdp_hscore', 'lifeexp_hscore', 'freedom_hscore',
                           'generosity_hscore', 'corruption_hscore', 'gdp_hscore']].values.tolist()

# years for slider
# years = []
# years_list = sorted(whrdf['year'].unique())
# for i in years_list[1:]:
#     years.append({
#         "label": i,
#         "value": i
#     })

radar = go.Figure()

radar.add_trace(go.Scatterpolar(
      r=radarlist[0],
      theta=categories,
      name='Central and Eastern Europe'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[1],
      theta=categories,
      name='Commonwealth of Independent States'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[2],
      theta=categories,
      name='East Asia'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[3],
      theta=categories,
      name='Latin America and Caribbean'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[4],
      theta=categories,
      name='Middle East and North Africa'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[5],
      theta=categories,
      name='North America and ANZ'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[6],
      theta=categories,
      name='South Asia'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[7],
      theta=categories,
      name='Southeast Asia'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[8],
      theta=categories,
      name='Sub-Saharan Africa'
))
radar.add_trace(go.Scatterpolar(
      r=radarlist[9],
      theta=categories,
      name='Western Europe'
))


radar.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 1.5]
    )),
  showlegend=True, height=700, margin={"r":0,"t":0,"l":25,"b":0}
)

names = ['Happiness Score', 'GDP Influence', 'Life Expectancy Influence', 'Freedom Influence',
         'Generosity Influence', 'Corruption Influence', 'Actual Crime', 'Actual GDP', 'Actual Life Expectancy']
r = pd.DataFrame(index = names, columns = names)
r['Happiness Score'] = np.array([1, 0.79, 0.75, 0.55, 0.15, 0.42, -0.34, 0.73, 0.71])
r['GDP Influence'] = np.array([0.79, 1, 0.78, 0.36, -0.0067, 0.33, -0.55, 0.73, 0.8])
r['Life Expectancy Influence'] = np.array([0.75, 0.78, 1, 0.38, 0.019, 0.3, -0.54, 0.63, 0.82])
r['Freedom Influence'] = np.array([0.55, 0.36, 0.38, 1, 0.3, 0.46, -0.18, 0.45, 0.33])
r['Generosity Influence'] = np.array([0.15, -0.0067, 0.019, 0.3, 1, 0.29, -0.023, 0.23, 0.035])
r['Corruption Influence'] = np.array([0.42, 0.33, 0.3, 0.46, 0.29, 1, -0.35, 0.63, 0.29])
r['Actual Crime'] = np.array([-0.34, -0.55, -0.54, -0.18, -0.023, -0.35, 1, -0.47, -0.47])
r['Actual GDP'] = np.array([0.73, 0.73, 0.63, 0.45, 0.23, 0.63, -0.47, 1, 0.61])
r['Actual Life Expectancy'] = np.array([0.71, 0.8, 0.82, 0.33, 0.035, 0.29, -0.47, 0.61, 1])

mask = np.triu(np.ones_like(r, dtype=bool))
rLT = r.mask(mask)

heat = go.Heatmap(
    z = rLT,
    x = rLT.columns.values,
    y = rLT.columns.values,
    zmin = -1, # Sets the lower bound of the color domain
    zmax = 1,
    xgap = 1, # Sets the horizontal gap (in pixels) between bricks
    ygap = 1,
    colorscale = 'YlGnBu'
)

title = 'Correlation Matrix'

layout = go.Layout(
    title_text=title,
    title_x=0.5,
    width=600,
    height=600,
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    yaxis_autorange='reversed'
)

corr_heatmap=go.Figure(data=[heat], layout=layout)

app.layout = html.Div(className="mainContainer", children=[
    html.Section(className="headercontainer"),
    html.Section(className="container1", children=[
        html.Div(className="write-up", children=[
            html.Div(className="card border-secondary mb-3", children=[
                html.Div(className="card-header", children=[
                    html.Div(className="card-text",children="How many top happiest countries would you like to see?"),
                    html.Div(className="nav-item dropdown", children=[
                            dcc.Dropdown(
                                id="topdropdown",
                                options=counts
                            )
                    ])
                ]),
                html.Div(className="card-body", children=[
                    html.P(className="slogan1", children="Western Europe, the happiest region on earth!"),
                    html.P(className="paragraph", children=writeupbar)
                ])
             ])
        ]),
        html.Div(className="graph", children=[
            html.Div(className="barchartrace", children=[
                    dcc.Graph(
                        id="top-25-bar-race",
                        figure=top50race
                     )
                 ])
            ])
        ]),
    html.Section(className="container2", children=[
        html.Div(className="choro-happy", children=[
            dcc.Graph(
                id="choropleth-map-happy",
                figure=choro_happy
             )
        ])
    ]),
    html.Section(className="container3", children=[
        html.Div(className="write-up-factors", children=[
            html.Div(className="card border-secondary mb-3", children=[
                html.Div(className="card-header", children=[
                    html.Div(className="card-text", children="What would you like to see?"),
                    html.Div(className="choro-inf-dropdown", children=[
                        dcc.Dropdown(
                            id="factor-radio",
                            options=factors
                        )
                    ])
                ]),
                html.Div(className="card-body", children=[
                    html.P(className="paragraph-factors", children=writeupbar)
                ])
            ])
        ]),
        html.Div(className="graph-factors", children=[
                dcc.Graph(
                    id="choropleth-map-factor",
                    figure=choro_factor
                )
        ])
    ]),
    html.Section(className="container4", children=[
        html.Div(className="write-up-radar", children=[
            html.Div(className="card border-secondary mb-3", children=[
                html.Div(className="card-header", children=[
                    html.Div(className="card-text", children="What year you like to see?"),
                    html.Div(className="radarslider", children=[
                        dcc.Slider(
                            id="radar-slider",
                            min=2015,
                            max=2020,
                            step=None,
                            marks={2015: '2015',
                                   2016: '2016',
                                   2017: '2017',
                                   2018: '2018',
                                   2019: '2019',
                                   2020: '2020'},
                            value=6
                        )
                    ])
                ]),
                html.Div(className="card-body", children=[
                    html.P(className="paragraph-factors", children=writeupbar)
                ])
            ])
        ]),
        html.Div(className="graph-radar", children=[
                    dcc.Graph(
                        id="radar-factor",
                        figure=radar
                    )
        ])
    ]),
    html.Section(className="container5", children=[
        html.Div(className="write-up-corr", children=[
            html.Div(className="card border-secondary mb-3", children=[
                html.Div(className="card-header", children=[
                    html.Div(className="card-text", children="[iNSERT tITLE PLS]")
                ]),
                html.Div(className="card-body", children=[
                    html.P(className="paragraph-factors", children=writeupbar)
                ])
            ])
        ]),
        html.Div(className="graph-corr", children=[
            dcc.Graph(
                id="heatmap",
                figure=corr_heatmap
            )
        ])
    ])
])

@app.callback(
    # id, property
    Output('top-25-bar-race', 'figure'),
    Input('topdropdown', 'value')
)

def update_barrace_graph(selected_count):
    if selected_count is None:
        #top 25
        my_raceplot = barplot(
            top50,
            item_column='country',
            value_column='happiness_score',
            category_column='region',
            rank_column='rank',
            time_column='year',
            top_entries=25,
            item_color=colors)

        top50race = my_raceplot.plot(title='Top 25 Happiest Countries (2015-2020)', item_label='Countries',
                                     value_label='Happiness Score',
                                     time_label='Year: ',
                                     frame_duration=800)

    else:
        my_raceplot = barplot(
            top50,
            item_column='country',
            value_column='happiness_score',
            category_column='region',
            rank_column='rank',
            time_column='year',
            top_entries=int(selected_count),
            item_color=colors)

        title = "Top" + " " + str(selected_count) + " " + "Happiest Countries"

        top50race = my_raceplot.plot(title=title, item_label='Countries',
                                     value_label='Happiness Score',
                                     time_label='Year: ',
                                     frame_duration=800)

    top50race.update_layout(
        autosize=False,
        width=1000,
        height=650,
        margin=dict(
            l=50,
            r=50,
            b=50,
            t=100,
            pad=4
        ),
        title_font_family="Franklin Gothic",
        title_font_size=40,
        paper_bgcolor="white",
    )

    return top50race

@app.callback(
    # id, property
    Output('choropleth-map-factor', 'figure'),
    Input('factor-radio', 'value')
)
def update_chorofactor_graph(selected_factor):
    if selected_factor is None:
        title = ""
        choro_factor = px.choropleth(whrdf,
                                     locations="iso_a3",
                                     color="gdp_hscore",
                                     hover_name="country",
                                     animation_frame="year",
                                     projection="kavrayskiy7",
                                     range_color=[whrdf['gdp_hscore'].min(), whrdf['gdp_hscore'].max()])

    else:
        choro_factor = px.choropleth(whrdf,
                                     locations="iso_a3",
                                     color=selected_factor,
                                     hover_name="country",
                                     animation_frame="year",
                                     projection="kavrayskiy7",
                                     range_color=[whrdf[selected_factor].min(), whrdf[selected_factor].max()])
    choro_factor.update_layout(autosize=True,
                               margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 4, "autoexpand": True},
                               paper_bgcolor="rgb(246, 250, 239)")
    return choro_factor

@app.callback(
    # id, property
    Output('radar-factor', 'figure'),
    Input('radar-slider', 'value')
)
def update_radarfactor_graph(selected_year):
    if selected_year is None:
        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
            r=radarlist[0],
            theta=categories,
            name='Central and Eastern Europe'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[1],
            theta=categories,
            name='Commonwealth of Independent States'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[2],
            theta=categories,
            name='East Asia'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[3],
            theta=categories,
            name='Latin America and Caribbean'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[4],
            theta=categories,
            name='Middle East and North Africa'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[5],
            theta=categories,
            name='North America and ANZ'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[6],
            theta=categories,
            name='South Asia'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[7],
            theta=categories,
            name='Southeast Asia'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[8],
            theta=categories,
            name='Sub-Saharan Africa'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radarlist[9],
            theta=categories,
            name='Western Europe'
        ))

    else:
        radaryear = radarlist
        if selected_year == 2015:
            radaryear = radar2015
        elif selected_year == 2016:
            radaryear = radar2016
        elif selected_year == 2017:
            radaryear = radar2017
        elif selected_year == 2018:
            radaryear = radar2018
        elif selected_year == 2019:
            radaryear = radar2019
        elif selected_year == 2020:
            radaryear = radar2020

        radar = go.Figure()

        radar.add_trace(go.Scatterpolar(
            r=radaryear[0],
            theta=categories,
            name='Central and Eastern Europe'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[1],
            theta=categories,
            name='Commonwealth of Independent States'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[2],
            theta=categories,
            name='East Asia'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[3],
            theta=categories,
            name='Latin America and Caribbean'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[4],
            theta=categories,
            name='Middle East and North Africa'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[5],
            theta=categories,
            name='North America and ANZ'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[6],
            theta=categories,
            name='South Asia'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[7],
            theta=categories,
            name='Southeast Asia'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[8],
            theta=categories,
            name='Sub-Saharan Africa'
        ))
        radar.add_trace(go.Scatterpolar(
            r=radaryear[9],
            theta=categories,
            name='Western Europe'
        ))

    radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1.5]
            )),
        showlegend=True, height=700,
        margin={"r": 0, "t": 0, "l": 25, "b": 0}
    )

    return radar

if __name__ == '__main__':
    app.run_server(debug=True)