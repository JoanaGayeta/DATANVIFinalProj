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
from raceplotly_happiness.plots import barplot


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
server = app.server
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
introparagraph = "Happiness is a subjective matter which is tricky to quantify," \
                 " but it is a key emotion in understanding people. While this would" \
                 " enable us to partially determine the possible key indicators of people’s " \
                 "happiness, such knowledge could aid in policy-making, allowing it to be much" \
                 " more effective and streamlined towards what would lead to a generally happy" \
                 " population. Through a generally happy population, it is hoped that productivity" \
                 " would be boosted as well."
writeupbar = "For the past 6 years, Western Europe is home to the happiest countries " \
             "in the world. The majority of the top 50 happiest countries also come " \
             "from western and developed regions (i.e., Latin America and the Caribbean" \
             ", North America and ANZ)."

writeupcorr= "All of the factors have a strong to very strong positive correlation " \
             "except when the actual crime rate for each country is involved. With this, " \
             "we can say that as the crime rate of a country increases, the values of " \
             "several variables tend to decrease with a strength of weak to medium."
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
                          width=900,
                          height=500,
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

choro_factor.update_layout(autosize=False,
                           width=900,
                           height=500,
                           margin={"r":0,"t":0,"l":0,"b":0,"pad":4,"autoexpand":True},
                           paper_bgcolor="rgb(255, 255, 255)")

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
#print(radardflist.head(10))

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


radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 1.5])),
                    showlegend=True, height=200, margin={"r":0,"t":0,"l":25,"b":0},
                    paper_bgcolor="rgb(246, 250, 239)",
                    legend=dict(
                        yanchor="top",
                        xanchor="left"

                    )
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
    colorscale = 'Tropic'
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

parfactors="For the year 2017, the influence of GDP on happiness " \
           "score peaked on most countries around the" \
           "world. The succeeding years however, it dropped. " \
           "There is little to no changes in the influence " \
           "in most African countries and some Asian countries."


app.layout = html.Div(className="mainContainer", children=[
    html.Section(id="headercontainer"),
    html.Section(id="introcontainer", children=[
        html.Div(className="introDiv", children=[
            html.P(children=introparagraph),
        ]),
        html.Div(className="button1", children=[
            html.A(className="toC1", href="#container1", children=[
                html.Img(className="scrolly", src="assets\images\scrolly.gif")
            ])
        ])
    ]),
    html.Section(id="container1", children=[
        html.Div(className="left1", children=[
            html.Div(className="write-up", children=[
                html.Div(className="card border-secondary mb-3", children=[
                    html.Div(className="card-header", children=[
                        html.Div(className="card-text",
                                 children="How many top happiest countries would you like to see?"),
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
            html.Div(className="legend", children=[
                html.P(className="legendTitle", children="Regions"),
                html.Table(className="legendTable", children=[
                    html.Tbody(className="tableBody", children=[
                        html.Tr(className="cee", children=[
                            html.Td(className="ceeColor"),
                            html.Td(className="tdTitle", children="Central and Eastern Europe")
                        ]),
                        html.Tr(className="ea", children=[
                            html.Td(className="eaColor"),
                            html.Td(className="tdTitle", children="East Asia")
                        ]),
                        html.Tr(className="sea", children=[
                            html.Td(className="seaColor"),
                            html.Td(className="tdTitle", children="Southeast Asia")
                        ]),
                        html.Tr(className="ssa", children=[
                            html.Td(className="ssaColor"),
                            html.Td(className="tdTitle", children="Sub-Saharan Africa")
                        ]),
                        html.Tr(className="cis", children=[
                            html.Td(className="cisColor"),
                            html.Td(className="tdTitle", children="Commonwealth of Independent States")
                        ]),
                        html.Tr(className="we", children=[
                            html.Td(className="weColor"),
                            html.Td(className="tdTitle", children="Western Europe")
                        ]),
                        html.Tr(className="naanz", children=[
                            html.Td(className="naanzColor"),
                            html.Td(className="tdTitle", children="North America and ANZ")
                        ]),
                        html.Tr(className="mena", children=[
                            html.Td(className="menaColor"),
                            html.Td(className="tdTitle", children="Middle East and North Africa")
                        ]),
                        html.Tr(className="lac", children=[
                            html.Td(className="lacColor"),
                            html.Td(className="tdTitle", children="Latin America and Carribean")
                        ])
                    ])
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
            ]),
        html.Div(className="button2", children=[
            html.A(className="toC2", href="#container2", children=[
                html.Img(className="scrolly2", src="assets\images\scrolly2.gif")
            ])
        ])
    ]),
    html.Section(id="container2", children=[
        html.Div(className="write-up-happy", children=[
            html.Div(className="card border-secondary mb-3", children=[
                html.Div(className="card-header", children=[
                    html.Div(className="card-text", children=[
                        html.P(className="disclaimer",children="Disclaimer: The gray-colored countries are missing values.")
                    ])
                ]),
                html.Div(className="card-body", children=[
                    html.P(className="paragraph", children="In the span of six years, Asian and African countries have low happiness scores. "\
                                                           "The majority of countries especially in Africa are not that well developed.")
                ])
            ])
        ]),
        html.Div(className="graph-happy", children=[
            dcc.Graph(
                id="choropleth-map-happy",
                figure=choro_happy
             )
        ]),
        html.Div(className="button3", children=[
            html.A(className="toC3", href="#container3", children=[
                html.Img(className="scrolly", src="assets\images\scrolly.gif")
            ])
        ])
    ]),
    html.Section(id="container3", children=[
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
                    html.P(id="writeupfac", children=parfactors)
                ])
            ])
        ]),
        html.Div(className="graph-factors", children=[
                dcc.Graph(
                    id="choropleth-map-factor",
                    figure=choro_factor
                )
        ]),
        html.Div(className="button4", children=[
            html.A(className="toC4", href="#container4", children=[
                html.Img(className="scrolly2", src="assets\images\scrolly2.gif")
            ])
        ])
    ]),
    html.Section(id="container4", children=[
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
                    html.P(className="paragraph", children="All regions virtually perceive the "\
                                                                   "factors that affect their happiness to"\
                                                                   " be of equal weight. Although having different"\
                                                                   " values, the pattern is generally the same. "\
                                                                   "All countries give most importance to their GDP, "\
                                                                   "while corruption has the least influence.")
                ])
            ])
        ]),
        html.Div(className="graph-radar", children=[
                    dcc.Graph(
                        id="radar-factor",
                        figure=radar
                    )
        ]),
        html.Div(className="button5", children=[
            html.A(className="toC5", href="#container5", children=[
                html.Img(className="scrolly", src="assets\images\scrolly.gif")
            ])
        ])
    ]),
    html.Section(id="container5", children=[
        html.Div(className="write-up-corr", children=[
            html.Div(className="card border-secondary mb-3", children=[
                html.Div(className="card-header", children=[
                    html.Div(className="card-text2", children="Correlation of Factors")
                ]),
                html.Div(className="card-body", children=[
                    html.P(className="paragraph", children=writeupcorr)
                ])
            ])
        ]),
        html.Div(className="graph-corr", children=[
            dcc.Graph(
                id="heatmap",
                figure=corr_heatmap
            )
        ]),
        html.Div(className="button6", children=[
            html.A(className="toC6", href="#conccontainer", children=[
                html.Img(className="scrolly2", src="assets\images\scrolly2.gif")
            ])
        ])
    ]),
    html.Section(id="conccontainer", children=[
        html.Div(className="concDiv", children=[
            html.P(children="To conclude, all countries around the globe "
                            "almost share the same sentiments when it comes "
                            "to the factors that affect their happiness. With "
                            "GDP and life expectancy being the most influential "
                            "factors of the happiness score, it can be said that "
                            "they are indicators of the overall well-being and "
                            "productiveness of the people."),
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
        title_font_size=30,
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
    choro_factor.update_layout(autosize=False,
                          width=900,
                          height=500,
                               margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 4, "autoexpand": True},
                               paper_bgcolor="rgb(255, 255, 255)")
    return choro_factor

@app.callback(
    # id, property
    Output('writeupfac', 'children'),
    Input('factor-radio', 'value')
)

def update_factorwriteup(selected_factor):
    parfactors = ""
    if selected_factor is None:
        parfactors = "For the year 2017, the influence of GDP on happiness " \
           "score peaked on most countries around the " \
           "world. In the succeeding years however, it dropped. " \
           "There is little to no changes in the influence " \
           "in most African countries and some Asian countries."
    elif selected_factor == 'gdp_hscore':
        parfactors = "For the year 2017, the influence of GDP on happiness " \
           "score peaked on most countries around the " \
           "world. In the succeeding years however, it dropped. " \
           "There is little to no changes in the influence " \
           "in most African countries and some Asian countries."
    elif selected_factor == 'lifeexp_hscore':
        parfactors= "From the years 2017 to 2019, the influence of life " \
                    "expectancy on happiness score was slowly rising but " \
                    "it dropped in the year 2020 because of the pandemic. " \
                    "African countries tend to have the lowest scores compared to other " \
                    "countries."
    elif selected_factor == 'freedom_hscore':
        parfactors= "In Western and some Asian countries, there is no consistency " \
                    "in the influence of freedom on happiness score. In African countries, " \
                    "the influence is consistent throughout the years but the score is low."
    elif selected_factor == 'generosity_hscore':
        parfactors= "Throughout the years starting 2015, the countries that have good " \
                    "scores slowly decreases up until 2020 where we can see that generosity does " \
                    "not have much influence on the happiness score."
    elif selected_factor == 'corruption_hscore':
        parfactors= "Australia, Canada, and some European countries have good influence " \
                    "of corruption in happiness score while the other countries have little " \
                    "to no influence."
    elif selected_factor == 'actual_crime':
        parfactors= "In terms of consistency, the countries in Latin America and Africa " \
                    "have the highest crime rate around the world while other countries do not " \
                    "mainly because western and some asian countries are already developed."
    elif selected_factor == 'actual_gdp':
        parfactors= "Western countries have higher GDP than other countries."
    elif selected_factor == 'actual_lifeexp':
        parfactors= "From 2015 up to 2019, the life expectancy of most countries specifically " \
                    "the developed ones are high but in 2020, all of the scores dropped because " \
                    "of the pandemic."
    return parfactors




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
        margin={"r": 0, "t": 0, "l": 25, "b": 0},
        paper_bgcolor = "rgba(246, 250, 239, 0)",
        legend=dict(
            yanchor="top",
            xanchor="left"

        )
    )

    return radar

if __name__ == '__main__':
    app.run_server(debug=True)