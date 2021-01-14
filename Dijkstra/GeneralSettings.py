import pygame
pygame.init()

WINSIZE = 800, 800 # window size

RectSize =20 # the size of each square
assert 800 % RectSize == 0, "check the value of RectSize line 6"

win = pygame.display.set_mode(WINSIZE)

Blocks = []  # list which will contain all the block barriers

# -------------
begining = [] # will contain the start node

ending = [] # will contain the target node

shortesPath = [] # list contain the current node of the shortes path

AllBlocks = []# list that will contain all the squares on the board

BlockType = 0 # this will determine which block the user is currently adding to the screen

currentNode = []# the current nodes the algorithem explores

unexploredset = [] # all the blocks on the matrix without the barrier(gray) blocks that the algorithem did not explore yet

closeSet = []#  the blocks that the algorithem has already explored

temporaryVar = [0,0]

G = 0

font = pygame.font.SysFont("Ariel", 20)
font2 = pygame.font.SysFont("Ariel", 100)

nodeCounter = 0
counter2 = 1 # copy of nodeCounter

Clock = pygame.time.Clock()

run = True
found = False

check = False # connected to the DeadEnd function
NoPath = False # connected to the DeadEnd function

WalkList = 0 # go through the list with the path between end to beginning node
animationPath = [] # here is the path


