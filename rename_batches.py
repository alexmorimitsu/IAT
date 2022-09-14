from os import listdir, rename
from os.path import join,  isfile

to_add = '_verao_g2'
project_name = 'verao_g2'

path_csvs = 'main/assets/' + project_name + '/dataframes/'
list_csvs = [f for f in listdir(path_csvs) if isfile(join(path_csvs, f))]

for f in list_csvs:
    rename(join(path_csvs, f), join(path_csvs, f[:-4] + to_add + '.csv'))
    
path_back = 'main/assets/' + project_name + '/backgrounds/'
list_back = [f for f in listdir(path_back) if isfile(join(path_back, f))]

for f in list_back:
    rename(join(path_back, f), join(path_back, f[:-4] + to_add + '.png'))