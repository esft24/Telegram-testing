from random import choice, random, randint

class Game:
    def __init__(self, totalTurns = 7):
        self.inactiveMonsters = []
        self.players = []
        self.playersIds = []
        self.playersDict = {}
        self.genMonsters()


        self.fullMoon = False
        self.totalFullMoons = 0
        self.turn = 0
        self.totalTurns = totalTurns

        # Telegram Variables
        self.chat_id = None

    def initialize(self):
        self.assignMonsters()

    def genMonsters(self):
        w = Witch()
        v = Vampire()
        pp = Puppet()
        t = TwoFaced()
        l = Leprechaun()
        m = MonsterHunter()
        a = Alien()
        z = Zombie()
        s = SerialKiller()
        vs = VengefulSpirit()
        i = Invisible()
        ww = Werewolf()
        b = BodySwapper()
        mm = Mummy()
        f = Frankenstein()

        self.inactiveMonsters = [w, v, pp, t, l, m, a, z, s, vs, i, ww, b, mm, f]

    def assignMonsters(self):
        for i in self.playersIds:
            monster = choice(self.inactiveMonsters)
            self.players.append(monster)
            monster.playerId = i
            monster.gameState = self
            self.playersDict[i] = monster
            self.inactiveMonsters.remove(monster)

    def checkIfAddable(self, playerId):
        if playerId in self.playersIds:
            return 1

        if len(self.players) >= 7:
            return 2
        
        return 0


    def addPlayer(self, playerId, playerName):

        # Choose monster
        monster = choice(self.inactiveMonsters)
        # Set Game
        self.playersIds.append(playerId)
        self.players.append(monster)
        self.playersDict[playerId] = monster
        self.inactiveMonsters.remove(monster)
        # Set monster
        monster.playerId = playerId
        monster.playerName = playerName
        monster.gameState = self
        return monster

    # Turn Phases
    def startGame(self):
        for p in self.players:
            p.startGame()

    def startRound(self):
        for p in self.players:
            p.startRound()
        
        self.turn += 1

        if self.turn != 1:
            if (randint(1,(self.totalTurns) - 1) + 2 * self.totalFullMoons) < self.turn:
                self.fullMoon = True
                self.totalFullMoons += 1

    def checkMatches(self, playersCopy=False):
        if playersCopy == False:
            self.checkMatches(self.players.copy())
            return

        if playersCopy == []:
            return

        chooser = playersCopy[0]
        choice = playersCopy[0].choice

        if choice == None:
            chooser.hearts -= 1
            playersCopy.remove(chooser)
        elif choice.choice == chooser:
            if choice.name == 'Werewolf' or choice.name == "Body Swapper":
                chooser.match(choice)
                choice.match(chooser)
            else:
                choice.match(chooser)
                chooser.match(choice)

            playersCopy.remove(chooser)
            playersCopy.remove(choice)
        else:
            chooser.rejected(choice)
            choice.rejects(chooser)
            playersCopy.remove(chooser)

        self.checkMatches(playersCopy)

    def orderPlayers(self):
        for p in self.players:
            p.beforeOrder()

        self.players.sort(key=lambda p: p.showScore(), reverse=True)
        pos = 1

        for p in self.players:
            p.changePosition(pos)
            pos += 1

    def revealFirstPlace(self):
        for p in self.players:
            if not p.revealed:
                p.reveal()
                break

    def endRound(self):
        for p in self.players:
            p.endRound()
        
        self.fullMoon = False

    def endGame(self):
        self.orderPlayers()
        for p in self.players:
            p.endGame(players)
        self.orderPlayers()

    # Choices
    def makeChoice(self, chooserId, choiceId):
        chooser = self.playersDict[chooserId]
        choice = self.playersDict[choiceId]
        chooser.choice = choice

    def afterChoice(self):
        self.checkMatches()
        self.orderPlayers()
        self.revealFirstPlace()
        self.endRound()

    # Score Strings
    def strPositions(self):
        return str([p.emoji for p in self.players])

    def strScores(self):
        return str([str(p.playerId) + " " + p.emoji + " " + str(p.showScore()) for p in self.players])

    # Object Management
    def deletePlayers(self):
        for p in self.players:
            del p
        for p in self.inactiveMonsters:
            del p
        
    # Start Game

    #*Start Round
    # ~Send Messages~
    # !!Make Choice!!
    # Check Matches and Score
    # Before Order Action
    # Order Players
    # Reveal Winning Player
    # End Round Actions
    # Goto *

    # Reveal All
    # End Game Actions

class Player:
    def __init__(self):
        self.name = "Name"
        self.playerId = None
        self.gameState = None
        self.playerName = "Anonymous"

        # Score Variables
        self.hearts = 0

        # Position Variables
        self.revealed = False
        self.position = 0

        # Monster Variables
        self.witch_Hair = False
        self.vampire_Thrall = None
        self.puppet_MatchLastTurn = True
        self.puppet_RejLastTurn = False

        self.twoFaced_Rej = False
        self.leprechaun_fakeHearts = 0
        self.leprechaun_olderPosition = 0
        self.zombie_Virus = None
        self.spirit_rejected = False
        self.mummy_Curse = None
        self.ogWerewolf = False
        self.wolf_alert = False

        # Round Variables
        self.choice = None

    # Match Actions
    def match(self, matchedBy):
        self.score()
        self.passCurses(matchedBy)
        self.puppet_MatchLastTurn = True
    
    def rejected(self, rejectedBy):
        self.puppet_MatchLastTurn = False
        self.spirit_rejected = True

    def rejects(self, rejecting):
        pass

    # Score Actions
    def score(self):
        self.hearts += 2

    def showScore(self):
        return self.hearts + self.leprechaun_fakeHearts

    def showMyScore(self):
        return self.showScore()

    # Round Time actions
    def startGame(self):
        pass

    def startRound(self):
        pass

    def beforeOrder(self):
        pass

    def reveal(self):
        self.revealed = True

    def endRound(self):
        self.puppet_RejLastTurn = not self.puppet_MatchLastTurn
        self.spirit_rejected = False
        self.choice = None

    def endGame(self):
        self.reveal()
        self.gameState.orderPlayers()

    def changePosition(self, pos):
        self.leprechaun_olderPosition = self.position
        self.position = pos

    def passCurses(self, matchedBy):
        curses = ["vampire_Thrall", "zombie_Virus", "mummy_Curse"]
        for curse in curses:
            if self.__dict__[curse]:
                matchedBy.__dict__[curse] = self.__dict__[curse]
                self.__dict__[curse].victims.add(matchedBy)

    def gameInfo(self):
        string = str(self.playerName) + "\n"
        string += "I am the " + self.name + " " + self.emoji + self.emoji + self.emoji + "\n"
        string += self.description + "\n"
        string += self.extraInfo() + "\n"
        string += "My identity was revealed!\n" if self.revealed else ""
        string += "Positions\n"
        string +=  self.gameState.strPositions()
        string += "\nScore\n"

        if self.showMyScore() < 0:
            string += str([u"\U0001F494" for _ in range(-(self.showMyScore()))])
        else:
            string += str([u"\U0001F5A4" for _ in range(self.showMyScore())])

        string += "\n"
        
        for p in self.gameState.players:
            if self != p and p.revealed:
                string += str(p.playerName) + " is the " + p.name + " " + p.emoji + p.emoji + p.emoji
                string += '\n'
                string += p.alert(self)
                string += '\n'
        
        return string

    def alert(self):
        return str("This is just a Human, what is he doing here?")

    def extraInfo(self):
        return ""

    def buildChoiceMenu(self):
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        buttonList = []

        for p in self.gameState.players:
            if p != self:
                buttonList.append(InlineKeyboardButton(
                    p.playerName, callback_data=p.playerId))

        reply_markup = InlineKeyboardMarkup(build_menu(buttonList,
                                                n_cols=3))

        return reply_markup

class Witch(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Witch"
        self.description = "The Witch takes a hair from each new player they date.\n\n" + \
            "When revealed, the Witch receives two bonus hearts for every hair collected."
        self.emoji = u"\U0001F9D9"
        self.hairsPlucked = 0
        self.victims = set([])

    def match(self, matchedBy):
        if not self.revealed and not matchedBy.witch_Hair:
            matchedBy.witch_Hair = True
            self.hairsPlucked += 2
            self.victims.add(matchedBy)
        
        super().match(matchedBy)

    def reveal(self):
        self.hearts = self.hearts + self.hairsPlucked 
        super().reveal()

    def alert(self, other):
        if other.witch_Hair:
            return "The Witch plucked a hair from you! She got two extra hearts from the evil potions she made!"
        else:
            return "Now that you know she will not be able to take a hair from your head now!"

    def extraInfo(self):
        return "You plucked the hair of " + " ".join([str(v.playerName) for v in self.victims])

class Vampire(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Vampire"
        self.description = "Everyone the Vampire dates becomes a vampire thrall. And then do so the people they date!\n\n" + \
            "At the end, the Vampire collects one heart from every vampire thrall."
        self.emoji = u"\U0001F9DB"
        self.vampire_Thrall = self
        self.victims = set([self])

    def endGame(self):
        self.vampire_Thrall = False
        for p in self.gameState.players:
            if p.vampire_Thrall:
                self.hearts += 1
        
        super().endGame()

    def alert(self, other):
        if other.vampire_Thrall:
            return ("You are his Vampire Thrall! Everybody you date will also become a vampire, and will give him an extra heart!")
        else:
            return ("Every vampire will give him an extra heart. And everybody he, or other vampire, will become a vampire, Beware!")

    def extraInfo(self):
        return " ".join([str(v.playerName) for v in self.victims]) + " are Vampire Thralls."

class Puppet(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Ventriloquist Puppet"
        self.description = "Sad people love puppets\n" + \
            "\nThe puppet gets two bonus heart every time they date someone that was rejected the night before."
        self.emoji = u"\U0001F921"

    def match(self, matchedBy):
        if matchedBy.puppet_RejLastTurn:
            self.score()
        
        super().match(matchedBy)

    def alert(self, other):
        return ("This creepy puppet wants to suck the sadness out of you! If you were rejected recently, you better date someone else.")

class TwoFaced(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Two Faced Creep"
        self.description = "The Two Faced Creep obtains two extra hearts for every player they reject...\n" + \
            "\nBut ONLY on nights they successfully get a date."
        self.emoji = u"\U0001F3AD"
        self.matchedThisTurn = False

    def match(self, matchedBy):
        super().match(matchedBy)
        self.matchedThisTurn = True

    def beforeOrder(self):
        if self.matchedThisTurn:
            for p in self.gameState.players:
                if p.twoFaced_Rej:
                    p.twoFaced_Rej = False
                    self.score()

        self.matchedThisTurn = False
        super().endRound()

    def rejects(self, rejecting):
        rejecting.twoFaced_Rej = True
        super().rejects(rejecting)

    def alert(self, other):
        return "The Two Faced Creep lives for betrayal! If he says he's gonna date you, take it with a grain of salt."

class Leprechaun(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Leprechaun"
        self.description = "Everyone who dates an unrevealed Leprechaun gets 2 hearts and 2 fake hearts.\n" + \
            "\nWhen the Leprechaun is revealed all fake hearts disappear. At this moment, leprechauns get 2 bonus hearts for every player that drops in the rankings"
        self.emoji = u"\U0001F340"
        self.revealedThisRound = False
    
    def match(self, matchedBy):
        if not self.revealed:
            matchedBy.leprechaun_fakeHearts += 2

        super().match(matchedBy)

    def reveal(self):
        self.revealedThisRound = True
        super().reveal()

    def endRound(self):
        self.leprechaunSteal()
        super().endRound()
    
    def endGame(self):
        super().endGame()
        self.leprechaunSteal()
        self.gameState.orderPlayers()

    def leprechaunSteal(self):
        if self.revealedThisRound:
            for p in self.gameState.players:
                p.leprechaun_fakeHearts = 0
            
            self.leprechaunOrderPlayers()
            for p in self.gameState.players:
                if p.leprechaun_olderPosition < p.position:
                    self.score()
        
        self.revealedThisRound = False
    
    def leprechaunOrderPlayers(self):
        for p in self.gameState.players:
            p.leprechaun_olderPosition = p.position

        self.gameState.orderPlayers() 

    def alert(self, other):
        return "The Leprechaun love is not as real as it seems! If you dated him, your score might have gone down. Now that you catch him, he can't lie to you anymore."

class MonsterHunter(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Monster Hunter"
        self.description = "At the end of the game the Monster Hunter gets 2 bonus hearts for every time they date the monster they've secretly been told to hunt."
        self.emoji = u"\U0001F52B"
        self.toHunt = None
        self.hunts = 0
        self.huntedThisRound = False

    def match(self, matchedBy):
        super().match(matchedBy)
        if self.toHunt.name == matchedBy.name:
            self.hunts += 2
            self.huntedThisRound = True

    def startGame(self):
        self.toHunt = choice(self.gameState.players)
        super().startGame()

    def endRound(self):
        if self.huntedThisRound:
            self.toHunt = choice(self.gameState.players)
            self.huntedThisRound = False
        super().endRound()
    
    def endGame(self):
        self.hearts += self.hunts
        super().endGame()

    def alert(self, other):
        return "The Monster Hunter lives for the hunt alone. He wants to catch the " + self.toHunt.name + " " + self.toHunt.emoji + "!"

    def extraInfo(self):
        return self.toHunt.name + " " + self.toHunt.emoji + " is your hunt objective. CATCH IT!"

class Alien(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Alien"
        self.description = "The Alien needs to conduct lengthy experiments on many terrestrials. \n\nEvery time the Alien successfully dates 3 new players its heart tally doubles"
        self.emoji = u"\U0001F47D"
        self.abducted = []
    
    def match(self, matchedBy):
        super().match(matchedBy)

        if not matchedBy in self.abducted:
            self.abducted.append(matchedBy)
            if len(self.abducted) == 3:
                self.hearts *= 2
                self.abducted = []

    def alert(self, other):
        return "The alien wants your vital organs for his collections! The more monsters he dates, the more hearts he gains!"

    def extraInfo(self):
        return "You have abducted " + " ".join([str(v.playerName) for v in self.abducted]) + " so far."

class Zombie(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Zombie"
        self.description = "Everyone the Zombie dates becomes an infected zobie. And then do so the people they date!\n\n" + \
            "At the end, if EVERYONE has been infected, it's the end of the world and only the original zombie wins."
        self.emoji = u"\U0001F9DF"
        self.zombie_Virus = self
        self.victims = set([self])
    
    def endGame(self):
        if all([p.zombie_Virus for p in self.gameState.players]):
            self.hearts = 999
        super().endGame()

    def alert(self, other):
        if other.zombie_Virus:
            return "He's the Patient Zero! He wants to infect every single monster, and you are helping him, stop that!"
        else:
            return "He's the Patient Zero! He wants to infect every single monster, Zombieism is rampant!"

    def extraInfo(self):
        return " ".join([str(v.playerName) for v in self.victims]) + " are Zombies."

class SerialKiller(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Serial Killer"
        self.description = "The Serial Killer steals 4 hearts from a player the second time they date each other."
        self.emoji = u"\U0001F52A"
        self.marks = []
        self.kills = []
    
    def match(self, matchedBy):
        super().match(matchedBy)
        if not matchedBy in self.marks:
            self.marks.append(matchedBy)
        elif matchedBy in self.marks and not matchedBy in self.kills:
            self.kills.append(matchedBy)
            self.hearts += 4
            matchedBy.hearts -= 4   

    def alert(self, other):
        if other in self.kills:
            return "He might have taken some hearts from you in the second date you had with this monster (4 to be exact)!"
        elif other in self.marks:
            return "He has you in his sights! Don't be surprised if after the next date you have less hearts than when you started."
        else:
            return "This guy is not to be trusted! Two dates will be enough for him to extract all your innards."       

    def extraInfo(self):
        marks = " ".join([str(v.playerName) for v in self.marks]) + " are your marks. Another date and you'll get those hearts!" if self.marks != [] else "No marks so far."
        kills = " ".join([str(v.playerName) for v in self.kills]) + " are crying for the hearts you took from them." if self.kills != [] else "No kills so far."

        return marks + "\n" + kills

class VengefulSpirit(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Vengeful Spirit"
        self.description = "The Vengeful Spirit is haunting its former lover. They receive two bonus hearts every night its former lover does NOT get a date."
        self.emoji = u"\U0001F47B"
        self.lover = None

    def startGame(self):
        players = self.gameState.players.copy()
        players.remove(self)
        self.lover = choice(players)
        super().startGame()

    def beforeOrder(self):
        if self.lover.spirit_rejected:
            self.score()

    def alert(self, other):
        if other == self.lover:
            return "This Spirit was your former lover! He wants you to suffer! (Which means, to get rejected)"
        else:
            return "This Spirit was " + str(self.lover.playerName) + "'s former lover!"

    def extraInfo(self):
        return str(self.lover.playerName) + " is your former lover. Make him suffer!"

class Invisible(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Invisible Person"
        self.description = "The Invisible Person score is invisible so they always appear to be in last place. Also it starts with four bonus hearts."
        self.emoji = u"\U0001F576"
        self.hearts = 4
        self.fakeScore = -10

    def showScore(self):
        return self.fakeScore

    def showMyScore(self):
        return self.hearts + self.leprechaun_fakeHearts

    def endGame(self, player):
        self.fakeScore = self.hearts
        super().endGame(player)

    def alert(self, other):
        return "I think is right there, is it?"

class Werewolf(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Werewolf"
        self.description = "The Werewolves get two bonus heart when dating on a FULL MOON and then turn their date into a Werewolf! (Stops being whatever monster it used to be).\n" + \
            "\nIf a werewolf is rejected on a full moon, they lose one heart."
        self.emoji = u"\U0001F43A"
        self.ogWerewolf = True
    
    def match(self, matchedBy):
        super().match(matchedBy)

        if self.gameState.fullMoon and not matchedBy.ogWerewolf:
            self.score()
            matchedBy.__class__ = Werewolf
            matchedBy.name = self.name
            matchedBy.description = self.description
            matchedBy.emoji = u"\U0001F415"
            matchedBy.ogWerewolf = False
            matchedBy.wolf_alert = True
        elif self.gameState.fullMoon:
            self.score()

    def rejected(self, rejectedBy):
        super().rejected(rejectedBy)
        if self.gameState.fullMoon:
            self.hearts -= 1
    
    def alert(self, other):
        if other.wolf_alert:
            return "AWOOOOOOOOOH!!"
        else:
            return "It might be a little too much to date a Werewolf during the full moon, unless you want to be one yourself!"

class BodySwapper(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Body Swapper"
        self.description = "On a FULL MOON, the Body Swapper will swap hearts (all of them) with the person they successfully date."
        self.emoji = u"\U0001F41B"
    
    def match(self, matchedBy):
        super().match(matchedBy)

        if self.gameState.fullMoon:
            self.hearts, matchedBy.hearts = matchedBy.hearts, self.hearts
            self.leprechaun_fakeHearts, matchedBy.leprechaun_fakeHearts = matchedBy.leprechaun_fakeHearts, self.leprechaun_fakeHearts
            self.emoji = u"\U0001F98B"
    
    def alert(self, other):
        return "This thing is a body swapper! In the full moon it will replace the hearts of its date with its own."
    
class Mummy(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Mummy"
        self.description = "Everyone the Mummy dates becomes cursed. Then so do the players they date. \n\n" + \
            "At the end, the Mummy steals a heart from every cursed player. But if EVERYONE has been cursed then the curse is lifted and no hearts are stolen."
        self.emoji = u"\U00002625"
        self.mummy_Curse = self
        self.victims = set([self])

    def endGame(self):
        if any([not p.mummy_Curse for p in self.gameState.players]):
            for p in self.gameState.players:
                if p.mummy_Curse:
                    p.hearts -= 1
                    self.hearts += 1

        super().endGame()

    def alert(self, other):
        if other.mummy_Curse:
            return "You have the Mummy Curse! The Mummy will steal a heart from you at the end, unless EVERYBODY is cursed! The curse is passed by dating, of course."
        else:
            return "There's a Mummy Curse around! If you date somebody with the Mummy Curse, you'll be cursed too and the Mummy will steal a heart from you! Unless EVERYBODY is cursed!"
    
    def extraInfo(self):
        return " ".join([str(v.playerName) for v in self.victims]) + " are Cursed."

class Frankenstein(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Frankenstein Monster"
        self.description = "Frankenstein's Monster has always been misunderstood, he only wanted to give love. \n" + \
            "\nEveryone who dates Frankenstein's Monster has a SMALL CHANCE of getting two bonus hearts. Frankie's Monster might get two bonus hearts randomly too, but the chance is higher."
        self.emoji = u"\U000026A1"

    def match(self, matchedBy):
        super().match(matchedBy)
        r = random()

        if r >= 0.20:
            self.hearts += 2
        if r >= 0.80:
            matchedBy.hearts += 2

    def alert(self, other):
        return "Frankenstein's Monster only wants to be loved. You might also be rewarded if you can look past its monstrous everythings."

def makeBulkChoice(game, choices):
    for (c, t) in choices:
        game.makeChoice(c, t)

# build button list from keyboard buttons
def build_menu(buttons, n_cols,
               header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.insert(footer_buttons)
    return menu


if __name__ == "__main__":
    game = Game([1,2,3,4,5,6,7,8])
    game.assignMonsters()
    game.startGame()

    game.startRound()
    print("ROUND: ", game.turn)
    print("Full Moon", game.fullMoon)
    choices = [(1,2), (2,4), (4,3), (3,5), (5,3), (6,2), (7,8), (8,7)]
    makeBulkChoice(game, choices)
    game.afterChoice()
    for p in game.players:
        print(p.gameInfo())
        print()
    
    game.startRound()
    print("ROUND: ", game.turn)
    print("Full Moon", game.fullMoon)
    choices = [(1, 2), (2, 4), (4, 3), (3, 5), (5, 3), (6, 2), (7, 8), (8, 7)]
    makeBulkChoice(game, choices)
    game.afterChoice()
    for p in game.players:
        print(p.gameInfo())
        print()
