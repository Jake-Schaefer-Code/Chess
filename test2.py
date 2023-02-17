import pygame
import sys

piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
piecedic = {}
column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
Width = 512
Height = 512


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None
        self.board = [["","","","","","","",""] for _ in range(8)]
        self.board[0] = ["br","bn","bb","bq","bk","bb","bn","br"]
        self.board[1] = ["bp","bp","bp","bp","bp","bp","bp","bp"]
        self.board[6] = ["wp","wp","wp","wp","wp","wp","wp","wp"]
        self.board[7] = ["wr","wn","wb","wq","wk","wb","wn","wr"]
        print(self.board)



    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i+1)%2 == 1 and (8-j)%2 == 1:
                     self.color = (169,108,69)
                elif (i+1)%2 == 0 and (8-j)%2 == 0:
                    self.color = (169,108,69)
                else:
                    self.color = (245,198,156)
                pygame.draw.rect(self.screen, self.color, pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8))
                square = self.board[j][i]
                if square != "":
                    self.screen.blit(pygame.transform.scale(piecedic[square],(Width//8,Height//8)), pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8))



class setup:
    def __init__(self, rows):
        self.board = [[] for _ in range(rows)]
        print(self.board)


def get_coords(pos):
    x = pos[0]
    y = pos[1]


def main():
    pygame.init()
    pygame.display.init()

    screen = pygame.display.set_mode((Width,Height))
    screen.fill(pygame.Color("white"))
    board1 = Board(screen)

    for piece in piecelist:
        piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG")


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()

        pos = pygame.mouse.get_pos()        
        if pygame.mouse.get_pressed()[0] == True:
            pygame.time.wait(100)
            get_coords(pos)
        
        pygame.display.update()


main()
