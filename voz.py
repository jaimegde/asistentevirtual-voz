import yfinance as yf
import pyttsx3
import speech_recognition as sr
import pywhatkit
import pyjokes
import webbrowser
import datetime
import wikipedia


# escuchar microfono y devolver audio como texto
def transformar_audio_a_texto():

    # almacenar el recognizer en una variable
    r = sr.Recognizer()

    # configurar el microfono
    with sr.Microphone() as origen:

        # tiempo de espera
        r.pause_threshold = 0.5

        # informar que comenzo la grabación
        print("ya puedes hablar")

        # guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # buscar en google
            pedido = r.recognize_google(audio, language="en-uk")

            # prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # prueba de que no comprendio el audio
            print("No se comprendió el audio")

            # devolver error
            return "estoy esperando"

        # en caso de no resolver el pedido
        except sr.RequestError:

            # prueba de que no comprendio el audio
            print("No se encontró el audio")

            # devolver error
            return "estoy esperando"

        # error inesperado
        except:

            # prueba de que no comprendio el audio
            print("Algo ha salido mal")

            # devolver error
            return "estoy esperando"


# funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    newVoiceRate = 100
    engine.setProperty('rate', newVoiceRate)
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# informar el día de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de dias
    calendario = {0:"Monday",
                  1:"Tuesday",
                  2:"Wednesday",
                  3:"Thursday",
                  4:"Friday",
                  5:"Saturday",
                  6:"Sunday"}

    # decir el dia de la semana
    hablar(f"Today is {calendario[dia_semana]}")


# informar que hora es
def pedir_hora():

    # crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"The time is {hora.hour} hours and {hora.minute} minutes"
    # decir la hora
    hablar(hora)


# funcion saludo inicial
def saludo_inicial():

    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Good night"
    elif 6 <= hora.hour < 13:
        momento = "Good morning"
    else:
        momento = "Good afternoon"

    # saludar
    hablar(f"{momento}, I'm R2D2 junior, your personal assistant.  How may I help you today?")


# funcion central del asistente
def pedir_cosas():

    # activar saludo inicial
    saludo_inicial()

    # variable de control
    comenzar = True

    # loop central
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_a_texto().lower()

        if "open youtube" in pedido:
            hablar("Yes sir, on it")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "open browser" in pedido:
            hablar("As you wish, master")
            webbrowser.open("https://www.google.com")
            continue
        elif "what day is it today" in pedido:
            pedir_dia()
            continue
        elif "what time is it" in pedido:
            pedir_hora()
            continue
        elif "search wikipedia" in pedido:
            hablar("Searching..please wait")
            pedido = pedido.replace("search wikipedia for", "")
            wikipedia.set_lang("en")
            resultado = wikipedia.summary(pedido, sentences = 2)
            hablar("Wikipedia says:")
            hablar(resultado)
            continue
        elif "quit" in pedido:
            comenzar = False
            hablar("See you later, alligator")
            break
        elif "search the internet" in pedido:
            hablar("On my way to surf the web")
            pedido = pedido.replace("search the internet for", "")
            pywhatkit.search(pedido)
            hablar("This is what I've found")
            continue
        elif "play" in pedido:
            hablar("Good idea, on my way")
            pywhatkit.playonyt(pedido)
            continue
        elif "joke" in pedido:
            hablar(pyjokes.get_joke("en"))
            continue
        elif "stock price" in pedido:
            accion = pedido.split("of")[-1].strip()
            cartera = {"apple":"AAPL",
                       "amazon":"AMZN",
                       "google":"GOOGL"}
            try:
                accion_busqueda = cartera[accion]
                accion_busqueda = yf.Ticker(accion_busqueda)
                precio_actual = accion_busqueda.info["regularMarketPrice"]
                hablar(f"I found the price of {accion} is currently at {precio_actual}")
                continue
            except:
                hablar("No clue, please try again")
                continue



pedir_cosas()