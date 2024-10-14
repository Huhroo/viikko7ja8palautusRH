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
                'Satamat': [],
                'tila':"epäsivistynyt"
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

#teköäly claude näytti miten säie koodin saa pakkattua one lineriksi jos sen haluaa käynnistää kerran
threading.Thread(target=apina_vartija, daemon=True).start()

def siivotaan():
    global tiedot, vanha_saari_luku

    for saari in tiedot['saaret']:
        canvas.delete(saari['object'])
        canvas.delete(saari['tekstilabel'])
        for satama in saari['Satamat']:
            canvas.delete(satama)
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
                        apina['sijainti'] = "haissa"
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

def paivita_saari_tekstilabelit():
    global tiedot
    while True:
        time.sleep(1)
        for saari in tiedot['saaret']:
            
            apinoiden_maara = len([apina for apina in saari['Apinat'] if apina['sijainti'] == "saari"])
            tekstilabel_teksti = f"S{saari['id']}\nApinoita: {apinoiden_maara}"
            
            if 'tekstilabel' in saari:  
                canvas.itemconfig(saari['tekstilabel'], text=tekstilabel_teksti)
            else:  
                saari_tekstilabel = canvas.create_text(saari['x'], saari['y'], text=tekstilabel_teksti, fill="white")
                saari['tekstilabel'] = saari_tekstilabel
                                 
threading.Thread(target=paivita_saari_tekstilabelit, daemon=True).start()

def satama_vahti():
    global tiedot
    while True:
        time.sleep(1)
        
        if tiedot['saaret']:  
            ekasaari = tiedot['saaret'][0]  
            ekasaari['tila'] = "sivistynyt"  
            
            for saari in tiedot['saaret']:
                if saari['tila'] == "sivistynyt" and not saari['Satamat']:  
                    x = saari['x']
                    y = saari['y']
                    
                    
                    Satamat = [
                        (x, y - 30),  
                        (x - 30, y), 
                        (x + 30, y),  
                        (x, y + 30)   
                    ]
                    
                   
                    for hx, hy in Satamat:
                        satama = canvas.create_rectangle(hx-3, hy-3, hx+3, hy+3, fill="brown")
                        saari['Satamat'].append(satama)
        else:
            print("Ei saaria vielä. Odotetaan...")

threading.Thread(target=satama_vahti, daemon=True).start()

def laheta_apina_uimaan():
    global tiedot
    while True:
        time.sleep(10)  
        for saari in tiedot['saaret']:
            if saari['tila'] == "sivistynyt":
                saaren_apinat = [apina for apina in saari['Apinat'] if apina['sijainti'] == "saari"]
                if saaren_apinat:
                    apina = random.choice(saaren_apinat)
                    suunta = random.choice(['pohjoinen', 'itä', 'etelä', 'länsi'])
                    
                    if suunta == 'pohjoinen':
                        apinax, apinay = saari['x'], saari['y'] - 30
                    elif suunta == 'itä':
                        apinax, apinay = saari['x'] + 30, saari['y']
                    elif suunta == 'etelä':
                        apinax, apinay = saari['x'], saari['y'] + 30
                    else:  # länsi
                        apinax, apinay = saari['x'] - 30, saari['y']
                    
                    canvas.coords(apina['leima'], apinax-2, apinay-2, apinax+2, apinay+2)
                    apina['sijainti'] = "meri"
                    apina['apinax'] = apinax
                    apina['apinay'] = apinay
                    apina['suunta'] = suunta
            for apina in saari['Apinat']:
                    if apina["sijainti"] == "saari":
                        apinax = saari['x'] + random.randint(-25,25)
                        apinay = saari['y'] + random.randint(-25,25)
                        canvas.coords(apina['leima'], apinax-2, apinay-2, apinax+2, apinay+2)
                        apina['sijainti'] = "saari"
                        apina['apinax'] = apinax
                        apina['apinay'] = apinay            

def liikuta_uivia_apinoita():
    global tiedot
    while True:
        time.sleep(0.5)  
        for saari in tiedot['saaret']:
            for apina in saari['Apinat']:
                if apina['sijainti'] == "meri":
                    if apina['suunta'] == 'pohjoinen':
                        apina['apinay'] -= 5
                    elif apina['suunta'] == 'itä':
                        apina['apinax'] += 5
                    elif apina['suunta'] == 'etelä':
                        apina['apinay'] += 5
                    else:  # länsi
                        apina['apinax'] -= 5

                    apina_aani = apina['ääni']  
                    
                    apinan_aani_saikeistin(apina_aani)

                    canvas.coords(apina['leima'], apina['apinax']-2, apina['apinay']-2, 
                                  apina['apinax']+2, apina['apinay']+2)
                    
                    
                    for toinen_saari in tiedot['saaret']: 
                        if toinen_saari != saari: 
                            if (abs(apina['apinax'] - toinen_saari['x']) <= 30 and  #Taas claude teköäly auttoi "törmäys" logiikan kanssa
                                abs(apina['apinay'] - toinen_saari['y']) <= 30):
                                
                                apina['sijainti'] = "saari"
                                toinen_saari['tila'] = "sivistynyt"
                                canvas.coords(apina['leima'], toinen_saari['x']-2, toinen_saari['y']-2, 
                                              toinen_saari['x']+2, toinen_saari['y']+2)
                                saari['Apinat'].remove(apina)
                                toinen_saari['Apinat'].append(apina)
                                break

threading.Thread(target=laheta_apina_uimaan, daemon=True).start()
threading.Thread(target=liikuta_uivia_apinoita, daemon=True).start()

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