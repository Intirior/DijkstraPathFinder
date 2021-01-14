# press space once you finish drawing the blocks and then comes the green block and afterwords press on next block without press space to draw the red block
from GeneralSettings import *
from GeneralSettings import nodeCounter,counter2,run

def drawBlocks():
    for block in Blocks:
        pygame.draw.rect(win, (175, 175, 175), (block[0], block[1], RectSize, RectSize))

    for start in begining:
        pygame.draw.rect(win, (0, 255, 0), (start[0], start[1], RectSize, RectSize))

    for end in ending:
        pygame.draw.rect(win, (0, 0, 255), (end[0], end[1], RectSize, RectSize))

# blits on each block the distance between him and the start point (optional)(blit numbers on blocks)
def drawNumber(node):
    '''text = font.render(f"{node[0]}", True, (0, 0, 0))
    win.blit(text, (node[1][0] + 5, node[1][1] + 5))'''

def drawNet():
    [pygame.draw.line(win, (255, 255, 255), (x, 0), (x, WINSIZE[1])) for x in range(int(WINSIZE[0])) if x % RectSize == 0 and x > 0]
    [pygame.draw.line(win, (255, 255, 255), (0, y), (WINSIZE[0], y)) for y in range(int(WINSIZE[1])) if y % RectSize == 0 and y > 0]

def DeadEnd(currentNode, start):
    global NoPath
    if len(currentNode) == 0 and start:
        NoPath = True

def BackTracking(animationPath):
    global WalkList
    # here you can see how the algorithm back tracking the shortes path
    pygame.draw.rect(win, (255, 0, 255), (animationPath[WalkList][0], animationPath[WalkList][1], RectSize, RectSize))
    WalkList += 1
    pygame.time.delay(10)


# adds all the squares on board to the AllBlocks list
for i in [i2 for i2 in range(WINSIZE[0]) if i2 % RectSize == 0]:
    for i3 in [i4 for i4 in range(WINSIZE[0]) if i4 % RectSize == 0]:
        AllBlocks.append((i, i3))

while run:
    Clock.tick(40)
    leftClick = pygame.mouse.get_pressed()[0]
    middleClick = pygame.mouse.get_pressed()[1]

    mouseRect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                BlockType += 1
            if event.key == pygame.K_ESCAPE:
                quit()

        for rect in AllBlocks:
            RectForm = pygame.Rect(rect, (RectSize, RectSize))
            if BlockType == 0:
                if leftClick:
                    if mouseRect.colliderect(RectForm) and (RectForm.x, RectForm.y) not in Blocks:
                        Blocks.append((RectForm.x, RectForm.y))
                if middleClick:
                    if mouseRect.colliderect(RectForm) and (RectForm.x, RectForm.y) in Blocks and middleClick:
                        Blocks.remove((RectForm.x, RectForm.y))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if BlockType == 1 and temporaryVar[0]==0:
                    if mouseRect.colliderect(RectForm) and (RectForm.x, RectForm.y) not in Blocks:
                        begining.append((RectForm.x, RectForm.y))
                        currentNode.append((RectForm.x, RectForm.y))
                        check = True
                        temporaryVar[0] += 1

                if BlockType == 2 and temporaryVar[1]==0:
                    if mouseRect.colliderect(RectForm) and (RectForm.x, RectForm.y) not in Blocks and (RectForm.x, RectForm.y) not in begining:
                        ending.append((RectForm.x, RectForm.y))
                        shortesPath.append((RectForm.x, RectForm.y))
                        for num in AllBlocks:
                            if num not in Blocks:
                                unexploredset.append(num)
                        temporaryVar[1] += 1

    win.fill((0, 0, 0))

    #drawNet()

    DeadEnd(currentNode, check)

    if BlockType >= 3:
        G += 1
        for i in range(counter2):
            node = currentNode[i]
            if (node[0]+RectSize,node[1]) in unexploredset:
                currentNode.append((node[0]+RectSize,node[1]))
                unexploredset.remove((node[0]+RectSize,node[1]))
                nodeCounter += 1
            if (node[0]-RectSize,node[1]) in unexploredset:
                currentNode.append((node[0]-RectSize,node[1]))
                unexploredset.remove((node[0] - RectSize, node[1]))
                nodeCounter += 1
            if (node[0],node[1]+RectSize) in unexploredset:
                currentNode.append((node[0],node[1]+RectSize))
                unexploredset.remove((node[0] , node[1]+ RectSize))
                nodeCounter += 1
            if (node[0],node[1]-RectSize) in unexploredset:
                currentNode.append((node[0],node[1]-RectSize))
                unexploredset.remove((node[0], node[1] - RectSize))
                nodeCounter += 1

        for i in range(len(currentNode)-nodeCounter):
            closeSet.append((G,currentNode.pop(0)))
        counter2 = nodeCounter
        nodeCounter = 0

        # here we color the nodes that are spreading
        for node in closeSet:
            if (node[1][0],node[1][1]) in ending:
                #print(Blocks)
                run = False
            pygame.draw.rect(win,(170,10,69),(node[1][0],node[1][1],RectSize,RectSize)) # draw the spread red blocks
            drawNumber(node)
    drawBlocks()

    if NoPath:
        text = font2.render("Dead End ",True , (255,255,255))
        win.blit(text,(WINSIZE[0]//4,WINSIZE[1]//2))

    # draw the current nodes in green
    if G>0:
        for i in currentNode:
            pygame.draw.rect(win, (0,255,0), (i[0], i[1], RectSize*2, RectSize*2))

    drawNet()

    pygame.display.update()


while not found:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()


    for node in reversed(closeSet):
        # we check by adding to the current node in the close list  the rect size  and the value in shortesPath is the previous/current node to what we add to the node
        if (node[1][0]+RectSize,node[1][1]) == shortesPath[-1] or(node[1][0], node[1][1] + RectSize)== shortesPath[-1] or(node[1][0], node[1][1] - RectSize)== shortesPath[-1] or (node[1][0] - RectSize, node[1][1]) == shortesPath[-1]:
            shortesPath[0] = (node[1][0], node[1][1])
            animationPath.append((node[1][0], node[1][1]))
            #pygame.draw.rect(win, (255, 0, 255), (node[1][0], node[1][1], RectSize, RectSize)) # draw the shortes path
        if node[1] in begining:
            StartSavePro = True

        drawNumber(node)

    BackTracking(animationPath)


    drawBlocks()

    drawNet()

    pygame.display.update()