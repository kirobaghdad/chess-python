"""
This is the main Driver file.
"""
import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = (HEIGHT - 32) // DIMENSION
MAX_FPS = 15
MARGIN = 16
IMAGES = {}

def loadImages():
    game = ChessEngine.GameState()
    board = game.board

    IMAGES['bp'] = p.transform.scale(p.image.load("./images/" + "bp" + ".png"), (SQ_SIZE, SQ_SIZE))
    IMAGES['wp'] = p.transform.scale(p.image.load("./images/" + "wp" + ".png"), (SQ_SIZE, SQ_SIZE))
    
    for color in board[0], board[7]:
        for piece in color:
            IMAGES[piece] = p.transform.scale(p.image.load("./images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def DrawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    #drawUndoButton(gs)

def drawBoard(screen):
    p.draw.rect(p.display.get_surface(), (0,0,0), p.Rect(MARGIN, MARGIN, WIDTH - 2 * MARGIN, HEIGHT - 2 * MARGIN), 2)
    colors = [p.Color("white"), p.Color("grey")]

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(p.display.get_surface(), color, p.Rect(MARGIN + c * SQ_SIZE, MARGIN + r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    return

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]

            if piece != "--":
                screen.blit(IMAGES[piece], (MARGIN + c * SQ_SIZE, MARGIN + r * SQ_SIZE))


"""
Handling User Input and Updating Graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill((139,69,19))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    loadImages()
    running = True
    playerClicks = []
    selectedSQ = ()
    moveMade = False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #Mouse Handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = (location[1] - MARGIN) // SQ_SIZE
                col = (location[0] - MARGIN) // SQ_SIZE
                if selectedSQ == (row, col):
                    selectedSQ = ()
                    playerClicks = []
                elif selectedSQ and  gs.board[row][col][0] == gs.board[selectedSQ[0]][selectedSQ[1]][0]: #The User Changed the selected piece
                    selectedSQ = (row, col)
                    playerClicks[0] = selectedSQ
                else:
                    selectedSQ = (row, col)
                    playerClicks.append(selectedSQ)
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            playerClicks = []
                            selectedSQ = ()
                        else: 
                            playerClicks.pop()
                            selectedSQ = playerClicks[0]

                        
            #Key Handlers
            elif e.type == p.KEYDOWN:
                if(e.key == p.K_z):
                    gs.undoMove()
                    moveMade = True

            if moveMade == True:
                validMoves = gs.getValidMoves()
                moveMade = False   

        clock.tick(MAX_FPS)
        DrawGameState(screen, gs)
        p.display.flip()


if __name__ == "__main__":
    main()