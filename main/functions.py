
from webbrowser import BackgroundBrowser
import pandas as pd
import plotly.graph_objs as go
import numpy as np

background_color = 'rgba(255, 250, 240, 100)'
aux_list = [] * 7 #new

def get_color(i):
    r = (201*i+100)%256
    g = (91*i+149)%256
    b = (53*i+237)%256
    return 'rgb(' + str(r) + ', ' + str(g) + ', ' + str(b) + ')'

def get_colorscale(num_colors):
    colorscale = []
    inc = 0
    if num_colors > 0:
        inc = 1/num_colors
    for i in range(num_colors+1):
        colorscale.append([i*inc, get_color(i)])
    return colorscale


def create_list_dics(
    _list_src,
    _list_thumbnail,
    _list_name_figure,
    _list_thumbnailWidth=None,
    _list_thumbnailHeight=None,
    _list_isSelected=None,
    _list_custom_data=None,
    _list_thumbnailCaption=None,
    _list_tags=None):

    _data = {
      'src': _list_src,
      'thumbnail': _list_thumbnail,
      'name_figure': _list_name_figure,
      'thumbnailWidth': _list_thumbnailWidth,
      'thumbnailHeight': _list_thumbnailHeight,
      'isSelected': _list_isSelected,
      'custom_data': _list_custom_data,
      'thumbnailCaption': _list_thumbnailCaption,
      'tags': _list_tags
    }

    _df_dict = pd.DataFrame(_data)
    _df_dict = _df_dict[['src', 'thumbnail', 'name_figure','thumbnailWidth','thumbnailHeight','isSelected','custom_data', 'thumbnailCaption']]
    _df_dict = _df_dict.to_dict('records')

    return _df_dict


def f_figure_scatter_plot(_df, _columns, _selected_custom_data):

    l_data = []
    column_name = 'colors'
    groups = _df.groupby(column_name)
    
    for idx, val in groups:
        _selectedpoints = _df[column_name][
            (_df[column_name] == idx) &
            (_df['custom_data'].isin(_selected_custom_data))
        ].index.values
        _custom_points = _df['custom_data'][(_df[column_name] == idx)]
        _label = str(val['manual_label'].iloc[0])

        _temp = []
        for i in range(len(_selectedpoints)):
            _temp.append(val.index.get_loc(_selectedpoints[i]))
        _selectedpoints = _temp

        scatter = go.Scattergl(
            name=_label,
            hoverinfo='skip',
            x=val[_columns[0]],
            y=val[_columns[1]],
            selectedpoints=_selectedpoints,
            customdata=_custom_points,
            mode="markers",
            #marker=dict(size=20, symbol="circle", colorscale='rainbow'),
            marker=dict(color = get_color(idx), size=12, symbol="circle"),
        )
        l_data.append(scatter)

    layout = go.Layout(
        modebar_orientation='h',
        legend=dict(yanchor='top', y=0.9),
        xaxis={'visible': False},
        yaxis={'visible': False},
        #xaxis={'range': [-1, 1.1], 'autorange': True,
        #       'gridcolor': 'rgba(0,0,0,0)', 'zeroline': False, 'showgrid': False},
        #yaxis={'range': [-1, 1.1], 'autorange': True,
        #       'gridcolor': 'rgba(0,0,0,0)', 'zeroline': False, 'showgrid': False},
        margin={'l': 0, 'r': 0, 'b': 0, 't': 0},
        dragmode='select',
        paper_bgcolor='aliceblue',
        plot_bgcolor=background_color,
    )

    figure_0 = go.Figure(data=l_data, layout=layout)
    #figure_0.update_layout(modebar_orientation='h', legend=dict(yanchor='top', y=0.9))
    return figure_0


def f_figure_paralelas_coordenadas(_df, _filtered_df, _columns, _selected_custom_data, _fig=None):

    #print('functions.py entrou no f_figure_paralelas_coordenadas')

    #_df_temp = _df[_df['custom_data'].isin(_selected_custom_data)]
    #_df_temp = _df_temp.reset_index(drop=True)


    #_list_visible = []
    #for i in range(len(_columns)):
    #    _list_visible.append(True)


    _list_range = []
    _list_values = []

    num_colors = _df['colors'].max()

    
    # range com max e min para cada dimensao de tsne
    for column in _columns:
        dim_min = _df[column].min()
        dim_max = _df[column].max()
        #dim_max += 0.1 # small overhead to place initial void selection
        _list_range.append([dim_min, dim_max])
        if _selected_custom_data != []:
            _list_values.append(_filtered_df[column].tolist())
        else:
            _list_values.append([dim_max+1]) #dummy point

    # determinar intervalos para selecoes de constraint range
    _list_constraint_range = []

    if _fig == None:
        if _selected_custom_data == []:
            for column in _columns:
                dim_max = _df[column].max()
                _list_constraint_range.append([[dim_max+50, dim_max + 55]])
                
        else:
            for column in _columns:
                col_min = _filtered_df[column].min()-0.1
                col_max = _filtered_df[column].max()+0.1
                ranges_list = [col_min, col_max]
                _list_constraint_range.append(ranges_list)

    else:
        _fig_list = _fig['data'][0]['dimensions']
        for i in range(len(_columns)):
            if 'constraintrange' in _fig_list[i]:
                _list_constraint_range.append(_fig_list[i]['constraintrange'])
            else:
                dim_max = _df[column].max()
                _list_constraint_range.append([[dim_max+50, dim_max + 55]])
                #_list_constraint_range.append([])
    
    
    _data = {
        'label': _columns,
        #'visible': _list_visible,
        'values': _list_values,
        'range': _list_range,
        'constraintrange': _list_constraint_range
    }

    dimensions_dict = pd.DataFrame(_data)
    dimensions_dict = dimensions_dict.to_dict('records')
    for i in range(len(dimensions_dict)):
        dimensions_dict[i]['ticktext'] = []
        #dimensions_dict[i]['tickvals'] = []
        #dimensions_dict[i]['label'] = ''

    #print(colors)
    custom_colorscale = get_colorscale(num_colors)
    #print('count: ', values, counts)

    layout = go.Layout(
        margin={'l': 10, 'r': 10, 'b': 5, 't': 5},
        paper_bgcolor = background_color,
    )

    coordenadas_paralelas = go.Parcoords(
            line = dict(color = _filtered_df['colors'],
                colorscale = custom_colorscale,
                #showscale = True,
                cmin=0,
                cmax=num_colors
            ),
            dimensions = dimensions_dict,
            tickfont = {'color': 'rgba(39,43,48,0)'},
            customdata = _df['custom_data'],
            )
    
    #print('coordenadas_paralelas[dimensions]')
    #print(coordenadas_paralelas['dimensions'])
    
    l_data = []
    l_data.append(coordenadas_paralelas)
    
    figure = go.Figure(data=l_data, layout=layout)
    return figure

def init_for_update_pc(selected_points):
    global aux_list
    aux_list = []
    for _ in range(7):
        aux_list.append(selected_points.copy())


def update_df_paralelas_coord(
    _df,
    _list_columns,
    _figure,
    _new_dim_vals): # new dimension values whenever user changes selection of a specific parcoord

    global aux_list

    for i in range(len(aux_list)):
        aux = aux_list[i]

    par_coord_data = _figure['data'][0]
    curr_dims = par_coord_data.get('dimensions', None)

    parcoord_index = int( list( _new_dim_vals[0].keys())[0] . split('.')[0][-2:-1] )
    i = parcoord_index
    points_in_i = []
    _vals = _df['D' + str(i+1)].tolist()
    _data = _df['custom_data'].tolist()

    if 'constraintrange' in curr_dims[i]:
        if isinstance(curr_dims[i]['constraintrange'][0], list):
            for _ranges in curr_dims[i]['constraintrange']:
                for j in range(len(_vals)):
                    val = _vals[j]
                    if val >= _ranges[0] and val <= _ranges[1]:
                        points_in_i.append(_data[j])
            aux_list[i] = points_in_i

        else:
            _ranges = curr_dims[i]['constraintrange']
            for j in range(len(_vals)):
                    val = _vals[j]
                    if val >= _ranges[0] and val <= _ranges[1]:
                        points_in_i.append(_data[j])

                #aux_list[i] = updated_df.query(query_string)
            aux_list[i] = points_in_i
    else:
        aux_list[i] = []
                
    intersected_points = aux_list[0]
    for i in range(len(aux_list)):
        aux = aux_list[i]
        if len(aux) == 0:
            return []
        elif len(aux) < len(intersected_points):
            intersected_points = aux

    for aux in aux_list:
        intersected_points = np.intersect1d(intersected_points, aux)

    return list(intersected_points)
    #return pd.DataFrame(columns=updated_df.columns)