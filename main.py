import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
WINDOW_TITLE = "Rook-Game"
pygame.display.set_caption(WINDOW_TITLE)
icon = pygame.image.load('grafiki/icon.png')
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

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
        font = pygame.font.SysFont('rockwell', 50)
        self.text_surf = font.render(text,True,(255,255,255))
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.name = text
    def check_action(self):
        if self.name == "Play":
            game = Game()
            game.run()
        elif self.name == "Load":
            print("Wczytanie zapisanych")
            # tu bedzie zrobic zapisy wszystkie
        elif self.name == "Rules":
            print("Zasady")
            # tu trzeba bedzie dopisac
        elif self.name == "Settings":
            print("Ustawienia")
            # tutaj przyciski z ustawieniami
        elif self.name == "Quit":
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

def main():
    start_button = Button("Play", 250, 125, (300, 25), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    load_button = Button("Load", 250, 125, (300, 175), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    rules_button = Button("Rules", 250, 125, (300, 325), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    settings_button = Button("Settings", 250, 125, (300, 475), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    quit_button = Button("Quit", 250, 125, (300, 625), 20, (128, 128, 255, 128), (255, 128, 255, 128))
    background_image = pygame.image.load("grafiki/tlo.png").convert()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        WIN.fill((255, 255, 255))
        WIN.blit(background_image, (0, 0))
        start_button.draw_button(WIN)
        load_button.draw_button(WIN)
        rules_button.draw_button(WIN)
        settings_button.draw_button(WIN)
        quit_button.draw_button(WIN)
        pygame.display.update()

class Game:
    def __init__(self):
        #pygame.init()

        self.SZER = 800
        self.WYS = 800
        self.screen = pygame.display.set_mode([self.SZER, self.WYS])
        self.font = pygame.font.Font('font/Truecat.ttf', 50)
        self.zegar = pygame.time.Clock()
        self.fps = 60
        self.tlo = 'wheat3'
        self.kolor_jasny = 'wheat'
        self.kolor_ciemny = 'wheat1'
        self.WINDOW_TITLE = "Rook-Game"
        pygame.display.set_caption(self.WINDOW_TITLE)
        self.icon = pygame.image.load('grafiki/icon.png')
        pygame.display.set_icon(self.icon)

        self.etap = 0
        self.wsje_ruchy = []

        self.biale_grafiki = [pygame.transform.scale(pygame.image.load('grafiki/biala.png'), (80, 80))]
        self.czarne_grafiki = [pygame.transform.scale(pygame.image.load('grafiki/czarna.png'), (80, 80))]

        self.pola_bialych = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
        self.pola_czarnych = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

        self.bierki = ['W']
        self.zbite_biale = []
        self.zbite_czarne = []

        self.biale_bierki = []
        self.czarne_bierki = []

        for i in range(16):
            self.biale_bierki.append('W')
            self.czarne_bierki.append('W')

        self.tmp = 100
        self.counter = 0
        self.winner = ''
        self.game_over = False

        self.strona = 'bialy'
        if self.strona == 'bialy':
            self.na_oborot()

        self.biale_opcje = self.opcje_ruchu(self.biale_bierki, self.pola_bialych, 'bialy')
        self.czarne_opcje = self.opcje_ruchu(self.czarne_bierki, self.pola_czarnych, 'czarny')

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

            tekst = ['Ruch bialego', 'Kaj jedzie bialy?', 'Ruch czarnego', 'Kaj jedzie czarny?']
            self.screen.blit(self.font.render(tekst[self.etap], True, 'wheat4'), (40, self.WYS - 400))

    def rysuj_bierki(self):
        for i in range(len(self.biale_bierki)):
            index = self.bierki.index(self.biale_bierki[i])
            self.screen.blit(self.biale_grafiki[index], (self.pola_bialych[i][0] * 100 + 10, self.pola_bialych[i][1] * 100 + 10))
            if self.etap < 2:
                if self.tmp == i:
                    pygame.draw.rect(self.screen, 'red', [self.pola_bialych[i][0] * 100 + 1, self.pola_bialych[i][1] * 100 + 1, 100, 100], 2)
        for i in range(len(self.czarne_bierki)):
            index = self.bierki.index(self.czarne_bierki[i])
            self.screen.blit(self.czarne_grafiki[index], (self.pola_czarnych[i][0] * 100 + 10, self.pola_czarnych[i][1] * 100 + 10))
            if self.etap >= 2:
                if self.tmp == i:
                    pygame.draw.rect(self.screen, 'blue', [self.pola_czarnych[i][0] * 100 + 1, self.pola_czarnych[i][1] * 100 + 1, 100, 100], 2)

    def opcje_ruchu(self, bierki, pozycje, czyja_tura):
        moves_list = []
        all_moves_list = []
        for i in range((len(bierki))):
            pozycja = pozycje[i]
            bierka = bierki[i]
            if bierka == 'W':
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
        run = True
        while run:
            self.zegar.tick(self.fps)
            self.screen.fill(self.tlo)

            self.rysuj_szachownice()
            self.rysuj_bierki()

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
                        if klik_coords == (8, 8) or klik_coords == (9, 8):
                            print('surrender bialych')
                            self.winner = 'black'
                        if klik_coords in self.pola_bialych:
                            self.tmp = self.pola_bialych.index(klik_coords)
                            if self.etap == 0:
                                self.etap = 1
                        if klik_coords in self.wsje_ruchy and self.tmp != 100:
                            self.pola_bialych[self.tmp] = klik_coords
                            if klik_coords in self.pola_czarnych:
                                black_piece = self.pola_czarnych.index(klik_coords)
                                self.zbite_biale.append(self.czarne_bierki[black_piece])
                                if self.czarne_bierki[black_piece] == 'king':
                                    self.winner = 'white'
                                self.czarne_bierki.pop(black_piece)
                                self.pola_czarnych.pop(black_piece)
                            self.czarne_opcje = self.opcje_ruchu(self.czarne_bierki, self.pola_czarnych, 'czarny')
                            self.biale_opcje = self.opcje_ruchu(self.biale_bierki, self.pola_bialych, 'bialy')
                            self.etap = 2
                            self.tmp = 100
                            self.wsje_ruchy = []
                    if self.etap > 1:
                        if klik_coords == (8, 8) or klik_coords == (9, 8):
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
                                    self.winner = 'black'
                                    print(self.winner)
                                self.biale_bierki.pop(biala_bierka)
                                self.pola_bialych.pop(biala_bierka)
                            self.czarne_opcje = self.opcje_ruchu(self.czarne_bierki, self.pola_czarnych, 'czarny')
                            self.biale_opcje = self.opcje_ruchu(self.biale_bierki, self.pola_bialych, 'bialy')
                            self.etap = 0
                            self.tmp = 100
                            self.wsje_ruchy = []

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()
