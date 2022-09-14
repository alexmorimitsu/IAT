import shutil
from random import shuffle
from math import ceil
from os import listdir, mkdir, system
from os.path import isfile, isdir, join, exists
from knn_labeling import run_knn
import pandas as pd

def map_ids(images_path):
    map_id_to_batch = {}    
    l = listdir(join('main', images_path))
    l.sort()
    
    for i in range(len(l)):
        map_id_to_batch[i+1] = l[i]
    
    return map_id_to_batch

def print_batches(dataframes_path, map_id_to_batch):
    for key in map_id_to_batch.keys():
        csv_name = map_id_to_batch[key] + '_verao_g2.csv'
        print('batch ' + str(key) + ': ' + csv_name)

def check_input(text, max_num):
    try:    
        assert int(text) > 0
        assert int(text) <= max_num
        return True
    except:
        print('Batch size should be an integer between 1 and', max_num)
        
def show_status(batches_path, dataframes_path):
    batch1_is_labeled = False

    batches_list = listdir(batches_path)
    batches_list.sort()
    print()
    for batch in batches_list:
        batch_file = dataframes_path + batch + '.csv'
        if isfile(batch_file):
            df = pd.read_csv(batch_file)
            not_labeled = 0
            value_counts = df['colors'].value_counts()
            if 0 in value_counts:
                not_labeled = value_counts[0]
            num_rows = len(df)
            num_labeled = num_rows-not_labeled
            
            if not_labeled == 0:
                print(batch, '-> features are already extracted. All ' + str(num_rows) + ' images are labeled.')
                if batch == 'batch0001':
                    batch1_is_labeled = True
            else:
                print(batch, '-> features are already extracted. ' + str(num_labeled) + ' out of ' + str(num_rows) + ' images are labeled.')
               
        else:
            print(batch, '-> needs features extraction.')
    return batch1_is_labeled

projects_path = 'main/assets/'

project_name = 'verao_g2'

dataframes_path = 'main/assets/' + project_name + '/dataframes/'
samples_path = 'main/assets/' + project_name + '/samples/' + project_name
images_path = 'assets/' + project_name + '/images/'
thumbnails_path = 'assets/' + project_name + '/thumbnails/'
batches_path = join('main', images_path)

num_batches = len(listdir(batches_path))

map_id_to_batch = map_ids(images_path)
print_batches(dataframes_path, map_id_to_batch)

text = input('\nChoose batch for labeling: ')
while not check_input(text, num_batches):
    text = input('\nChoose batch for labeling: ')
batch_id = int(text)

path_to_images = join(images_path, map_id_to_batch[batch_id], 'samples/')
path_to_thumbnails = join(thumbnails_path, map_id_to_batch[batch_id], 'samples/')
path_to_csv = dataframes_path + map_id_to_batch[batch_id] + '_verao_g2.csv'

system('python main/app.py ' + path_to_images + ' ' + path_to_thumbnails + ' ' + path_to_csv + ' 100')