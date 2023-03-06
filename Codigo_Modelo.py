# -*- coding: utf-8 -*-

# Obtención de datos

import os
import pandas as pd
import numpy as np

path = './Pets_Breeds'

dogs = pd.DataFrame(columns = ['path', 'breed', 'type', 'dataset'])
dataset = os.listdir(f'{path}/Dog')
for d in dataset:
  breeds = os.listdir(f'{path}/Dog/{d}')
  for b in breeds:
    name = os.listdir(f'{path}/Dog/{d}/{b}')
    for n in name: 
      p = f'Dog/{d}/{b}/{n}'
      dogs = dogs.append({'path':p, 'breed':b, 'type':'Dog', 'dataset':d}, ignore_index=True)

cats = pd.DataFrame(columns = ['path', 'breed', 'type', 'dataset'])
breeds = os.listdir(f'{path}/Cat')
for b in breeds:
  cont = 0
  name = os.listdir(f'{path}/Cat/{b}')
  for n in name:
    if cont <= 9:
      d = 'test'
      cont += 1
    elif 9 < cont <= 19:
      d = 'valid'
      cont += 1
    else:
      d = 'train'
    p = f'Cat/{b}/{n}'

    cats = cats.append({'path':p, 'breed':b, 'type':'Cat', 'dataset':d}, ignore_index=True)

# Descripción y limpieza de los datos

print(dogs.info())

print(dogs['breed'].unique())

print(cats.info())

print(cats['breed'].unique())

# Exploración y visualización de los datos

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns

pets = pd.concat([dogs, cats], axis=0)

# Type count pets
type_count = pets.groupby('type')['path'].count().reset_index()
plt.figure(figsize=(10, 8))
sns.barplot(x=type_count['type'].unique(), y=type_count['path']).set(ylabel='type_count')
plt.show()

# Dataset use count
data_count = pets.groupby(['dataset', 'type'])['path'].count().reset_index().sort_values('path', ascending=False)
plt.figure(figsize=(10, 8))
sns.barplot(x=data_count['dataset'], y=data_count['path'], hue=data_count['type']).set(xlabel='dataset_count')
plt.show()

# Breed count pets
dog_breed_count = dogs.groupby('breed')['path'].count().reset_index().sort_values('path', ascending=False)
plt.figure(figsize=(15, 20))
sns.barplot(x=dog_breed_count['path'], y=dog_breed_count['breed'].unique()).set(xlabel='dog_breed_count')
plt.show()

cat_breed_count = cats.groupby('breed')['path'].count().reset_index().sort_values('path', ascending=False)
plt.figure(figsize=(15, 20))
sns.barplot(x=cat_breed_count['path'], y=cat_breed_count['breed'].unique()).set(xlabel='cats_breed_count')
plt.show()

# Image visualization
p = dogs['path'][12]
img = mpimg.imread(f'{path}/{p}')
plt.imshow(img)
plt.axis('off')
plt.show()

p = cats['path'][12]
img = mpimg.imread(f'{path}/{p}')
plt.imshow(img)
plt.axis('off')
plt.show()

p = dogs['path'][3700]
img = mpimg.imread(f'{path}/{p}')
plt.imshow(img)
plt.axis('off')
plt.show()

p = cats['path'][3700]
img = mpimg.imread(f'{path}/{p}')
plt.imshow(img)
plt.axis('off')
plt.show()

# Preparación de los datos para los algoritmos de Machine Learning

from keras.preprocessing.image import ImageDataGenerator

img_gen = ImageDataGenerator(rescale=1./255.)

pets_b_uniq = pets['breed'].unique().tolist()
pets_train = pets[(pets['dataset'] == 'train')]
pets_val = pets[(pets['dataset'] == 'valid')]
pets_test = pets[(pets['dataset'] == 'test')]

pets_gen_train = img_gen.flow_from_dataframe(
    dataframe=pets_train,
    directory=path,
    x_col='path',
    y_col='breed',
    classes=pets_b_uniq,
    shuffle=True,
    class_mode='categorical',
    target_size=(256, 256),
    batch_size=64
)

pets_gen_valid = img_gen.flow_from_dataframe(
    dataframe=pets_val,
    directory=path,
    x_col='path',
    y_col='breed',
    classes=pets_b_uniq,
    shuffle=True,
    class_mode='categorical',
    target_size=(256, 256),
    batch_size=128
)

pets_gen_test = img_gen.flow_from_dataframe(
    dataframe=pets_test,
    directory=path,
    x_col='path',
    y_col='breed',
    classes=pets_b_uniq,
    shuffle=False,
    class_mode='categorical',
    target_size=(256, 256),
    batch_size=1
)

# Entrenamiento del modelo y comprobación del rendimiento

from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import ( Dense, GlobalAveragePooling2D )

from tensorflow.python.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model

from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.applications.inception_v3 import InceptionV3

# Modelo 1: VGG19

v_model = VGG19(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
v_model.trainable = False
v_model.summary()
# plot_model(v_model)

vgg = Sequential()
vgg.add(v_model)

vgg.add(GlobalAveragePooling2D())
vgg.add(Dense(128))
vgg.add(Dropout(0.2))
vgg.add(Dense(len(pets_b_uniq), activation='softmax'))

vgg.build([None, 256, 256, 3])
vgg.summary()

vgg.compile(optimizer=Adam(),
             loss="categorical_crossentropy",
             metrics=["accuracy"])

cb_early_stopper = EarlyStopping(monitor='val_loss', patience=15)

history_v = vgg.fit(pets_gen_train, validation_data=pets_gen_valid, callbacks=cb_early_stopper, epochs=100)

model_v_score = vgg.evaluate(pets_gen_test)

print("Model Test Loss:",model_v_score[0])
print("Model Test Accuracy:",model_v_score[1])

reg = len(history_v.history['loss'])
v_data = {
    'model': ['VGG19'] * reg,
    'loss': history_v.history['loss'],
    'val_loss': history_v.history['val_loss'],
    'acc': history_v.history['accuracy'],
    'val_acc': history_v.history['val_accuracy'],
    'epoch': range(reg)
}
df_v = pd.DataFrame.from_dict(v_data)

df_v.to_csv('vgg19.csv')

# Modelo 2: RestNet50

r_model = ResNet50(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
r_model.trainable = False
r_model.summary()
# plot_model(r_model)

restn = Sequential()
restn.add(r_model)

restn.add(GlobalAveragePooling2D())
restn.add(Dense(128))
restn.add(Dropout(0.2))
restn.add(Dense(len(pets_b_uniq), activation='softmax'))

restn.build([None, 256, 256, 3])
restn.summary()

restn.compile(optimizer=Adam(),
             loss="categorical_crossentropy",
             metrics=["accuracy"])

cb_early_stopper = EarlyStopping(monitor='val_loss', patience=15)

history_r = restn.fit(pets_gen_train, validation_data=pets_gen_valid, callbacks=cb_early_stopper, epochs=100)

model_r_score = restn.evaluate(pets_gen_test)

print("Model Test Loss:",model_r_score[0])
print("Model Test Accuracy:",model_r_score[1])

reg = len(history_r.history['loss'])
r_data = {
    'model': ['RestNet50'] * reg,
    'loss': history_r.history['loss'],
    'val_loss': history_r.history['val_loss'],
    'acc': history_r.history['accuracy'],
    'val_acc': history_r.history['val_accuracy'],
    'epoch': range(reg)
}
df_r = pd.DataFrame.from_dict(r_data)

df_r.to_csv('RestNet50.csv')

# Modelo 3: InceptionV3

i_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
i_model.trainable = False
i_model.summary()
# plot_model(i_model)

incep = Sequential()
incep.add(i_model)

incep.add(GlobalAveragePooling2D())
incep.add(Dense(128))
incep.add(Dropout(0.2))
incep.add(Dense(len(pets_b_uniq), activation='softmax'))

incep.build([None, 256, 256, 3])
incep.summary()

incep.compile(optimizer=Adam(),
             loss="categorical_crossentropy",
             metrics=["accuracy"])

cb_early_stopper = EarlyStopping(monitor='val_loss', patience=15)

history_i = incep.fit(pets_gen_train, validation_data=pets_gen_valid, callbacks=cb_early_stopper, epochs=100)

model_i_score = incep.evaluate(pets_gen_test)

print("Model Test Loss:",model_i_score[0])
print("Model Test Accuracy:",model_i_score[1])

reg = len(history_i.history['loss'])
i_data = {
    'model': ['InceptionV3'] * reg,
    'loss': history_i.history['loss'],
    'val_loss': history_i.history['val_loss'],
    'acc': history_i.history['accuracy'],
    'val_acc': history_i.history['val_accuracy'],
    'epoch': range(reg)
}
df_i = pd.DataFrame.from_dict(i_data)

df_i.to_csv('InceptionV3.csv')

# Comparación de los modelos

# Métricas de VGG19
v_acc = history_v.history['accuracy']
v_val_acc = history_v.history['val_accuracy']
v_loss = history_v.history['loss']
v_val_loss = history_v.history['val_loss']

v_metrics = history_v.history['accuracy']
v_epochs_range = range(1, len(v_metrics) + 1)

# Métricas de RestNet50
r_acc = history_r.history['accuracy']
r_val_acc = history_r.history['val_accuracy']
r_loss = history_r.history['loss']
r_val_loss = history_r.history['val_loss']

r_metrics = history_r.history['accuracy']
r_epochs_range = range(1, len(r_metrics) + 1) 

# Métricas de InceptionV3
i_acc = history_i.history['accuracy']
i_val_acc = history_i.history['val_accuracy']
i_loss = history_i.history['loss']
i_val_loss = history_i.history['val_loss']

i_metrics = history_i.history['accuracy']
i_epochs_range = range(1, len(i_metrics) + 1) 

# Gráficas
plt.figure(figsize=(23, 8))
plt.subplot(1, 2, 1)
plt.plot(v_epochs_range, v_acc, label='VGG19 Training Accuracy')
plt.plot(v_epochs_range, v_val_acc, label='VGG19 Validation Accuracy')
plt.plot(r_epochs_range, r_acc, label='RestNet50 Training Accuracy')
plt.plot(r_epochs_range, r_val_acc, label='RestNet50 Validation Accuracy')
plt.plot(i_epochs_range, i_acc, label='InceptionV3 Training Accuracy')
plt.plot(i_epochs_range, i_val_acc, label='InceptionV3 Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(v_epochs_range, v_loss, label='VGG19 Training Loss')
plt.plot(v_epochs_range, v_val_loss, label='VGG19 Validation Loss')
plt.plot(r_epochs_range, r_loss, label='RestNet50 Training Loss')
plt.plot(r_epochs_range, r_val_loss, label='RestNet50 Validation Loss')
plt.plot(i_epochs_range, i_loss, label='InceptionV3 Training Loss')
plt.plot(i_epochs_range, i_val_loss, label='InceptionV3 Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

# Guardar modelo

import joblib

joblib.dump(incep, 'pet_model.pkl')