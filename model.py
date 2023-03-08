from tensorflow.keras.models import load_model
from tensorflow import keras
import numpy as np
from tensorflow.keras.applications.inception_v3 import preprocess_input
import json


class Model:
    def __init__(self, weights_path: str, classes_name_path: str) -> None:
        # Carga del modelo y clases
        
        self.model = load_model(weights_path)
        with open(classes_name_path, 'r') as c:
            classes = json.load(c)
        self.classes = {int(k): v for k, v in classes.items()}
        
    def predict(self, img_path: str) -> str:
        # Predicción de la imagen

        img = keras.preprocessing.image.load_img(img_path, target_size=(256, 256))
        img_array = keras.utils.img_to_array(img)
        img_batch = np.expand_dims(img_array, axis=0)
        img_preprocessed = preprocess_input(img_batch)
        pred = self.model.predict(img_preprocessed)
        pred = pred.argmax()
        
        return self.classes[pred]


if __name__ == '__main__':
    # Ejemplo de predicción
    
    model = Model(weights_path='inceptionV3.h5', classes_name_path='breeds.json')

    import os

    path_img = os.listdir('Pets_Breeds/Dog/test/Afghan/01.jpg')
    pred = model.predict(path_img)
    print(pred)
