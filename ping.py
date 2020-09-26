from time import sleep
from icmplib import ping
from gtts import gTTS
import os
from vlc import MediaPlayer
import json

def checkIP(ip):
    host = ping(ip, count=3, interval = 0.2)
    return host.is_alive


def playMessage(msg):
    """
        Cria um arquivo na pasta audios,
        dizendo uma mensagem passada por parametro
        espera 15s e deleta o arquivo
    """
    tts = gTTS(msg, lang="pt-br")
    file = "./audios/temp.mp3"

    tts.save(file)
    player = MediaPlayer(file)
    player.play()
    sleep(10)
    os.remove(file)

def checkIsAlive(devices):
    """
        Recebe uma lista com dicionarios
        pega o ip no dicionario e checa
        se ele esta na rede.
    """
    while True:

        for device in devices:
            isAlive = checkIP(device["ip"])

            if isAlive:
                msg = f'O dispositivo {device["name"]} está na rede!'
                print(msg)
                playMessage(msg)
            else:
                print(f'O dispositivo {device["name"]} está morto!')
        
        sleep(30*60)


def loadDevices(filename):
    """
        Carrega uma listade devices vinda de json
    """
    with open(filename, "r") as file:
        data = json.loads(file.read())

    return data["devices"]


if __name__ == "__main__":
    devices = loadDevices("./config/devices.json")
    checkIsAlive(devices)