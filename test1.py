import pygame
import sys

class Board:
    def __init__(self, screen, x, y, image):
        self.screen = screen
        self.image = image
        self.x = x
        self.y = y
        self.square_color = ""
    
    def draw(self):
        current_image = self.image
        self.screen.blit(current_image, (self.x, self.y))
    
    def coordinates(self):
        self.ycoords = ['a','b','c','d','e','f','g','h']
        for i in range(8):
            for j in range(8):
                coordslist.append(self.ycoords[j]+str(i+1))
                
                #coordsx[(i+1)] = ((i)*(self.image.get_width()/8),(i+1)*(self.image.get_width()/8)) #defines each square to be 1/8 of the board
                #coordsy[self.ycoords[j]] = ((j)*(self.image.get_height()/8),(j+1)*(self.image.get_height()/8))
                #if (i+1)%2 == 1:
                    #self.square_color = "black"
                #elif (i+1)%2 == 0:
                    #self.square_color = "white"
        print(coordslist)


coordslist = []
coordsx = {}
coordsy = {}

def main():
    pygame.init()
    pygame.display.init()
    
    boardimage = pygame.image.load("chessboard.png")
    screen = pygame.display.set_mode((boardimage.get_width(), boardimage.get_height()))
    board1 = Board(screen, 0, 0, boardimage)
    coords = board1.coordinates()

    while True:
        board1.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pos = pygame.mouse.get_pos()
        pygame.display.update()


main()
