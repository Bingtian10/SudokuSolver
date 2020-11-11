import pygame, random, copy

pygame.init()
from pygame.locals import (
        K_UP,
        K_DOWN,
        K_LEFT,
        K_RIGHT,
        K_ESCAPE,
        KEYDOWN,
        QUIT,
        K_RETURN,
        K_g,
)

class Game():
    def __init__(self, screen, surf, font):
        self.screen = screen
        self.surf = surf
        self.rect = self.surf.get_rect()
        self.rect.move_ip(SCREEN_WIDTH/2 - BOARD_LENGTH/2, SCREEN_HEIGHT/2 - BOARD_LENGTH/2)
        self.font = font
        self.board = []

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.surf, self.rect)
        self.draw_lines(self.rect.topleft, self.rect.bottomleft, True)
        self.draw_lines(self.rect.topleft, self.rect.topright, False)
        self.draw_vals()
        self.instructions()
        pygame.display.update()
        #pygame.time.delay(50)

    def draw_lines(self,p1, p2, isVertical):
        thick = 1
        if isVertical:
            for i in range(9):
                if(i > 0 and i % 3 == 0):
                    thick = 7
                else:
                    thick = 1
                pygame.draw.line(self.screen, (0,0,0), (p1[0] + i*50, p1[1]), (p2[0] + i*50, p2[1]), thick)
        else:
            for i in range(9):
                if(i > 0 and i % 3 == 0):
                    thick = 7
                else:
                    thick = 1
                pygame.draw.line(self.screen, (0,0,0), (p1[0], p1[1] + i*50), (p2[0], p2[1] + i*50), thick)         

    def draw_vals(self):
        p = self.rect.topleft
        for i in range(9):
            for j in range(9):
                if(self.board[i][j] > 0):
                    text = self.font.render(str(self.board[i][j]), 1, (0,0,0))
                    self.screen.blit(text, (p[0]+j*50+20, p[1]+i*50+20))

    def instructions(self):
        msg = "Press g to generate a new board, Press enter/return to solve the board"
        text = self.font.render(msg,1, (255,255,255))
        self.screen.blit(text, (190, 540))

    def isValid(self, board, row, col, c):
        for i in range(9):
            if board[i][col] == c:
                return False
            if board[row][i] == c:
                return False
            #checking the 3x3 sub-board (i,j) is located at
            y = 3 * (row//3) + i//3;
            x = 3 * (col//3) + i%3;
            if(board[y][x] == c):
                return False;
        return True

    def solve(self, toDraw):
        #pygame.event.clear()
        for i in range(9):
            for j in range(9):
                # For every empty spaces
                if self.board[i][j] == 0:
                    # If exhausted all candidates and still no solutions, backtrack
                    for c in range(1, 10):
                        if self.isValid(self.board, i, j, c):
                            self.board[i][j] = c
                            if toDraw:
                                self.draw()
                            if self.solve(toDraw):
                                return True
                            else:
                                self.board[i][j] = 0
                                if toDraw:
                                    self.draw()
                    return False
        return True

    def countSol(self, board):
        #pygame.event.pump()
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    count = 0
                    for c in range(1, 10):
                        if self.isValid(board, i, j, c):
                            board[i][j] = c
                            count += self.countSol(board)
                            if count > 1:
                                return 2
                            else:
                                board[i][j] = 0
                    return count
        return 1

    # Randomly generate a full board, then remove each
    # value. If the board still has 1 solution, continue; else
    # place the number back
    def generateRandomBoard(self):
        self.board = [[0 for j in range(9)] for i in range(9)]
        candidates = [i for i in range(9)]
        for row in range(3):
            for col in range(3):
                p = random.randint(0,8)
                random.shuffle(candidates)
                for c in candidates:
                    i = row*3 + p//3
                    j = col*3 + p%3
                    if self.isValid(self.board, i, j, c):
                        self.board[i][j] = c
                        break

        pos = [i for i in range(81)]
        random.shuffle(pos)
        if self.solve(False):
            print("good")
        else:
            print("bad")
            
        for p in pos:
            i = p//9
            j = p%9
            temp = self.board[i][j]
            self.board[i][j] = 0
            if self.countSol(copy.deepcopy(self.board)) != 1:
                self.board[i][j] = temp
        self.draw()





SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BOARD_LENGTH = 450

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Font
font = pygame.font.SysFont(None, 20)

# Create board surface, draw the lines
board_surf = pygame.Surface((BOARD_LENGTH, BOARD_LENGTH))
board_surf.fill((255,255,255))
game = Game(screen, board_surf, font)
game.generateRandomBoard()
game.draw()

running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RETURN:
                game.solve(True)
            if event.key == K_g:
                game.generateRandomBoard()

        elif event.type == pygame.QUIT:
            running = False

    
    
pygame.quit()
