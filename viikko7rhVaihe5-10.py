import tkinter as tk
import random
import math
import winsound
import threading
import time

tiedot = {}
tiedot['saaret'] = []
tiedot['saarimäärä'] = 0
tiedot['apinaluku'] = 0
vanha_saari_luku = 0 

def distance(x1, y1, x2, y2): #teköäly claude koodia 
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)


def luo_saari():
    global tiedot
    for _ in range(100):  
        x = random.randint(40, 360)
        y = random.randint(40, 360)
        
        if not any(distance(x, y, saari['x'], saari['y']) < 90 for saari in tiedot['saaret']): #teköäly claude koodia (distance logiikka pelkästään)
            saari = canvas.create_rectangle(x-30, y-30, x+30, y+30, fill="green")
            tiedot['saaret'].append({
                'id':tiedot['saarimäärä']+ 1,
                'x': x,
                'y': y,
                'object': saari,
                'Apinat': [],
                'Satamat': []
            })

            #print(tiedot['saaret'][tiedot['saarimäärä']])
            tiedot['saarimäärä'] += 1
            winsound.Beep(244,500)
            return True  
    
    print("Saaren luominen epäonnistui 100 yrityksen jälkeen.")
    return False  

def apina_vartija():
    global tiedot,vanha_saari_luku

    vanha_saari_luku = tiedot['saarimäärä']
    
    while True:
        time.sleep(0.1)  
        if tiedot['saarimäärä'] > vanha_saari_luku:
            
            time.sleep(0.1)
            uusi_saari = tiedot['saaret'][vanha_saari_luku]
            for _ in range(10):  
                apina_aani = random.randint(400, 2000)  
                apinax =uusi_saari['x']+random.randint(-25,25)
                apinay=uusi_saari['y']+random.randint(-25,25)
                apinaleima = canvas.create_oval(apinax-2, apinay-2, apinax+2, apinay+2, fill="brown")
                uusi_saari['Apinat'].append({
                    'id': tiedot['apinaluku'],
                    'kotisaarenid':uusi_saari['id'],
                    'ääni': apina_aani,
                    'sijainti': "saari",
                    'leima': apinaleima,
                    'apinax': apinax,
                    'apinay':apinay,


                })
                tiedot['apinaluku'] += 1
                #print(f"Lisättiin apina saarelle ({uusi_saari['x']}, {uusi_saari['y']}) äänellä {apina_aani}")
                #print(uusi_saari)
            vanha_saari_luku += 1

def apina_aani():
    global tiedot
    while True:
        time.sleep(10)  
        for saari in tiedot['saaret']:
            for apina in saari['Apinat']:
                apina_aani = apina['ääni'] 
                winsound.Beep(apina_aani, 300) 
                #apinan_aani_saikeistin(apina_aani)

def apinan_aani(aani):
    winsound.Beep(aani,300)

def apinan_aani_saikeistin(aani):
    apinan_aani_saike = threading.Thread(target=apinan_aani,args=(aani,))
    apinan_aani_saike.daemon = True
    apinan_aani_saike.start() 


apina_aani_saike = threading.Thread(target=apina_aani)
apina_aani_saike.daemon = True  
#apina_aani_saike.start() #hox

#teköäly claude näytti miten säie koodin saa pakkattua one lineriksi jos sen haluaa käynnistää kerran.
threading.Thread(target=apina_vartija, daemon=True).start()

def siivotaan():
    global tiedot, vanha_saari_luku

    for saari in tiedot['saaret']:
        canvas.delete(saari['object'])
        for apina in saari['Apinat']:
                canvas.delete(apina['leima'])  
    

    tiedot['saarimäärä'] = 0
    tiedot['saaret'] = []
    vanha_saari_luku = 0 


def apina_nauru():
    global tiedot
    while True:
        time.sleep(10) 
        for saari in tiedot['saaret']:
            for apina in saari['Apinat']:
                if apina['sijainti'] == "saari":
                    noppa = random.randint(1,100)
                    if noppa == 1:
                        canvas.itemconfig(apina['leima'], fill="black")
                        apina_aani = apina['ääni']  
                        winsound.Beep(apina_aani, 250)
                        winsound.Beep(apina_aani, 250)
                        winsound.Beep(apina_aani, 400)    
                        print(f"Apina{apina['id']}: Olipas hauska vitsi!!! Voi ei...")
                        time.sleep(1)
                        canvas.delete(apina['leima'])
                        saari['Apinat'].remove(apina)

                

apina_nauru_saike = threading.Thread(target=apina_nauru)
apina_nauru_saike.daemon = True  
apina_nauru_saike.start()

def saarisaikeistin():
    saari_saike = threading.Thread(target = luo_saari)
    saari_saike.daemon = True
    saari_saike.start()

def hai():
    global tiedot
    while True:
        time.sleep(1) 
        for saari in tiedot['saaret']:
            for apina in saari['Apinat']:
                if apina['sijainti'] == "meri":
                    noppa = random.randint(1,100)
                    if noppa == 1:
                        canvas.itemconfig(apina['leima'], fill="black")
                        winsound.Beep(244,500)
                        print("Hai: Olipas maukaus apina!")
                        time.sleep(1)
                        canvas.delete(apina['leima'])
                        saari['Apinat'].remove(apina)


def siirto():
    global tiedot
    for saari in tiedot['saaret']:
        for apina in saari['Apinat']:
            kolikko = random.randint(0,1)
            if kolikko == 0:
                reuna = random.choice(['ylä', 'ala', 'vasen', 'oikea'])

            
                if reuna == 'ylä':
                    apinax = saari['x'] + random.randint(-30, 30)
                    apinay = saari['y'] - 35  
                elif reuna == 'ala':
                    apinax = saari['x'] + random.randint(-30, 30)
                    apinay = saari['y'] + 35  
                elif reuna == 'vasen':
                    apinax = saari['x'] - 35  
                    apinay = saari['y'] + random.randint(-30, 30)
                elif reuna == 'oikea':
                    apinax = saari['x'] + 35 
                    apinay = saari['y'] + random.randint(-30, 30)

                canvas.coords(apina['leima'], apinax-2, apinay-2, apinax+2, apinay+2)
                apina['sijainti'] = "meri"
                apina['apinax'] = apinax
                apina['apinay'] = apinay
                
            else:
                apinax = saari['x'] + random.randint(-25,25)
                apinay = saari['y'] + random.randint(-25,25)
                canvas.coords(apina['leima'], apinax-2, apinay-2, apinax+2, apinay+2)
                apina['sijainti'] = "saari"
                apina['apinax'] = apinax
                apina['apinay'] = apinay

 
                


hai_saike = threading.Thread(target=hai)
hai_saike.daemon = True  
hai_saike.start()

root = tk.Tk()
root.title("Saaripeli")
root.configure(bg="blue")

canvas = tk.Canvas(root, width=400, height=400, bg="blue")
canvas.pack()

luo_saari_button = tk.Button(root, text="Tulivuoren purkaus", command=saarisaikeistin)
luo_saari_button.pack()

siivous_button = tk.Button(root, text="Siivous", command=siivotaan)
siivous_button.pack()

siirto_button = tk.Button(root, text="Siirrä apinoita", command=siirto)
siirto_button.pack()




root.protocol("WM_DELETE_WINDOW", root.quit)

root.mainloop()