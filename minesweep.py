import pygame
import random
import sys




class GridSquare:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE-1, SQUARE_SIZE-1)
        self.isMine = False
        self.isFlagged = False
        self.isRevealed = False
        self.numAdjacentMines = 0



pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 1000
GRID_SIZE = 10
MINES = GRID_SIZE*GRID_SIZE//8
SQUARE_SIZE = WIDTH/GRID_SIZE

COVERED_SQUARE_COLOUR = (25,195,25)
UNCOVERED_SQUARE_COLOUR = (120,75,0)

def initGame():
    global grid, gameRunning, uncoveredSquares, squaresToUncover
    grid = [[GridSquare(i, j) for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]
    generateMines()
    calculateAdjacentMines()
    gameRunning = True
    uncoveredSquares = {}
    loadGrid()
    


def generateMines():
    for i in range(MINES):
        minePlaced = False
        # Ensures that all mines are uniquely placed
        while not minePlaced:
            randX = random.randint(0, GRID_SIZE-1)
            randY = random.randint(0, GRID_SIZE-1)
            if grid[randX][randY].isMine == False:
                grid[randX][randY].isMine = True
                minePlaced = True
        
        

def calculateAdjacentMines():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            gridSquare = grid[i][j]
            if not gridSquare.isMine:
                adjacentPositions = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
                for pos in adjacentPositions:
                    adjX = i + pos[0]
                    adjY = j + pos[1]
                    if adjX >= 0 and adjX < GRID_SIZE and adjY >= 0 and adjY < GRID_SIZE:
                        if grid[adjX][adjY].isMine:
                            gridSquare.numAdjacentMines += 1
                            
            


def revealAdjacentSquares(gridSquare):
        adjacentPositions = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[1,-1],[-1,1],[-1,-1]]
        pygame.draw.rect(screen, UNCOVERED_SQUARE_COLOUR, gridSquare.rect)
        for pos in adjacentPositions:
            adjX = gridSquare.x + pos[0]
            adjY = gridSquare.y + pos[1]
            # If its a valid square, reveal it
            if adjX >= 0 and adjX < GRID_SIZE and adjY >= 0 and adjY < GRID_SIZE and grid[adjX][adjY].isRevealed == False:
                currentGridSquare = grid[adjX][adjY]
                currentGridSquare.isRevealed = True
                pygame.draw.rect(screen, UNCOVERED_SQUARE_COLOUR, currentGridSquare.rect)
                uncoveredSquares[currentGridSquare.x,currentGridSquare.y] = currentGridSquare

                # If its got no adjacent mines, reveal the adjacent squares
                if currentGridSquare.numAdjacentMines == 0:
                    revealAdjacentSquares(currentGridSquare)
                    

                else:
                    makeText(str(currentGridSquare.numAdjacentMines),32,currentGridSquare.rect.center[0],currentGridSquare.rect.center[1],(0,0,0))



def loadGrid():
    # Fill screen with background color first
    screen.fill((128, 128, 128))  # Gray background
    
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(i*SQUARE_SIZE, j*SQUARE_SIZE, SQUARE_SIZE-1, SQUARE_SIZE-1)
            pygame.draw.rect(screen, COVERED_SQUARE_COLOUR, rect)
    
    # Update display once after drawing all squares
    pygame.display.flip()


def makeText(text, size,x,y,col):
    font = pygame.font.Font('freesansbold.ttf', size)
    text = font.render(text, True, col)
    textRect = text.get_rect()
    textRect.center = (x,y)
    screen.blit(text, textRect)


def gameOver():
    screen.fill((0,0,0))
    makeText("Game Over!",32,WIDTH//2,HEIGHT//2,(255,0,0))

def winnerView():
    screen.fill((0,0,0))
    makeText("You Win!",32,WIDTH//2,HEIGHT//2,(150,150,0))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()

initGame()
squaresToUncover = GRID_SIZE*GRID_SIZE - MINES
while True:
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Add proper exit
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                initGame()

        if event.type == pygame.MOUSEBUTTONDOWN and gameRunning:
            pos = pygame.mouse.get_pos()

            gridPos = (int(pos[0]//SQUARE_SIZE), int(pos[1]//SQUARE_SIZE))
            gridSquare = grid[gridPos[0]][gridPos[1]]
            rect = gridSquare.rect

            # Left CLicked
            if pygame.mouse.get_pressed()[0]:
                if not gridSquare.isFlagged:
                    # If its a mine the game ends
                    if gridSquare.isMine:
                        gameOver()
                        gameRunning = False
                    else:
                        if(gridSquare.numAdjacentMines == 0):
                            # If no adjacent mines, reveal safe squares
                            revealAdjacentSquares(gridSquare)
                        else: 
                            # If its not a mine then it reveals the number of adjacent mines
                            gridSquare.isRevealed = True
                            pygame.draw.rect(screen, (UNCOVERED_SQUARE_COLOUR), rect)
                            makeText(str(gridSquare.numAdjacentMines),32,rect.center[0],rect.center[1],(0,0,0))
                            uncoveredSquares[gridSquare.x,gridSquare.y] = gridSquare
            # Right Clicked
            elif pygame.mouse.get_pressed()[2]:
                

                # Flags square
                if gridSquare.isFlagged == False and gridSquare.isRevealed == False:
                    pygame.draw.rect(screen, (200,0,0), rect)
                    gridSquare.isFlagged = True
                # De Flags
                elif gridSquare.isRevealed == False:
                    pygame.draw.rect(screen, COVERED_SQUARE_COLOUR, rect)
                    gridSquare.isFlagged = False


    # If all squares are uncovered then the game ends
    if len(uncoveredSquares) == squaresToUncover:
        winnerView()
        gameRunning = False
                
                
            
    


    # Call loadGrid only once, not every frame
    if not hasattr(loadGrid, 'called'):
        loadGrid()
        loadGrid.called = True

    pygame.display.flip()
    timer.tick(60)
            
            




