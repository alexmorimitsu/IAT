import sys
assert len(sys.argv) >= 2

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
import timeit
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
#from openTSNE import TSNE
#from umap import UMAP
import random
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
import os
import time

#os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def read_model(model_name = 'inception', model_path = 'models/inception/model/', base_model_path = 'models/inception/base_model/', layer_name = 'conv_7b_ac'):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time, 'Reading model...')
    if model_name == 'inception': #InceptionResNetV2, num_features=1536
        img_height = 299  
        img_width = 299
        model = keras.models.load_model(model_path)
        base_model = keras.models.load_model(base_model_path)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time, 'Model read\n')
    return (img_height, img_width, model, base_model)

def get_final_model(model, base_model, layer_name = 'conv_7b_ac'):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time, 'Creating the final model...')
    layer_features = len(model.layers)-4
    
    model1 = Model(inputs=model.input, outputs=model.layers[layer_features-1].output)
    model2 = Model(inputs=base_model.input, outputs=base_model.get_layer(layer_name).output)
    output = model2(model1.output)
    
    #features_list = [layer.output for layer in final_model.layers if layer.name in layer_names]
    #print(len(features_list))
    
    global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
    output = global_average_layer(output)
    
    final_model = Model(model1.input, output)
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time, 'Final model created\n')
    return final_model

def prepare_images(images_path, img_width, img_height):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time, 'Preparing images...')

    test_gen = ImageDataGenerator()
    images = test_gen.flow_from_directory(
        directory=images_path,
        shuffle = False,
        class_mode=None,
        target_size=(img_height, img_width),
        batch_size=30,
    )
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time, 'Images created\n')

    return images

def compute_features(layer_name, model, base_model, images):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time, 'Computing features of ', layer_name, '...')

    final_model = get_final_model(model, base_model, layer_name)
    x = final_model.predict(images)

    image_names = []
    for filepath in images.filenames:
        image_names.append(filepath)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    print(current_time, 'Features computed\n')

    return x, image_names

def read_csv(filename, feature_names):
    '''
        Input:
            filename: path to the csv file
            feature_names: list of the names of the features 
        Output:
            names: list with the paths to the images
            features: values of the features
    '''
    df = pd.read_csv(filename)
        
    names = df['names'].values

    features = df[feature_names].values
    
    return names, features

def compute_pca(features, n=2):
    '''
        Input:
            n: number of PCA dimensions
        Output:
            PCA with n dimensions
    '''

    pca = PCA(n_components=n)
    return pca.fit_transform(features)

def compute_tsne(features, n=2):            
    #tsne = TSNE(n_components=n)
    #return tsne.fit_transform(features)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time, 't-SNE starting...')

    #tsne = TSNE( #opentsne
    #    n_components=n,
    #    perplexity=30,
    #    initialization="pca",
    #    metric="cosine",
    #    n_jobs=8,
    #    random_state=3,
    #).fit(features)
    tsne = TSNE(n_components=n, method='exact', verbose=1).fit_transform(features)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time, 't-SNE computed\n')
    print(tsne.shape)

    return tsne

#def compute_umap(features, n=2):            
#    umap = UMAP(n_components=n)
#    return umap.fit_transform(features)

def save_csv(features, features2d, image_names, csv_path, file_name = ''):
    header = ['names', 'x', 'y', 'custom_data', 'manual_label', 'correct_label',\
    'x2', 'y2', 'colors', 'y3', 'x4', 'y4', 'D1','D2','D3','D4','D5','D6','D7']

    basenames = [os.path.basename(name) for name in image_names]

    names_col = np.array(basenames).reshape(len(basenames), 1)

    ids = []
    for i in range(len(image_names)):
        ids.append(i)
    ids = np.array(ids).reshape(len(image_names), 1)

    manual_labels = []
    for i in range(len(image_names)):
        manual_labels.append('_')
    manual_labels = np.array(manual_labels).reshape((len(image_names), 1))

    correct_labels = []
    for i in range(len(image_names)):
        name = image_names[i]
        end = name.find('/')
        correct_labels.append(name[0:end])
    correct_labels = np.array(correct_labels).reshape((len(image_names), 1))
    zeros_6cols = np.zeros((len(image_names), 6))

    print(names_col.shape)
    print(features2d.shape)
    print(features.shape)

    
    data = np.hstack((names_col, features2d, ids, manual_labels, correct_labels, zeros_6cols, features))
    
    df = pd.DataFrame(data, columns = header)
    df.to_csv(csv_path + file_name + '.csv', index=False)
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time, csv_path + '.csv saved\n')

def main(path_to_parent, csv_path):
#    layer_names_1d = ['block17_1_ac', 'block17_6_ac', 'block17_11_ac', 'block17_16_ac', 'mixed_7a', 'block8_1_ac', 'conv_7b_ac']
    layer_names_1d = ['mixed_7a']
    layer_names_2d = ['mixed_7a']
#    feature_names = ['Layer_A', 'Layer_B', 'Layer_C', 'Layer_D', 'Layer_E', 'Layer_F', 'Layer_G']
    tsnes = []
    img_height, img_width, model, base_model = read_model()
    images = prepare_images(path_to_parent, img_width, img_height)    

    for layer_name in layer_names_1d:
        features, _ = compute_features(layer_name, model, base_model, images)
        tsne = compute_tsne(features, 7)
        #tsnes.append(tsne[0])
    #transposed_features = np.transpose(np.array(tsnes))[0]
    tsnes = tsne

    for layer_name in layer_names_2d:
        features, image_names = compute_features(layer_name, model, base_model, images)
        tsne2d = compute_tsne(features, 2)
        file_name = ''
        if len(layer_names_2d) > 1:
            file_name = '_' + layer_name
        save_csv(tsnes, tsne2d, image_names, csv_path, file_name)

dataset_path = sys.argv[1]

if len(sys.argv) >= 3:
    csv_path = sys.argv[2]
else:
    csv_path = './projection'

if __name__ == '__main__':
    main(dataset_path, csv_path)

print('\nfeatures were extracted.')

print('\n2D projection was generated.')

print('\nnow proceed with the command:')

print('\npython app.py assets/unlabeled/samples/ ' + csv_path + '.csv\n')

