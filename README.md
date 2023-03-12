# P.E.T: Pet Enhacement Transition
https://pet-animal-shelter.streamlit.app/

## Justificación y descripción del proyecto
Se realizará un modelo para predecir razas de mascotas a partir de una imagen. Para ello
se han utilizado dos *datasets* encontrados en kaggle, uno de *perro* y otro de *gatos*, que se
han obtenido por separado pero trabajamos con los dos mezclados.

Para comprobar qué modelo se debería utilizar se ha trabajado con tres diferentes: *VGG19,
RestNet50 e InceptionV3*.

Una vez se haya comprobado el modelo con mejor rendimiento (acierto cerca del 1 y
pérdida cerca del -1) se guardará el modelo para su posterior uso en una página web.

La página web se ha realizado en la plataforma streamlit simulando una página real que
podría utilizar una protectora. Tendrá varias pestañas con distinta información, pero los
apartados a destacar son:
* **Predictor**: Donde se subirá la imagen de una mascota con su nombre y una
descripción y se guardaran estos datos junto con la predicción de la mascota.
* **Adoptar un animal**: En este apartado se podrá seleccionar si queremos adoptar un
perro o un gato y la raza de esta.

Se ha decidido buscar las mascotas para adoptar según su raza ya que, a partir de esta, se
sobreentiende si es perro o gato y si es de tamaño pequeño, mediano o grande.

Respecto al **NLP** se ha optado por la traducción de texto a dos idiomas (Inglés y Alemán).

Y para el apartado de **Big Data** se ha optado por realizar una base de datos de voluntarios
en *MongoDB*.

Este proyecto se ha pensado para facilitar el trabajo de identificación a las protectoras de
animales y fomentar la adopción

## Comparación de los modelos utilizados
Para comparar los modelos se ha utilizado el historial de entrenamiento y las métricas
obtenidas durante cada época.

Para mostrar las métricas, se han agrupado en dos gráficas:
1. **Training and Validation Accuracy**: Va mostrando el acierto que ha ido teniendo
cada modelo en cada época de entrenamiento y evaluación.
2. **Training and Validation Loss**: Va mostrando la función de pérdida obtenida en cada
época de entrenamiento y evaluación de los modelos.

![image](https://drive.google.com/uc?id=1ccBx6DvPGzPal1hFUFinVx4e27gQ85Ex)

En las gráficas se puede ver que no todos han entrenado las mismas épocas, ni obtenido
los mismos resultados:
* **RestNet50**: Es el modelo que más épocas ha entrenado pero no el que tiene mejor
resultado, ya que en *100* épocas el acierto es de *0.202* y su pérdida de *3.177* en la
evaluación.

* **VGG19**: Este modelo se quedaría a mitad de los otros dos, ya que en *49* épocas el
acierto es de *0.678* y su pérdida de *1.066* en la evaluación.

* **InceptionV3**: Es el modelo con mejor resultado de los entrenados. Ha realizado *19*
épocas, y a pesar de ser el que menos épocas ha realizado, obtiene un *0.914* de
acierto y *0.358* de pérdida en la evaluación.

Según los resultados observados, se ha utilizado el modelo **InceptionV3** para el uso de la página web.

## Procesamiento de Lenguaje Natural
Hemos implementado DialogFlow en nuestra aplicación y le hemos puesto frases típicas de
chatbot de una protectora como, háblame de tu protectora, quiero ser voluntario,
donaciones, etc.

![image](https://drive.google.com/uc?id=1s4YMhl0OrTOkqhCX7hapWWPCCw7or63C)

El agente entiende las frases en español:

![image](https://drive.google.com/uc?id=1u0QIC7UXmzmAAFE6nLsbssbUBIUEFhmk)

Inglés:

![image](https://drive.google.com/uc?id=1FFeUTzIPqnViGVYfUK5q92QJbbxu2YvN)

Y alemán:

![image](https://drive.google.com/uc?id=1xbW1ttDEFgakMdWTt3xuAKc6itjoSL8j)


## Muestra de la página web
La aplicación se ha realizado en streamlit y voy a mostrar el contenido de algunas de las pestañas más importantes:

* **Adopción de mascotas**: En este apartado tenemos dos selectbox para que el usuario elija si quiere perro o gato y la raza. Sale del apartado de predicción, el nombre, la descripción y la imagen usada que se muestra en la pantalla para el cliente.

![image](https://drive.google.com/uc?id=17K5e17WiulxmYklgy2kYpbpoM3JkIOt0)

* **Voluntariado**: Un formulario donde te puedes registrar como voluntario, se guardará en la base de datos de mongodb y se enviará un email al correo de la protectora.

    ![image](https://drive.google.com/uc?id=1h_-Ig1qjP48iCgmxLdk7pMXPnCTTW4Oc)

    * **Guardado de datos en MongoDB**:

    ![image](https://drive.google.com/uc?id=1j0nLZR044Sg3apg7wBEQ_cqWeUbCTeJf)

    * **Correo enviado**:
    
    ![image](https://drive.google.com/uc?id=1eU1amkd_FVEKi2CRcxCAKChlKh0AoB98)

* Administración: Esta página solo está habilitada para los administradores de la página, es donde se harán las predicciones. Tendrá dos apartados:

    * **Inicio de sesión**: Requerirá una contraseña para acceder al apartado de predicción. Si no se introduce una contraseña correcta, no se mostrará.

    ![image](https://drive.google.com/uc?id=1vChQe51idXFzhafrrNnxAWdOySX7Ksjm)

    * **Predictor**: Una vez iniciada la sesión correctamente, permitirá subir una imagen, indicarle un nombre y una breve descripción de la mascota. Una vez se guarden estos datos, mostrará la raza predicha.

    ![image](https://drive.google.com/uc?id=13zA-qknG7FXDymDg360CXBlzqyt7Xbdv)

    ![image](https://drive.google.com/uc?id=1cOvOO9yXbM1D8DrINkxQKRZzXOfoFuEL)
    
    ## Video
    Como el video pesaba mucho se ha compartido su enlace desde Drive.
    
    https://drive.google.com/file/d/11xlm258nj6EXtyG0aYFJLR1JbShNuGee/view?usp=sharing
