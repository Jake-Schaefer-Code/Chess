import pygame
import sys

piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
piecedic = {}
column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None



    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i+1)%2 == 1 and (8-j)%2 == 1:
                     self.color = (169,108,69)
                elif (i+1)%2 == 0 and (8-j)%2 == 0:
                    self.color = (169,108,69)
                else:
                    self.color = (245,198,156)
                pygame.draw.rect(self.screen, self.color, pygame.Rect((512//8)*i,(512//8)*j,512//8,512//8))



class setup:
    def __init__(self, rows):
        self.board = [[] for _ in range(rows)]
        print(self.board)



def main():
    pygame.init()
    pygame.display.init()

    screen = pygame.display.set_mode((512,512))
    screen.fill(pygame.Color("white"))
    board1 = Board(screen)

    for piece in piecelist:
        piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG")


    while True:
        
        
        pygame.display.set_caption("Chess")

        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()


main()
