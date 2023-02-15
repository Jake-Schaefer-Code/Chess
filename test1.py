import pygame
import sys

#universal variables? can we put this somewhere else like inside main or will it not work?
coordslist = []
coordsx = {}
coordsy = {}
squarecolor = {}


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
            coordsx[((i)*(self.image.get_width()/8),(i+1)*(self.image.get_width()/8))] = i + 1
            for j in range(8):
                coordslist.append(self.ycoords[j]+str(i+1))
                coordsy[((j)*(self.image.get_width()/8),(j+1)*(self.image.get_width()/8))] = self.ycoords[(-(j+1))]                
                if (i+1)%2 == 1 and (8-j)%2 == 1:
                    squarecolor[self.ycoords[-(j+1)] + str(i+1)] = "black"
                elif (i+1)%2 == 0 and (8-j)%2 == 0:
                    squarecolor[self.ycoords[-(j+1)] + str(i+1)] = "black"
                else:
                    squarecolor[self.ycoords[-(j+1)] + str(i+1)] = "white"
        print(coordslist)
        print(coordsx)
        print(coordsy)
        

    def get_coords(self, pos):
        print(pos)
        x_square = None
        y_square = None
        for (k1,k2) in coordsx:
            if (k1 < pos[0] and k2 > pos[0]):
                x_square = coordsx[(k1,k2)]
        for (k1,k2) in coordsy:
            if (k1 < pos[1] and k2 > pos[1]):
                y_square = coordsy[(k1,k2)]

        print(str(y_square) + str(x_square))
        print(squarecolor[str(y_square) + str(x_square)])



class square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    



def main():
    pygame.init()
    pygame.display.init()
    
    boardimage = pygame.image.load("chessboard.png")
    screen = pygame.display.set_mode((boardimage.get_width(), boardimage.get_height()))
    board1 = Board(screen, 0, 0, boardimage)
    board1.coordinates() #defines the coordiate system

    while True:
        board1.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == True:
            pygame.time.wait(100)
            board1.get_coords(pos)
        
        
        
        pygame.display.update()
        

main()
