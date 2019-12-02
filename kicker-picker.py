import math
import random

class BreakIt(Exception): pass

class PlayerPool(list):
    def next(self, p):
        index = p.id
        if index >= len(self):
            index = 0
        return self[index]

class Player:
    counter = 1

    def __init__(self, name: str):
        self.name = name
        self.id = Player.counter

        Player.counter += 1

class Team:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __eq__(self, other):
        return math.fabs(self.p1.id - self.p2.id) == math.fabs(other.p1.id - self.p2.id)
        # return (self.p1.id - self.p2.id == other.p1.id - self.p2.id) \
        #        or (self.p1.id - self.p2.id == other.p2.id - self.p1.id)
        # return (self.p1.id == other.p1.id and self.p2.id == other.p2.id) \
        #        or (self.p1.id == other.p2.id and self.p2.id == other.p1.id)

    def determinant(self, pool: PlayerPool):
        teamDet = math.fabs(self.p1.id - self.p2.id)
        poolDet = math.fabs(len(pool) - teamDet)
        return min(teamDet, poolDet)

class TeamMemory(list):

    def __init__(self, pool: PlayerPool):
        self.pool = pool

    def isUnique(self, team: Team):
        det = team.determinant(pool)
        for t in self:
            if t.determinant(pool) == det:
                return False
            # if team == t:
            #     return False
        return True

    def areUnique(self, team1: Team, team2: Team):
        if team1.determinant(pool) == team2.determinant(pool):
            return False
        return True

def format(p: Player) -> str:
    return '({:}) {:}'.format(p.id, p.name)

def printPlayers(p1, p2, p3, p4):
    print('{:{width}} + {:{width}}  vs  {:{width}} + {:{width}} '
          .format(format(p1), format(p2), format(p3), format(p4), width=24))

pool = PlayerPool()
pool.append(Player("Klaudia Zalewska"))
pool.append(Player("Natalia Zuchowska"))
pool.append(Player("Przemysław Olszewski"))
pool.append(Player("Mateusz Belwon"))
pool.append(Player("Paweł Janik"))
pool.append(Player("Mariusz Raczyk"))
pool.append(Player("Jakub Grzegorzyk"))
pool.append(Player("Dawid Zieliński"))
pool.append(Player("Michał Popielski"))
pool.append(Player("Grzegorz Konupek"))
pool.append(Player("Jakub Sengerski"))

loopCount = len(pool)
# if loopCount % 2 != 0:
#     loopCount = 2 * loopCount

shuffled = pool.copy()
random.seed(42)

z = 0;
loopError = False

memory = TeamMemory(pool)
try:
    for i in range(2):  # X cycles
        while True:
            random.shuffle(shuffled)
            p1 = shuffled[0]
            p2 = shuffled[1]
            p3 = shuffled[2]
            p4 = shuffled[3]
            team1 = Team(p1, p2)
            team2 = Team(p3, p4)
            unique = memory.areUnique(team1, team2) \
                     and memory.isUnique(team1) \
                     and memory.isUnique(team2)
            if unique:
                break
            else:
                print('Powtórnie wybrane teamy, losuje jeszcze raz:')
                printPlayers(p1, p2, p3, p4)
            z += 1
            if z > 10000:
                raise BreakIt
            loopError = z > 1000
        memory.append(team1)
        memory.append(team2)

        print('Round {} (det1:{}, det2:{}) '.format(i + 1, team1.determinant(pool), team2.determinant(pool)))
        for j in range(loopCount):  # one cycle
            printPlayers(p1, p2, p3, p4)
            p1 = pool.next(p1)
            p2 = pool.next(p2)
            p3 = pool.next(p3)
            p4 = pool.next(p4)
except BreakIt:
    print('popsuło się (z: {})'.format(z))
