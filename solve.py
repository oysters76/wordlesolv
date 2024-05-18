

# Load all plausible words 
all_words = [] 
with open("words.txt", "r") as wordfile:
    for line in wordfile:
        all_words.append(line.replace('\n', ''))


        

# Interface 
import pygame



# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.key.set_repeat()
TEXT_FONT = pygame.font.Font(None, 40)

from algorithm import * 
from structures import * 

board = WordleBoard(100, 100, (150,150,150), 36)  
wordPool = WordProbPool(600, 50, TEXT_FONT, 30)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.K_SPACE <= event.key <= pygame.K_z:
                # Convert the key code to a character
                char = chr(event.key)
                board.add_char(str(char).upper())
            if pygame.K_BACKSPACE == event.key:
                board.del_char()
            if pygame.K_KP_ENTER:
                can_move = board.move_to_next() 
                if (can_move):
                    info = board.get_info()
                    updateWordPool(wordPool, info, all_words) 
        elif event.type == pygame.MOUSEBUTTONDOWN: 
            x, y = pygame.mouse.get_pos()
            board.board_click(x,y) 
        

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    board.draw_board(screen) 
    wordPool.render(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()