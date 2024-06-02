from machine import Pin, PWM
import utime
from gpio_lcd import GpioLcd


#Matrice qui servira pour print pendant la fonction scanKeypad : pour renvoyer quel bouton on a pressé.
#Sert à afficher des mèmes sur l'écran.

keyMatrix = [["Praise The Sun !", "Get Over Here !", "Okeeeey Lezgo", "HOG RIDAAAAAA"],
             ["It's Dangerous  To Go Alone !", "Show Me Your     Moves !", "Can You Feel My HEEEAAAAART",
              "You'll Never SeeIt COMMIIIIINNN"],
             ["BABABOOEY", "KappaChungus    Deluxe", "MOM GET THE     CAMERA", "THEN THE WINGED HUSSARS ARRIVED"],
             ["Stop Right ThereCriminal Scum !", "FUS RO DAH !", "OOOOMAGAAHD",
              "HES JUST STANDINHERE, MENACINGLY"]]



#Numéros des différents GP auxquels le keypad est branché

colPins = [3,2,1,0]
rowPins = [7,6,5,4]

row = []
column = []



#Définition des pins utilisés par le keypad, le mode OUT utilisé pour les lignes a son importance pour la suite

for item in rowPins:
    row.append(machine.Pin(item,machine.Pin.OUT))
    
#On définit les colonnes en mode IN; on en verra l'utilité plus tard 
 
for item in colPins:
    column.append(machine.Pin(item,machine.Pin.IN,machine.Pin.PULL_DOWN))



#On initialise la valeur du keypad à 0 par défaut

key = '0'



#Initialisation de l'écran

lcd = GpioLcd(rs_pin=Pin(16),
              enable_pin=Pin(17),
              d4_pin=Pin(18),
              d5_pin=Pin(19),
              d6_pin=Pin(20),
              d7_pin=Pin(21),
              num_lines=2, num_columns=16)



#Fonction qui renvoie la position de l'appui sur le keypad

def scanKeypad():
    global key
    
    #On commence par activer les pins des ligne, un par un
    
    for rowKey in range(4):
        row[rowKey].value(1)
        for colKey in range(4):
            
            #On vérifie s'il y a un appui dans les colonnes, une par une...
            #...Si appui il y a, on obtient l'indice de la colonne, et comme on a aussi celui de la ligne active...
            #...On va simplement chercher la bonne clé dans keyMatrix, à l'aide des deux indices...
            #...Puis on désactive le pin de la ligne, et on renvoie la clé
            
            if column[colKey].value() == 1: 
                key = keyMatrix[rowKey][colKey] 
                row[rowKey].value(0)
                return(key)
            
        #On désactive le pin de la ligne actuelle, et la boucle passe à la ligne suivante
            
        row[rowKey].value(0) 



#Fonction qui utilise scanKeypad pour simplement print le résultat et l'afficher sur l'écran

def printFromKey():
    key=scanKeypad()
    if key is not None:
        print("Key pressed is:{}".format(key))
        lcd.putstr(key)
        
    utime.sleep(0.75)
    lcd.clear()


    
#Et on fait boucler le tout !

try:
    while True:
        printFromKey()
except KeyboardInterrupt:
    lcd.clear()