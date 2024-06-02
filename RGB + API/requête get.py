import network   #import des fonction lier au wifi
import urequests	#import des fonction lier au requetes http
import utime	#import des fonction lier au temps
import ujson	#import des fonction lier aà la convertion en Json
from machine import Pin, PWM
from random import randint

wlan = network.WLAN(network.STA_IF) # met la raspi en mode client wifi
wlan.active(True) # active le mode client wifi
    
ssid = 'Gjallahórn'
password = 'spookikoo'
wlan.connect(ssid, password) # connecte la raspi au réseau
url = "https://hp-api.lainocs.fr/characters"


# Initialisation des différentes leds de la diode à leurs GP respectifs

red = PWM(Pin(2,mode=Pin.OUT))
red.freq(1000)
green = PWM(Pin(1,mode=Pin.OUT))
green.freq(1000)
blue = PWM(Pin(0,mode=Pin.OUT))
blue.freq(1000)


#Tableau contenant les différentes couleurs de la diode (les différentes intensités de chaque led)
#Les keys correspondent aux différentes houses dans le json qu'on obtient plus tard

houses = {"Gryffindor":(30000, 0, 0),
          "Slytherin":(0, 30000, 0),
          "Hufflepuff":(int((227*30000)/255), 20000, 0),
          "Ravenclaw":(int((30*30000)/255), int((144*30000)/255), 30000),
          "":(30000, 30000, 30000)}


#Réinitialisation de la diode

red.duty_u16(0)
green.duty_u16(0)
blue.duty_u16(0)


#Pour attendre la connection

while not wlan.isconnected():
    print("pas co")
    utime.sleep(1)
    pass


#gotten sert à vérifier que le Get a bien fonctionné
#big_list contient le json renvoyé par l'api

gotten = False
big_list = list()

try:
    while gotten == False:
        print("GET")
        r = urequests.get(url) # lance une requete sur l'url
        print("Gotten !")
        print(r.json()) # traite sa reponse en Json
        big_list = r.json() #stocke le json 
        gotten = True #confirme le bon fonctionnement du get
        r.close() # ferme la demande
        
        
    while True :    
        i = randint(0, len(big_list)-1) #on choisit un personnage au hasard dans la liste
        chara = big_list[i] 
        print(chara)
        
        
        #on récupère les bonnes intensités dans le dictionnaire houses, à partir de la string liée à...
        #...la clé house du dictionnaire chara récupéré dans le json
        
        intensity = houses[chara["house"]] 
        print(intensity)
        
        
        #on attribue les différentes intensités à leur led respectives
        
        red.duty_u16(intensity[0])
        green.duty_u16(intensity[1])
        blue.duty_u16(intensity[2])
        
        utime.sleep(5)
    
except Exception as e:
    print(e)
except KeyboardInterrupt :
    red.duty_u16(0)
    green.duty_u16(0)
    blue.duty_u16(0)
        