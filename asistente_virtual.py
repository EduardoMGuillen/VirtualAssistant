import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Opciones de voz/idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'


# escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():
    # Almacenar el recognizer en una variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # informar que comenzo la grabacion
        print('Ya comenzo la grabacion')

        # Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en google
            pedido = r.recognize_google(audio, language="es-ES")

            # prueba que pudo ingresar
            print("Texto: " + pedido)

            return pedido

        # No se comprende el audio
        except sr.UnknownValueError:

            # Prueba que no entendio el audio
            print('No se reconoce el texto')

            # Devolver Error
            return 'Esperando texto'

        # En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba que no entendio el audio
            print('No hay Servicio')

            # Devolver Error
            return 'Esperando texto'


# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):
    # Encender pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# pedir dia de la semana
def pedir_dia():
    # Crear variable de datps de hoy
    dia = datetime.date.today()
    print(dia)

    # Crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # Diccionario con nombre de dias
    calendario = {0: 'Lunes', 1: 'Martes', 3: 'Miercoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sabado', 7: 'Domingo'}
    hablar(f'Hoy es {calendario[dia_semana]}')


# Pedir Hora
def pedir_hora():
    # Crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)
    hablar(hora)


# Saludo Incial
def saludo_incial():
    # Crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buenos dias'
    else:
        momento = 'Buenas tardes'

    # Decir el saludo
    hablar(f'{momento} soy Sabina, tu asistente personal. Porfavor dime en que te puedo ayudar?')


# Centro de pedidos \ pedidos
def pedir():

    # Activar Saludo incial
    saludo_incial()

    # Variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # Activar el micro y guardar pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar(' Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences = 1)
            hablar(f'Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Ahora comienzo a reproducirlo')
            pedido = pedido.replace('reproducir', '')
            pywhatkit.playonyt(pedido)
            continue
        elif 'cuenta un chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple':'APPL','amazon':'AMZN','google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontre, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdon, no he encontrado esa accion')
                continue
        elif 'adiós' in pedido:
            hablar('Esta bien, me voy a descansar. Cualquier cosa me avisas!')
            break

pedir()