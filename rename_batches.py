from os import listdir, rename
from os.path import join,  isfile

to_add = '_g4'
project_name = 'lroot_g4'

path = 'main/assets/' + project_name + '/dataframes/'
list_files = [f for f in listdir(path) if isfile(join(path, f))]

for f in list_files:
    rename(join(path, f), join(path, f[:-4] + to_add + '.csv'))