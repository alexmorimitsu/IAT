import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

import webbrowser
import pandas as pd
from os import listdir, getcwd, mkdir
from os.path import join, isdir, exists, isfile
from shutil import copy2

from main.functions import *


def get_projects_list():
    
    projects_folder = join(getcwd(), 'main', 'assets')
    projects_list = [f for f in listdir(projects_folder) if isdir(join(projects_folder, f))]
    projects_list.sort()

    return projects_list

def get_batches_list(project_name):
    batches_folder = join(getcwd(), 'main', 'assets', project_name, 'dataframes')
    batches_list = [f for f in listdir(batches_folder) if isfile(join(batches_folder, f))]
    batches_list.sort()

    return batches_list

def load_dataframe(project_name, batch_name):
    csv_path = join(getcwd(), 'main', 'assets', project_name, 'dataframes', batch_name)
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    return df

def load_scatterplot(df, project_name, batch_name, background_ranges = {'x': [-100, 100], 'y': [-100, 100]}):
    background_path = join(getcwd(), 'main', 'assets', project_name, 'backgrounds', batch_name[:-4] + '.png')

    fig = f_figure_scatter_plot(
        df,
        _columns=['x', 'y'],
        _selected_custom_data=[],
        background_img=background_path,
        xrange = background_ranges['x'],
        yrange=background_ranges['y']
    )

    return fig

projects_list = get_projects_list()

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1.0'
        }
    ]
)

app.layout = html.Div([
    dbc.Container(
        dbc.Row([
            dbc.Col(html.H1('ILT'), width={'size': 1}),
            dbc.Col(dcc.Dropdown(projects_list, '', placeholder='Select a project', id='dropdown_project', clearable=False), width={'size': 3}),
            dbc.Col(dcc.Dropdown([], '', placeholder='Select a batch', id='dropdown_batch', clearable=False, style={'display': 'none'}), width={'size': 6}),
            dbc.Col(dbc.Button('Load batch', n_clicks=0, id='button_load_batch', style={'background':'chocolate', 'width':'100%', 'display': 'none'}), width={'size': 2})
        ]),
    ),

    dbc.Row([dbc.Col(html.Hr()),],),

    dbc.Container(
        dbc.Col([
            html.P('', id='p_batch_name'),
            dcc.Graph(id="graph_scatterplot", figure=None, style={"height": "74vh"}, config={'displaylogo':False, 'modeBarButtonsToRemove': ['toImage', 'resetScale2d']}),
        ])
    ),
    dcc.Store(id='dummy', data=0),

])

"""
    Updates and displays the batches of a selected project
"""
@app.callback(
    Output('dropdown_batch', 'style'),
    Output('dropdown_batch', 'options'),
    Output('dropdown_batch', 'value'),
    Input('dropdown_project', 'value')
)
def update_dropdown_batch(project_name):
    if len(project_name) > 0:
        batches_list = get_batches_list(project_name)
        return  {'display': 'block'}, batches_list, ''
    return {'display': 'none'}, [], ''

"""
    Displays the button to load the batch
"""
@app.callback(
    Output('button_load_batch', 'style'),
    Input('dropdown_batch', 'value'),
)
def update_dropdown_batch(batch_name):
    if len(batch_name) > 0:
        return  {'display': 'block'}
    return {'display': 'none'}

"""
    Loads the selected batch
"""
@app.callback(
    Output('graph_scatterplot', 'figure'),
    Output('p_batch_name', 'children'),
    Input('button_load_batch', 'n_clicks'),
    State('dropdown_project', 'value'),
    State('dropdown_batch', 'value'),
)
def update_dropdown_batch(nclicks, project_name, batch_name):
    if nclicks > 0:
        df = load_dataframe(project_name, batch_name)
        fig = load_scatterplot(df, project_name, batch_name)

        return fig, project_name + ' > ' + batch_name

    return '', 'No batches loaded.'



port = 8020
opened = False

if not opened:
    webbrowser.open('http://127.0.0.1:' + str(port) + '/', new=2, autoraise=True)
    opened = True

if __name__ == '__main__':
    app.title = 'Image Labeling Tool'
    app.run_server(debug=False, port=port)
