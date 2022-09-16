from os import listdir, rename
from os.path import join,  isfile

to_add = '_g4'
project_name = 'lroot_g4'

path_csvs = 'main/assets/' + project_name + '/dataframes/'
list_csvs = [f for f in listdir(path_csvs) if isfile(join(path_csvs, f))]

for f in list_csvs:
    rename(join(path_csvs, f), join(path_csvs, f[:-4] + to_add + '.csv'))
    
path_back = 'main/assets/' + project_name + '/backgrounds/'
list_back = [f for f in listdir(path_back) if isfile(join(path_back, f))]

for f in list_back:
    rename(join(path_back, f), join(path_back, f[:-4] + to_add + '.png'))