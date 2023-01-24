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

from functions import *
import imageselector

def get_projects_list():
    
    projects_folder = join(getcwd(), 'assets')
    projects_list = [f for f in listdir(projects_folder) if isdir(join(projects_folder, f))]
    projects_list.sort()

    return projects_list

def get_batches_list(project_name):
    batches_folder = join(getcwd(), 'assets', project_name, 'dataframes')
    batches_list = [f for f in listdir(batches_folder) if isfile(join(batches_folder, f))]
    batches_list.sort()

    return batches_list

def load_dataframe(batch_name):
    global loaded_project, loaded_batch

    csv_path = join(getcwd(), 'assets', loaded_project, 'dataframes', batch_name)
    df = pd.read_csv(csv_path, encoding='ISO-8859-1')

    loaded_batch = batch_name

    return df

def get_batch_basename(project_name, batch_name):
    basename = batch_name[:-4] # remove extension (.csv)
    if project_name in basename: # if batchName has the format batchName_projectName
        basename = basename[:-len(project_name)-1]

    return basename

def load_scatterplot(df, opacity, marker_size, order_by,
                     background_ranges = {'x': [-100, 100], 'y': [-100, 100]}):
    global loaded_project, loaded_batch

    project_name = loaded_project
    background_path = join(getcwd(), 'assets', project_name, 'backgrounds')
    batch_name = get_batch_basename(loaded_project, loaded_batch)

    list_candidates = [f for f in listdir(background_path) if batch_name in f] # match backgrounds in both jpg and png formats
    background_img = join(background_path, list_candidates[0])

    fig = f_figure_scatter_plot(
        df,
        _columns=['x', 'y'],
        _selected_custom_data=[],
        background_img=background_img,
        opacity=opacity,
        marker_size=marker_size,
        order_by=order_by,
        xrange = background_ranges['x'],
        yrange=background_ranges['y']
    )

    return fig

projects_list = get_projects_list()
df = pd.DataFrame()
fig = ''
loaded_project = ''
loaded_batch = ''
empty_list_dics = create_list_dics(
    _list_src=[],
    _list_thumbnail=[],
    _list_name_figure=[]
)

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
    dbc.Row([
        dbc.Col(html.H1('ILT'), width={'size': 1}),
        dbc.Col([
            dbc.Row([
                dbc.Col(dcc.Dropdown(projects_list, '', placeholder='Select a project', id='dropdown_project', clearable=False), width={'size': 4}),
                dbc.Col(dcc.Dropdown([], '', placeholder='Select a batch', id='dropdown_batch', clearable=False, style={'display': 'none'}), width={'size': 6}),
                dbc.Col(dbc.Button('Load batch', n_clicks=0, id='button_load_batch', style={'background':'chocolate', 'width':'100%', 'display': 'none'}), width={'size': 2})
            ]),
            dbc.Row(dbc.Col(html.P('', id='p_batch_name'), width={'size': 11}))
        ], width={'size': 11}),
    ]),

    dbc.Row([dbc.Col(html.Hr()),],),

    dbc.Row([   
        dbc.Col([
            dbc.Row([
                dbc.Col(
                    html.Div(
                        html.P('Background opacity'),    
                    style={'textAlign': 'left'}), width={'size': 2}),
                dbc.Col([
                    dcc.Slider(0, 1, 0.1,
                        value=0,
                        id='slider_map_opacity',
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )], width={'size': 3}),
                dbc.Col(
                    html.Div(
                        html.P('Marker size'),    
                    style={'textAlign': 'right'})
                , width={'size': 2}),
                dbc.Col([
                    dcc.Slider(1, 25, 3,
                        value=10,
                        id='slider_marker_size',
                        marks=None,
                        tooltip={"placement": "bottom", "always_visible": True},
                    )], width={'size': 3}),
                dbc.Col(
                    dcc.Dropdown(['A-Z, a-z', 'Frequency'], value='A-Z, a-z', id='dropdown_order_labels', clearable = False)
                , width={'size': 2}),
            ], align='bottom'),
            dcc.Graph(id="graph_scatterplot", figure={}, style={"height": "74vh"}, config={'displaylogo':False, 'modeBarButtonsToRemove': ['toImage', 'resetScale2d']}),
        ], width={'size': 7}),
        dbc.Col([
            dbc.Row(
                html.Div(imageselector.ImageSelector(id='div_image_selector', images=empty_list_dics,
                    galleryHeaderStyle = {'position': 'sticky', 'top': 0, 'height': '0px', 'background': "#000000", 'zIndex': -1},),
                    id='XXXXXXXXXX', style=dict(height='63vh',overflow='scroll', backgroundColor=background_color)
                )
            )
        ], width={'size': 5}),
    ]),    
    dcc.Store(id='selected_points_ids', data=0),
    dcc.Store(id='button_load_batch_clicks', data=0),

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
    global loaded_project

    print('entering update dropdown batch')


    if len(project_name) > 0:
        batches_list = get_batches_list(project_name)
        loaded_project = project_name
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
    Output('button_load_batch_clicks', 'data'),
    Input('button_load_batch', 'n_clicks'),
    Input('slider_map_opacity', 'value'),
    Input('slider_marker_size', 'value'),
    Input('dropdown_order_labels', 'value'),
    State('dropdown_batch', 'value'),
    State('button_load_batch_clicks', 'data')
)
def load_batch(nclicks, opacity, marker_size, order_by, batch_name, prev_nclicks):
    global fig, df

    print('entering load batch')

    ctx = dash.callback_context
    flag_callback = ctx.triggered[0]['prop_id'].split('.')[0]

    print(flag_callback, nclicks)

    if flag_callback == 'button_load_batch' and nclicks > prev_nclicks:
        df = load_dataframe(batch_name)
    elif len(flag_callback) < 1 or len(df.index) == 0: #page reloaded or df not loaded
        df = pd.DataFrame()
        fig = {}

        return fig, 'No batches loaded.', nclicks
    
    fig = load_scatterplot(df, opacity, marker_size, order_by)

    return fig, 'Loaded: ' + loaded_project + ' > ' + loaded_batch , nclicks

"""
    Updates the selected images
"""
@app.callback(
    Output('div_image_selector', 'images'),
    Input('graph_scatterplot', 'selectedData'),
)
def update_image_selector(selected_data):
    global loaded_project, loaded_batch

    print('entering update image selector')
    if selected_data is not None:
        selected_points_ids = [c['customdata'] for c in selected_data['points']]
        filtered_df = df.loc[df['custom_data'].isin(selected_points_ids)]

        batch_basename = get_batch_basename(loaded_project, loaded_batch)

        images_full_path = join(getcwd(), 'assets', loaded_project, 'images', batch_basename)
        in_folder = listdir(images_full_path)[0]
        images_path = join('assets', loaded_project, 'images', batch_basename, in_folder)
        thumbnails_full_path = join(getcwd(), 'assets', loaded_project, 'thumbnails')
        if exists(thumbnails_full_path):
            thumbnails_path = join('assets', loaded_project, 'thumbnails', batch_basename, in_folder)
        else:
            thumbnails_path = images_path

        list_paths = [join(images_path, f) for f in filtered_df['names']]
        list_thumbs = [join(thumbnails_path, f) for f in filtered_df['thumbnails']]
        size = len(list_paths)
        print('Update image selector', size)


        list_dics = create_list_dics(
            _list_src=list_paths,
            _list_thumbnail=list_thumbs,
            _list_name_figure=filtered_df['names'].tolist(),
            _list_thumbnailWidth=[10]*size,
            _list_thumbnailHeight=[10]*size,
            _list_isSelected= [True]*size,
            _list_custom_data=selected_points_ids,
            _list_caption=filtered_df['manual_label'].tolist(),
            _list_thumbnailCaption=[[]]*size,
            _list_tags=[[]]*size
        )
        print(list_dics)

        return list_dics
    print('Update image selector = None')

    return []


port = 8020
opened = False



if not opened:
    webbrowser.open('http://127.0.0.1:' + str(port) + '/', new=2, autoraise=True)
    opened = True

if __name__ == '__main__':
    app.title = 'Image Labeling Tool'
    app.run_server(debug=False, port=port)
