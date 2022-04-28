import shutil
from clustering import prepare_data
from random import shuffle
from math import ceil
from os import listdir, mkdir, system
from os.path import isfile, isdir, join, exists

def check_input(text, max_num):
    try:    
        assert int(text) > 0
        assert int(text) <= max_num
        return True
    except:
        print('Batch size should be an integer between 1 and', max_num)
        

def check_case(text):
    if text == 'ALL':
        for i in range(num_batches):
            prepare_data('dataframes/batch{:04d}'.format(i+1), join(batches_path, 'batch{:04d}'.format(i+1)))
            print('\nBatch', i+1, 'prepared.\n')
        return False
    elif text == 'SKIP':
        return False
    else:
        while not check_input(text, num_batches):
            text = input('\nChoose batch number for feature extraction: ')
        batch_id = int(text)

        prepare_data('dataframes/batch{:04d}'.format(batch_id), join(batches_path, 'batch{:04d}'.format(batch_id)))
        
        return True

def show_status(batches_path, dataframes_path):
    batches_list = listdir(batches_path)
    batches_list.sort()
    print()
    for folder in batches_list:
        if isfile(dataframes_path + folder + '.csv'):
            print(folder, 'features are OK.')
        else:
            print(folder, 'needs features extraction.')


projects_path = 'main/assets/images/'
dataframes_path = 'dataframes/'

print('\nList of ongoing projects:')
list_of_projects = listdir(projects_path)
for folder in list_of_projects:
    if isdir(join(projects_path, folder)):
        print(folder)

text = input('\nType name of ongoing project, or "NEW" to begin a project: ')
while text not in list_of_projects and text != 'NEW':
    text = input('\nType name of ongoing project, or "NEW" to begin a project: ')    

if text == 'NEW':
    text = input('\nChoose a name for the new project: ')
    while text in list_of_projects:
        print(text, 'is already an ongoing project.')
        text = input('\nChoose a name for the new project: ')
    mkdir(join(projects_path, text))
    mkdir(join(projects_path, text, 'batches'))

project_name = text

samples_path = 'main/assets/images/' + project_name + '/samples/'
batches_path = 'main/assets/images/' + project_name + '/batches/'

print('\nChecking dataset', project_name, '...\n')
if project_name not in list_of_projects:
    if not exists(project_name):
        raise Exception('Dataset ' + project_name + ' not found.')
    shutil.move(project_name, samples_path)

num_batches = len(listdir(batches_path))
if num_batches == 0: #creating batches if they do not exist yet
    files = [f for f in listdir(samples_path) if isfile(join(samples_path, f))]
    print(str(len(files)) + ' images found.')
    text = input('\nChoose batch size (default = 1000): ')
    while not check_input(text, len(files)):
        text = input('\nChoose batch size (default = 1000): ')
    if text == '':
        batch_size = 1000
    else:
        batch_size = int(text)

    print('\nProceeding with batch size = ' + str(batch_size))
    shuffle(files)

    num_batches = ceil(len(files)/batch_size)

    for i in range(num_batches):
        folder_name = 'batch{:04d}'.format(i+1)
        inner_folder_name = folder_name + '/samples'
        
        if exists(join(batches_path, folder_name)):
            shutil.rmtree(join(batches_path, folder_name))
        mkdir(join(batches_path, folder_name))
        mkdir(join(batches_path, inner_folder_name))
        folder_files = files[i*batch_size:(i+1)*batch_size]
        for f in folder_files:
            shutil.move(join(samples_path, f), join(batches_path, inner_folder_name))
    shutil.rmtree(samples_path)

    print('\n' + str(num_batches) + ' batches created:')

show_status(batches_path, dataframes_path)
text = input('\nChoose batch number for feature extraction, "ALL" for all batches, or "SKIP" to proceed to labeling: ')
while check_case(text):
    show_status(batches_path, dataframes_path)
    text = input('\nChoose batch number for feature extraction, "ALL" for all batches, or "SKIP" to proceed to labeling: ')

text = input('\nChoose batch for labeling: ')
while not check_input(text, num_batches):
    text = input('\nChoose batch for labeling: ')
batch_id = int(text)

path_to_images = join(batches_path, 'batch{:04d}'.format(batch_id), 'samples/')
print(path_to_images)
path_to_csv = 'dataframes/batch{:04d}'.format(batch_id) + '.csv'
system('python main/app.py ' + path_to_images + ' ' + path_to_csv)