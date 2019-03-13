from random import choice, random

class Player:
    def __init__(self):
        self.name = "Name"

        # Score Variables
        self.hearts = 0

        # Position Variables
        self.revealed = False
        self.position = 0

        # Monster Variables
        self.witch_Hair = False
        self.vampire_Thrall = False
        self.puppet_MatchLastTurn = True
        self.puppet_RejLastTurn = False

        self.twoFaced_Rej = False
        self.leprechaun_fakeHearts = 0
        self.leprechaun_olderPosition = 0
        self.zombie_Virus = False
        self.spirit_rejected = False
        self.mummy_Curse = False
        self.fullMoon = False
        self.ogWerewolf = False

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
        self.hearts += 1
    

    def showScore(self):
        return self.hearts + self.leprechaun_fakeHearts


    def showMyScore(self):
        return showScore()


    # Round Time actions
    def startGame(self, players):
        pass


    def startRound(self, players, fullMoon):
        self.fullMoon = fullMoon


    def beforeOrder(self, players):
        pass


    def reveal(self):
        self.revealed = True


    def endRound(self, players):
        self.puppet_RejLastTurn = not self.puppet_MatchLastTurn
        self.spirit_rejected = False
        self.choice = None


    def endGame(self, players):
        self.reveal()
        orderPlayers(players)


    def changePosition(self, pos):
        self.leprechaun_olderPosition = self.position
        self.position = pos


    def passCurses(self, matchedBy):
        curses = ["vampire_Thrall", "zombie_Virus", "mummy_Curse"]
        for curse in curses:
            if self.__dict__[curse]:
                matchedBy.__dict__[curse] = True


class Witch(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Witch"
        self.description = "The Witch takes a hair from each new player they date.\n" + \
            "When revealed, the Witch receives one bonus heart for every hair collected."
        self.emoji = u"\U0001F9D9"
        self.hairsPlucked = 0


    def match(self, matchedBy):
        if not self.revealed and not matchedBy.witch_Hair:
            matchedBy.witch_Hair = True
            self.hairsPlucked += 1
        
        super().match(matchedBy)


    def reveal(self):
        self.hearts = self.hearts + self.hairsPlucked 
        super().reveal()


class Vampire(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Vampire"
        self.description = "Everyone the Vampire dates becomes a vampire thrall. And then do so the people they date!\n" + \
            "At the end, the Vampire collects half a heart from every vampire thrall."
        self.emoji = u"\U0001F9DB"
        self.vampire_Thrall = True

    def endGame(self, players):
        self.vampire_Thrall = False
        for p in players:
            if p.vampire_Thrall:
                self.hearts += 0.5
        
        super().endGame(players)


class Puppet(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Ventriloquist Puppet"
        self.description = "Sad people love puppets\n" + \
            "The puppet gets a bonus heart every time they date someone that was rejected the night before."
        self.emoji = u"\U0001F921"


    def match(self, matchedBy):
        if matchedBy.puppet_RejLastTurn:
            self.score()
        
        super().match(matchedBy)


class TwoFaced(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Two Faced Creep"
        self.description = "The Two Faced Creep obtains an extra heart for every player they reject...\n" + \
            "But ONLY on nights they successfully get a date."
        self.emoji = u"\U0001F3AD"
        self.matchedThisTurn = False


    def match(self, matchedBy):
        super().match(matchedBy)
        self.matchedThisTurn = True


    def beforeOrder(self, players):
        if self.matchedThisTurn:
            for p in players:
                if p.twoFaced_Rej:
                    p.twoFaced_Rej = False
                    self.score()


        self.matchedThisTurn = False
        super().endRound(players)


    def rejects(self, rejecting):
        rejecting.twoFaced_Rej = True
        super().rejects(rejecting)


class Leprechaun(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Leprechaun"
        self.description = "Everyone who dates an unrevealed Leprechaun gets 2 fake hearts.\n" + \
            "When the Leprechaun is revealed all fake hearts disappear. At this moment, leprechauns get 1 bonus heart for every player that drops in the rankings"
        self.emoji = u"\U0001F340"
        self.revealedThisRound = False
    

    def match(self, matchedBy):
        if not self.revealed:
            matchedBy.leprechaun_fakeHearts += 1

        super().match(matchedBy)


    def reveal(self):
        self.revealedThisRound = True
        super().reveal()


    def endRound(self, players):
        self.leprechaunSteal(players)
        super().endRound(players)
        
    
    def endGame(self, players):
        super().endGame(players)
        self.leprechaunSteal(players)
        orderPlayers(players)


    def leprechaunSteal(self, players):
        if self.revealedThisRound:
            for p in players:
                p.leprechaun_fakeHearts = 0
            
            self.leprechaunOrderPlayers(players)
            for p in players:
                if p.leprechaun_olderPosition < p.position:
                    self.score()
        
        self.revealedThisRound = False
    

    def leprechaunOrderPlayers(self, players):
        for p in players:
            p.leprechaun_olderPosition = p.position

        orderPlayers(players) 


class MonsterHunter(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Monster Hunter"
        self.description = "At the end of the game the Monster Hunter gets a bonus heart for every time they date the monster-type they've secretly been told to hunt."
        self.emoji = u"\U0001F52B"
        self.toHunt = None
        self.hunts = 0
        self.huntedThisRound = False


    def match(self, matchedBy):
        super().match(matchedBy)
        if self.toHunt.name == matchedBy.name:
            self.hunts += 1
            self.huntedThisRound = True


    def startGame(self, players):
        self.toHunt = choice(players)
        super().startGame(players)


    def endRound(self, players):
        if self.huntedThisRound:
            self.toHunt = choice(players)
            self.huntedThisRound = False
        super().endRound(players)
    

    def endGame(self, players):
        self.hearts += self.hunts
        super().endGame(players)


class Alien(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Alien"
        self.description = "The Alien needs to conduct lengthy experiments on many terrestrials. \nEvery time the Alien successfully dates 3 new players its heart tally doubles"
        self.emoji = u"\U0001F47D"
        self.abducted = []
    
    def match(self, matchedBy):
        super().match(matchedBy)

        if not matchedBy in self.abducted:
            self.abducted.append(matchedBy)
            if len(self.abducted) == 3:
                self.hearts *= 2
                self.abducted = []


class Zombie(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Zombie"
        self.description = "Everyone the Zombie dates becomes an infected zobie. And then do so the people they date!\n" + \
            "At the end, if EVERYONE has been infected, it's the end of the world and only the original zombie wins."
        self.emoji = u"\U0001F9DF"
        self.zombie_Virus = True
    
    def endGame(self, players):
        if all([p.zombie_Virus for p in players]):
            self.hearts = 999
        super().endGame(players)
            

class SerialKiller(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Serial Killer"
        self.description = "The Serial Killer steals 2 hearts from a player the second time they date each other"
        self.emoji = u"\U0001F52A"
        self.marks = []
        self.kills = []

    
    def match(self, matchedBy):
        super().match(matchedBy)
        if not matchedBy in self.marks:
            self.marks.append(matchedBy)
        elif matchedBy in self.marks and not matchedBy in self.kills:
            self.kills.append(matchedBy)
            self.hearts += 2
            matchedBy.hearts -= 2
            

class VengefulSpirit(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Vengeful Spirit"
        self.description = "The Vengeful Spirit is haunting its former lover. They receive a bonus heart every night its former lover does NOT get a date."
        self.emoji = u"\U0001F47B"
        self.lover = None


    def startGame(self, players):
        self.lover = choice(players)
        super().startGame(players)
    

    def beforeOrder(self, players):
        if self.lover.spirit_rejected:
            self.hearts += 1


class Invisible(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Invisible Person"
        self.description = "The Invisible Person score is invisible so they always appear to be in last place. Also it starts with two bonus hearts."
        self.emoji = u"\U0001F576"
        self.hearts = 2
        self.fakeScore = -10
    
    def showScore(self):
        return self.fakeScore


    def showMyScore(self):
        return self.hearts + self.leprechaun_fakeHearts

    def endGame(self, player):
        self.fakeScore = self.hearts
        super().endGame(player)
    

class Werewolf(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Werewolf"
        self.description = "The Werewolves get a bonus heart when dating on a FULL MOON and then turn their date into a Werewolf! (Stops being whatever monster it used to be).\n" + \
            "If a werewolf is rejected on a full moon, they lose half a heart."
        self.emoji = u"\U0001F43A"
        self.ogWerewolf = True
    
    def match(self, matchedBy):
        super().match(matchedBy)

        if self.fullMoon and not matchedBy.ogWerewolf:
            self.hearts += 1
            matchedBy.__class__ = Werewolf
            matchedBy.name = self.name
            matchedBy.description = self.description
            matchedBy.emoji = u"\U0001F415"
            matchedBy.ogWerewolf = False
        elif self.fullMoon:
            self.hearts += 1

    
    def rejected(self, rejectedBy):
        super().rejected(rejectedBy)
        self.hearts -= 0.5
    

class BodySwapper(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Body Swapper"
        self.description = "On a FULL MOON, the Body Swapper will swap hearts (all of them) with the person they successfully date."
        self.emoji = u"\U0001F41B"
    
    def match(self, matchedBy):
        super().match(matchedBy)

        if self.fullMoon:
            self.hearts, matchedBy.hearts = matchedBy.hearts, self.hearts
            self.leprechaun_fakeHearts, matchedBy.leprechaun_fakeHearts = matchedBy.leprechaun_fakeHearts, self.leprechaun_fakeHearts
            self.emoji = u"\U0001F98B"


class Mummy(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Mummy"
        self.description = "Everyone the Mummy dates becomes cursed. Then so do the players they date. \n" + \
            "At the end, the Mummy steals half a heart from every cursed player. But if EVERYONE has been cursed then the curse is lifted and no hearts are stolen."
        self.emoji = u"\U00002625"
        self.mummy_Curse = True

    def endGame(self, players):
        if any([not p.mummy_Curse for p in players]):
            for p in players:
                if p.mummy_Curse:
                    p.hearts -= 0.5
                    self.hearts += 0.5

        super().endGame(players)
    

class Frankenstein(Player):
    def __init__(self):
        Player.__init__(self)
        self.name = "Frankenstein Monster"
        self.description = "Frankenstein's Monster has always been misunderstood, he only wanted to give love. \n" + \
            "Everyone who dates Frankenstein's Monster has a SMALL CHANCE of getting a bonus heart. Frankie's Monster might get a bonus heart randomly too, but the chance is higher."
        self.emoji = u"\U000026A1"

    def match(self, matchedBy):
        super().match(matchedBy)
        r = random()

        if r >= 0.20:
            self.hearts += 1
        if r >= 0.80:
            matchedBy.hearts += 1
        
# Turn Phases

def startGame(players):
    for p in players:
        p.startGame(players)


def startRound(players, fullMoon = False):
    for p in players:
        p.startRound(players, fullMoon)


def checkMatches(playersCopy):
    if playersCopy == []:
        return

    chooser = playersCopy[0]
    choice = playersCopy[0].choice

    if choice == None:
        chooser.hearts -= 0.5
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
    
    checkMatches(playersCopy)


def orderPlayers(players):
    for p in players:
        p.beforeOrder(players)

    players.sort(key=lambda p: p.showScore(), reverse=True)
    pos = 1

    for p in players:
        p.changePosition(pos)
        pos += 1


def revealFirstPlace(players):
    for p in players:
        if not p.revealed:
            p.reveal()
            break


def endRound(players):
    for p in players:
        p.endRound(players)


def endGame(players):
    orderPlayers(players)
    for p in players:
        p.endGame(players)
    orderPlayers(players)


def runTurn(players, choices, fullMoon = False):
    startRound(players, fullMoon)

    for (p, c) in choices:
        p.choice = c 
    
    checkMatches(players.copy())
    orderPlayers(players)
    
    revealFirstPlace(players)
    endRound(players)
    for p in players:
        print(p.emoji, p.showScore())


# Start Game

#*Start Round
# ~Send Messages~
# Choose Partner
# Check Matches and Score
# Before Order Action
# Order Players
# Reveal Winning Player
# End Round Actions
# Goto *

# Reveal All
# End Game Actions

if __name__ == "__main__":

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

    players = [w, v, pp, t, l, m, a, z, s, vs, i, ww, b, mm, f]

    startGame(players)

    choices = [(a,mm), (mm,a)]
    runTurn(players, choices, False)
    print()
    choices = [(mm, v), (v, mm), (a, pp), (pp, a)]
    runTurn(players, choices, False)
    print()
    choices = [(mm, t), (t, mm), (l, pp), (pp, l), (v, w), (w, v), (m, a), (a, m)]
    runTurn(players, choices, False)
    print()
    choices = [(mm, s), (s, mm), (vs, pp), (pp, vs),
               (v, i), (i, v), (ww, a), (a, ww), (w, b), (b, w),
               (z, l), (l, z), (f, t), (t, f)]
    runTurn(players, choices, False)
    endGame(players)
    print()
    print()
    for p in players:
        print(p.emoji, p.hearts)
