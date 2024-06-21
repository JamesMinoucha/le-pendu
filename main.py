from tkinter import *
from PIL import ImageTk, Image
import random
import json

# ╰⊱♥⊱╮ღ꧁ Options ꧂ღ╭⊱♥≺

with open("config.json", 'r') as fichier:
    configFile = json.load(fichier)

min_words = configFile['min']
max_words = configFile['max']
mots_francais_fichier = configFile['dictionnaire']
alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
faviconpath = "resources/favicon.ico"
background1path = "resources/background1.png"
background2path = "resources/background2.png"
headpath = "resources/head.png"
bodypath = "resources/body.png"
leftarmpath = "resources/leftarm.png"
leftlegpath = "resources/leftleg.png"
rightarmpath = "resources/rightarm.png"
rightlegpath = "resources/rightleg.png"
backgroundmenupath = "resources/menu.png"

playbuttonpath = "resources/playbutton.png"
optionbuttonpath = "resources/optionbutton.png"

# ╰⊱♥⊱╮ღ꧁ Setup ꧂ღ╭⊱♥≺

def loadImage(path):
    return ImageTk.PhotoImage(Image.open(path))

root = Tk()
root.title('Jeu du Pendu')
root.iconbitmap("resources/favicon.ico")
root.iconphoto(True, loadImage(faviconpath))
root.geometry('390x500')
root.resizable(False, False)

background1 = loadImage(background1path)
background2 = loadImage(background2path)
backgroundmenu = loadImage(backgroundmenupath)
headimg = loadImage(headpath)
bodyimg = loadImage(bodypath)
leftarmimg = loadImage(leftarmpath)
leftlegimg = loadImage(leftlegpath)
rightarmimg = loadImage(rightarmpath)
rightlegimg = loadImage(rightlegpath)

playbutton = loadImage(playbuttonpath)
optionbutton = loadImage(optionbuttonpath)

heightText = 85
health = 0
status = "menu"
def tryKey(event):
    global health,word
    if event.char in alphabet:
        if event.char.lower() in list(chosenWord):
            index = [i for i, c in enumerate(chosenWord.lower()) if c == event.char.lower()]
            newstring = list(word)
            for letter in index:
                newstring[letter] = event.char.upper()
            word = newstring
            printImages()
        else:
            health += 1
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

        for letterSection in range(letters):
            canva.create_rectangle(51+(lengthOfLetterSection*letterSection)+(spaceBetween*letterSection),heightText,51+(lengthOfLetterSection*(letterSection+1))+(spaceBetween*(letterSection-1)),heightText+(5 if letters < 6 else 4),outline="#000", fill="#000")
            text = canva.create_text(51+(lengthOfLetterSection*letterSection)+(spaceBetween*letterSection),heightText, text=word[letterSection].upper(), font=font, anchor='sw')
            bbox = canva.bbox(text)
            newFont = ("Arial", int(lengthOfLetterSection/1.2))
            canva.itemconfig(text, font=newFont)
            bbox = canva.bbox(text)
            canva.move(text,lengthOfLetterSection/2-(bbox[2] - bbox[0])/1.85,0)
    elif status == "menu":
        background = canva.create_image(0, 0, anchor=NW, image=backgroundmenu)
        play_button = canva.create_image(0, 165, anchor=NW, image=playbutton)

    root.update_idletasks()
    root.update()

with open(mots_francais_fichier, 'r') as fichier:
    dictionnaire = fichier.read().splitlines()

word = ""
chosenWord = "naissance"
find = True
while not find:
    chosenWordTest = random.choice(dictionnaire)
    if not len(chosenWordTest) <= max_words:
        continue
    if not min_words <= len(chosenWordTest):
        continue
    chosenWord = chosenWordTest
    find = True

word = " "*len(chosenWord)
font = ("Arial", 20)
letters = len(chosenWord)
spaceBetween = 3 if letters > 7 else 6
lengthOfLetterSection = (287-(spaceBetween*(letters-1)))/letters
printImages()

# ╰⊱♥⊱╮ღ꧁ Choose the letter correctly ꧂ღ╭⊱♥≺



root.bind("<Key>",tryKey)
root.mainloop()