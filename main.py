from pathlib import Path
import pygame
import sys
import time
import pickle
import pygame.freetype
import os


pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW_TITLE = "Gra-Wiezami"
pygame.display.set_caption(WINDOW_TITLE)
icon = pygame.image.load('grafiki/icon.png')
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

save_path = 'save.txt'

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def save_lists_to_file(list1, list2, str, filename):
    with open(filename, 'wb') as file:
        pickle.dump((list1, list2, str), file)
def load_lists_from_file(filename):
    with open(filename, 'rb') as file:
        list1, list2, str = pickle.load(file)
    return list1, list2, str
def save_font_to_file(str, filename):
    with open(filename, 'wb') as file:
        pickle.dump(str, file)
def load_font_from_file(filename):
    with open(filename, 'rb') as file:
        str = pickle.load(file)
    return str
def clear_file(filename):
    with open(filename, 'w') as file:
        pass

class Figure():
    def __init__(self, font):
        self.graphics = [('Nowoczesne', 'font/CHEQ_TT.TTF'),
                         ('Przypadki', 'font/CASEFONT.TTF'),
                         ('Maya', 'font/MAYAFONT.TTF'),
                         ('Alfa', 'font/Alpha.TTF'),
                         ('Condal','font/CONDFONT.TTF'),
                         ('Leipzig','font/LEIPFONT.TTF')]
        self.tmp = ''
        for i in self.graphics:
            if i[0] == font:
                self.tmp = i[1]
                f = open("settings.txt", "w")
                f.write(i[1])
                f.close()
        self.font = pygame.font.Font(self.tmp, 100)
        self.bierki = ['t', 'r']
        self.text_surface = ""
        self.text_surface = ""

    @staticmethod
    def render_text(text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()
    def rysuj_bierke(self):
        index = self.bierki.index(self.bierki[0])
        text_surface, text_rect = self.render_text(self.bierki[1], self.font, 'white')
        text_rect.center = (570, 225)
        return text_surface, text_rect

def main():
    button_width = 250
    button_length = 100
    position_x = (WIDTH-button_width)/2
    position_y = 75
    path = Path('./save.txt')
    if path.is_file() and bool(path.stat().st_size):
        load_button = Button("Wznow Gre", button_width, button_length, (position_x, position_y), 20,(128, 128, 255, 128), (255, 128, 255, 128))
        position_y += 125
    new_game_button = Button("Nowa Gra", button_width, button_length, (position_x, position_y), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    rules_button = Button("Zasady", button_width, button_length, (position_x, position_y+125), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    settings_button = Button("Ustawienia", button_width, button_length, (position_x, position_y+250), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    quit_button = Button("Wyjscie", button_width, button_length, (position_x, position_y+375), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        background_image = pygame.image.load("grafiki/tlo.png").convert()
        WIN.fill((255, 255, 255))
        WIN.blit(background_image, (0, 0))
        if path.is_file() and bool(path.stat().st_size):
            load_button.draw_button(WIN)
        new_game_button.draw_button(WIN)
        rules_button.draw_button(WIN)
        settings_button.draw_button(WIN)
        quit_button.draw_button(WIN)
        pygame.display.update()
    pygame.quit()
    sys.exit()

class Game:
    def __init__(self, font, iscontinued):
        self.font = pygame.font.Font(font, 100)
        self.counter_draw_moves = 0
        self.SZER = 800
        self.WYS = 800
        self.screen = pygame.display.set_mode([self.SZER, self.WYS])
        self.zegar = pygame.time.Clock()
        self.fps = 60
        self.tlo = 'wheat3'
        #self.i_motyw = 1
        #self.tlo = motywy[i_motyw][2]
        self.kolor_jasny = 'wheat'
        #self.kolor_jasny = motywy[i_motyw][0]
        self.kolor_ciemny = 'wheat1'
        #self.kolor_ciemny = motywy[i_motyw][1]
        self.WINDOW_TITLE = "Gra-Wiezami"
        pygame.display.set_caption(self.WINDOW_TITLE)
        self.icon = pygame.image.load('grafiki/icon.png')
        pygame.display.set_icon(self.icon)

        self.etap = 0
        self.wsje_ruchy = []

        if iscontinued:
            self.pola_bialych, self.pola_czarnych, self.etap = load_lists_from_file(save_path)
            # print("wczytuje")
            # print(self.pola_bialych)
            # print(self.pola_czarnych)
            # print("Z pliku: " + str(self.etap))
        else:
            self.pola_bialych = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6), (1, 6), (2, 6),
                                 (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
            self.pola_czarnych = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1),
                                  (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

        self.bierki = ['t', 'r']
        self.zbite_biale = []
        self.zbite_czarne = []

        self.biale_bierki = []
        self.czarne_bierki = []

        for i in range(len(self.pola_bialych)):
            self.biale_bierki.append('r')
        for i in range(len(self.pola_czarnych)):
            self.czarne_bierki.append('t')

        self.tmp = 100
        self.counter = 0
        self.winner = ''
        self.game_over = False

        self.strona = 'bialy'

        self.biale_opcje = self.opcje_ruchu(self.biale_bierki, self.pola_bialych, 'bialy')
        self.czarne_opcje = self.opcje_ruchu(self.czarne_bierki, self.pola_czarnych, 'czarny')

    @staticmethod
    def render_text(text, font, color):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def na_oborot(self):
        yeet = []
        for j in range(len(self.pola_czarnych)):
            yeet.append(self.pola_czarnych[j])
            self.pola_czarnych[j] = self.pola_bialych[j]
            self.pola_bialych[j] = yeet[j]

    def rysuj_szachownice(self):
        for i in range(32):
            kolumna = i % 4
            wiersz = i // 4
            if wiersz % 2 == 0:
                pygame.draw.rect(self.screen, self.kolor_jasny, [600 - (kolumna * 200), wiersz * 100, 100, 100])
            else:
                pygame.draw.rect(self.screen, self.kolor_ciemny, [700 - (kolumna * 200), wiersz * 100, 100, 100])

            pygame.draw.rect(self.screen, 'wheat3', [0, 800, self.SZER, 100])
            pygame.draw.rect(self.screen, 'wheat4', [0, 800, self.SZER, 100], 5)
            pygame.draw.rect(self.screen, 'wheat4', [800, 0, 200, self.WYS], 5)
    def rysuj_bierki(self):
        for i in range(len(self.biale_bierki)):
            index = self.bierki.index(self.biale_bierki[i])
            text_surface, text_rect = self.render_text(self.biale_bierki[i], self.font, 'black')
            text_rect.center = (self.pola_bialych[i][0] * 100 + 50, self.pola_bialych[i][1] * 100 + 50)
            self.screen.blit(text_surface, text_rect)
            if self.etap < 2:
                if self.tmp == i:
                    pygame.draw.rect(self.screen, 'red',
                                     [self.pola_bialych[i][0] * 100 + 1, self.pola_bialych[i][1] * 100 + 1, 100, 100],
                                     2)
        for i in range(len(self.czarne_bierki)):
            index = self.bierki.index(self.czarne_bierki[i])
            text_surface, text_rect = self.render_text(self.czarne_bierki[i], self.font, 'black')
            text_rect.center = (self.pola_czarnych[i][0] * 100 + 50, self.pola_czarnych[i][1] * 100 + 50)
            self.screen.blit(text_surface, text_rect)
            if self.etap >= 2:
                if self.tmp == i:
                    pygame.draw.rect(self.screen, 'blue',
                                     [self.pola_czarnych[i][0] * 100 + 1, self.pola_czarnych[i][1] * 100 + 1, 100, 100],
                                     2)
    def opcje_ruchu(self, bierki, pozycje, czyja_tura):
        moves_list = []
        all_moves_list = []
        for i in range((len(bierki))):
            pozycja = pozycje[i]
            bierka = bierki[i]
            # 3 razy
            if bierka == 't':
                moves_list = self.ruchy_wieza(pozycja, czyja_tura)
            elif bierka == 'r':
                moves_list = self.ruchy_wieza(pozycja, czyja_tura)
            all_moves_list.append(moves_list)
        return all_moves_list
    def ruchy_wieza(self, position, strona):
        moves_list = []
        if strona == 'bialy':
            friends_list = self.pola_bialych
            enemies_list = self.pola_czarnych
        else:
            friends_list = self.pola_czarnych
            enemies_list = self.pola_bialych
        for i in range(4):
            path = True
            chain = 1
            if i == 0:
                x = 0
                y = 1
            elif i == 1:
                x = 0
                y = -1
            elif i == 2:
                x = 1
                y = 0
            else:
                x = -1
                y = 0
            while path:
                if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                        0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                    moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                    if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                        path = False
                    chain += 1
                else:
                    path = False
        return moves_list
    def sprawdz_wsje_ruchy(self):
        if self.etap < 2:
            opcje = self.biale_opcje
        else:
            opcje = self.czarne_opcje
        mozliwosci = opcje[self.tmp]
        return mozliwosci
    def draw_valid(self, moves):
        if self.etap < 2:
            color = 'red'
        else:
            color = 'blue'
        for i in range(len(moves)):
            pygame.draw.circle(self.screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
    def run(self):
        if not os.path.exists(save_path):
            with open(save_path, "w") as f:
                pass
        run = True
        while run:
            if self.winner == 'bialy':
                clear_file(save_path)
                img = pygame.image.load("grafiki/bialy_win.png").convert()
                font = pygame.freetype.Font("font/LaPicaDemo-LaPicaDemo.otf", 86)
                font.render_to(img, (10, 10), "Wygrana bialego", (255, 255, 255))
                screen_rect = self.screen.get_rect()
                img_rect = img.get_rect()
                img_x = screen_rect.centerx - img_rect.width // 2
                img_y = screen_rect.centery - img_rect.height // 2
                self.screen.fill((255, 244, 229))
                self.screen.blit(img, (img_x, img_y))
                pygame.display.update()
                i = 0
                while i < 50:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                main()
                    pygame.time.wait(100)
                    i = i + 1
                main()
            elif self.winner == 'czarny':
                clear_file(save_path)
                img = pygame.image.load("grafiki/czarne_win.png").convert()
                font = pygame.freetype.Font("font/LaPicaDemo-LaPicaDemo.otf", 78)
                font.render_to(img, (10, 10), "Wygrana czarnego", (75, 75, 75))
                screen_rect = self.screen.get_rect()
                img_rect = img.get_rect()
                img_x = screen_rect.centerx - img_rect.width // 2
                img_y = screen_rect.centery - img_rect.height // 2
                self.screen.fill((255, 244, 229))
                self.screen.blit(img, (img_x, img_y))
                pygame.display.update()
                i = 0
                while i < 50:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                main()
                    pygame.time.wait(100)
                    i = i + 1
                main()
            elif self.winner == 'remis':
                clear_file(save_path)
                img = pygame.image.load("grafiki/remis.jpg").convert()
                font = pygame.freetype.Font("font/Komigo3D-Regular.ttf", 300)
                font.render_to(img, (50, 250), "Remis", (147, 112, 219))
                screen_rect = self.screen.get_rect()
                img_rect = img.get_rect()
                img_x = screen_rect.centerx - img_rect.width // 2
                img_y = screen_rect.centery - img_rect.height // 2
                self.screen.fill((255, 244, 229))
                self.screen.blit(img, (img_x, img_y))
                pygame.display.update()
                i = 0
                while i < 50:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                main()
                    pygame.time.wait(100)
                    i = i + 1
                main()
            else:
                self.zegar.tick(self.fps)
                self.screen.fill(self.tlo)
                self.rysuj_szachownice()
                self.rysuj_bierki()
                ile_czarnych_bierek = len(self.czarne_bierki)
                ile_bialych_bierek = len(self.biale_bierki)
                if self.tmp != 100:
                    self.wsje_ruchy = self.sprawdz_wsje_ruchy()
                    self.draw_valid(self.wsje_ruchy)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            main()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                        x_coord = event.pos[0] // 100
                        y_coord = event.pos[1] // 100
                        klik_coords = (x_coord, y_coord)
                        if self.etap <= 1:
                            # nie istniejacy przycisk poddawania sie xd
                            if klik_coords == (8, 8) or klik_coords == (9, 8):
                                print('surrender bialych')
                                self.winner = 'czarny'
                            if klik_coords in self.pola_bialych:
                                self.tmp = self.pola_bialych.index(klik_coords)
                                if self.etap == 0:
                                    self.etap = 1
                            if klik_coords in self.wsje_ruchy and self.tmp != 100:
                                self.pola_bialych[self.tmp] = klik_coords
                                if klik_coords in self.pola_czarnych:
                                    black_piece = self.pola_czarnych.index(klik_coords)
                                    self.zbite_biale.append(self.czarne_bierki[black_piece])
                                    self.czarne_bierki.pop(black_piece)
                                    self.pola_czarnych.pop(black_piece)
                                    self.counter_draw_moves = 0
                                self.czarne_opcje = self.opcje_ruchu(self.czarne_bierki, self.pola_czarnych, 'czarny')
                                self.biale_opcje = self.opcje_ruchu(self.biale_bierki, self.pola_bialych, 'bialy')
                                if len(self.biale_bierki) == len(self.czarne_bierki):
                                    self.counter_draw_moves += 1
                                self.etap = 2
                                self.tmp = 100
                                self.wsje_ruchy = []
                                save_lists_to_file(self.pola_bialych, self.pola_czarnych, self.etap, save_path)
                                # print("zapisuje")
                                # print(self.etap)
                                # print("czarny")
                        if self.etap > 1:
                            if len(self.czarne_bierki) == 0:
                                self.winner = 'bialy'
                            if klik_coords in self.pola_czarnych:
                                self.tmp = self.pola_czarnych.index(klik_coords)
                                if self.etap == 2:
                                    self.etap = 3
                            if klik_coords in self.wsje_ruchy and self.tmp != 100:
                                self.pola_czarnych[self.tmp] = klik_coords
                                if klik_coords in self.pola_bialych:
                                    biala_bierka = self.pola_bialych.index(klik_coords)
                                    self.zbite_czarne.append(self.biale_bierki[biala_bierka])
                                    if len(self.biale_bierki) == 0:
                                        self.winner = 'czarny'
                                    self.biale_bierki.pop(biala_bierka)
                                    self.pola_bialych.pop(biala_bierka)
                                self.czarne_opcje = self.opcje_ruchu(self.czarne_bierki, self.pola_czarnych, 'czarny')
                                self.biale_opcje = self.opcje_ruchu(self.biale_bierki, self.pola_bialych, 'bialy')
                                self.etap = 0
                                self.tmp = 100
                                self.wsje_ruchy = []
                                if (len(self.biale_bierki) == ile_bialych_bierek and len(self.czarne_bierki) == ile_czarnych_bierek):
                                    self.counter_draw_moves += 1
                                else:
                                    self.counter_draw_moves = 0
                                save_lists_to_file(self.pola_bialych, self.pola_czarnych, self.etap, save_path)
                                # print("zapisuje")
                                # print(self.etap)
                                # print("bialy")
                                # print(self.pola_bialych)
                                # print(self.pola_czarnych)

                    if len(self.biale_bierki) == 0:
                        self.winner = 'czarny'
                    if self.counter_draw_moves == 6:
                        self.winner = 'remis'
                        clear_file(save_path)
                        #print("Remis")
                pygame.display.flip()

        pygame.quit()
        sys.exit()



class Button():
    def __init__(self, text, width, height, pos, elevation, color, hover):
        self.elevation = elevation
        self.original_y_pos = pos[1]
        self.color = color
        self.hover = hover
        self.clicked = False
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = color
        self.bottom_rect = pygame.Rect(pos,(width,height))
        font = pygame.font.Font('font/CampanaScript_PERSONAL_USE_ONLY.otf', 90)
        self.text_surf = font.render(text,True,(255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.name = text
        # test
        self.name_chess_pieces = "Nowoczesne"
        self.name_color_board = "Drewno"
        self.tmp_name_chess_pieces = ""
    def window_settings(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gra-Wiezami-Ustawienia")
        button_width = 250
        button_length = 100
        position_x = (WIDTH - button_width) / 2
        position_y = 175
        font = self.name_chess_pieces
        if os.path.isfile('font.txt'):
            font = load_font_from_file('font.txt')
        figure = Figure(font)
        figure.rysuj_bierke()
        chess_pieces_button = Button(font, button_width, button_length, (position_x, position_y), 20,
                             (128, 128, 255, 128), (255, 128, 255, 128))
        back_button = Button("Powrot", button_width, button_length, (position_x, position_y + 125), 20,
                             (128, 128, 255, 128), (255, 128, 255, 128))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.display.set_caption("Gra-Wiezami")
                        main()
            background_image = pygame.image.load("grafiki/tlo.png").convert()
            screen.fill((255, 255, 255))
            screen.blit(background_image, (0, 0))
            screen.blit(figure.rysuj_bierke()[0], figure.rysuj_bierke()[1])
            back_button.draw_button(screen)
            chess_pieces_button.draw_button(screen)
            pygame.display.update()

    def check_action(self):
        if self.name == "Nowa Gra":
            f = open("settings.txt", "r")
            chess_pieces = f.read()
            f.close()
            if os.path.exists(save_path):
                os.remove(save_path)
            game = Game(chess_pieces, False)
            game.run()
        elif self.name == "Wznow Gre":
            f = open("settings.txt", "r")
            chess_pieces = f.read()
            f.close()
            game = Game(chess_pieces, True)
            game.run()
        elif self.name == "Zasady":
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Gra-Wiezami-Zasady")
            screen.fill('wheat3')

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            pygame.display.set_caption("Gra-Wiezami")
                            main()

                background_image = pygame.image.load("grafiki/Zasady.png").convert()
                screen_rect = screen.get_rect()
                image_rect = background_image.get_rect()
                image_x = screen_rect.centerx - image_rect.width // 2
                image_y = screen_rect.centery - image_rect.height // 2
                screen.fill((255, 244, 229))
                screen.blit(background_image,(image_x, image_y-125))
                pygame.display.update()
        elif self.name == "Ustawienia":
            self.window_settings()
        elif self.name in ["Nowoczesne", "Przypadki", "Maya", "Alfa", "Condal", "Leipzig"]:
            names = ["Przypadki", "Maya", "Alfa", "Condal", "Leipzig", "Nowoczesne"]
            index = (names.index(self.name) + 1) % len(names)
            save_font_to_file(names[index], 'font.txt')
            self.name_chess_pieces = names[index]
            self.window_settings()
        elif self.name == "Plansza":
            print("plansza")
        elif self.name == "Powrot":
            main()
        elif self.name == "Wyjscie":
            pygame.quit()
            sys.exit()

    def draw_button(self, screen):
        action = False
        pos = pygame.mouse.get_pos()
        top_rect = self.top_rect.copy()
        bottom_rect = self.bottom_rect.copy()
        bottom_rect.x += 20
        bottom_rect.y += 20
        if top_rect.collidepoint(pos):
            self.top_color = self.hover
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                bottom_rect.inflate_ip(self.elevation, self.elevation)
                top_rect.inflate_ip(self.elevation, self.elevation)

            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
                self.check_action()
            self.top_color = self.hover
        else:
            self.top_color = self.color

        bottom_surf = pygame.Surface(bottom_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(bottom_surf, 0, (0, 0, *bottom_rect.size), border_radius = 12)
        screen.blit(bottom_surf, bottom_rect.topleft)

        top_surf = pygame.Surface(top_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(top_surf, self.top_color, (0, 0, *top_rect.size), border_radius = 12)
        screen.blit(top_surf, top_rect.topleft)

        screen.blit(self.text_surf, self.text_rect)
        return action

if __name__ == "__main__":
    main()
