from tkinter import *
from pytube import YouTube
from moviepy.editor import *
from PIL import Image, ImageTk
from soundcloud import Client
import os
import soundcloud

root = Tk()
root.geometry('800x600')
root.resizable(0, 0)
root.title('DESCARGADOR ENTONCES')

# Cargar la imagen de fondo de capibara y redimensionarla
background_image = Image.open("capibara.jpg")
background_image = background_image.resize((800, 600))
background_photo = ImageTk.PhotoImage(background_image)

background_label = Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

Label(root, text='Carpincho APP', font='arial 20 bold', bg='#AACDE2').place(x=32, y=20)

link = StringVar()
client_id = 'https://soundcloud.com/jesus-moral-580501209'

def DownloaderVideo():
    url = YouTube(str(link.get()))
    video = url.streams.get_highest_resolution()
    video.download()
    Label(root, text="Video Descargado", font="arial 13 bold", bg="#AACDE2", fg="#B57199").place(x=120, y=240)

def DownloaderAudio():
    url = YouTube(str(link.get()))
    audio = url.streams.filter(only_audio=True).first()
    audio_file = audio.download(filename="audio")
    Label(root, text="Musica descargada", font="arial 13 bold", bg="#AACDE2", fg="#B57199").place(x=120, y=320)
    mp4_file = AudioFileClip(audio_file)
    title = "".join(x for x in url.title if x.isalnum() or x in "_-.").rstrip()
    mp3_file_path = f"{title}.mp3"  # Nombre del archivo MP3 con el título de la canción
    mp4_file.write_audiofile(mp3_file_path)
    mp4_file.close()
    os.remove(audio_file)  # Eliminar el archivo de audio temporal



def DownloaderSoundCloud(client_id, track_id, dir, override=False):
    """Download from URL"""
    client = soundcloud.Client(client_id=client_id)
    track = client.get('/resolve', url=link)
    download(client, track, dir, override)
def download(client, track, dir, override=False):
    """Download the audio track from SoundCloud."""
    # Obtener la URL de descarga del audio
    stream_url = client.get(track.stream_url, allow_redirects=False).location

    # Comprobar si el directorio de destino existe, si no, crearlo
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Crear el nombre de archivo utilizando el título de la pista
    filename = os.path.join(dir, f"{track.title}.mp3")

    # Si el archivo ya existe y no se desea sobrescribir, sal de la función
    if not override and os.path.exists(filename):
        print(f"El archivo '{filename}' ya existe. Para sobrescribir, establezca 'override' como True.")
        return

    # Realizar la solicitud HTTP para descargar el audio
    response = requests.get(stream_url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Guardar el contenido de la respuesta en el archivo
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Audio descargado exitosamente como '{filename}'.")
    else:
        print("Error al descargar el audio. Por favor, comprueba la URL de la pista.")

Label(root, text='Inserta el enlace aquí:', font='arial 13', bg='#AACDE2').place(x=32, y=100)
link_enter = Entry(root, width=30, textvariable=link, borderwidth=5).place(x=32, y=130)

Button(root, text="DESCARGAR VIDEO", font='arial 13 bold italic', bg='#B57199', padx=2, command=DownloaderVideo).place(x=120, y=200)
Button(root, text="DESCARGAR AUDIO", font='arial 13 bold italic', bg='#B57199', padx=2, command=DownloaderAudio).place(x=120, y=280)
Button(root, text="DESCARGAR MÚSICA DE SOUNDCLOUD", font='arial 13 bold italic', bg='#B57199', padx=2,
       command=lambda: DownloaderSoundCloud(client_id, link, dir)).place(x=120, y=360)

root.mainloop()


