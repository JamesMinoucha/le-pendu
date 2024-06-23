from tkinter import *
from PIL import ImageTk, Image
import tkinter.font as tkFont
import random
import time
import json

# ╰⊱♥⊱╮ღ꧁ Path & Variables ꧂ღ╭⊱♥≺

with open("config.json", 'r') as fichier:
    configFile = json.load(fichier)

min_words = configFile['min']
max_words = configFile['max']
mots_francais_fichier = configFile['dictionnaire']
alphabet = list("abcdefghijklmnopqrstuvwxyz")
faviconpath = "resources/favicon.ico"

headpath = "resources/head.png"
bodypath = "resources/body.png"
loadingpath = "resources/loading.png"
leftarmpath = "resources/leftarm.png"
leftlegpath = "resources/leftleg.png"
rightarmpath = "resources/rightarm.png"
rightlegpath = "resources/rightleg.png"
winbackgroundpath = "resources/win.png"
backgroundmenupath = "resources/menu.png"
losebackgroundpath = "resources/lose.png"
playbuttonpath = "resources/playbutton.png"
background1path = "resources/background1.png"
background2path = "resources/background2.png"
replaybuttonpath = "resources/replaybutton.png"
optionbuttonpath = "resources/optionbutton.png"
madebypath = "resources/madeby.png"

# ╰⊱♥⊱╮ღ꧁ Main Application ꧂ღ╭⊱♥≺

def loadImage(path):
    return ImageTk.PhotoImage(Image.open(path))
def fadingImage(path):
    return Image.open(path)

root = Tk()
root.title('Jeu du Pendu')
root.iconbitmap("resources/favicon.ico")
root.iconphoto(True, loadImage(faviconpath))
font = tkFont.Font(family="Arial",size=36,weight="normal")
smallfont = tkFont.Font(family="Arial",size=14,weight="bold")
root.geometry('390x500')
root.resizable(False, False)

headimg = loadImage(headpath)
bodyimg = loadImage(bodypath)
madeby = loadImage(madebypath)
leftarmimg = loadImage(leftarmpath)
leftlegimg = loadImage(leftlegpath)
rightarmimg = loadImage(rightarmpath)
rightlegimg = loadImage(rightlegpath)
playbutton = loadImage(playbuttonpath)
background1 = loadImage(background1path)
background2 = loadImage(background2path)
replaybutton = loadImage(replaybuttonpath)
optionbutton = loadImage(optionbuttonpath)
winbackground = loadImage(winbackgroundpath)
losebackground = loadImage(losebackgroundpath)
backgroundmenu = loadImage(backgroundmenupath)

loadingimg = fadingImage(loadingpath).convert('RGBA')
resultloadingimg = None


heightText = 85
health = 0
status = "menu"
fading = False
triedLetters = []

playbuttondimension = {
    "x": 50,
    "y": 165,
    "width": 175,
    "height": 47
}
replaybuttondimension = {
    "x": 12,
    "y": 220,
    "width": 175,
    "height": 47
}

def fade_in(speed=5):
    global fading,resultloadingimg
    fading = True
    canva.config(cursor="")
    for alpha in range(0,255,speed):
        loadingimg_with_alpha = loadingimg.copy()
        loadingimg_with_alpha.putalpha(alpha)
        resultloadingimg = ImageTk.PhotoImage(loadingimg_with_alpha)
        printImages()
        time.sleep(0.01)
    fading = False
def fade_out(speed=5):
    global fading,resultloadingimg
    fading = True
    canva.config(cursor="")
    for alpha in range(255,0,speed*-1):
        loadingimg_with_alpha = loadingimg.copy()
        loadingimg_with_alpha.putalpha(alpha)
        resultloadingimg = ImageTk.PhotoImage(loadingimg_with_alpha)
        printImages()
        time.sleep(0.01)
    fading = False
def click(event):
    global status, resultloadingimg,health,triedLetters
    if fading == False:
        if status == "menu":
            if event.x >= playbuttondimension["x"] and event.x <= playbuttondimension["x"]+playbuttondimension["width"] and event.y >= playbuttondimension["y"] and event.y <= playbuttondimension["y"]+playbuttondimension["height"]:
                fade_in()
                status = "ingame"
                printImages()
                fade_out()
        elif status in ["lose","win"]:
            if event.x >= replaybuttondimension["x"] and event.x <= replaybuttondimension["x"]+replaybuttondimension["width"] and event.y >= replaybuttondimension["y"] and event.y <= replaybuttondimension["y"]+replaybuttondimension["height"]:
                fade_in()
                findWord()
                triedLetters = []
                health = 0
                status = "ingame"
                printImages()
                fade_out()

def movingCursor(event):
    if fading == False:
        if status == "menu":
            if event.x >= playbuttondimension["x"] and event.x <= playbuttondimension["x"]+playbuttondimension["width"] and event.y >= playbuttondimension["y"] and event.y <= playbuttondimension["y"]+playbuttondimension["height"]:
                canva.config(cursor="hand2")
            else:
                canva.config(cursor="")
        elif status in ["lose","win"]:
            if event.x >= replaybuttondimension["x"] and event.x <= replaybuttondimension["x"]+replaybuttondimension["width"] and event.y >= replaybuttondimension["y"] and event.y <= replaybuttondimension["y"]+replaybuttondimension["height"]:
                canva.config(cursor="hand2")
            else:
                canva.config(cursor="")
        
    
def tryKey(event):
    global health,word,status,fading
    if status == "ingame" and fading == False:
        if event.char.lower() in alphabet:
            if not event.char.lower() in triedLetters:
                if event.char.lower() in list(chosenWord):
                    index = [i for i, c in enumerate(chosenWord.lower()) if c == event.char.lower()]
                    newstring = list(word)
                    for letter in index:
                        newstring[letter] = event.char.upper()
                    word = newstring
                    triedLetters.append(event.char.lower())
                else:
                    health += 1
                    triedLetters.append(event.char.lower())
                if health == 6:
                    fade_in()
                    status = "lose"
                    fade_out()
                elif word.count(" ") == 0:
                    fade_in()
                    status = "win"
                    fade_out()
                if status == "ingame":
                    fade_out(10)
                printImages()


canva = Canvas(root, width=390, height=500,highlightthickness=0)
canva.pack()


def printImages():
    global background,head,body,leftarm,leftleg,rightarm,rightleg
    canva.delete('all')
    if status == "ingame":
        background = canva.create_image(0, 0, anchor=NW, image=background2 if health > 0 else background1)

        if health >= 1: head = canva.create_image(0, 0, anchor=NW, image=headimg)
        if health >= 2: body = canva.create_image(0, 0, anchor=NW, image=bodyimg)
        if health >= 3: leftarm = canva.create_image(0, 0, anchor=NW, image=leftarmimg)
        if health >= 4: rightarm = canva.create_image(0, 0, anchor=NW, image=rightarmimg)
        if health >= 5: leftleg = canva.create_image(0, 0, anchor=NW, image=leftlegimg)
        if health >= 6: rightleg = canva.create_image(0, 0, anchor=NW, image=rightlegimg)


        text = canva.create_text(51,120,text=' '.join(triedLetters).upper(), font=smallfont, anchor='sw',width=287)
        for letterSection in range(letters):
            canva.create_rectangle(51+(lengthOfLetterSection*letterSection)+(spaceBetween*letterSection),heightText,51+(lengthOfLetterSection*(letterSection+1))+(spaceBetween*(letterSection-1)),heightText+(5 if letters < 6 else 4),outline="#000", fill="#000")
            text = canva.create_text(51+(lengthOfLetterSection*letterSection)+(spaceBetween*letterSection),heightText, text=word[letterSection].upper(), font=font, anchor='sw')
            bbox = canva.bbox(text)
            newFont = tkFont.Font(family="Inter",size=int(lengthOfLetterSection/1.2),weight="bold")
            canva.itemconfig(text, font=newFont)
            bbox = canva.bbox(text)
            canva.move(text,lengthOfLetterSection/2-(bbox[2] - bbox[0])/1.85,0)
    elif status == "menu":
        background = canva.create_image(0, 0, anchor=NW, image=backgroundmenu)
        canva.create_image(0, 165, anchor=NW, image=playbutton)
        canva.create_image(390-163-7,500-18-7,anchor=NW, image=madeby)
    elif status == "win":
        background = canva.create_image(0, 0, anchor=NW, image=winbackground)
        canva.create_text(113,155,text=''.join(chosenWord.upper()), font=smallfont, anchor='n',justify=CENTER)
        canva.create_image(replaybuttondimension["x"], replaybuttondimension["y"], anchor=NW, image=replaybutton)
    elif status == "lose":
        background = canva.create_image(0, 0, anchor=NW, image=losebackground)
        canva.create_text(113,155,text=''.join(chosenWord.upper()), font=smallfont, anchor='n',justify=CENTER)
        canva.create_image(replaybuttondimension["x"], replaybuttondimension["y"], anchor=NW, image=replaybutton)
    canva.create_image(0,0, anchor=NW, image=resultloadingimg)

    root.update_idletasks()
    root.update()

with open(mots_francais_fichier, 'r') as fichier:
    dictionnaire = fichier.read().splitlines()

lengthOfLetterSection = 0
spaceBetween = 0
word = ""
chosenWord = ""
letters = 0
find = False
def findWord():
    global chosenWord,find,word,lengthOfLetterSection,spaceBetween,letters
    lengthOfLetterSection = 0
    spaceBetween = 0
    letters = 0
    word = ""
    chosenWord = ""
    find = False
    while not find:
        chosenWordTest = random.choice(dictionnaire)
        if not len(chosenWordTest) <= max_words:
            continue
        if not min_words <= len(chosenWordTest):
            continue
        chosenWord = chosenWordTest
        find = True
    word = " "*len(chosenWord)
    letters = len(chosenWord)
    spaceBetween = 3 if letters > 7 else 6
    lengthOfLetterSection = (287-(spaceBetween*(letters-1)))/letters
findWord()
printImages()

# ╰⊱♥⊱╮ღ꧁ Execute it ꧂ღ╭⊱♥≺

canva.bind("<Button-1>", click)
root.bind("<Motion>",movingCursor)
root.bind("<Key>",tryKey)
root.mainloop()