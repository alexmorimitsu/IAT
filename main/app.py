
import sys
from turtle import width
#assert len(sys.argv) == 3

from functions import *

import dash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd
pd.options.mode.chained_assignment = None # default='warn'
import pandas_datareader.data as web

import imageselector
import json
import ast

from os import mkdir
from os.path import exists, join
import shutil
import webbrowser
from timeit import default_timer as timer

#path_to_images = sys.argv[1]
#csv_file = sys.argv[2]
path_to_images = ''
csv_file = ''

df = pd.read_csv(csv_file, encoding='ISO-8859-1').iloc[:,:]
init_par_coords = False #used for recomputing the intervals of the parcoords

THUMBNAIL_WIDTH = 28
THUMBNAIL_HEIGHT = 28
background_color = 'rgba(255, 250, 240, 100)'

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
labels_buffer = None
colors_buffer = None

labels_list = []
labels_colors = {}

#############################################################################

header = html.H1("Image Annotation Tool", style={'color': 'CornflowerBlue'})

#button_group_1 = dbc.ButtonGroup(
#    [
#        dbc.Button("Keep", n_clicks=0, id='button_galeria_filtrar', style={'background':'darkgreen'}),
#        dbc.Button("Discard", n_clicks=0, id='button_galeria_excluir', style={'background':'darkred'}),
#        #dbc.Button("Select all", n_clicks=0, id='button_galeria_selecionar_todos', style={'background':'darkslateblue'}),
#    ],
#    vertical=True,
#    className='my-btn-group',
#    size="lg",
#)

button_group_2 = dbc.ButtonGroup(
    [
        dbc.Input(placeholder="enter label here", id='input_aplicar_novo_label', type="text", style={'width': '50%', 'background':'Floralwhite'}),
        dbc.Button("Label",n_clicks=0, id='button_aplicar_novo_label', style={'background':'chocolate', 'width':'50%'}),
    ],
    #vertical=True,
    className='my-btn-group',
    size="lg",
)

button_group_3 = dbc.ButtonGroup(
    [
        dbc.Input(value="checkpoint.csv", id='input_save_csv', type="text", style={'width': '50%', 'background':'Floralwhite'}),
        dbc.Button("Save CSV",n_clicks=0, id='button_save_csv', style={'background':'chocolate', 'width':'50%'}),
    ],
    #vertical=True,
    className='my-btn-group',
    size="lg",
)

button_group_4 = dbc.ButtonGroup(
    [
        dbc.Input(value="annotated_dataset", id='input_finish_work', type="text", style={'width': '50%', 'background':'Floralwhite'}),
        dbc.Button("Save Annotated Dataset", n_clicks=0, id='button_finish_work', style={'background':'chocolate', 'width':'50%'}),
    ],
    #vertical=True,
    className='my-btn-group',
    size="lg",
)

button_group_5 = dbc.ButtonGroup(
    [
        dbc.Button("UNDO", n_clicks=0, id='button_undo', style={'background':'firebrick', 'width':'100%'}),
    ],
    #vertical=True,
    className='my-btn-group',
    size="lg",
)

IMAGES = create_list_dics(
    _list_src=[],
    _list_thumbnail=[],
    _list_name_figure=[]
)

#IMAGES = create_list_dics(
#    _list_src=list(path_to_images + df['names']),
#    _list_thumbnail=list(path_to_images + df['names']),
#    _list_name_figure=list(df['names']),
#    _list_thumbnailWidth=[THUMBNAIL_WIDTH] * df.shape[0],
#    _list_thumbnailHeight=[THUMBNAIL_HEIGHT] * df.shape[0],
#    _list_isSelected= [True] * df.shape[0],
#    _list_custom_data=list(df['custom_data']),
#    _list_thumbnailCaption='',
#    _list_tags='')

#fig = f_figure_scatter_plot(df, _columns=['x', 'y'], _selected_custom_data=list(df['custom_data']))
fig = f_figure_scatter_plot(df, _columns=['x', 'y'], _selected_custom_data=[])

#_columns_paralelas_coordenadas = ['Layer_A', 'Layer_B', 'Layer_C', 'Layer_D', 'Layer_E', 'Layer_F', 'Layer_G']
_columns_paralelas_coordenadas = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']

fig_paral =  f_figure_paralelas_coordenadas(
                        _df=df,
                        _filtered_df=pd.DataFrame(columns=df.columns),
                        _columns=_columns_paralelas_coordenadas,
                        #_selected_custom_data=list(df['custom_data']),
                        _selected_custom_data=[],
                        _fig = None
                    )

##############################################################################################################

app.layout = html.Div([
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        header
                    ),
                ),
            ],
            style={'max-height': '128px','color': 'white',}
        ),
        className='d-flex align-content-end',
        style={'max-width': '100%','background-color': 'Floralwhite'},
    ),

    dbc.Row([dbc.Col(html.Hr()),],),

    dbc.Container(
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="g_scatter_plot", figure=fig, style={"height": "80vh"}, config={'displaylogo':False, 'modeBarButtonsToRemove': ['toImage', 'resetScale2d']}), width={"size": 7}),

                dbc.Col([

                    dbc.Row([
                        #dbc.Col(button_group_1, width={"size": 6}),
                        #dbc.Col(button_group_2, width={"size": 6})
                        dbc.Col(button_group_2, width={"size": 12})
                        ]),

                    dbc.Row([dbc.Col(html.Hr()),],),

                    dbc.Row(
                        html.Div(imageselector.ImageSelector(id='g_image_selector', images=IMAGES,
                            galleryHeaderStyle = {'position': 'sticky', 'top': 0, 'height': '0px', 'background': "#000000", 'zIndex': -1},),
                            id='XXXXXXXXXX', style=dict(height='72vh',overflow='scroll', backgroundColor=background_color)
                            )
                        ),
                    ], width={"size": 5})
            ]),
        style={'max-width': '100%'},
        # className='mt-2'
    ),

    dbc.Row([dbc.Col(html.Hr()),],),
    
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="g_coordenadas_paralelas", figure=fig_paral, style={"height": "70vh"}, config={'displayModeBar': False}), style=dict(width='100%',overflow='scroll'), width={"size": 12}),
            ]
        ),
        style={'max-width': '100%'},
    ),

    dbc.Row([dbc.Col(html.Hr()),],),

    dbc.Container(
        dbc.Row([
            dbc.Col(button_group_3, width={"size": 4}),
            dbc.Col(width={"size": 1}),
            dbc.Col(button_group_4, width={"size": 4}),
            dbc.Col(width={"size": 1}),
            dbc.Col(button_group_5, width={"size": 2}),
        ]),
        style={'max-width': '100%'},
    ),

    #dcc.Store(id='selected_custom_points', data=json.dumps(list(df['custom_data']))),
    dcc.Store(id='selected_custom_points', data=json.dumps([])),
    dcc.Store(id='unchecked_points', data=json.dumps([])),
    dcc.Store(id='chart_flag', data=0),
    dcc.Store(id='state_store_df', data=df.to_json()),
    dcc.Store(id='dummy_csv_save', data=0),
    dcc.Store(id='dummy_finish_work', data=0),
    html.Div(id='output')
]) #End html.DIV

##############################################################################################################

@app.callback(
    [
        Output('dummy_finish_work', 'data'),
    ],
    [
        Input('button_finish_work', 'n_clicks'),
    ],
    [
        State('state_store_df', 'data'),
        State("input_finish_work", "value"),
    ]
    )
def save_dataset(
    i_button_save_csv_nclicks,
    s_store_df,
    s_input_finish_work_value
    ):

    if i_button_save_csv_nclicks > 0:
        df_updated = pd.read_json(s_store_df)

        if not exists (s_input_finish_work_value):
            mkdir(s_input_finish_work_value)

        labels = df_updated['manual_label']
        for label in labels:
            if not exists(join(s_input_finish_work_value, label)):
                mkdir(join(s_input_finish_work_value, label))

        for index, row in df_updated.iterrows():
            name = row['names']
            folder = row['manual_label']
            shutil.copy2(path_to_images + name, join(s_input_finish_work_value, folder))

        print('\nDataset recorded.\n')
    
    return [0]


@app.callback(
    [
        Output('dummy_csv_save', 'data'),
    ],
    [
        Input('button_save_csv', 'n_clicks'),
    ],
    [
        State('state_store_df', 'data'),
        State("input_save_csv", "value"),
    ]
    )
def save_csv(
    i_button_save_csv_nclicks,
    s_store_df,
    s_input_save_csv_value
    ):

    if i_button_save_csv_nclicks > 0:
        df_updated = pd.read_json(s_store_df)
        filename = str(s_input_save_csv_value)
        df_updated.to_csv(filename, index=False)
        print('\ncsv recorded.\n')
    
    return [0]


@app.callback(
    [
        Output('selected_custom_points', 'data'),
        Output('state_store_df', 'data'),
        Output('chart_flag', 'data'),
        Output('unchecked_points', 'data'),
    ],
    [
        Input('g_scatter_plot', 'selectedData'),
        Input('g_coordenadas_paralelas', 'restyleData'),
        #Input('button_galeria_filtrar', 'n_clicks'),
        #Input('button_galeria_excluir', 'n_clicks'),
        Input('button_aplicar_novo_label', 'n_clicks'),
        Input('button_undo', 'n_clicks'),
    ],
    [
        State('selected_custom_points', 'data'),
        State('unchecked_points', 'data'),
        State('state_store_df', 'data'),
        State('g_coordenadas_paralelas', 'figure'),
        State('g_image_selector', 'images'),
        State("input_aplicar_novo_label", "value"),
    ]
    )
def mudanca_custom_data(
    i_selection_g_scatter_plot,
    i_g_coordenadas_paralelas_restyleData,
    #i_button_galeria_filtrar_nclicks,
    #i_button_galeria_excluir_nclicks,
    i_button_aplicar_novo_label_nclicks,
    i_button_undo_nclicks,
    s_selected_custom_points,
    s_unchecked_points,
    s_store_df,
    s_g_coordenadas_paralelas_figure,
    s_button_galeria_filtrar_images,
    s_input_aplicar_novo_label_value
    ):

    #print('app.py entrou no mudanca_custom_data')
    
    global labels_list
    global labels_colors
    global labels_buffer # for the undo
    global colors_buffer # for the undo
    global init_par_coords

    print()
    print('----- mudanca custom data -----')
    t1 = timer()

    init_par_coords = False
    set_chart_flag = 0
    df_updated = pd.read_json(s_store_df)
    ctx = dash.callback_context
    flag_callback = ctx.triggered[0]['prop_id'].split('.')[0]

    df_store_updated = df_updated.to_json()
    unchecked_points = []

    t2 = timer()
    print('Initialization:', t2 - t1) 

    if flag_callback == 'g_scatter_plot':
        #print('app.py entrou na callback do g_scatter_plot')
        set_chart_flag = 0
        if i_selection_g_scatter_plot and i_selection_g_scatter_plot['points']:
            selectedpoints = [d['customdata'] for d in i_selection_g_scatter_plot['points']]
            selectedpoints = json.dumps(selectedpoints)
        else:
            #selectedpoints = json.dumps(list(df_updated['custom_data']))
            selectedpoints = json.dumps([])
        t3 = timer()
        init_par_coords = True
        print('  Scatter plot:', t3 - t2) 

    elif flag_callback == 'g_coordenadas_paralelas':
        #print('app.py entrou na callback g_coordenadas_paralelas')
        set_chart_flag = 1
        selectedpoints = [d['customdata'] for d in i_selection_g_scatter_plot['points']]

        filtered_df = df_updated[df_updated['custom_data'].isin(selectedpoints)]
        
        if i_g_coordenadas_paralelas_restyleData is not None:
            selected_and_checked = update_df_paralelas_coord(
                _df =filtered_df,
                _list_columns =_columns_paralelas_coordenadas,
                _figure = s_g_coordenadas_paralelas_figure,
                _new_dim_vals=i_g_coordenadas_paralelas_restyleData
            )

            for point in s_button_galeria_filtrar_images:
                if point['custom_data'] not in selected_and_checked:
                    unchecked_points.append(point['custom_data'])
            if i_selection_g_scatter_plot:
                selectedpoints = [d['customdata'] for d in i_selection_g_scatter_plot['points']]
            else:
                selectedpoints = []
            selectedpoints = json.dumps(selectedpoints)
        else:
            selectedpoints = json.dumps(list(df_updated['custom_data']))
        t3 = timer()
        print('  Parccords:', t3 - t2) 

    elif flag_callback == 'button_aplicar_novo_label':
        s_selected_custom_points = ast.literal_eval(s_selected_custom_points)
        selected_and_checked = []
        selected_not_checked = []
        for point in s_button_galeria_filtrar_images:
            if point['isSelected'] == True:
                selected_and_checked.append(point['custom_data'])
            else:
                selected_not_checked.append(point['custom_data'])
        new_label = str(s_input_aplicar_novo_label_value)
        labels_buffer = df_updated['manual_label'].copy() # for the undo
        colors_buffer = df_updated['colors'].copy()  # for the undo
        df_updated['manual_label'][df_updated['custom_data'].isin(selected_and_checked)]= new_label
        if new_label not in labels_list:
            labels_list.append(new_label)
            labels_colors[new_label] = len(labels_list)
        df_updated['colors'][df_updated['custom_data'].isin(selected_and_checked)] = labels_colors[new_label]
        df_store_updated = df_updated.to_json()
        selectedpoints = json.dumps(selected_not_checked)
        t3 = timer()
        print('  Novo label:', t3 - t2) 

    elif flag_callback == 'button_undo':
        df_updated['manual_label'] = labels_buffer
        df_updated['colors'] = colors_buffer
        df_store_updated = df_updated.to_json()
        selectedpoints = json.dumps([])
        t3 = timer()
        print('  Undo:', t3 - t2) 

    else:
        set_chart_flag = 0
        #selectedpoints = json.dumps(list(df_updated['custom_data']))
        selectedpoints = json.dumps([])
        t3 = timer()
        print('  Else:', t3 - t2) 

    s_unchecked_points = json.dumps(unchecked_points)
    t4 = timer()
    print('Total:', t4 - t1) 
    print()    
    return [selectedpoints, df_store_updated, set_chart_flag, s_unchecked_points]


@app.callback(
    [
    Output('g_scatter_plot', 'figure'),
    Output('g_image_selector', 'images'),
    Output('g_coordenadas_paralelas', 'figure'),
    ],
    [
    Input('selected_custom_points', 'data'),
    Input('unchecked_points', 'data'),
    ],
    [
    State('g_scatter_plot', 'figure'),
    State('g_image_selector', "images"),
    State('g_coordenadas_paralelas', 'figure'),
    State('state_store_df', 'data'),
    State('chart_flag', 'data')
    ]
    )
def gerar_scatter_plot(
    i_selected_custom_points,
    i_unchecked_points,
    s_g_scatter_plot_figure,
    s_g_image_selector_images,
    s_g_coordenadas_paralelas_figure,
    s_store_df,
    s_chart_flag_data,
    ):

    #print('app.py entrou na gerar_scatter_plot')

    ctx = dash.callback_context
    flag_callback = ctx.triggered[0]['prop_id'].split('.')[0]

    _df = pd.read_json(s_store_df)

    if flag_callback == 'selected_custom_points':
        print()
        print('----- gerar scatter plot -----')
        t1 = timer()

        unchecked_points = json.loads(i_unchecked_points)

        #print('app.py entrou na callback selected_custom_points')
        selected_points = json.loads(i_selected_custom_points)
        if init_par_coords:
            init_for_update_pc(selected_points)

        fig = f_figure_scatter_plot(_df, _columns=['x', 'y'], _selected_custom_data=selected_points)

        filtered_df = _df.loc[_df['custom_data'].isin(selected_points)]
        ordered_df = filtered_df.sort_values(by='D6') # show similar images close to each other
        checked_df = ordered_df.loc[-_df['custom_data'].isin(unchecked_points)]
        unchecked_df = ordered_df.loc[_df['custom_data'].isin(unchecked_points)]
        ordered_df = pd.concat([checked_df, unchecked_df])

        _image_teste_list_correct_label = ordered_df['correct_label']
        _image_teste_list_names = ordered_df['names']
        _image_teste_list_caption = ordered_df['manual_label']
        _image_teste_list_custom_data = ordered_df['custom_data']

        #old
        #_image_teste_list_correct_label = updated_df['correct_label'][updated_df['custom_data'].isin(selected_points)]
        #_image_teste_list_names = updated_df['names'][updated_df['custom_data'].isin(selected_points)]
        #_image_teste_list_caption = updated_df['manual_label'][updated_df['custom_data'].isin(selected_points)]
        #_image_teste_list_custom_data = updated_df['custom_data'][updated_df['custom_data'].isin(selected_points)]

        t2 = timer()
        print('Time to create lists (new):', t2 - t1) 

        fig2 = create_list_dics(
            _list_src=list(path_to_images + _image_teste_list_names),
            _list_thumbnail=list(path_to_images + _image_teste_list_names),
            _list_name_figure=list(_image_teste_list_names),
            _list_thumbnailWidth=[THUMBNAIL_WIDTH] * _image_teste_list_correct_label.shape[0],
            _list_thumbnailHeight=[THUMBNAIL_HEIGHT] * _image_teste_list_correct_label.shape[0],
            _list_isSelected= [True] * _image_teste_list_correct_label.shape[0],
            _list_custom_data=list(_image_teste_list_custom_data),
            _list_thumbnailCaption=_image_teste_list_caption,
            _list_tags='')

        t3 = timer()
        print('Time to create fig2:', t3 - t2) 

        for point in fig2:
            if point['custom_data'] in unchecked_points:
                point['isSelected'] = False

        t4 = timer()
        print('Time to unckeck points:', t4 - t3) 



        if s_chart_flag_data == 1:
            #print('app.py chamando fpc via if')
            fig3 =  f_figure_paralelas_coordenadas(
                _df=_df,
                _filtered_df = filtered_df,
                _columns=_columns_paralelas_coordenadas,
                _selected_custom_data=json.loads(i_selected_custom_points),
                _fig = s_g_coordenadas_paralelas_figure
            )
        else:
            #print('app.py chamando fpc via else')
            fig3 =  f_figure_paralelas_coordenadas(
                        _df=_df,
                        _filtered_df = filtered_df,
                        _columns=_columns_paralelas_coordenadas,
                        _selected_custom_data=json.loads(i_selected_custom_points),
                        _fig = None
                    )

        t5 = timer()
        print('Time for parcoords:', t5 - t4) 
        print('Total:', t5-t1)
        print()

        return [fig, fig2, fig3]

    else:
        return [s_g_scatter_plot_figure, s_g_image_selector_images, s_g_coordenadas_paralelas_figure]

##############################################################################################################

webbrowser.open('http://127.0.0.1:8025/', new=2, autoraise=True)

def run_iat(images, path_to_csv):
    global path_to_images
    global csv_file

    path_to_images = images
    csv_file = path_to_csv

    app.run_server(debug=True, port=8025)

if __name__ == '__main__':
    app.run_server(debug=True, port=8025)

