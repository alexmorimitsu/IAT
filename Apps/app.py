import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime
import pathlib
import json
import ast

import functions as demo_f
import plotly.graph_objects as go ## https://medium.com/plotly/plotly-py-4-0-is-here-offline-only-express-first-displayable-anywhere-fc444e5659ee

import imageselector

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )


#############################################################################
logo = html.Img(src=app.get_asset_url('ime2.png'),
                        # style={'width': "128px", 'height': "128px",
                        style={'width': "110px", 'height': "110px",
                        },className='justify-content-start') #inline-image

header = html.H3("Plankton Explorer Tool", style={})

logo_and_header = dbc.FormGroup(
        [
            logo,
            html.Div(
                [
                    header
                ],
                className="p-5"
            )
        ],
        className='form-row'
)


card_content = [
    dbc.CardHeader("Qtd. Imagens"),
    dbc.CardBody(
        [
            html.H1("132", className="card-title"),
            # html.P(
            #     "This is some card content that we'll reuse",
            #     className="card-text",
            # ),
        ]
    ),
]

button_group_1 = dbc.ButtonGroup(
    [
        dbc.Button("Filtrar", n_clicks=0, id='button_galeria_filtrar'),
        dbc.Button("Excluir", n_clicks=0, id='button_galeria_excluir'),
        dbc.Button("Organizar", n_clicks=0, id='button_galeria_organizar'),
        dbc.Button("Selecionar Todos", n_clicks=0, id='button_galeria_selecionar_todos'),
    ],
    vertical=True,
    className='my-btn-group',
    size="l",
)

button_group_2 = dbc.ButtonGroup(
    [
        dbc.Button("Resumo", n_clicks=0, id='button_resumo'),
        dbc.Button("Aplicar Novo Label",n_clicks=0, id='button_aplicar_novo_label'),
        dbc.Input(placeholder="-", id='input_aplicar_novo_label', type="text"),
        # dbc.Button("Third", ),
    ],
    vertical=True,
    className='my-btn-group mt-1',
    size="lg",
)

button_group_3 = dbc.ButtonGroup(
    [
        dbc.Button("Active Learning", n_clicks=0, id='button_active_learning'),
        dbc.Button("Imagens Semelhantes", id='button_imagens_semelhantes')
    ],
    vertical=True,
    className='my-btn-group mt-1',
    size="lg",
)




## DF
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('data.csv'), encoding='ISO-8859-1').iloc[:70,:]



IMAGES = demo_f.create_list_dics(
    _list_src=list('/assets/images/LClass_' + df['correct_label'] + '/' + df['names']),
    _list_thumbnail=list('/assets/images/LClass_' + df['correct_label'] + '/' + df['names']),
    _list_name_figure=list(df['names']),
    _list_thumbnailWidth=[28] * df.shape[0],
    _list_thumbnailHeight=[28] * df.shape[0],
    _list_isSelected= [False] * df.shape[0],
    _list_custom_data=list(df['custom_data']),
    _list_thumbnailCaption='',
    _list_tags='')





# import plotly.express as px
# _df = px.data.iris()
# fig = px.scatter(df, x="x", y="y", hover_data=['custom_data'])


import imageselector
import functions as demo_f
import io
import pathlib
## dataFrame:
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("data").resolve()
# df = pd.read_csv(DATA_PATH.joinpath('data.csv'), encoding='ISO-8859-1').iloc[:10,:]


# import plotly.graph_objects as go
# df_paral = pd.read_csv("https://raw.githubusercontent.com/bcdunbar/datasets/master/parcoords_data.csv")



def f_figure_scatter_plot(_df, _columns, _selected_custom_data):

    l_data = []
    groups = _df.groupby('manual_label')

    for idx, val in groups:
        _selectedpoints = _df['manual_label'][
            (_df['manual_label'] == idx) &
            (_df['custom_data'].isin(_selected_custom_data))
        ].index.values
        _custom_points = _df['custom_data'][(_df['manual_label'] == idx)]

        _temp = []
        for i in range(len(_selectedpoints)):
            _temp.append(val.index.get_loc(_selectedpoints[i]))
        _selectedpoints = _temp

        scatter = go.Scattergl(
            name=idx,
            x=val[_columns[0]], #x
            y=val[_columns[1]],
            text=val['manual_label'],
            selectedpoints=_selectedpoints,
            customdata=_custom_points,
            textposition="top center",
            mode="markers",
            marker=dict(size=20, symbol="circle")
        )
        l_data.append(scatter)

    layout = go.Layout(
        xaxis={'range': [-1, 1.1], 'autorange': True,
               'gridcolor': 'rgba(0,0,0,0)', 'zeroline': False, 'showgrid': False},
        yaxis={'range': [-1, 1.1], 'autorange': True,
               'gridcolor': 'rgba(0,0,0,0)', 'zeroline': False, 'showgrid': False},
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        dragmode='lasso',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(39,43,48,100)',
    )

    figure_0 = go.Figure(data=l_data, layout=layout)
    return figure_0


def f_figure_paralelas_coordenadas(_df, _columns, _selected_custom_data, _fig=None):

    _filters_label = []
    _filters_bottom = []
    _filters_top = []

    _df_temp = df[df['custom_data'].isin(_selected_custom_data)]
    _df_temp = _df_temp.reset_index(drop=True)

    for i in range(len(_columns)):
        _filters_label.append(_columns[i])
        _temp = []
        for ii in range(_df_temp.shape[0]):
            _temp.append(_df_temp[_columns[i]][ii])


        _filters_bottom.append(_temp)
        _filters_top.append(_temp)




    _list_visible = []
    _list_values = []
    _list_range = []
    _list_constraintrange = []

    if _fig != None:
        _fig_list = _fig['data'][0]['dimensions'] #NOVO




    for i in range(len(_columns)):


        _list_visible.append(True)

        _list_values.append(list(_df[_columns[i]]))

        _temp_list = []
        _temp_list.append(_df[_columns[i]].min())
        _temp_list.append(_df[_columns[i]].max())
        _list_range.append(_temp_list)


        _list_constraintrange = []
        for i in range(len(_columns)):

            _list_t0 = []
            for ii in range(len(_filters_bottom[i])):

                _list_t = []
                _list_t.append(_filters_bottom[i][ii] - 0.01)
                _list_t.append(_filters_top[i][ii] + 0.01)
                _list_t0.append(_list_t)


            if _df_temp.shape[0] == df.shape[0]:
                _list_constraintrange.append(None)
            else:
                _list_constraintrange.append(_list_t0)


            if _fig != None:

                for iii in range(len(_fig_list)): #NOVO
                    if _fig_list[iii]['label'] == _columns[i]: #NOVO

                        try:
                            _list_max_min_temp = _fig_list[iii]['constraintrange']
                            _check_max_min = 0

                            if isinstance(_list_max_min_temp, list):
                                for i_ind in range(len(_list_max_min_temp)):
                                    _min_range = _list_max_min_temp[i_ind][0]
                                    _max_range = _list_max_min_temp[i_ind][1]
                                    _min_check = _list_constraintrange[i][0][0]
                                    _max_check = _list_constraintrange[i][0][1]
                            else:
                                _min_range = _list_max_min_temp[0]
                                _max_range = _list_max_min_temp[1]
                                _min_check = _list_constraintrange[i][0]
                                _max_check = _list_constraintrange[i][1]

                            if (_min_check >= _min_range and min_check <= _max_range) and (_max_check >= _min_range and _max_check <= _max_range):
                                _check_max_min = 1
                            else:
                                _list_constraintrange[i][0] =  None

                        except:
                            None





                        try:
                            if isinstance(_fig_list[iii]['constraintrange'][0], list):
                                l_temp = None
                                l_temp = _fig_list[iii]['constraintrange']
                                # print("_list_constraintrange[i]", i, " ", _list_constraintrange[i])
                                _list_constraintrange[i].extend(l_temp)
                                break
                            else:
                                l_temp = []
                                l_temp.append(_fig_list[iii]['constraintrange'])
    #                             if _list_constraintrange[i] is None:
    #                                 _list_constraintrange[i] = l_temp
    #                             else:
    #                                 _list_constraintrange[i].extend(l_temp)
                                _list_constraintrange[i].extend(l_temp)

                                break
                        except:
                            _list_constraintrange[i] = None
                            break



                    else:
                        None




    #remove None from constraintrange:
    for i in range(len(_list_constraintrange)):
        try:
            _list_constraintrange[i] = list(filter(None, _list_constraintrange[i]))
        except:
            None


    _data = {

        'label': _columns,
        'visible': _list_visible,
        'values': _list_values,
        'range': _list_range,
        'constraintrange': _list_constraintrange
    }



    dimensions_dict = pd.DataFrame(_data)
    dimensions_dict = dimensions_dict.to_dict('records')


    coordenadas_paralelas = go.Parcoords(
            line = dict(
                    showscale = True,
                    cmin = -4000,
                    cmax = -100
            ),
            dimensions = dimensions_dict,
            customdata = _df['custom_data']
        )


    l_data = []
    l_data.append(coordenadas_paralelas)


    figure = go.Figure(data=l_data)
    # print("end")
    return figure


def update_df_paralelas_coord(
    _df,
    _list_columns,
    _figure,
    _novas_cor):

    # print("_figure"),
    # print(_figure)

    # print("_novas_cor")
    # print(_novas_cor)


    _filters_label = []
    _filters_top = []
    _filters_bottom = []
    _filters_conca = []
    _filters_left_paren = []
    _filters_right_paren = []

    par_coord_data = _figure['data'][0]
    curr_dims = par_coord_data.get('dimensions', None)



    for i in range(len(curr_dims)):

        try:
            _ranges = curr_dims[i]['constraintrange']
            _label = curr_dims[i]['label']

            if isinstance(_ranges[0], list):
                for ii in range(len(_ranges)):
                    if ii == 0:
                        _filters_left_paren.append('(')
                    else:
                        _filters_left_paren.append('')

                    print(ii)
                    _filters_bottom.append(_ranges[ii][0])
                    _filters_top.append(_ranges[ii][1])
                    _filters_label.append(_label)

                    if ii == (len(_ranges) - 1):
                        _filters_conca.append('&')
                        _filters_right_paren.append(')')
                    else:
                        _filters_conca.append('|')
                        _filters_right_paren.append('')

            else:
                _filters_left_paren.append('(')
                _filters_bottom.append(_ranges[0])
                _filters_top.append(_ranges[1])
                _filters_label.append(_label)
                _filters_right_paren.append(')')
                _filters_conca.append('&')



        except:
            None



    _filters_conca[-1:] = ' '
    query = ''.join(f'{lp} {i} >= {j} &  {i} <= {k} {rp} {z} ' for lp, i, j, k, rp, z in zip(_filters_left_paren, _filters_label, _filters_bottom, _filters_top, _filters_right_paren, _filters_conca))

    updated_df = _df.query(query)

    return updated_df

#############################################################################

fig = f_figure_scatter_plot(df, _columns=['x', 'y'], _selected_custom_data=list(df['custom_data']))

# fig2 = f_figure_scatter_plot(df, _columns=['x2', 'y2'], _selected_custom_data=list(df['custom_data']))




_image_teste_list_correct_label = df['correct_label']
_image_teste_list_names = df['names']
_image_teste_list_caption = df['manual_label']
_image_teste_list_custom_data = df['custom_data']

# print("SHAPE!!!!", _image_teste_list_correct_label.shape)
# print(_image_teste_list_correct_label)
# print("\n\n\n\n-------------------------------------------")

fig2 = demo_f.create_list_dics(
    _list_src=list('/assets/images/LClass_' + _image_teste_list_correct_label + '/' + _image_teste_list_names),
    _list_thumbnail=list('/assets/images/LClass_' + _image_teste_list_correct_label + '/' + _image_teste_list_names),
    _list_name_figure=list(_image_teste_list_names),
    _list_thumbnailWidth=[28] * _image_teste_list_correct_label.shape[0],
    _list_thumbnailHeight=[28] * _image_teste_list_correct_label.shape[0],
    _list_isSelected= [False] * _image_teste_list_correct_label.shape[0],
    _list_custom_data=list(_image_teste_list_custom_data),
    _list_thumbnailCaption=_image_teste_list_caption,
    _list_tags='')



_columns_paralelas_coorenadas = ['Area_pxl', 'AreaNoHole_Area_pxl', 'Solidity', 'Perimeter_pxl', 'ConvexPerimeter_pxl', 'Convexity', 'Max_ConvexityDef']

fig_paral =  f_figure_paralelas_coordenadas(
                        _df=df,
                        _columns=_columns_paralelas_coorenadas,
                        _selected_custom_data=list(df['custom_data']),
                        _fig = None
                    )


##############################################################################################################

app.layout = html.Div([



    dbc.Container(

        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        logo_and_header,
                    ),
                ),
            ],
            style={'max-height': '128px','color': 'white',}
        ),
        className='d-flex align-content-end',
        style={'max-width': '100%','background-color': '#27292b'},
    ),

    dbc.Row([dbc.Col(html.Hr()),],),
    dbc.Container(

        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="secondary", inverse=True), width={"size": 2}),
                dbc.Col(dbc.Card(card_content, color="secondary", inverse=True), width={"size": 2}),
                dbc.Col(dbc.Card(card_content, color="secondary", inverse=True), width={"size": 2}),

                # dbc.Col(dbc.Card(card_content, color="secondary", inverse=True), width={"size": 2}),
                dbc.Col(button_group_3, width={"size": 2}),
                dbc.Col(button_group_1, width={"size": 2}),
                dbc.Col(button_group_2, width={"size": 2}),

            ]
        ),
        style={'max-width': '100%'},
        # className='mt-2'
    ),

    dbc.Row([dbc.Col(html.Hr()),],),
    dbc.Container(

        dbc.Row(
            [
                # dbc.Col(dcc.Graph(id="scatter-plot", figure=fig, style={"height": "50vh"}), width={"size": 6}),
                # dbc.Col(imageselector.ImageSelector(id='g_imageselector', images=IMAGES, galleryHeaderStyle={'position': 'sticky', 'top': 50, 'height': '30px', 'background': "#ffffff", 'zIndex': 990},),
                # style=dict(height='50vh',overflow='scroll'), width={"size": 6}),
                # # dbc.Col(dbc.Card(card_content, color="secondary", inverse=True), width={"size": 6}),

                dbc.Col(dcc.Graph(id="g_scatter_plot", figure=fig, style={"height": "50vh"}), width={"size": 6}),
                # dbc.Col(imageselector.ImageSelector(id='g_imageselector', images=[], galleryHeaderStyle={'position': 'sticky', 'top': 50, 'height': '30px', 'background': "#ffffff", 'zIndex': 990},),
                # style=dict(height='50vh',overflow='scroll'), width={"size": 6}),
                dbc.Col(
                    # dcc.Graph(id="g_scatter_plot_2", figure=fig2, style={"height": "50vh"}), width={"size": 6}
                    html.Div(

                            imageselector.ImageSelector(id='g_image_selector', images=IMAGES,
                            galleryHeaderStyle = {'position': 'sticky', 'top': 0, 'height': '0px', 'background': "#ffffff", 'zIndex': 990},),
                            id='XXXXXXXXXX', style=dict(height='50vh',overflow='scroll'))


                    ),

            ]
        ),
        style={'max-width': '100%'},
    ),


    dbc.Row([dbc.Col(html.Hr()),],),
    dbc.Container(

        dbc.Row(
            [
                # dbc.Col(width={"size": 6}),
                dbc.Col(dcc.Graph(id="g_coordenadas_paralelas", figure=fig_paral, style={"height": "50vh"}), style=dict(width='50vh',overflow='scroll'), width={"size": 12}),
            ]
        ),
        style={'max-width': '100%'},
    ),


    # dcc.Store(id='state-gallery'),
    dcc.Store(id='selected_custom_points', data=json.dumps(list(df['custom_data']))),
    dcc.Store(id='chart_flag', data=0),
    dcc.Store(id='state_store_df', data=df.to_json()),
    html.Div(id='output')
]) #End html.DIV


# Callback section: connecting the components
# ************************************************************************
@app.callback(
    [
        Output('selected_custom_points', 'data'),
        Output('state_store_df', 'data'),
        Output('chart_flag', 'data'),
    ],
    [
        Input('g_scatter_plot', 'selectedData'),
        Input('g_coordenadas_paralelas', 'restyleData'),
        Input('button_galeria_filtrar', 'n_clicks'),
        Input('button_galeria_excluir', 'n_clicks'),
        Input('button_aplicar_novo_label', 'n_clicks'),

    ],
    [
        State('selected_custom_points', 'data'),
        State('state_store_df', 'data'),
        State('g_coordenadas_paralelas', 'figure'),
        State('g_image_selector', 'images'),
        State("input_aplicar_novo_label", "value"),
    ]
    )
def mudanca_custom_data(
    i_selection_g_scatter_plot,
    i_g_coordenadas_paralelas_restyleData,
    i_button_galeria_filtrar_nclicks,
    i_button_galeria_excluir_nclicks,
    i_button_aplicar_novo_label_nclicks,
    s_selected_custom_points,
    s_store_df,
    s_g_coordenadas_paralelas_figure,
    s_button_galeria_filtrar_images,
    s_input_aplicar_novo_label_value
    ):


    set_chart_flag = 0
    df_updated = pd.read_json(s_store_df)
    ctx = dash.callback_context
    flag_callback = ctx.triggered[0]['prop_id'].split('.')[0]



    df_store_updated = df_updated.to_json()


    if flag_callback == 'g_scatter_plot':
        set_chart_flag = 0
        if i_selection_g_scatter_plot and i_selection_g_scatter_plot['points']:
            selectedpoints = [d['customdata'] for d in i_selection_g_scatter_plot['points']]
            selectedpoints = json.dumps(selectedpoints)
        else:
            selectedpoints = json.dumps(list(df_updated['custom_data']))

    elif flag_callback == 'button_galeria_filtrar':
        selectedpoints = []
        for i in range(len(s_button_galeria_filtrar_images)):
            if s_button_galeria_filtrar_images[i]['isSelected'] == True:
                selectedpoints.append(s_button_galeria_filtrar_images[i]['custom_data'])
        selectedpoints = json.dumps(selectedpoints)

    elif flag_callback == 'button_galeria_excluir':
        selectedpoints = []
        for i in range(len(s_button_galeria_filtrar_images)):
            if s_button_galeria_filtrar_images[i]['isSelected'] == False:
                selectedpoints.append(s_button_galeria_filtrar_images[i]['custom_data'])
        selectedpoints = json.dumps(selectedpoints)



    elif flag_callback == 'g_coordenadas_paralelas':
        set_chart_flag = 1
        if i_g_coordenadas_paralelas_restyleData is not None:
            selectedpoints = update_df_paralelas_coord(
                _df =df_updated,
                _list_columns =_columns_paralelas_coorenadas,
                _figure = s_g_coordenadas_paralelas_figure,
                _novas_cor=i_g_coordenadas_paralelas_restyleData
            )

            selectedpoints = json.dumps(list(selectedpoints['custom_data']))
        else:
            selectedpoints = json.dumps(list(df_updated['custom_data']))




    elif flag_callback == 'button_aplicar_novo_label':
        s_selected_custom_points = ast.literal_eval(s_selected_custom_points)
        df_updated['manual_label'][df_updated['custom_data'].isin(s_selected_custom_points)] = str(s_input_aplicar_novo_label_value)
        df_store_updated = df_updated.to_json()
        selectedpoints = json.dumps(list(df_updated['custom_data']))


    else:
        set_chart_flag = 0
        selectedpoints = json.dumps(list(df_updated['custom_data']))



    return [selectedpoints, df_store_updated, set_chart_flag]






@app.callback(
    [
    Output('g_scatter_plot', 'figure'),
    Output('g_image_selector', 'images'),
    Output('g_coordenadas_paralelas', 'figure'),

    ],
    [
    Input('selected_custom_points', 'data'),
    Input('button_galeria_organizar', 'n_clicks'),
    Input('button_galeria_selecionar_todos', 'n_clicks'),

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
    i_button_galeria_organizar_nclicks,
    i_button_galeria_selecionar_todos_nclicks,
    s_g_scatter_plot_figure,
    s_g_image_selector_images,
    s_g_coordenadas_paralelas_figure,
    s_store_df,
    s_chart_flag_data,
    ):
# s_store_df

    ctx = dash.callback_context
    flag_callback = ctx.triggered[0]['prop_id'].split('.')[0]

    updated_df = pd.read_json(s_store_df)

    if flag_callback == 'selected_custom_points':

        fig = f_figure_scatter_plot(updated_df, _columns=['x', 'y'], _selected_custom_data=json.loads(i_selected_custom_points))


        _image_teste_list_correct_label = updated_df['correct_label'][updated_df['custom_data'].isin(json.loads(i_selected_custom_points))]
        _image_teste_list_names = updated_df['names'][updated_df['custom_data'].isin(json.loads(i_selected_custom_points))]
        _image_teste_list_caption = updated_df['manual_label'][updated_df['custom_data'].isin(json.loads(i_selected_custom_points))]
        _image_teste_list_custom_data = updated_df['custom_data'][updated_df['custom_data'].isin(json.loads(i_selected_custom_points))]

        fig2 = demo_f.create_list_dics(
            _list_src=list('/assets/images/LClass_' + _image_teste_list_correct_label + '/' + _image_teste_list_names),
            _list_thumbnail=list('/assets/images/LClass_' + _image_teste_list_correct_label + '/' + _image_teste_list_names),
            _list_name_figure=list(_image_teste_list_names),
            _list_thumbnailWidth=[28] * _image_teste_list_correct_label.shape[0],
            _list_thumbnailHeight=[28] * _image_teste_list_correct_label.shape[0],
            _list_isSelected= [False] * _image_teste_list_correct_label.shape[0],
            _list_custom_data=list(_image_teste_list_custom_data),
            _list_thumbnailCaption=_image_teste_list_caption,
            _list_tags='')


        if s_chart_flag_data == 1:
            fig3 =  f_figure_paralelas_coordenadas(
                _df=updated_df,
                _columns=_columns_paralelas_coorenadas,
                _selected_custom_data=json.loads(i_selected_custom_points),
                _fig = s_g_coordenadas_paralelas_figure
            )
        else:
            fig3 =  f_figure_paralelas_coordenadas(
                        _df=updated_df,
                        _columns=_columns_paralelas_coorenadas,
                        _selected_custom_data=json.loads(i_selected_custom_points),
                        _fig = None
                    )
        return [fig, fig2, fig3]



    elif flag_callback == 'button_galeria_selecionar_todos':
        for i in range(len(s_g_image_selector_images)):
            s_g_image_selector_images[i]['isSelected'] = True
        return [s_g_scatter_plot_figure, s_g_image_selector_images, s_g_coordenadas_paralelas_figure]

    elif flag_callback == 'button_galeria_organizar':
        print ("Precisa fazer...!")
        return [s_g_scatter_plot_figure, s_g_image_selector_images, s_g_coordenadas_paralelas_figure]



    else:
        return [s_g_scatter_plot_figure, s_g_image_selector_images, s_g_coordenadas_paralelas_figure]




if __name__ == '__main__':
    app.run_server(debug=True, port=8025)
