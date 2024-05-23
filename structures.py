import pygame 

class FilterRule(object):
    
    RULE_LETTER_SHOULD_BE_HERE     = 1 
    RULE_LETTER_SHOULD_NOT_BE_HERE = 2
    RULE_LETTER_CAN_BE_THERE       = 3 

    def __init__(self, letter, position, rule): 
        self.letter = letter 
        self.position = position 
        self.rule = rule 

    def checkLetterShouldBeThere(self, l):
        return self.letter == l; 

    def checkLetterShouldNotBeThere(self, l, word):
        return self.letter not in word;  

    def checkLetterCanBeThere(self, l, word):
        return self.letter in word;   

    def check_rule(self, letter, position, word):
        if (self.position != position): return True 

        if self.rule == FilterRule.RULE_LETTER_SHOULD_BE_HERE:
            return self.checkLetterShouldBeThere(letter) 
        if self.rule == FilterRule.RULE_LETTER_SHOULD_NOT_BE_HERE: 
            return self.checkLetterShouldNotBeThere(letter, word) 
        if self.rule == FilterRule.RULE_LETTER_CAN_BE_THERE:
            return self.checkLetterCanBeThere(letter, word) 
        return False  

class WordleBoard(object):
    TRIES = 6 
    WORD_SIZE = 5 
    RECT_SIZE = 80 
    
    CLICK_STATE_DEF          = 0 #white
    CLICK_STATE_NOT_IN       = 1 #grey out
    CLICK_STATE_IN_WRONG_POS = 2 #yellow
    CLICK_STATE_IN_CORRE_POS = 3 #green 
    ALL_CLICK_STATES         = 4

    FILTER_RULE_MAP = [FilterRule.RULE_LETTER_SHOULD_NOT_BE_HERE, 
                        FilterRule.RULE_LETTER_CAN_BE_THERE, 
                        FilterRule.RULE_LETTER_SHOULD_BE_HERE] 

    def __init__(self, x, y, rect_color, ft_size):
        self.state = self.init_state() 
        self.x = x 
        self.y = y 
        self.rect_color = rect_color
        self.rects = [] 
        self.ft_size = ft_size 
        self.font = pygame.font.Font(None, self.ft_size)
        self.xloc = 0 
        self.yloc = 0 
        self.r_clicks = [] 

        self.fg_map = [(0,0,0), (255,255,255), (255,255,255), (255,255,255)] 
        self.bg_map = [(0,0,0), (128,128,128), (255,196,37), (1,154,1)]

        self.results = [] 
    
    class RectState(object):
        def __init__(self, value, click, rect):
            self.value = value 
            self.click = click 
            self.rect = rect 

    def init_state(self):
        s = [] 
        for i in range(WordleBoard.TRIES):
            r = [] 
            for j in range(WordleBoard.WORD_SIZE):
                r.append(WordleBoard.RectState(' ', 0, None))

            s.append(r) 
        return s
    
    def draw_board(self, screen):
        for i, row in enumerate(self.state):
            for j, cell in enumerate(row):
                r = None 
                if cell.value == ' ':
                    # draw a blank 
                    r = self.draw_blank(i, j, screen)
                else:
                    # draw a letter box 
                    r = self.draw_letterbox(i, j, screen)
                cell.rect = r
    
    def draw_blank(self, i, j, screen):
        rect = pygame.Rect(self.x + (WordleBoard.RECT_SIZE * j), (self.y + 
                                                                  (WordleBoard.RECT_SIZE * i)), WordleBoard.RECT_SIZE, 
                WordleBoard.RECT_SIZE);
        pygame.draw.rect(screen, self.rect_color, rect, 2, border_radius=2)
        return rect 
    
    def get_cell_fg_color(self, click):
        return self.fg_map[click]

    
    def get_cell_bg_color(self, click):
        return self.bg_map[click] 

    def draw_letterbox(self, i, j, screen):
        rect = pygame.Rect(self.x + (WordleBoard.RECT_SIZE * j), 
                           (self.y + (WordleBoard.RECT_SIZE * i)), WordleBoard.RECT_SIZE, 
                WordleBoard.RECT_SIZE);
        
        
        letter = self.state[i][j].value 
        click_count = self.state[i][j].click
        fg_color = self.get_cell_fg_color(click_count)
        bg_color = self.get_cell_bg_color(click_count)
        text_surface = self.font.render(letter, True, fg_color)

        text_x = rect.x + (rect.width - text_surface.get_width()) // 2
        text_y = rect.y + (rect.height - text_surface.get_height()) // 2
        
        
        do_fill = 0 
        if (click_count == 0):
            do_fill = 2
        pygame.draw.rect(screen, bg_color, rect, do_fill, border_radius=2)
        screen.blit(text_surface, (text_x, text_y))
        return rect  
        
    def add_char(self, letter):
        if (self.xloc >= WordleBoard.WORD_SIZE):
            return 
        self.state[self.yloc][self.xloc].value = letter  
        self.xloc += 1 
        if (self.xloc >= WordleBoard.WORD_SIZE):
            self.xloc = WordleBoard.WORD_SIZE-1; 
        
    def del_char(self):
        if (self.state[self.yloc][self.xloc] == ' '):
            self.xloc -= 1    
        self.state[self.yloc][self.xloc].value = ' '
        self.state[self.yloc][self.xloc].click = 0 
        self.xloc -= 1 
        if (self.xloc <= 0):
            self.xloc = 0
    
    def board_click(self, x, y): 
        for row in self.state:
            for cell in row:
                if cell.value == ' ':
                    continue  
                if (cell.rect.collidepoint(x,y)):
                    cell.click += 1 
                    cell.click %= WordleBoard.ALL_CLICK_STATES

    def __check_if_can_move(self):
        for cell in self.state[self.yloc]: 
            if (cell.value == ' '):
                return False
            if (cell.click == 0):
                return False 
        return True 

    def __add_to_results(self):
        for i, cell in enumerate(self.state[self.yloc]):
            self.results.append(FilterRule(str(cell.value).lower(), i, 
                                            WordleBoard.FILTER_RULE_MAP[cell.click-1])) 

    def move_to_next(self):
        if (self.yloc >= WordleBoard.TRIES):
            return False
        if (self.__check_if_can_move()):
            self.__add_to_results()
            self.yloc += 1
            self.xloc = 0
            return True 
        return False
    
    def get_info(self):
        return self.results 
    
class WordProb(object):
    def __init__(self, word, prob, font):
        self.word = word 
        self.prob = prob 
        self.font = font 
    
    def render(self, x, y, screen):
        text_surface = self.font.render(str(self.word).upper() + " (" + str(self.prob) + "%)", True, (0,0,0)) 
        screen.blit(text_surface, (x, y))

class WordProbPool(object):
    def __init__(self, ix, iy, font, gap):
        self.probpool = [] 
        self.ix = ix 
        self.iy = iy 
        self.font = font 
        self.gap = gap
        self.remainingWords = [] 
    
    def clear(self):
        self.probpool = [] 
        self.remainingWords = [] 

    def add(self, word, prob):
        w = str(word).lower()
        self.remainingWords.append(w)
        self.probpool.append(WordProb(w, prob, self.font)) 
    
    def reset(self):
        self.probpool = [] 
    
    def render(self, screen):
        x = self.ix 
        y = self.iy 
        for w in self.probpool:
            w.render(x,y,screen) 
            y += self.gap
    
    def print_pool(self):
        print("-----------printing pool--------")
        for p in self.probpool:
            print(p.word)

   