#versao antiga
def update_df_paralelas_coord(
    _df,
    _list_columns,
    _figure,
    _novas_cor):

    print("_figure"),
    print(_figure)

    print("_novas_cor")
    print(_novas_cor)


    _filters_label = []
    _filters_top = []
    _filters_bottom = []
    _filters_conca = []

    par_coord_data = _figure['data'][0]
    curr_dims = par_coord_data.get('dimensions', None)


    _dimension = None
    for i in range(5):
        _s = 'dimensions['+ str(i) + '].constraintrange'
        try:
            if isinstance(_novas_cor[0][_s][0][0], list):
                _dimension = i
            else:
                _dimension = i
        except:
            None




    for i in range(len(curr_dims)):


        if _dimension == i:
            _range = curr_dims[i]['constraintrange']
            _s = 'dimensions['+ str(i) + '].constraintrange'

            if isinstance(_novas_cor[0][_s][0][0], list):
                for ii in range(len(_novas_cor[0][_s][0])):
                    _filters_bottom.append(_novas_cor[0][_s][0][ii][0])
                    _filters_top.append(_novas_cor[0][_s][0][ii][1])
                    _filters_label.append(curr_dims[i]['label'])


                    if ii == len(_novas_cor[0][_s][0])  - 1:
                        _filters_conca.append('&')
                    else:
                        _filters_conca.append('|')
            else:
                _filters_bottom.append(_novas_cor[0][_s][0][0])
                _filters_top.append(_novas_cor[0][_s][0][1])
                _filters_label.append(curr_dims[i]['label'])
                _filters_conca.append('&')


        else:
            # print("Check 3")

            _filters_bottom.append(_df[curr_dims[i]['label']].min())
            _filters_top.append(_df[curr_dims[i]['label']].max())
            # _filters_bottom.append(curr_dims[i]['label'].min())
            # _filters_top.append(curr_dims[i]['label'].max())
            _filters_label.append(curr_dims[i]['label'])
            _filters_conca.append('&')



        # print("_filters_label", _filters_label)
        # print("_filters_top", _filters_top)
        # print("_filters_bottom", _filters_bottom)
        # print("_____________________________________\n\n")
    _filters_conca[-1:] = ' '
    # query = ' & '.join(f'{i} >= {j} &  {i} <= {k}' for i, j, k in zip(_filters_label, _filters_bottom, _filters_top))
    query = ''.join(f'{i} >= {j} &  {i} <= {k} {z} ' for i, j, k, z in zip(_filters_label, _filters_bottom,_filters_top, _filters_conca))
    # query = ''
    # label_anterior = ''
    # for i in range(len(_filters_label)):


    #     if i == 0:
    #         query = _filters_label[i] + '>=' + str(_filters_bottom[i]) + ' & ' + _filters_label[i] + '<='+ str(_filters_top[i])
    #     elif label_anterior == _filters_label[i]:
    #         query = query + ' | ' + _filters_label[i] + '>=' + str(_filters_bottom[i]) + ' & ' + _filters_label[i] + '<='+ str(_filters_top[i])
    #     else:
    #         query = query + ' & ' + _filters_label[i] + '>=' + str(_filters_bottom[i]) + ' & ' + _filters_label[i] + '<='+ str(_filters_top[i])
    #     label_anterior = _filters_label[i]

    # print("QUERY: \n", query)
    # print("\n\n\n\n\n")
    # # print("FIGURE \n")
    # print(_figure)
    # print("_______________________________________________________________________________________________________________________________________________________________________________ ")
    # print("_______________________________________________________________________________________________________________________________________________________________________________ ")
    # print("_______________________________________________________________________________________________________________________________________________________________________________\n\n\n ")
    updated_df = _df.query(query)

    return updated_df