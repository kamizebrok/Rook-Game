import pygame

pygame.init()

SZER = 1000
WYS = 900
screen = pygame.display.set_mode([SZER, WYS])
font = pygame.font.Font('font/Truecat.ttf', 50)
zegar = pygame.time.Clock()
fps = 60

tlo = 'wheat3'
kolor_jasny = 'wheat'
kolor_ciemny = 'wheat1'

etap = 0
wsje_ruchy = []
biala_wieza = pygame.image.load('grafiki/biala.png')
biala_wieza = pygame.transform.scale(biala_wieza, (80, 80))
czarna_wieza = pygame.image.load('grafiki/czarna.png')
czarna_wieza = pygame.transform.scale(czarna_wieza, (80, 80))

biale_grafiki = [biala_wieza]
czarne_grafiki = [czarna_wieza]

biale_bierki = []
czarne_bierki = []

pola_bialych = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
pola_czarnych = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

bierki = ['W']
zbite_biale = []
zbite_czarne = []

for i in range(16):
    biale_bierki.append('W')
    czarne_bierki.append('W')

tmp = 100
counter = 0
winner = ''
game_over = False

def na_oborot(pola_bialych, pola_czarnych):
    yeet = []
    for j in range(len(pola_czarnych)):
        yeet.append(pola_czarnych[j])
        pola_czarnych[j] = pola_bialych[j]
        pola_bialych[j] = yeet[j]

def rysuj_szachownice():
    for i in range(32):
        kolumna = i % 4
        wiersz = i // 4
        if wiersz % 2 == 0:
            pygame.draw.rect(screen, kolor_jasny, [600 - (kolumna * 200), wiersz * 100, 100, 100])
        else:
            pygame.draw.rect(screen, kolor_ciemny, [700 - (kolumna * 200), wiersz * 100, 100, 100])

        pygame.draw.rect(screen, 'wheat3', [0, 800, SZER, 100])
        pygame.draw.rect(screen, 'wheat4', [0, 800, SZER, 100], 5)
        pygame.draw.rect(screen, 'wheat4', [800, 0, 200, WYS], 5)

        tekst = ['Ruch bialego', 'Gdzie rusza bialy?', 'Ruch czarnego', 'Gdzie rusza czarny?']
        screen.blit(font.render(tekst[etap], True, 'wheat4'), (40,WYS - 80))

def rysuj_bierki():
    for i in range(len(biale_bierki)):
        index = bierki.index(biale_bierki[i])
        screen.blit(biale_grafiki[index], (pola_bialych[i][0] * 100 + 10, pola_bialych[i][1] * 100 + 10))
        if etap < 2:
            if tmp == i:
                pygame.draw.rect(screen, 'red', [pola_bialych[i][0] * 100 + 1, pola_bialych[i][1] * 100 + 1, 100, 100], 2)
    for i in range(len(czarne_bierki)):
        index = bierki.index(czarne_bierki[i])
        screen.blit(czarne_grafiki[index], (pola_czarnych[i][0] * 100 + 10, pola_czarnych[i][1] * 100 + 10))
        if etap >= 2:
            if tmp == i:
                pygame.draw.rect(screen, 'blue', [pola_czarnych[i][0] * 100 + 1, pola_czarnych[i][1] * 100 + 1, 100, 100], 2)

def opcje_ruchu(bierki, pozycje, czyja_tura):
    moves_list = []
    all_moves_list = []
    for i in range((len(bierki))):
        pozycja = pozycje[i]
        bierka = bierki[i]
        if bierka == 'W':
            moves_list = ruchy_wieza(pozycja, czyja_tura)
        all_moves_list.append(moves_list)
    return all_moves_list

def ruchy_wieza(position, strona):
    moves_list = []
    if strona == 'bialy':
        enemies_list = pola_czarnych
        friends_list = pola_bialych
    else:
        friends_list = pola_czarnych
        enemies_list = pola_bialych
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

def sprawdz_wsje_ruchy():
    if etap < 2:
        opcje = biale_opcje
    else:
        opcje = czarne_opcje
    mozliwosci = opcje[tmp]
    return mozliwosci

def draw_valid(moves):
    if etap < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

strona = 'bialy'
if strona == 'bialy':
    na_oborot(pola_bialych, pola_czarnych)

biale_opcje = opcje_ruchu(biale_bierki, pola_bialych, 'bialy')
czarne_opcje = opcje_ruchu(czarne_bierki, pola_czarnych, 'czarny')
run = True
while run:
    zegar.tick(fps)
    screen.fill(tlo)

    rysuj_szachownice()
    rysuj_bierki()

    if tmp != 100:
        wsje_ruchy = sprawdz_wsje_ruchy()
        draw_valid(wsje_ruchy)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            klik_coords = (x_coord, y_coord)
            if etap <= 1:
                if klik_coords == (8, 8) or klik_coords == (9, 8):
                    print('surrender bialych')
                    winner = 'black'
                if klik_coords in pola_bialych:
                    tmp = pola_bialych.index(klik_coords)
                    if etap == 0:
                        etap = 1
                if klik_coords in wsje_ruchy and tmp != 100:
                    pola_bialych[tmp] = klik_coords
                    if klik_coords in pola_czarnych:
                        black_piece = pola_czarnych.index(klik_coords)
                        captured_pieces_white.append(czarne_bierki[black_piece])
                        if czarne_bierki[black_piece] == 'king':
                            winner = 'white'
                        czarne_bierki.pop(black_piece)
                        pola_czarnych.pop(black_piece)
                    czarne_opcje = opcje_ruchu(czarne_bierki, pola_czarnych, 'czarny')
                    biale_opcje = opcje_ruchu(biale_bierki, pola_bialych, 'bialy')
                    etap = 2
                    tmp = 100
                    wsje_ruchy = []
            if etap > 1:
                if klik_coords == (8, 8) or klik_coords == (9, 8):
                    winner = 'bialy'
                if klik_coords in pola_czarnych:
                    tmp = pola_czarnych.index(klik_coords)
                    if etap == 2:
                        etap = 3
                if klik_coords in wsje_ruchy and tmp != 100:
                    pola_czarnych[tmp] = klik_coords
                    if klik_coords in pola_bialych:
                        biala_bierka = pola_bialych.index(klik_coords)
                        captured_pieces_black.append(biale_bierki[biala_bierka])
                        if len(biale_bierki) == 0:
                            winner = 'black'
                            print(winner)
                        biale_bierki.pop(biala_bierka)
                        pola_bialych.pop(biala_bierka)
                    czarne_opcje = opcje_ruchu(czarne_bierki, pola_czarnych, 'black')
                    biale_opcje = opcje_ruchu(biale_bierki, pola_bialych, 'white')
                    etap = 0
                    tmp = 100
                    wsje_ruchy = []
    pygame.display.flip()
pygame.quit()