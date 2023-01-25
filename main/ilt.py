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
from utils import *
from graph_updates import *
import imageselector
from datetime import date

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

def load_scatterplot(df, opacity, marker_size, order_by, prev_selection,
                     background_ranges = {'x': [-100, 100], 'y': [-100, 100]}):
    global loaded_project, loaded_batch

    project_name = loaded_project
    background_path = join(getcwd(), 'assets', project_name, 'backgrounds')
    batch_name = get_batch_basename(loaded_project, loaded_batch)

    list_candidates = [f for f in listdir(background_path) if batch_name in f] # match backgrounds in both jpg and png formats
    background_img = join(background_path, list_candidates[0])

    selected_points = []
    if prev_selection is not None:
        selected_points = [p['customdata'] for p in prev_selection['points']]

    fig = f_figure_scatter_plot(
        df,
        _columns=['x', 'y'],
        _selected_custom_data=selected_points,
        background_img=background_img,
        opacity=opacity,
        marker_size=marker_size,
        order_by=order_by,
        xrange = background_ranges['x'],
        yrange=background_ranges['y']
    )

    return fig

def update_labels(marked_images, new_label):
    global df

    if new_label != '' and len(marked_images) > 0:
        rows = df.index[df['custom_data'].isin(marked_images)]
        df.loc[rows, 'manual_label'] = new_label

def save_csv():
    global df, loaded_project, loaded_batch

    dataframe_path = join(getcwd(), 'assets', loaded_project, 'dataframes', loaded_batch)
    print('   ', dataframe_path)
    
    df.to_csv(dataframe_path, index=False)
    
    backup_folder = join(getcwd(), 'assets', loaded_project, 'dataframes', 'backups')
    if not exists(backup_folder):
        mkdir(backup_folder)
    backup_path = join(backup_folder, loaded_batch[:-4] + '_bkp' + str(date.today()) + '.csv')

    print('   ', backup_path)
    
    df.to_csv(backup_path, index=False)

def get_marked_images(imageselector_images):
    return [i['custom_data'] for i in imageselector_images if i['isSelected']]


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
suggested_classes = read_list_classes()

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
    html.Datalist(
        id='datalist_suggested_classes', 
        children=[html.Option(value=name) for name in suggested_classes]
    ),

    dbc.Container(
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
        ])
    ,style={'max-width': '100%'},),

    dbc.Row(html.Hr()),

    dbc.Container(
        dbc.Row([   
            dbc.Col([
                dbc.Row([
                    dbc.Col(
                        html.Div(
                            html.P('Opacity'),    
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
                dcc.Graph(id="graph_scatterplot", figure={}, style={"height": "64vh"}, config={'displaylogo':False, 'modeBarButtonsToRemove': ['toImage', 'resetScale2d']}),
                dcc.Graph(id="graph_histogram", figure={}, style={'height': '18vh', 'margin-top': '1vh'}, config={'displaylogo':False, 'modeBarButtonsToRemove': ['toImage', 'resetScale2d']} ),
            ], width=6),
            dbc.Col([
                dbc.Row([
                    dbc.Col(dcc.Checklist([' Save CSV after labeling'], value = [' Save CSV after labeling'], id = 'check_save_csv'), width=6),
                    dbc.Col(dcc.Checklist([' Discard image after labeling'], value = [' Discard image after labeling'], id = 'check_discard_image'), width=6),
                ]),
                dbc.Row([
                    dbc.Col(
                        dbc.Input(
                            value='',
                            id='input_label_images',
                            type="text",
                            style={'width': '100%', 'background':'Floralwhite'},
                            list = 'datalist_suggested_classes'
                        )
                    , width = 8),
                    dbc.Col(
                        dbc.Button('Label', n_clicks=0, id='button_label', style={'background':'chocolate', 'width':'100%'}),
                    width=4)
                ]),
                dbc.Row([dbc.Col(html.Hr()),],),

                dbc.Row(
                    html.Div(imageselector.ImageSelector(id='div_image_selector', images=empty_list_dics,
                        galleryHeaderStyle = {'position': 'sticky', 'top': 0, 'height': '0px', 'background': "#000000", 'zIndex': -1},),
                        id='XXXXXXXXXX', style=dict(height='68vh',overflow='scroll', backgroundColor=background_color)
                    )
                )
            ], width=True),
        ])
    , style={'max-width': '100%'}),
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
    Output('graph_scatterplot', 'selectedData'),
    Output('p_batch_name', 'children'),
    Output('button_load_batch_clicks', 'data'),
    Input('button_load_batch', 'n_clicks'),
    Input('slider_map_opacity', 'value'),
    Input('slider_marker_size', 'value'),
    Input('dropdown_order_labels', 'value'),
    Input('button_label', 'n_clicks'),
    State('dropdown_batch', 'value'),
    State('button_load_batch_clicks', 'data'),
    State('graph_scatterplot', 'selectedData'),
    State('check_save_csv', 'value'),
    State('check_discard_image', 'value'),
    State('input_label_images', 'value'),
    State('div_image_selector', 'images'),
)
def load_batch(nclicks, opacity, marker_size, order_by, label_nclicks,
               batch_name, prev_nclicks, prev_selection, check_save, check_discard, new_label, imageselector_images):
    global fig, df

    print('entering load batch')

    ctx = dash.callback_context
    flag_callback = ctx.triggered[0]['prop_id'].split('.')[0]

    print(flag_callback, nclicks)

    if flag_callback == 'button_load_batch' and nclicks > prev_nclicks:
        df = load_dataframe(batch_name)
        prev_selection = None
    elif len(flag_callback) < 1 or len(df.index) == 0: #page reloaded or df not loaded
        df = pd.DataFrame()
        fig = {}

        return fig, prev_selection, 'No batches loaded.', nclicks
    elif flag_callback == 'button_label':
        marked_images = get_marked_images(imageselector_images)
        update_labels(marked_images, new_label)
        if len(check_save) > 0:
            save_csv()
        if len(check_discard) > 0:
            prev_selection = None
    
    fig = load_scatterplot(df, opacity, marker_size, order_by, prev_selection)

    return fig, prev_selection, 'Loaded: ' + loaded_project + ' > ' + loaded_batch , nclicks


"""
    Updates the selected images
"""
@app.callback(
    Output('graph_histogram', 'figure'),
    Output('div_image_selector', 'images'),
    Input('graph_scatterplot', 'selectedData'),
)
def update_image_selector(selected_data):
    global loaded_project, loaded_batch

    print('entering update image selector')
    if selected_data is not None:
        selected_points_ids = [c['customdata'] for c in selected_data['points']]
        filtered_df = df.loc[df['custom_data'].isin(selected_points_ids)]

        ### Histogram update
        fig_histogram = compute_histogram(filtered_df)

        ### Image selector update

        batch_basename = get_batch_basename(loaded_project, loaded_batch)

        images_full_path = join(getcwd(), 'assets', loaded_project, 'images', batch_basename)
        in_folder = listdir(images_full_path)[0]
        images_path = join('assets', loaded_project, 'images', batch_basename, in_folder)
        list_paths = [join(images_path, f) for f in filtered_df['names']]

        thumbnails_full_path = join(getcwd(), 'assets', loaded_project, 'thumbnails')
        if exists(thumbnails_full_path):
            thumbnails_path = join('assets', loaded_project, 'thumbnails', batch_basename, in_folder)
            list_thumbs = [join(thumbnails_path, f) for f in filtered_df['thumbnails']]
        else:
            thumbnails_path = images_path
            list_thumbs = list_paths

        list_paths = [join(images_path, f) for f in filtered_df['names']]
        list_labels = filtered_df['manual_label'].tolist()
        list_captions = ['id: ' + str(id) + ' (' + label + ') - ' + name \
            for id, label, name in zip(selected_points_ids, list_labels, list_paths)]
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
            _list_caption=list_labels,
            _list_thumbnailCaption=list_labels,
            _list_tags=[[]]*size
        )

        return fig_histogram, list_dics
    print('Update image selector = None')

    return {}, []


port = 8020
opened = False



if not opened:
    webbrowser.open('http://127.0.0.1:' + str(port) + '/', new=2, autoraise=True)
    opened = True

if __name__ == '__main__':
    app.title = 'Image Labeling Tool'
    app.run_server(debug=False, port=port)
