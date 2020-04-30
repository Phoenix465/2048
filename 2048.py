# Library Imports
import pygame
from random import choice, random
from time import time


class Game2048:
    def __init__(self):
        # Initialising Components
        pygame.init()

        pygame.display.set_caption('2048')
        WindowIcon = pygame.image.load("2048.png")
        (self.screenWidth, self.screenHeight) = (450, 520)
        background_colour = (255, 255, 255)

        # Initial Settings - DON'T TOUCH
        self.windowScreen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.windowScreen.fill(background_colour)

        pygame.display.set_icon(WindowIcon)
        pygame.display.flip()

        # Game Settings
        self.addblock = False
        self.moveup = False
        self.movedown = False
        self.moveleft = False
        self.moveright = False
        self.reset = False

        self.squarewidth = 65

        self.score = 0
        try:
            self.best = int(open("best.txt", "r").read())
        except ValueError:
            self.best = 0
        self.bestfile = open("best.txt", "a")

        self.combinechanged = []

        self.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        self.gridColour = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 199),
            8: (242, 177, 122),
            16: (245, 149, 99),
            32: (255, 116, 85),
            64: (245, 95, 58),
            128: (237, 207, 115),
            256: (237, 204, 98),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 45),
        }

        self.gridTextColour = {
            0: (205, 193, 180),
            2: (119, 110, 101),
            4: (119, 110, 101),
            8: (249, 246, 242),
            16: (249, 246, 242),
            32: (249, 246, 242),
            64: (249, 246, 242),
            128: (249, 246, 242),
            256: (249, 246, 242),
            512: (249, 246, 242),
            1024: (249, 246, 242),
            2048: (249, 246, 242),
        }

        self.gridFontSize = {
            0: 0,
            2: 30,
            4: 30,
            8: 30,
            16: 30,
            32: 30,
            64: 30,
            128: 27,
            256: 27,
            512: 27,
            1024: 25,
            2048: 25,
        }

        self.running = True

    def addNumber(self):
        options = []

        for rowI, row in enumerate(self.grid):
            for colI, number in enumerate(row):
                if number == 0:
                    options.append({"row": rowI, "col": colI})

        if len(options) > 0:
            gridSpot = choice(options)
            r = random()

            if r < 0.9:
                self.grid[gridSpot["row"]][gridSpot["col"]] = 2
            else:
                self.grid[gridSpot["row"]][gridSpot["col"]] = 4

    def animateAddNumber(self, oldGrid, newGrid):
        s = time()

        differentCell = []

        for rowi, (oldRow, newRow) in enumerate(zip(oldGrid, newGrid)):
            for cellI, (oldCell, newCell) in enumerate(zip(oldRow, newRow)):
                if oldCell != newCell:
                    differentCell.append({"row": rowi, "cell": cellI})

        if len(differentCell) == 0:
            return

        origSize = 55

        while origSize <= self.squarewidth:
            self.drawbackground(self.squarewidth)
            self.applyscoreandbestandnewbutton((self.offset, self.offset - 10, 104, 64))
            self.applysquare(oldGrid)

            for celldata in differentCell:

                x = (25 + self.offset) + ((self.offset + self.squarewidth) * celldata["cell"])
                y = (100 + self.offset) + ((self.offset + self.squarewidth) * celldata["row"])

                x += self.squarewidth // 2
                y += self.squarewidth // 2

                self.roundrect(self.gridColour[newGrid[celldata["row"]][celldata["cell"]]], (x - (origSize // 2), y - origSize // 2, origSize, origSize), 5, False)

            pygame.display.update()
            origSize += 5

        #print(round((time() - s) * 1000)) # Drop To 20

    def printboard(self):
        [print(" ".join([str(char) for char in row])) for row in self.grid]

    def roundrect(self, colour, rect, circleR=0, thicknessOut=True):
        #  colour = (R, G, B)
        #  rect = (x, y, width, height)
        #  rect coordinates describe the middle rectangle
        #  circleR = radius of thickness

        if not thicknessOut:
            rect = (rect[0] + circleR, rect[1] + circleR, rect[2] - (2 * circleR), rect[3] - (2 * circleR))

        pygame.draw.circle(self.windowScreen, colour, (rect[0], rect[1]), circleR)
        pygame.draw.circle(self.windowScreen, colour, (rect[0] + rect[2], rect[1]), circleR)
        pygame.draw.circle(self.windowScreen, colour, (rect[0], rect[1] + rect[3]), circleR)
        pygame.draw.circle(self.windowScreen, colour, (rect[0] + rect[2], rect[1] + rect[3]), circleR)

        pygame.draw.rect(self.windowScreen, colour, rect)

        pygame.draw.rect(self.windowScreen, colour, (rect[0] + rect[2], rect[1], circleR, rect[3]))
        pygame.draw.rect(self.windowScreen, colour, (rect[0] - circleR, rect[1], circleR, rect[3]))

        pygame.draw.rect(self.windowScreen, colour, (rect[0], rect[1] - circleR, rect[2], circleR))
        pygame.draw.rect(self.windowScreen, colour, (rect[0], rect[1] + rect[3], rect[2], circleR))

        return [rect[0] - circleR, rect[0] + rect[2] + circleR, rect[1] - circleR, rect[1] + rect[3] +circleR]

    def drawbackground(self, squarewidth):
        self.squarewidth = squarewidth
        self.roundrect((187, 173, 160), (25, 100, 400, 400), 10, False)
        self.offset = (400 - (squarewidth * 4)) // 5

        for i in range(4):
            for j in range(4):
                self.roundrect((255, 255, 255), ((25 + self.offset) + ((self.offset + squarewidth) * i),
                                                 (100 + self.offset) + ((self.offset + squarewidth) * j), squarewidth,
                                                 squarewidth), 5, False)

    def applysquare(self, grid):
        for i in range(4):
            for j in range(4):
                value = grid[i][j]
                colour = self.gridColour[value]

                textSettings = pygame.font.Font('freesansbold.ttf', self.gridFontSize[value])

                x = (25 + self.offset) + ((self.offset + self.squarewidth) * j)
                y = (100 + self.offset) + ((self.offset + self.squarewidth) * i)
                self.roundrect(colour, (x, y, self.squarewidth, self.squarewidth), 5, False)

                Text = textSettings.render(str(value), True, self.gridTextColour[value])
                TextRect = Text.get_rect()
                TextRect.center = (x + (self.squarewidth // 2), y + (self.squarewidth // 2))
                self.windowScreen.blit(Text, TextRect)

    def applyscoreandbestandnewbutton(self, rect, rect2=None, rect3=None):
        textSettings = pygame.font.Font('freesansbold.ttf', 20)

        self.roundrect((187, 173, 160), rect, 5, False)

        Text = textSettings.render("SCORE", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (rect[0] + (rect[2] // 2), rect[1] + 20)
        self.windowScreen.blit(Text, TextRect)

        Text = textSettings.render(str(self.score), True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (rect[0] + (rect[2] // 2), rect[1] + 45)
        self.windowScreen.blit(Text, TextRect)

        if rect2 is None:
            rect2 = list(rect)
            rect2[0] += rect2[2] + 10

        self.roundrect((187, 173, 160), rect2, 5, False)

        Text = textSettings.render("BEST", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (rect2[0] + (rect2[2] // 2), rect2[1] + 20)
        self.windowScreen.blit(Text, TextRect)

        Text = textSettings.render(str(self.best), True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (rect2[0] + (rect2[2] // 2), rect2[1] + 45)
        self.windowScreen.blit(Text, TextRect)

        if rect3 is None:
            rect3 = list(rect2)
            rect3[0] += rect3[2] + 10

        self.buttonCoord = self.roundrect((187, 173, 160), rect3, 5, False)
        Text = pygame.font.Font('freesansbold.ttf', 15).render("NEW GAME", True, (255, 255, 255))
        TextRect = Text.get_rect()
        TextRect.center = (rect3[0] + (rect3[2] // 2), rect3[1] + (rect3[3] // 2))
        self.windowScreen.blit(Text, TextRect)

    def newgamebutton(self):
        mouseCoord = pygame.mouse.get_pos()
        leftC, _, _ = pygame.mouse.get_pressed()
        if self.buttonCoord[0] < mouseCoord[0] < self.buttonCoord[1] and self.buttonCoord[2] < mouseCoord[1] < self.buttonCoord[3] and leftC and not self.reset:
            self.reset = not self.reset
            self.newgame()
        else:
            if not(self.buttonCoord[0] < mouseCoord[0] < self.buttonCoord[1] and self.buttonCoord[2] < mouseCoord[1] < self.buttonCoord[3] and leftC):
                self.reset = not self.reset

    def newgame(self):
        self.grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]

        self.addNumber()
        self.addNumber()
        self.drawbackground(self.squarewidth)
        self.applysquare(self.grid)
        self.animateAddNumber([[0, 0, 0, 0]] * 4, self.grid)
        self.score = 0

    def isgameover(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False

                if i != 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False

                if j != 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False

        return True

    def isgamewon(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 2048:
                    return True
        return False

    def reflect(self, grid):
        return [[row[i] for row in grid] for i in range(4)]

    def animateshift(self, oldgrid, newgrid, direction):
        slidingspeed = 50
        if direction == "up" or direction == "down":
            oldgrid = self.reflect(oldgrid)
            newgrid = self.reflect(newgrid)

        if direction == "left" or direction == "right":
            oldmodgrid = [
                [
                    {"row": rowi,
                     "cell": celli,
                     "x-off": 0,
                     "y-off": 0,
                     "x-start": (25 + self.offset) + ((self.offset + self.squarewidth) * celli),
                     "y-start": (100 + self.offset) + ((self.offset + self.squarewidth) * rowi),
                     "val": cell
                     } for celli, cell in enumerate(row.copy()) if cell != 0
                ] for rowi, row in enumerate(oldgrid)
            ]

            newmodgrid = [
                [
                    {"row": rowi,
                     "cell": celli,
                     "x-end": (25 + self.offset) + ((self.offset + self.squarewidth) * celli),
                     "y-end": (100 + self.offset) + ((self.offset + self.squarewidth) * rowi),
                     "val": cell
                     } for celli, cell in enumerate(row.copy()) if cell != 0
                ] for rowi, row in enumerate(newgrid)
            ]

            mappingGrids = [
                [
                    oldCell,
                    newCell
                ] for oldRow, newRow in zip(oldmodgrid, newmodgrid) for oldCell, newCell in zip(oldRow, newRow) if oldCell["row"] != newCell["row"] or oldCell["cell"] != newCell["cell"]
            ]
        else:
            oldgrid = self.reflect(oldgrid)
            newgrid = self.reflect(newgrid)

            oldmodgrid = [
                [
                    {"row": celli,
                     "cell": coli,
                     "x-off": 0,
                     "y-off": 0,
                     "x-start": (25 + self.offset) + ((self.offset + self.squarewidth) * coli),
                     "y-start": (100 + self.offset) + ((self.offset + self.squarewidth) * celli),
                     "val": cell
                     } for celli, cell in enumerate(col.copy()) if cell != 0
                ] for coli, col in enumerate(oldgrid)
            ]

            newmodgrid = [
                [
                    {"row": celli,
                     "cell": coli,
                     "x-end": (25 + self.offset) + ((self.offset + self.squarewidth) * coli),
                     "y-end": (100 + self.offset) + ((self.offset + self.squarewidth) * celli),
                     "val": cell
                     } for celli, cell in enumerate(col.copy()) if cell != 0
                ] for coli, col in enumerate(newgrid)
            ]

            mappingGrids = [
                [
                    oldCell,
                    newCell
                ] for oldRow, newRow in zip(oldmodgrid, newmodgrid) for oldCell, newCell in zip(oldRow, newRow) if oldCell["row"] != newCell["row"] or oldCell["cell"] != newCell["cell"]
            ]

        if direction == "up" or direction == "down":
            oldgrid = self.reflect(oldgrid)

        for cells in mappingGrids:
            oldgrid[cells[0]["row"]][cells[0]["cell"]] = 0

        slide = True
        inpos = [False] * len(mappingGrids)

        while slide:
            self.drawbackground(self.squarewidth)
            self.applyscoreandbestandnewbutton((self.offset, self.offset - 10, 104, 64))
            self.applysquare(oldgrid)

            for i, slideCells in enumerate(mappingGrids):
                if not inpos[i]:
                    if direction == "right":
                        if slideCells[0]["x-start"] + slideCells[0]["x-off"] + slidingspeed <= slideCells[1]["x-end"]:
                            slideCells[0]["x-off"] += slidingspeed
                        else:
                            slideCells[0]["x-off"] = slideCells[1]["x-end"] - slideCells[0]["x-start"]
                            inpos[i] = True

                    elif direction == "left":
                        if slideCells[0]["x-start"] + slideCells[0]["x-off"] - slidingspeed >= slideCells[1]["x-end"]:
                            slideCells[0]["x-off"] -= slidingspeed
                        else:
                            slideCells[0]["x-off"] = slideCells[1]["x-end"] - slideCells[0]["x-start"]
                            inpos[i] = True

                    elif direction == "down":
                        if slideCells[0]["y-start"] + slideCells[0]["y-off"] + slidingspeed <= slideCells[1]["y-end"]:
                            slideCells[0]["y-off"] += slidingspeed
                        else:
                            slideCells[0]["y-off"] = slideCells[1]["y-end"] - slideCells[0]["y-start"]
                            inpos[i] = True

                    elif direction == "up":
                        if slideCells[0]["y-start"] + slideCells[0]["y-off"] - slidingspeed >= slideCells[1]["y-end"]:
                            slideCells[0]["y-off"] -= slidingspeed
                        else:
                            slideCells[0]["y-off"] = slideCells[1]["y-end"] - slideCells[0]["y-start"]
                            inpos[i] = True

                    else:
                        return

                self.roundrect(self.gridColour[slideCells[0]["val"]], (slideCells[0]["x-start"] + slideCells[0]["x-off"], slideCells[0]["y-start"] + slideCells[0]["y-off"], self.squarewidth, self.squarewidth), 5, False)

                Text = pygame.font.Font('freesansbold.ttf', self.gridFontSize[slideCells[0]["val"]]).render(str(slideCells[0]["val"]), True, self.gridTextColour[slideCells[0]["val"]])
                TextRect = Text.get_rect()
                TextRect.center = (slideCells[0]["x-start"] + slideCells[0]["x-off"] + (self.squarewidth // 2), slideCells[0]["y-start"] + slideCells[0]["y-off"] + (self.squarewidth // 2))
                self.windowScreen.blit(Text, TextRect)

            if all(inpos):
                slide = False

            pygame.display.update()
        return

    def shift(self, rowcol, direction):
        direction = direction.lower()

        nonzero = [cell for cell in rowcol if cell != 0]
        empty = 4 - len(nonzero)
        zeros = [0] * empty

        if direction == "left" or direction == "up":
            return nonzero + zeros
        elif direction == "right" or direction == "down":
            return zeros + nonzero
        else:
            return rowcol

    def animatecombine(self):
        s = time()

        origsize = self.squarewidth
        maxsize = self.squarewidth + 10

        if len(self.combinechanged) == 0:
            return

        while origsize <= maxsize:
            self.drawbackground(self.squarewidth)
            self.applyscoreandbestandnewbutton((self.offset, self.offset - 10, 104, 64))
            self.applysquare(self.grid)

            for combined in self.combinechanged:
                x = (25 + self.offset) + ((self.offset + self.squarewidth) * combined["col"])
                y = (100 + self.offset) + ((self.offset + self.squarewidth) * combined["row"])

                x += self.squarewidth // 2
                y += self.squarewidth // 2

                self.roundrect(self.gridColour[combined["val"]], (x - (origsize // 2), y - origsize // 2, origsize, origsize), 5, False)

            origsize += 5
            pygame.display.update()

    def combine(self, rowcol, direction, rowI):
        if direction == "left" or direction == "up":
            for i in range(3):
                currentcell = rowcol[i]
                backcell = rowcol[i + 1]

                if currentcell == backcell and currentcell != 0:
                    rowcol[i] = currentcell + backcell

                    if direction == "left":
                        self.combinechanged.append({"row": rowI, "col": i, "val": currentcell + backcell})
                    elif direction == "up":
                        self.combinechanged.append({"row": i, "col": rowI, "val": currentcell + backcell})

                    self.score += rowcol[i]
                    if self.score > self.best:
                        self.best = self.score
                        self.bestfile.truncate(0)
                        self.bestfile.write(str(self.best))
                    rowcol[i + 1] = 0

        elif direction == "right" or direction == "down":
            for i in range(3, 0, -1):
                currentcell = rowcol[i]
                backcell = rowcol[i - 1]

                if currentcell == backcell and currentcell != 0:
                    rowcol[i] = currentcell + backcell

                    if direction == "right":
                        self.combinechanged.append({"row": rowI, "col": i, "val": currentcell + backcell})
                    elif direction == "down":
                        self.combinechanged.append({"row": i, "col": rowI, "val": currentcell + backcell})

                    self.score += rowcol[i]
                    if self.score > self.best:
                        self.best = self.score
                        self.bestfile.truncate(0)
                        self.bestfile.write(str(self.best))
                    rowcol[i - 1] = 0

        return rowcol

    def makemove(self, grid, direction):
        if direction == "up" or direction == "down":
            grid = [[row[i] for row in grid] for i in range(4)]

        oldgrid = [row.copy() for row in grid]
        newgrid = [self.shift(row, direction) for row in grid]
        self.animateshift(oldgrid, newgrid, direction)

        newgrid = [self.combine(row, direction, rowi) for rowi, row in enumerate(newgrid)]

        oldgrid = [row.copy() for row in newgrid]
        newgrid = [self.shift(row, direction) for row in newgrid]
        self.animateshift(oldgrid, newgrid, direction)

        if direction == "up" or direction == "down":
            newgrid = [[row[i] for row in newgrid] for i in range(4)]

        return newgrid

    def handleinputs(self, grid):
        self.combinechanged = []

        if not self.addblock:
            if self.InputKey[pygame.K_q]:
                self.addblock = not self.addblock
                self.addNumber()

        else:
            if not self.InputKey[pygame.K_q]:
                self.addblock = not self.addblock

        if not self.moveup:
            if self.InputKey[pygame.K_UP]:
                self.moveup = not self.moveup
                return self.makemove(grid, "up"), True
        else:
            if not self.InputKey[pygame.K_UP]:
                self.moveup = not self.moveup

        if not self.movedown:
            if self.InputKey[pygame.K_DOWN]:
                self.movedown = not self.movedown
                return self.makemove(grid, "down"), True
        else:
            if not self.InputKey[pygame.K_DOWN]:
                self.movedown = not self.movedown

        if not self.moveleft:
            if self.InputKey[pygame.K_LEFT]:
                self.moveleft = not self.moveleft
                return self.makemove(grid, "left"), True
        else:
            if not self.InputKey[pygame.K_LEFT]:
                self.moveleft = not self.moveleft

        if not self.moveright:
            if self.InputKey[pygame.K_RIGHT]:
                self.moveright = not self.moveright
                return self.makemove(grid, "right"), True

        else:
            if not self.InputKey[pygame.K_RIGHT]:
                self.moveright = not self.moveright

        return grid, False

    def finishgame(self):
        win = self.isgamewon()
        lose = self.isgameover()

        if win:
            text = "YOU WIN"
        elif lose:
            text = "YOU LOSE"
        else:
            text = "YOU GLITCHED"

        if win or lose:
            transparenyScreen = pygame.Surface((400, 400), pygame.SRCALPHA)
            transparenyScreen.fill((255, 255, 255, 128))
            transparenyScreenRect = transparenyScreen.get_rect()
            transparenyScreenRect.center = (self.screenWidth // 2, self.screenHeight // 2 + 40)
            self.windowScreen.blit(transparenyScreen, transparenyScreenRect)

            Text = pygame.font.Font('freesansbold.ttf', 40).render("GAME OVER", True, (143, 120, 101))
            TextRect = Text.get_rect()
            TextRect.center = (self.screenWidth // 2, transparenyScreenRect.y + transparenyScreen.get_height()//2 - 100)
            self.windowScreen.blit(Text, TextRect)

            Text = pygame.font.Font('freesansbold.ttf', 25).render(text, True, (143, 120, 101))
            TextRect2 = Text.get_rect()
            TextRect2.center = (self.screenWidth // 2, TextRect.y + TextRect.height + 30)
            self.windowScreen.blit(Text, TextRect2)

            TryAgain = self.roundrect((143, 120, 101), (self.screenWidth//2 - 100, TextRect2.y + TextRect2.height + 80, 200, 60), 10, False)
            Text = pygame.font.Font('freesansbold.ttf', 30).render("Try Again", True, (255, 255, 255))
            TextRect3 = Text.get_rect()
            TextRect3.center = (TryAgain[0] + (TryAgain[1] - TryAgain[0]) // 2, TryAgain[2] + (TryAgain[3] - TryAgain[2]) // 2)
            self.windowScreen.blit(Text, TextRect3)

            mouseCoord = pygame.mouse.get_pos()
            leftC, _, _ = pygame.mouse.get_pressed()
            if TryAgain[0] < mouseCoord[0] < TryAgain[1] and TryAgain[2] < mouseCoord[1] < \
                    TryAgain[3] and leftC and not self.reset:
                self.reset = not self.reset
                self.newgame()
            else:
                if not (TryAgain[0] < mouseCoord[0] < TryAgain[1] and TryAgain[2] < mouseCoord[1] < TryAgain[3] and leftC):
                    self.reset = not self.reset

    def update(self):
        self.addNumber()
        self.addNumber()
        self.animateAddNumber([[0, 0, 0, 0]] * 4, self.grid.copy())

        while self.running:
            self.InputKey = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not (self.isgamewon() or self.isgameover()):
                tempgrid = self.grid
                self.grid, keypressed = self.handleinputs(self.grid.copy())

                if not self.grid == tempgrid and keypressed:
                    self.animatecombine()
                    oldGrid = [row.copy() for row in self.grid]
                    self.addNumber()
                    pygame.time.wait(10)
                    self.animateAddNumber(oldGrid, self.grid.copy())

            self.applysquare(self.grid)
            self.applyscoreandbestandnewbutton((self.offset, self.offset - 10, 104, 64))
            self.newgamebutton()
            self.finishgame()

            pygame.display.update()


if __name__ == "__main__":
    game = Game2048()
    game.update()
