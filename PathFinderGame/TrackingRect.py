import pygame,pygame_menu,json
from pygame import mouse

pygame.init()

WINSIZE = (840, 840) # window size

RectSize =35 # the size of each square

assert WINSIZE[0]%RectSize==0 and WINSIZE[1]%RectSize==0, " height/width does not divide equally by RectSize"

win = pygame.display.set_mode(WINSIZE)

BackGroundDecoration = pygame_menu.baseimage.BaseImage(image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_WALLPAPER, drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)

MyTheme = pygame_menu.themes.Theme(widget_font=pygame_menu.font.FONT_HELVETICA, background_color = BackGroundDecoration, title_background_color=(0, 0, 0), title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE, widget_font_color = (0, 0, 0))


menu = pygame_menu.Menu(height=WINSIZE[1], width=WINSIZE[0], title='Settings', theme=MyTheme)

Bg = pygame.transform.scale(pygame.image.load("MapImages/Bg.jpg"), WINSIZE)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Board:
    white = (255, 255, 255)
    black = (0,0,0)
    def __init__(self, width:int,height:int,win:pygame.Surface,RectSize:int):
        self.height = height
        self.width = width
        self.win = win
        self.RectSize = RectSize
        self.AllBlocks = self.__GetAllSquares()

    def DrawNet(self): # Drawing the net in on the board
        [pygame.draw.line(self.win, self.white, (x, 0), (x, self.height)) for x in range(int(self.width)) if x % self.RectSize == 0 and x > 0]
        [pygame.draw.line(self.win,self.white, (0, y), (self.width, y)) for y in range(int(self.height)) if y % self.RectSize == 0 and y > 0]

    def __GetAllSquares(self):
        l = []
        # adds all the squares on board to the AllBlocks list
        for i in [i2 for i2 in range(self.width) if i2 % self.RectSize == 0]:
            for i3 in [i4 for i4 in range(self.height) if i4 % self.RectSize == 0]:
                l.append((i, i3))
        return l

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class BlockManagement:
    gray = (100,100,100)

    def __init__(self,win:pygame.surface,RectSize:int,AllBlocks:list):
        self.win = win
        self.RectSize = RectSize
        self.vel = self.RectSize
        self.AllBlocks = AllBlocks
        self.BlockType = "gray"
        self.GrayBlocks = []
        self.BlockRect =[pygame.Rect(pos,(self.RectSize,self.RectSize)) for pos in AllBlocks]
        self.PlayerNode = (-100, -100)
        self.AlgoPlayerNode = (-100, -100)
        self.WalkByShortestPath = 0 # walk through the shortest path list
        self.PlayerNodeChangePos = False

    def __MouseClicks(self):
        self.LeftClick = mouse.get_pressed()[0]
        self.MidleClick = mouse.get_pressed()[1]
        self.RightClick = mouse.get_pressed()[2]
        self.MouseRect = pygame.Rect(mouse.get_pos(),(1,1))

    def DrawGrayBlocks(self):
        for pos in self.GrayBlocks:
            pygame.draw.rect(self.win,self.gray,(pos[0],pos[1],self.RectSize,self.RectSize))

    def EraseGrayBlocks(self):
        self.GrayBlocks.clear()

    def BlockListModify(self):
        self.__MouseClicks()
        for rect in self.BlockRect:
            if rect.colliderect(self.MouseRect):
                if self.BlockType == "gray":
                    if self.LeftClick and (rect.x, rect.y) not in self.GrayBlocks:
                        self.GrayBlocks.append((rect.x, rect.y))
                    if self.MidleClick and (rect.x, rect.y) in self.GrayBlocks or [rect.x, rect.y] in self.GrayBlocks:
                        self.GrayBlocks.remove((rect.x, rect.y))
                else:
                    if (rect.x, rect.y) not in self.GrayBlocks:
                        if self.LeftClick and (rect.x, rect.y) != self.AlgoPlayerNode:
                            self.PlayerNode = (rect.x, rect.y)
                            self.PlayerNodeChangePos = True
                        if self.RightClick and (rect.x, rect.y) != self.PlayerNode:
                            self.AlgoPlayerNode = (rect.x, rect.y)
                    # The Gray blocks list appending the gray blocks created while the playing
                    if (rect.x,rect.y) != self.AlgoPlayerNode and (rect.x, rect.y) != self.PlayerNode and self.MidleClick:
                        self.GrayBlocks.append((rect.x,rect.y))

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Dijkstra:
    purple = (147,112,219)
    red = (255,0,0)
    def __init__(self,win:pygame.surface,RectSize:int,AllBlocks:list):
        self.win = win
        self.RectSize = RectSize
        self.AllBlocks = AllBlocks
        self.unexploredSet = []
        self.CloseSet = []
        self.shortestPath = []
        self.CurrentNodes = [None]
        self.previousAlgoPlayerPos =(None, None)
        self.previousPlayerNodePos =(None, None)
        self.ShortestPathNode = None
        self.CurrentNodesAmount = len(self.CurrentNodes)
        self.NodeCounter = 0
        self.Found = 0
        self.WalkShortestList = 0  # walks through the shortest path list

    def SetVariablesValue(self, GrayBlockList:list, PlayerNode:tuple, AlgoPlayerNode:tuple):
        '''here i initialize variables'''
        self.__init__(self.win,self.RectSize,self.AllBlocks)
        self.previousAlgoPlayerPos = AlgoPlayerNode
        self.previousPlayerNodePos = PlayerNode
        self.shortestPath = [AlgoPlayerNode]
        self.CurrentNodes = [PlayerNode]
        for node in self.AllBlocks:
            if node not in GrayBlockList and node not in self.unexploredSet:
                self.unexploredSet.append(node)

    def Spread(self):
        for i in range(self.CurrentNodesAmount):
            node = self.CurrentNodes[i]
            if (node[0]+self.RectSize,node[1]) in self.unexploredSet:
                self.CurrentNodes.append((node[0]+self.RectSize,node[1]))
                self.unexploredSet.remove((node[0]+self.RectSize,node[1]))
                self.NodeCounter += 1
            if (node[0]-self.RectSize,node[1]) in self.unexploredSet:
                self.CurrentNodes.append((node[0]-self.RectSize,node[1]))
                self.unexploredSet.remove((node[0] - self.RectSize, node[1]))
                self.NodeCounter += 1
            if (node[0],node[1]+self.RectSize) in self.unexploredSet:
                self.CurrentNodes.append((node[0],node[1]+self.RectSize))
                self.unexploredSet.remove((node[0] , node[1]+ self.RectSize))
                self.NodeCounter += 1
            if (node[0],node[1]-self.RectSize) in self.unexploredSet:
                self.CurrentNodes.append((node[0],node[1]-self.RectSize))
                self.unexploredSet.remove((node[0], node[1] - self.RectSize))
                self.NodeCounter += 1

    def __CalBackTracing(self):
        for node in reversed(self.CloseSet):
            # we check by adding to the current node in the close list  the rect size  and the value in shortesPath is the previous/current node to what we add to the node
            if (node[0] + self.RectSize, node[1]) == self.shortestPath[-1] or (node[0], node[1] + self.RectSize) == self.shortestPath[-1] or (node[0], node[1] - self.RectSize) == self.shortestPath[-1] or (node[0] - self.RectSize, node[1]) == self.shortestPath[-1]:
                self.shortestPath.append((node[0], node[1]))

    def UpdateCloseSet(self, AlgoPlayerNode:tuple):
        for _ in range(len(self.CurrentNodes)-self.NodeCounter):
            if self.CurrentNodes[0] != AlgoPlayerNode:
                self.CloseSet.append(self.CurrentNodes.pop(0))
            else:
                if not self.Found:
                    self.__CalBackTracing()
                    self.Found+=1

        self.CurrentNodesAmount = self.NodeCounter
        self.NodeCounter = 0

    def MoveAfterPlayerNode(self):
        if len(self.shortestPath)>0:
            self.ShortestPathNode = self.shortestPath[self.WalkShortestList]
            self.WalkShortestList+=1
        if self.WalkShortestList>=len(self.shortestPath)-1:
            self.WalkShortestList = 0
        return self.shortestPath[self.WalkShortestList]

    def DrawAlgoNode(self, AlgoPos:tuple):
        pygame.draw.rect(self.win, self.red, (AlgoPos[0], AlgoPos[1], self.RectSize, self.RectSize))

    def DrawPath(self):
        for node in self.shortestPath:
            pygame.draw.rect(self.win,(0,0,0),(node[0],node[1],self.RectSize,self.RectSize))

    def DrawSpreading(self):
        for node in self.CloseSet:
            pygame.draw.rect(self.win,self.purple,(node[0],node[1],self.RectSize,self.RectSize))

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class MapManagement():
    imagePath = 'D:\PycharmProjects\DijkstraPathFinder\PathFinderGame\MapImages\GameImage.png'
    def __init__(self,win,menu):
        self.win = win
        self.menu = menu
        self.PossibleMapNum = []
        self.UploadedGrayBlocks = []
        self.MapList = {}
        self.currentMap = None
        self.MapNumSelector = None
        self.BiggestKey = None
        self.IsUploaded = False

    def __ReadFile(self):
        with open('MapDB.json', 'r') as f:
            return json.load(f)

    def __WriteToFile(self,info):
        with open('MapDB.json', 'w') as f:
            json.dump(info,f)

    def __StartGame(self, MapNumSelector, currentGrayBlocks:list):
        self.menu.disable()
        self.currentMap = MapNumSelector.get_value()[0]
        self.IsUploaded = True
        currentGrayBlocks.clear()
        self.UploadedGrayBlocks = self.__ReadFile()[self.currentMap]

    def __SavingMap(self, GrayBlocksList: list):
        self.MapList = self.__ReadFile()
        self.BiggestKey = max(list(self.MapList.keys()))
        self.MapList[f'{int(self.BiggestKey)+1}'] = GrayBlocksList
        self.__WriteToFile(self.MapList)
        self.menu.disable()

    def __RemoveMap(self,MapNum):
        self.currentMap = MapNum.get_value()[0]
        if self.currentMap != "1":
            self.MapList = self.__ReadFile()
            del self.MapList[self.currentMap]
            self.__WriteToFile({})
            self.__WriteToFile(self.MapList)
            self.menu.disable()

    def MenuSurface(self, GrayBlocksList:list):
         self.menu.clear()
         self.PossibleMapNum = [f"{i}" for i in self.__ReadFile()]
         self.menu.add_button(" Return To Game " , self.menu.disable,background_color = (100, 100, 100), font_color = 	(255,255,0), font_name ="arial")
         self.MapNumSelector = menu.add_selector(' map ', self.PossibleMapNum)
         self.menu.add_button(' Play ', self.__StartGame, self.MapNumSelector, GrayBlocksList, background_color = (100, 100, 100), font_color = (255, 0, 0), font_name ="arial")
         self.menu.add_button(' Quit ', pygame_menu.events.EXIT ,background_color = (100,100,100) ,font_color = (255,0,0) ,font_name = "arial")
         self.menu.add_button(" Save Map ", self.__SavingMap, GrayBlocksList, background_color = (100, 100, 100), font_color = (0, 255, 0), font_name ="arial")
         self.MapNumSelectorRemove = menu.add_selector(' select map to remove ', self.PossibleMapNum)
         self.menu.add_button(" Remove Map ", self.__RemoveMap, self.MapNumSelectorRemove)
         self.menu.mainloop(self.win)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class PlayerNodeClass:
    blue = (0,0,255)

    def __init__(self,RectSize:int , PlayerNode:tuple, win):
        self.RectSize = RectSize
        self.vel = RectSize
        self.pos = list(PlayerNode)
        self.win = win

    def SetPosToPlayerNode(self,PlayerNodePos:tuple):
        self.pos = list(PlayerNodePos)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and self.pos[0] < self.win.get_width() - self.RectSize:
            self.pos[0] += self.vel
        if keys[pygame.K_LEFT] and self.pos[0] > 0:
            self.pos[0] -= self.vel
        if keys[pygame.K_DOWN] and self.pos[1] < self.win.get_height() - self.RectSize:
            self.pos[1] += self.vel
        if keys[pygame.K_UP] and self.pos[1] > 0:
            self.pos[1] -= self.vel
        return tuple(self.pos)

    def DrawPlayerNode(self):
        pygame.draw.rect(self.win, self.blue,(self.pos[0], self.pos[1], self.RectSize, self.RectSize))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

menuScreen  = MapManagement(win=win, menu=menu)

board = Board(width = WINSIZE[0],height = WINSIZE[1],win = win,RectSize=RectSize)

startBlocks = BlockManagement(win = win, RectSize = RectSize, AllBlocks= board.AllBlocks)

dijkstra = Dijkstra(win = win, RectSize = RectSize, AllBlocks= board.AllBlocks)

player = PlayerNodeClass(RectSize = RectSize , PlayerNode = startBlocks.PlayerNode, win = win)

ConvertMap = [] # when i get the uploaded map it is a list with lists in side of it so i convert the lists to tuple

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

OneTimeRun = 0

InZone = False

while not InZone:
    menuScreen.IsUploaded = False
    startBlocks.PlayerNodeChangePos = False
    win.blit(Bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                startBlocks.BlockType = "other"
            if event.key == pygame.K_e:
                startBlocks.EraseGrayBlocks()
            if event.key == pygame.K_ESCAPE:
                menu.enable()

    if startBlocks.BlockType == "other" and startBlocks.PlayerNode != (-100, -100) and startBlocks.AlgoPlayerNode != (-100, -100):
        for _ in range(5000):
            if dijkstra.previousAlgoPlayerPos != startBlocks.AlgoPlayerNode or dijkstra.previousPlayerNodePos != startBlocks.PlayerNode:
                startBlocks.WalkByShortesPath = 0 # erase if you want to move your char
                OneTimeRun = 0
            if OneTimeRun == 0:
                dijkstra.SetVariablesValue(startBlocks.GrayBlocks, startBlocks.PlayerNode, AlgoPlayerNode=startBlocks.AlgoPlayerNode)
                OneTimeRun = 1
            dijkstra.Spread()
            dijkstra.UpdateCloseSet(startBlocks.AlgoPlayerNode)
            OneTimeRun = 1
        #dijkstra.DrawSpreading() # Draw the spreading of the nodes
        #dijkstra.DrawPath() # draw the path that the algo player following
        startBlocks.AlgoPlayerNode = dijkstra.MoveAfterPlayerNode()

    startBlocks.DrawGrayBlocks()
    startBlocks.BlockListModify()
    menuScreen.MenuSurface(startBlocks.GrayBlocks)
    dijkstra.DrawAlgoNode(startBlocks.AlgoPlayerNode)

    if menuScreen.IsUploaded:
        startBlocks.BlockType = 'gray' #if you want the algo start running only after pressing space when uploading new map
        for pos in menuScreen.UploadedGrayBlocks:
            ConvertMap.append(tuple(pos))
        startBlocks.GrayBlocks = ConvertMap

    if startBlocks.PlayerNodeChangePos:
        player.SetPosToPlayerNode(startBlocks.PlayerNode)

    startBlocks.PlayerNode = player.movement()
    player.DrawPlayerNode()

    pygame.display.update()
