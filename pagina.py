import streamlit as st
import requests
import streamlit.components.v1 as components
from PIL import Image
import PIL.Image
import os 
import csv
import pandas as pd
import pymongo
from pymongo import MongoClient
from io import BytesIO
import base64
import markdown
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yagmail



st.set_page_config(page_title="P.E.T", page_icon=":paw_prints:")

st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">', unsafe_allow_html=True)

PAGE_1 = "Inicio"
PAGE_2 = "Adoptar un animal"
PAGE_3 = "Donar"
PAGE_4 = "Contacto"
PAGE_5 = "Voluntariado"

def write_page_1():
    st.write("<h1>Bienvenidos a la protectora P.E.T!</h1>", unsafe_allow_html=True)
    st.write("<p>Somos una organización malagueña sin ánimo de lucro que se encarga de cuidar gatos y perros y darles un nuevo hogar.</p>", unsafe_allow_html=True)
    st.header("Adopción")
    st.write("En nuestra protectora contamos con un proceso de adopción muy sencillo y transparente. Si estás interesado en adoptar un animal, visita nuestra sección de Adoptar un animal para conocer los requisitos y los pasos a seguir.")
    file_id = "1ZVdlLCMy-HsmG2HC1_ZgalBySg7Td5UY"
    url = f'https://drive.google.com/uc?id={file_id}'
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    st.image(image, caption='Gatos y perros unidos')

    st.header("Colabora con nosotros")
    st.write("Si quieres colaborar con nuestra protectora, tienes varias opciones:")
    st.write("- Haz una donación para ayudarnos a cubrir los gastos de alimentación, cuidado veterinario, etc.")
    st.write("- Conviértete en voluntario y ayúdanos con las tareas diarias en la protectora.")
    st.write("- Comparte nuestro mensaje en tus redes sociales para ayudarnos a llegar a más personas.")
    

    st.header("Síguenos en redes sociales")
    st.write("Síguenos en nuestras redes sociales para estar al tanto de las últimas noticias y novedades de nuestra protectora:")
    st.markdown('<i class="fa fa-facebook-square"></i> [Facebook](https://www.facebook.com/mi_protectora)', unsafe_allow_html=True)
    st.markdown('<i class="fa fa-instagram"></i> [Instagram](https://www.instagram.com/mi_protectora)', unsafe_allow_html=True)
    st.markdown('<i class="fa fa-twitter"></i> [Twitter](https://www.twitter.com/mi_protectora)', unsafe_allow_html=True)

    
def write_page_2():
    st.write("<h2>Adoptar un animal:</h2>", unsafe_allow_html=True)
    animals = ['Perro', 'Gato']
    animal_choice = st.selectbox("¿Qué animal te gustaría adoptar?", animals)
    breeds = {
        'Perro': ['Labrador', 'Golden Retriever', 'Caniche'],
        'Gato': ['Siamés', 'Persa', 'Británico de pelo corto']
    }
    breed_choice = st.selectbox("¿De qué raza te gustaría adoptar?", breeds[animal_choice])
    st.write("Has seleccionado adoptar un", breed_choice, animal_choice)
    st.write("Aquí hay algunas fotos de los", breed_choice, animal_choice, "s disponibles para su adopción:")
    
    import os
    image_dir = f"{animal_choice.lower()}_{breed_choice.lower()}_images"
    animal_images = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".jpg")]
    st.image(animal_images, width=200)

    
    with open("adoptions.csv", "a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([breed_choice, animal_choice])


def write_page_3():
    st.write("<h2>Donar:</h2>", unsafe_allow_html=True)
    st.write("<p>Gracias por considerar una donación a nuestro refugio de animales.</p>", unsafe_allow_html=True)
    st.write("<p>Todas las donaciones serán utilizadas para:</p>", unsafe_allow_html=True)
    st.write("<ul>", unsafe_allow_html=True)
    st.write("<li>Proporcionar atención médica a los animales</li>", unsafe_allow_html=True)
    st.write("<li>Comprar alimentos y suministros</li>", unsafe_allow_html=True)
    st.write("<li>Construir nuevas instalaciones en el refugio</li>", unsafe_allow_html=True)
    st.write("</ul>", unsafe_allow_html=True)
    st.write("<p>Si prefieres donar en especie, estas son algunas opciones:</p>", unsafe_allow_html=True)
    st.write("<ul>", unsafe_allow_html=True)
    st.write("<li>Alimentos para animales</li>", unsafe_allow_html=True)
    st.write("<li>Mantas</li>", unsafe_allow_html=True)
    st.write("<li>Juguetes</li>", unsafe_allow_html=True)
    st.write("</ul>", unsafe_allow_html=True)
    st.write("<p>Por favor, póngase en contacto con nosotros si desea donar alguno de estos elementos.</p>", unsafe_allow_html=True)
    donation = st.number_input("¿Cuánto te gustaría donar?", value=0, min_value=0, max_value=1000, step=1)
    if st.button("Donar"):
        st.write("<p>Gracias por tu aportación :)</p>", unsafe_allow_html=True)
    st.write("<p>Has seleccionado donar ${}</p>".format(donation), unsafe_allow_html=True)
    st.write("<p>Si lo prefieres, puedes donar con Paypal:</p>", unsafe_allow_html=True)
    st.markdown("<a href='https://www.paypal.com'><img src='https://www.paypalobjects.com/webstatic/mktg/logo/AM_mc_vs_dc_ae.jpg' alt='Paypal'></a>", unsafe_allow_html=True)
    st.write("<p>Además, ¡nos encantaría contar con tu ayuda como voluntario!</p>", unsafe_allow_html=True)
    st.write("<p>Si estás interesado en ser voluntario, por favor ponte en contacto con nosotros.</p>", unsafe_allow_html=True)



def write_page_4():
    st.write("<h2>Contacto:</h2>", unsafe_allow_html=True)
    st.write("<p>Para cualquier consulta, por favor contáctenos en el siguiente formulario:</p>", unsafe_allow_html=True)
    
    with st.form(key='contact_form'):
        name = st.text_input('Nombre')
        email = st.text_input('Email')
        message = st.text_area('Mensaje')
        submit = st.form_submit_button(label='Enviar mensaje')

    if submit:
        
        yag = yagmail.SMTP('pruebapet262@gmail.com', 'ahcvndowfanwyesa')
        
        
        to = 'petprotectora@gmail.com'
        subject = 'Mensaje desde Refugio de Animales P.E.T'
        body = f'Nombre: {name}\nEmail: {email}\nMensaje: {message}'
        yag.send(to, subject, body)
        
        st.write(f"¡Gracias {name}! Tu mensaje ha sido enviado.")

    st.write("<p>O puedes contactarnos directamente:</p>", unsafe_allow_html=True)
    st.write("<ul>",unsafe_allow_html=True)
    st.write("<li>Teléfono: 555-1234</li>", unsafe_allow_html=True)
    st.write("<li>Dirección: Calle Principal 123</li>", unsafe_allow_html=True)
    st.write("<li>Horario: Lunes a Viernes de 9am a 5pm</li>", unsafe_allow_html=True)
    st.write("</ul>", unsafe_allow_html=True)

    st.write("<p>Ubicación:</p>", unsafe_allow_html=True)
    st.markdown('<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d60268.33258723767!2d-73.98750179272074!3d40.74881777062273!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMzDCsDA0JzM1LjAiTiA3M8KwMTUnMTYuOCJX!5e0!3m2!1sen!2sus!4v1644866163477!5m2!1sen!2sus" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>', unsafe_allow_html=True)
    st.write("<p>O puedes hablar con nuestro Agente por si necesitas algo a tiempo real</p>", unsafe_allow_html=True)
    components.iframe("https://console.dialogflow.com/api-client/demo/embedded/d8988215-f3ba-4d6c-aeba-9a3a58d150da", width=300, height=500)

client = MongoClient('mongodb+srv://Diegovp97:12345@cluster0.rfquoc6.mongodb.net/test')
db = client['PET']
voluntarios = db["Voluntarios"]

def save_volunteer_to_mongo(volunteer):
    """
    Función para guardar los datos del voluntario en MongoDB
    """
    # Recuperar los datos existentes de MongoDB
    existing_volunteer = voluntarios.find_one({"email": volunteer["email"]})

    if not existing_volunteer:
        # Si no hay datos antiguos, crear un nuevo objeto voluntario
        volunteer_data = {
          "nombre": volunteer["nombre"],
            "email": volunteer["email"],
            "telefono": volunteer["telefono"],
            "direccion": volunteer["direccion"],
            "ciudad": volunteer["ciudad"],
            "provincia": volunteer["provincia"],
            "pais": volunteer["pais"],
            "intereses": volunteer["intereses"],
            "disponibilidad": volunteer["disponibilidad"]
        }
        voluntarios.insert_one(volunteer_data)
        send_volunteer_email(volunteer["nombre"], volunteer["email"])
        st.success("Gracias por tu interés en ser voluntario. Nos pondremos en contacto contigo pronto.")
    else:
        # Si ya existen datos antiguos, actualizar el objeto voluntario
        existing_volunteer["nombre"] = volunteer["nombre"]
        existing_volunteer["telefono"] = volunteer["telefono"]
        existing_volunteer["direccion"] = volunteer["direccion"]  
        existing_volunteer["ciudad"] = volunteer["ciudad"]
        existing_volunteer["provincia"] = volunteer["provincia"]
        existing_volunteer["pais"] = volunteer["pais"]
        existing_volunteer["intereses"] = volunteer["intereses"]
        existing_volunteer["disponibilidad"] = volunteer["disponibilidad"]
        voluntarios.replace_one({"email": volunteer["email"]}, existing_volunteer)
        st.warning("Este voluntario ya había sido registrado previamente y sus datos han sido actualizados")

def volunteer_already_registered(volunteer):
    """
    Función para comprobar si un voluntario ya ha sido registrado previamente
    """
    existing_volunteer = voluntarios.find_one({"email": volunteer["email"]})
    if existing_volunteer:
        return True
    else:
        return False

def send_volunteer_email(name, email):
    """
    Función para enviar un correo electrónico al encargado del voluntariado cuando se registra un nuevo voluntario
    """
    yag = yagmail.SMTP('pruebapet262@gmail.com', 'ahcvndowfanwyesa')
    to = "petprotectora@gmail.com"
    subject = "Nuevo voluntario registrado"
    body = f"Hola encargado del voluntariado,\n\nTe informamos que {name} se ha registrado como voluntario en nuestra organización.\n\nSu dirección de correo electrónico es: {email}\n\n¡Gracias!"
    yag.send(to=to, subject=subject, contents=body)




def write_page_5():
    st.header("Voluntariado")
    st.write("¡Únete a nuestro equipo de voluntarios y ayúdanos a mejorar el mundo!")
    st.write("Rellena el siguiente formulario y nos pondremos en contacto contigo pronto.")
    st.write("")

    with st.form("volunteer_form"):
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Email")
        telefono = st.text_input("Teléfono")
        direccion= st.text_input("Dirección")
        ciudad = st.text_input("Ciudad")
        provincia = st.text_input("Provincia")
        pais = st.text_input("País")
        intereses = st.text_area("Áreas de interés como voluntario")
        disponibilidad = st.selectbox("Disponibilidad", ["Tiempo completo", "Medio tiempo", "Fines de semana"])
        submit_button = st.form_submit_button(label="Enviar formulario")

    if submit_button:
        
        volunteer = {
            "nombre": nombre,
            "email": email,
            "telefono": telefono,
            "direccion": direccion,
            "ciudad": ciudad,
            "provincia": provincia,
            "pais": pais,
            "intereses": intereses,
            "disponibilidad": disponibilidad
        }
        save_volunteer_to_mongo(volunteer)

def main():
    page = st.sidebar.selectbox("Elige una pagina", [PAGE_1, PAGE_2, PAGE_3, PAGE_4,PAGE_5])

    if page == PAGE_1:
        write_page_1()
    elif page == PAGE_2:
        write_page_2()
    elif page == PAGE_3:
        write_page_3()
    elif page == PAGE_4:
        write_page_4()
    elif page == PAGE_5:
        write_page_5()

if __name__ == "__main__":
    main()
