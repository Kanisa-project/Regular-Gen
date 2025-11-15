import os
import random
import pygame
from settings import *

#Setup asset folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")
rune_folder = os.path.join(img_folder, "runes")
pygame.init()
screen = pygame.display.set_mode((64,64))

class Rune():
    def __init__(self):
        self.phonetic_value = "none"
        self.numeric_value = 0
        self.germanic = "None"
        self.english = "None"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "blank.png")).convert()
        self.bright_keywords = ["None."]
        self.murky_keywords = ["None."]
        self.runetype = ["Vigor", "Finesse", "Divination"]
        self.vfdscore = [2,2,3]
        pass
    def brightstave(self):
        pass
    def murkystave(self):
        pass
    
class Fehu(Rune):
    def __init__(self):
        self.phonetic_value = "F"
        self.numeric_value = 1
        self.germanic = "Fehu"
        self.english = "fee"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "fehu.png")).convert()
        self.bright_keywords = ["Social Success", "Wealth energy", "Foresight", "New beginning"]
        self.murky_keywords = ["Greed","'burnout'", "atrophy", "Poverty", "Discord"]
        self.runetype = "Finesse"
        self.vfdscore = [0,4,3]
        pass
    def brightstave(self):
        return self.phonetic_value
    def murkystave(self):
        return self.phonetic_value.lower()
    
class Uruz(Rune):
    def __init__(self):
        self.phonetic_value = "U"
        self.numeric_value = 2
        self.germanic = "Uruz"
        self.english = "urox"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "uruz.png")).convert()
        self.bright_keywords = ["Strength", "Defence", "Tenacity", "Freedom", "Form", "Health", "Understanding"]
        self.murky_keywords = ["Weakness", "Obsession", "Misdirected force", "Domination by others", "Sickness", "Inconsistency", "Ignorance"]
        self.runetype = "Vigor"
        self.vfdscore = [7,0,0]
        pass
    def brightstave(self):
        return self.phonetic_value
    def murkystave(self):
        return self.phonetic_value.lower()
    
class Thurisaz(Rune):
    def __init__(self):
        self.phonetic_value = "Th"
        self.numeric_value = 3
        self.germanic = "Thurisaz"
        self.english = "thorn"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "thurisaz.png")).convert()
        self.bright_keywords = ["Reactive force", "Directed force", "Vital eroticism", "Regenerative catalyst"]
        self.murky_keywords = ["Danger", "Defenselessness" "Compulsion", "Betrayal", "Dullness"]
        self.runetype = "Vigor"
        self.vfdscore = [2,5,0]
        pass
    def brightstave(self):
        return self.phonetic_value
    def murkystave(self):
        return self.phonetic_value.lower()
    
class Ansuz(Rune):
    def __init__(self):
        self.phonetic_value = "A"
        self.numeric_value = 4
        self.germanic = "Ansuz"
        self.english = "Ans"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "ansuz.png")).convert()
        self.bright_keywords = ["Inspiration (enthusiasm)", "Synthesis", "Transformation", "Words"]
        self.murky_keywords = ["Misunderstanding", "Delusion", "Manipulation by others", "Boredom"]
        self.runetype = "Divination"
        self.vfdscore = [0,1,6]
        pass
    def brightstave(self):
        return self.phonetic_value
    def murkystave(self):
        return self.phonetic_value.lower()
    
class Raidho(Rune):
    def __init__(self):
        self.phonetic_value = "R"
        self.numeric_value = 5
        self.germanic = "Raidho"
        self.english = "Riding"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "raidho.png")).convert()
        self.bright_keywords = ["Rationality", "Action", "Justice", "Ordered growth", "Journey"]
        self.murky_keywords = ["Crisis", "Rigid", "Static", "Injustice", "Irrationality"]
        self.runetype = "Finesse"
        self.vfdscore = [1,6,0]
        pass
    def brightstave(self):
        return self.phonetic_value
    def murkystave(self):
        return self.phonetic_value.lower()
    
class Kenaz(Rune):
    def __init__(self):
        self.phonetic_value = "K"
        self.numeric_value = 6
        self.germanic = "Kenaz"
        self.english = "keen"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "kenaz.png")).convert()
        self.bright_keywords = ["Technical ability", "Inspiration", "Creativity", "Transformation", "Offspring"]
        self.murky_keywords = ["Disease", "Break-up", "Inability", "Lack of creativity"]
        self.runetype = "Finesse"
        self.vfdscore = [1,6,0]
        pass
    def brightstave(self):
        return self.phonetic_value
    def murkystave(self):
        return self.phonetic_value.lower()
    
class Gebo(Rune):
    def __init__(self):
        self.phonetic_value = "G"
        self.numeric_value = 7
        self.germanic = "Gebo"
        self.english = "gift"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "gebo.png")).convert()
        self.bright_keywords = ["Gift (giving)", "Generosity", "Magical exchange", "Honor", "Sacrifice"]
        self.murky_keywords = ["Influence-buying", "Greed", "Loneliness", "Dependence", "Over-sacrifice"]
        self.runetype = "Divination"
        self.vfdscore = [0,2,5]
        pass
    
class Wunjo(Rune):
    def __init__(self):
        self.phonetic_value = "W"
        self.numeric_value = 8
        self.germanic = "Wunjo"
        self.english = "wyn"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "wunjo.png")).convert()
        self.bright_keywords = ["Harmony", "Joy", "Fellowship", "Prosperity"]
        self.murky_keywords = ["Stultification", "Sorrow", "Strife", "Alienation"]
        self.runetype = "Finesse"
        self.vfdscore = [1,5,1]
        pass
    
class Hagalaz(Rune):
    def __init__(self):
        self.phonetic_value = "H"
        self.numeric_value = 9
        self.germanic = "Hagalaz"
        self.english = "Hail"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "hagalaz.png")).convert()
        self.bright_keywords = ["Change according to ideals", "Controlled crisis", "Completion", "Inner harmony"]
        self.murky_keywords = ["Catastrophe", "Crisis", "Stagnation", "Loss of power"]
        self.runetype = "Divination"
        self.vfdscore = [1,0,6]
        pass
    
class Nauthiz(Rune):
    def __init__(self):
        self.phonetic_value = "N"
        self.numeric_value = 10
        self.germanic = "Nauthiz"
        self.english = "Need"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "nauthiz.png")).convert()
        self.bright_keywords = ["Resistance (leading to strength)", "Recognition of orlog", "Innovation", "Need-fire (self-reliance)"]
        self.murky_keywords = ["Constraint of freedom", "Distress", "Toil", "Drudgery", "Laxity"]
        self.runetype = "Vigor"
        self.vfdscore = [4,3,0]
        pass
    
class Isa(Rune):
    def __init__(self):
        self.phonetic_value = "I"
        self.numeric_value = 11
        self.germanic = "Isa"
        self.english = "Ice"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "isa.png")).convert()
        self.bright_keywords = ["Concentrated self", "(Ego) Consciousness", "Self-control", "Unity"]
        self.murky_keywords = ["Ego-mania", "Dullness", "Blindness", "Dissipation"]
        self.runetype = "Divination"
        self.vfdscore = [0,2,5]
        pass
    
class Jera(Rune):
    def __init__(self):
        self.phonetic_value = "J"
        self.numeric_value = 12
        self.germanic = "Jera"
        self.english = "Year"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "jera.png")).convert()
        self.bright_keywords = ["Reward", "Plenty", "Peace", "Proper timing"]
        self.murky_keywords = ["Repetition", "Bad timing", "Poverty", "Conflict"]
        self.runetype = "Finesse"
        self.vfdscore = [1,4,2]
        pass
    
class Eihwaz(Rune):
    def __init__(self):
        self.phonetic_value = "EI"
        self.numeric_value = 13
        self.germanic = "Eihwaz"
        self.english = "Yew"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "eihwaz.png")).convert()
        self.bright_keywords = ["Enlightenment", "Endurance", "Initiation", "Protection"]
        self.murky_keywords = ["Confusion", "Destruction", "Dissatisfaction", "Weakness"]
        self.runetype = "Divination"
        self.vfdscore = [2,0,5]
        pass
    
class Perthro(Rune):
    def __init__(self):
        self.phonetic_value = "P"
        self.numeric_value = 14
        self.germanic = "Perthro"
        self.english = "Perd"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "perthro.png")).convert()
        self.bright_keywords = ["Good lot", "Knowledge of orlog", "Fellowship and joy", "Evolutionary change"]
        self.murky_keywords = ["Addiction", "Stagnation", "Loneliness", "Malaise"]
        self.runetype = "Finesse"
        self.vfdscore = [0,7,0]
        pass
    
class Elhaz(Rune):
    def __init__(self):
        self.phonetic_value = "Z"
        self.numeric_value = 15
        self.germanic = "Elhaz"
        self.english = "Elks"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "elhaz.png")).convert()
        self.bright_keywords = ["Connection with the gods", "Awakening", "Higher life", "Protection"]
        self.murky_keywords = ["Hidden danger", "Consumption by divine forces", "Loss of divine link"]
        self.runetype = "Divination"
        self.vfdscore = [0,0,7]
        pass
    
class Sowilo(Rune):
    def __init__(self):
        self.phonetic_value = "S"
        self.numeric_value = 16
        self.germanic = "Sowilo"
        self.english = "Sun"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "sowilo.png")).convert()
        self.bright_keywords = ["Guidance", "Hope", "Success", "Goals achieved", "Honor"]
        self.murky_keywords = ["False goals", "Bad counsel", "False success", "Gullibility", "Loss of goals"]
        self.runetype = "Vigor"
        self.vfdscore = [5,2,0]
        pass
    
class Tiwaz(Rune):
    def __init__(self):
        self.phonetic_value = "T"
        self.numeric_value = 17
        self.germanic = "Tiwaz"
        self.english = "Teu"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "tiwaz.png")).convert()
        self.bright_keywords = ["Troth", "Justice", "Rationality", "Self-sacrifice", "Analysis"]
        self.murky_keywords = ["Mental paralysis", "Over-analysis", "Over-sacrifice", "Injustice", "Imbalance"]
        self.runetype = "Vigor"
        self.vfdscore = [4,2,1]
        pass
    
class Berkano(Rune):
    def __init__(self):
        self.phonetic_value = "B"
        self.numeric_value = 18
        self.germanic = "Berkano"
        self.english = "Birch"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "berkano.png")).convert()
        self.bright_keywords = ["Birth", "Becoming", "Life changes", "Shelter", "Liberation"]
        self.murky_keywords = ["Blurring of consciousness", "Deceit", "Sterility", "Stagnation"]
        self.runetype = "Divination"
        self.vfdscore = [0,1,6]
        pass
    
class Ehwaz(Rune):
    def __init__(self):
        self.phonetic_value = "E"
        self.numeric_value = 19
        self.germanic = "Ehwaz"
        self.english = "Eh"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "ehwaz.png")).convert()
        self.bright_keywords = ["Harmony", "Teamwork", "Trust", "Loyalty"]
        self.murky_keywords = ["Duplication", "Disharmony", "Mistrust", "Betrayal"]
        self.runetype = "Vigor"
        self.vfdscore = [4,3,0]
        pass
    
class Mannaz(Rune):
    def __init__(self):
        self.phonetic_value = "M"
        self.numeric_value = 20
        self.germanic = "Mannaz"
        self.english = "Man"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "mannaz.png")).convert()
        self.bright_keywords = ["Divine structure", "Intellegence", "Awareness", "Social order"]
        self.murky_keywords = ["Depression", "Mortality", "Blindness", "Self-delusion"]
        self.runetype = "Divination"
        self.vfdscore = [1,1,5]
        pass
    
class Laguz(Rune):
    def __init__(self):
        self.phonetic_value = "L"
        self.numeric_value = 21
        self.germanic = "Laguz"
        self.english = ["Lake", "leek"]
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "laguz.png")).convert()
        self.bright_keywords = ["Life", "'Water' journey", "Sea of vitality", "Sea of unconscious", "Growth"]
        self.murky_keywords = ["Fear", "Circular motion", "Avoidance", "Withering"]
        self.runetype = "Vigor"
        self.vfdscore = [6,1,0]
        pass
    
class Ingwaz(Rune):
    def __init__(self):
        self.phonetic_value = "NG"
        self.numeric_value = 22
        self.germanic = "Ingwaz"
        self.english = "Ing"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "ingwaz.png")).convert()
        self.bright_keywords = ["Rest stage", "Internal growth", "Gestation"]
        self.murky_keywords = ["Impotence", "Scattering", "Movement without change"]
        self.runetype = "Finesse"
        self.vfdscore = [1,5,1]
        pass
    
class Dagaz(Rune):
    def __init__(self):
        self.phonetic_value = "D"
        self.numeric_value = 23
        self.germanic = "Dagaz"
        self.english = "Day"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "dagaz.png")).convert()
        self.bright_keywords = ["Awakening", "Hope/happiness", "Awareness", "The ideal"]
        self.murky_keywords = ["Blindness", "Hopelessness"]
        self.runetype = "Finesse"
        self.vfdscore = [0,6,1]
        pass
    
class Othala(Rune):
    def __init__(self):
        self.phonetic_value = "O"
        self.numeric_value = 24
        self.germanic = "Othala"
        self.english = "Odal"
        self.elder_form = pygame.image.load(os.path.join(rune_folder, "othala.png")).convert()
        self.bright_keywords = ["A home", "Group prosperity", "Group order", "Freedom", "Productive interaction"]
        self.murky_keywords = ["Lack of customary order", "Totalitarianism", "Slavery", "Poverty", "Homelessness"]
        self.runetype = "Vigor"
        self.vfdscore = [4,3,0]
        pass
    
def runeprint(rune):
    os.system('clear')
    print("Phonetic value: " + str(rune.phonetic_value))
    print("Numeric value: " + str(rune.numeric_value))
    print("Germanic name: " + str(rune.germanic))
    print("English name: " + str(rune.english))
    print("Bright keywords: ")
    for line in rune.bright_keywords:
        print("  -=" + line)
    print("Murky Keywords: ")
    for line in rune.murky_keywords:
        print("  -=" + line)
    if rune.runetype == "Vigor":
        print("*Vigor: +" + str(rune.vfdscore[0]))
    else:
        print("Vigor: +" + str(rune.vfdscore[0]))
    if rune.runetype == "Finesse":
        print("*Finesse: +" + str(rune.vfdscore[1]))
    else:
        print("Finesse: +" + str(rune.vfdscore[1]))
    if rune.runetype == "Divination":
        print("*Divination: +" + str(rune.vfdscore[2]))
    else:
        print("Divination: +" + str(rune.vfdscore[2]))
    
def rudun():
    ayd = str(input("Are you done? (True/False) "))
    return ayd

#runewindow = pygame.display.set_mode((64,64), 0, 0)
fehurune = Fehu()
uruzrune = Uruz()
thurisazrune = Thurisaz()
ansuzrune = Ansuz()
raidhorune = Raidho()
kenazrune = Kenaz()
geborune = Gebo()
wunjorune = Wunjo()
hagalazrune = Hagalaz()
nauthizrune = Nauthiz()
isarune = Isa()
jerarune = Jera()
eihwazrune = Eihwaz()
perthrorune = Perthro()
elhazrune = Elhaz()
sowilorune = Sowilo()
tiwazrune = Tiwaz()
berkanorune = Berkano()
ehwazrune = Ehwaz()
mannazrune = Mannaz()
laguzrune = Laguz()
ingwazrune = Ingwaz()
dagazrune = Dagaz()
othalarune = Othala()
blankrune = Rune()
rune_list = [fehurune,uruzrune,thurisazrune,ansuzrune,raidhorune,kenazrune,geborune,wunjorune,hagalazrune,nauthizrune,isarune,jerarune,eihwazrune,perthrorune,elhazrune,sowilorune,tiwazrune,berkanorune,ehwazrune,mannazrune,laguzrune,ingwazrune,dagazrune,othalarune]