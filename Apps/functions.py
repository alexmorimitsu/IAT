import base64
import io
import pathlib
import time

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from PIL import Image
from io import BytesIO
import json
# import utils

import pandas as pd
import plotly.graph_objs as go
import scipy.spatial.distance as spatial_distance

import warnings

import dash_bootstrap_components as dbc


import datetime
import math
from PIL import Image
import json




def create_paar_dimensions(
    _df,
    _list_columns,
    figure_update_dict=None):

    # _df is the updated dataframe, with all columns
    # as reference: https://www.semicolonworld.com/question/59812/dynamically-filtering-a-pandas-dataframe


    if figure_update_dict is None:
        _list_visible = []
        _list_values = []
        _list_range = []


        for i in range(len(_list_columns)):

            _temp_list = []
            _list_values.append(list(_df[_list_columns[i]]))

            _temp_list.append(_df[_list_columns[i]].min())
            _temp_list.append(_df[_list_columns[i]].max())
            _list_range.append(_temp_list)
            _list_visible.append(True)


        _data = {

            'label': _list_columns,
            'visible': _list_visible,
            'values': _list_values,
            'range': _list_range
        }

        _df_dict = pd.DataFrame(_data)
        _df_dict = _df_dict.to_dict('records')

        return [_df_dict, None]


    else:
        _filters_label = []
        _filters_top = []
        _filters_bottom = []

        par_coord_data = figure_update_dict['data'][0]
        curr_dims = par_coord_data.get('dimensions', None)

        for i in range(len(curr_dims)):

            print("LEN ==", len(curr_dims))

            try:
                _range = curr_dims[i]['constraintrange']
                if isinstance(_range[0], list):
                    for ii in range(len(_range)):
                        print("Check 1")
                        _filters_bottom.append(_range[ii][0])
                        _filters_top.append(_range[ii][1])
                        _filters_label.append(curr_dims[i]['label'])
                else:
                    print("Check 2")
                    _filters_bottom.append(_range[0])
                    _filters_top.append(_range[1])
                    _filters_label.append(curr_dims[i]['label'])
            except:
                print("Check 3")

                _filters_bottom.append(_df[curr_dims[i]['label']].min())
                _filters_top.append(_df[curr_dims[i]['label']].max())
                # _filters_bottom.append(curr_dims[i]['label'].min())
                # _filters_top.append(curr_dims[i]['label'].max())
                _filters_label.append(curr_dims[i]['label'])




            print("_filters_label", _filters_label)
            print("_filters_top", _filters_top)
            print("_filters_bottom", _filters_bottom)
            print("_____________________________________\n\n")

        query = ' & '.join(f'{i} >= {j} &  {i} <= {k}' for i, j, k in zip(_filters_label, _filters_bottom, _filters_top))
        print("QUERY: \n", query)
        updated_df = _df.query(query)
        return [None, updated_df]


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
    # _df_dict = _df_dict[['src', 'thumbnail','thumbnailWidth','thumbnailHeight','isSelected','customdata','thumbnailCaption','tags']]
    _df_dict = _df_dict[['src', 'thumbnail', 'name_figure','thumbnailWidth','thumbnailHeight','isSelected','custom_data', 'thumbnailCaption']]
    _df_dict = _df_dict.to_dict('records')


    return _df_dict


def create_images_layout(qtd_pontos=0, _qtd_cols_figure_2=6, selectedpoints=[1], images_names=None, _list_x=None, _list_y=None):

    _data = {
        'x': _list_x,
        'y': _list_y,
        'sizex': 0.5,
        'sizey': 0.5,
        'images': images_names,
        'source': images_names,
        'folder': 'data/',
        'png': '.png',
        'opacity': 1,
        'xanchor': 'center',
        'yanchor': 'middle',
        'xref': 'x',
        'yref': 'y'
    }

    _df_dict = pd.DataFrame(_data)
    _df_dict = _df_dict[['x', 'y', 'sizex', 'sizey', 'source',
                         'opacity', 'xanchor', 'yanchor', 'xref', 'yref']]
    _df_dict = _df_dict.to_dict('records')

    return _df_dict


def f_selection_check(_df, _list_selection, _list_memory, _list_figure):

    _x_selection = None
    _y_selection = None

    # Selection_0 vs Memory_0
    if _list_selection[0] != _list_memory[0]:
        try:

            temp_df = pd.DataFrame(_list_selection[0]["points"])


            _x_selection = temp_df['x'].values.tolist()
            _y_selection = temp_df['y'].values.tolist()
        except:
            temp_df = None
    else:
        None

    # Selection_2 vs Memory_2
    if _list_selection[1] != _list_memory[1]:
        try:
            _list_figure[1] = _list_figure[1]['data']
            _x_selection = []
            _y_selection = []
            for i in range(len(_list_figure[1])):
                _x = []
                _y = []
                _selected_points = _list_figure[1][i]['selectedpoints']
                for ii in range(len(_selected_points)):
                    _x.append(_list_figure[1][i]['x'][_selected_points[ii]])
                    _y.append(_list_figure[1][i]['y'][_selected_points[ii]])

                _x_temp = _df['x'][
                    (_df['x2'].isin(_x)) &
                    (_df['y2'].isin(_y))
                ]
                _x_temp = round(_x_temp, 7)
                _x_selection.append(_x_temp.tolist())

                _y_temp = _df['y'][
                    (_df['x2'].isin(_x)) &
                    (_df['y2'].isin(_y))
                ]

                _y_temp = round(_y_temp, 7)
                _y_selection.append(_y_temp.tolist())

            _t_x = []
            _t_y = []
            for i in range(len(_x_selection)):
                for ii in range(len(_x_selection[i])):
                    _t_x.append(_x_selection[i][ii])
                    _t_y.append(_y_selection[i][ii])

            _x_selection = _t_x
            _y_selection = _t_y

        except:
            temp_df = None
    else:
        None

    # Selection_3 vs Memory_3
    if _list_selection[2] != _list_memory[2]:
        try:
            _list_figure[2] = _list_figure[2]['data']
            _x_selection = []
            _y_selection = []
            for i in range(len(_list_figure[2])):
                _x = []
                _y = []
                _selected_points = _list_figure[2][i]['selectedpoints']
                for ii in range(len(_selected_points)):
                    _x.append(_list_figure[2][i]['x'][_selected_points[ii]])
                    _y.append(_list_figure[2][i]['y'][_selected_points[ii]])

                _x_temp = _df['x'][
                    (_df['x3'].isin(_x)) &
                    (_df['y3'].isin(_y))
                ]
                _x_temp = round(_x_temp, 7)
                _x_selection.append(_x_temp.tolist())

                _y_temp = _df['y'][
                    (_df['x3'].isin(_x)) &
                    (_df['y3'].isin(_y))
                ]

                _y_temp = round(_y_temp, 7)
                _y_selection.append(_y_temp.tolist())

            _t_x = []
            _t_y = []
            for i in range(len(_x_selection)):
                for ii in range(len(_x_selection[i])):
                    _t_x.append(_x_selection[i][ii])
                    _t_y.append(_y_selection[i][ii])

            _x_selection = _t_x
            _y_selection = _t_y

        except:
            temp_df = None
    else:
        None

    # Selection_4 vs Memory_4
    if _list_selection[3] != _list_memory[3]:
        try:
            _list_figure[3] = _list_figure[3]['data']
            _x_selection = []
            _y_selection = []
            for i in range(len(_list_figure[3])):
                _x = []
                _y = []
                _selected_points = _list_figure[3][i]['selectedpoints']
                for ii in range(len(_selected_points)):
                    _x.append(_list_figure[3][i]['x'][_selected_points[ii]])
                    _y.append(_list_figure[3][i]['y'][_selected_points[ii]])

                _x_temp = _df['x'][
                    (_df['x4'].isin(_x)) &
                    (_df['y4'].isin(_y))
                ]
                _x_temp = round(_x_temp, 7)
                _x_selection.append(_x_temp.tolist())

                _y_temp = _df['y'][
                    (_df['x4'].isin(_x)) &
                    (_df['y4'].isin(_y))
                ]

                _y_temp = round(_y_temp, 7)
                _y_selection.append(_y_temp.tolist())

            _t_x = []
            _t_y = []
            for i in range(len(_x_selection)):
                for ii in range(len(_x_selection[i])):
                    _t_x.append(_x_selection[i][ii])
                    _t_y.append(_y_selection[i][ii])

            _x_selection = _t_x
            _y_selection = _t_y

        except:
            temp_df = None
    else:
        None

    if _x_selection == None:
        _x_selection = _df['x'].values.tolist()
    elif len(_x_selection) == 0:
        _x_selection = _df['x'].values.tolist()
    else:
        None

    if _y_selection == None:
        _y_selection = _df['y'].values.tolist()
    elif len(_y_selection) == 0:
        _y_selection = _df['y'].values.tolist()
    else:
        None

    return _x_selection, _y_selection


def f_figure_1(_df, _x_selection, _y_selection):

    l_data = []
    groups = _df.groupby('manual_label')

    for idx, val in groups:
        _selectedpoints = _df['manual_label'][
            (_df['manual_label'] == idx) &
            (_df['x'].isin(_x_selection)) &
            (_df['y'].isin(_y_selection))
        ].index.values
        _temp = []
        for i in range(len(_selectedpoints)):
            _temp.append(val.index.get_loc(_selectedpoints[i]))
        _selectedpoints = _temp

        scatter = go.Scattergl(
            name=idx,
            x=val["x"],
            y=val["y"],
            text=val['manual_label'],
            selectedpoints=_selectedpoints,
            customdata=_selectedpoints,
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



def f_figure_2(_df, _x_selection, _y_selection):

    l_data = []
    groups = _df.groupby('manual_label')

    for idx, val in groups:
        _selectedpoints = _df['manual_label'][
            (_df['manual_label'] == idx) &
            (_df['x'].isin(_x_selection)) &
            (_df['y'].isin(_y_selection))
        ].index.values
        _temp = []
        for i in range(len(_selectedpoints)):
            _temp.append(val.index.get_loc(_selectedpoints[i]))
        _selectedpoints = _temp


        scatter = go.Scattergl(
            name=idx,
            x=val["x2"],
            y=val["y2"],
            text=val['manual_label'],
            selectedpoints=_selectedpoints,
            customdata=_selectedpoints,
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




def f_figure_3(_df, _x_selection, _y_selection):


    l_data = []
    groups = _df.groupby('manual_label')

    for idx, val in groups:
        _selectedpoints = _df['manual_label'][
            (_df['manual_label'] == idx) &
            (_df['x'].isin(_x_selection)) &
            (_df['y'].isin(_y_selection))
        ].index.values
        _temp = []
        for i in range(len(_selectedpoints)):
            _temp.append(val.index.get_loc(_selectedpoints[i]))
        _selectedpoints = _temp

        scatter = go.Scattergl(
            name=idx,
            x=val["x3"],
            y=val["y3"],
            text=val['manual_label'],
            selectedpoints=_selectedpoints,
            customdata=_selectedpoints,
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


def f_figure_4(_df, _x_selection, _y_selection):

    l_data = []
    groups = _df.groupby('manual_label')

    for idx, val in groups:
        _selectedpoints = _df['manual_label'][
            (_df['manual_label'] == idx) &
            (_df['x'].isin(_x_selection)) &
            (_df['y'].isin(_y_selection))
        ].index.values
        _temp = []
        for i in range(len(_selectedpoints)):
            _temp.append(val.index.get_loc(_selectedpoints[i]))
        _selectedpoints = _temp

        scatter = go.Scattergl(
            name=idx,
            x=val["x4"],
            y=val["y4"],
            text=val['manual_label'],
            selectedpoints=_selectedpoints,
            customdata=_selectedpoints,
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
