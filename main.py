import pygame
import random

from sprites import Spritesheet

# inicializando a biblioteca
pygame.init()
# pygame.mixer.init()

# inicializando a tela
screen = pygame.display.set_mode((900, 600), 0)

# cores para o desenho
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERDE = (0, 100, 0)
MARROMT = (150, 75, 0, 99)
AZULE = (0, 0, 139)
CINZA = (211, 211, 211)
CINZAET = (128, 128, 128, 100)


class Cenario:
    def __init__(self, tamanho, bat, sprites):
        self.sprites = sprites
        self.bat = bat
        self.tamanho = tamanho
        # , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        # , 2, 2, 2, 2, 2
        # , 3, 3, 3, 3, 3
        self.matriz = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
             2, 2, 2, 2, 2, 2, 2, 2, 2],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
             3, 3, 3, 3, 3, 3, 3, 3, 3],
        ]

    def calcular_regras(self, col_int, lin_int):
        if 0 <= col_int < 1 and 0 <= lin_int < 3:
            if self.matriz[lin_int][col_int] != 0:
                bat.aceitar_movimento()

    def pintar_linha(self, tela, l, linha):
        for c, coluna in enumerate(linha):
            x = c * self.tamanho / 10
            y = l * self.tamanho
            cor = PRETO
            if coluna == 2:
                cor = AZULE
            pygame.draw.rect(tela, cor, (x, y, self.tamanho / 10, self.tamanho), 0)
            if coluna == 1:
                for f in range(9):
                    pygame.draw.circle(tela, AMARELO, (x + self.tamanho / 20, y + ((self.tamanho / 10) * (f + 1))),
                                       self.tamanho // 100.0)
            if coluna == 3:
                cor = VERDE
                pygame.draw.rect(tela, cor, (x, y, self.tamanho / 10, self.tamanho), 0)

    def pintar(self, tela):
        myfont = pygame.font.SysFont("Comic Sans MS", 50)
        # apply it to text on a label
        label = myfont.render(str(bat.pontos), True, BRANCO)
        # put the label object on the screen at point x=100, y=100
        for l, linha in enumerate(self.matriz):
            self.pintar_linha(tela, l, linha)
        screen.blit(label, (450, 25))


class Morcego:
    # construtor
    def __init__(self, tamanho, sprites):
        # posição que será desenhado
        self.sprites = sprites
        self.coluna = 0
        self.linha = 1
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.centro_x = 100
        self.centro_y = 300
        self.tamanho = tamanho
        self.raio = int(self.tamanho / 2)
        self.mode = 1
        self.pontos = 0
        # velocidade
        self.vel_x = 0
        self.vel_y = 0

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def aceitar_movimento(self):
        descer = pygame.mixer.Sound("descendo.wav")
        subir = pygame.mixer.Sound("subindo.wav")
        if self.linha_intencao > self.linha:
            pygame.mixer.Sound.play(descer)
        elif self.linha_intencao < self.linha:
            pygame.mixer.Sound.play(subir)
        self.coluna = self.coluna_intencao
        self.linha = self.linha_intencao

    def pintar(self, tela):
        # corpo
        # Pré morcego
        """
        pygame.draw.circle(tela, CINZA, (self.centro_x, self.centro_y), self.raio / 1, 0)
        pe = (self.centro_x, self.centro_y + self.raio)
        asa1 = (self.centro_x - self.raio, self.centro_y)
        asa2 = (self.centro_x + self.raio, self.centro_y)
        pontos = [pe, asa1, asa2]
        pygame.draw.polygon(tela, MARROM, pontos, 0)
        """
        # Tentativas de mexer com o sprite
        # batpy1 = pygame.transform.smoothscale(self.sprites.parse_sprite(self.mode, 0), (250, 250))
        # batpy1 = pygame.transform.rotozoom(self.sprites.parse_sprite(self.mode, 0), 0, 15)
        #batpy1 =pygame.transform.scale2x(pygame.transform.scale2x(pygame.transform.scale2x(pygame.transform.scale2x(
        #self.sprites.parse_sprite(self.mode, 0)))))
        batpy1 = pygame.transform.scale(self.sprites.parse_sprite(self.mode, 0), (250, 250))
        pygame.display.flip()
        tela.blit(batpy1, (self.centro_x - self.raio * 1.3, self.centro_y - self.raio))
        if self.mode == 1:
            self.mode = 0
        else:
            self.mode = 1
        pygame.display.flip()

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.vel_y = -1
                if e.key == pygame.K_DOWN:
                    self.vel_y = 1
                if e.key == pygame.K_w:
                    self.vel_y = -1
                if e.key == pygame.K_s:
                    self.vel_y = 1
                if e.key == pygame.K_ESCAPE:
                    e.type = pygame.QUIT

            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    self.vel_y = 0
                if e.key == pygame.K_DOWN:
                    self.vel_y = 0
                if e.key == pygame.K_w:
                    self.vel_y = 0
                if e.key == pygame.K_s:
                    self.vel_y = 0


class Inimigos:
    # construtor
    def __init__(self, tamanho, bat, sprites):
        # posição que será desenhado
        self.sprites = sprites
        self.bat = bat
        self.tipo = random.randint(1, 3)
        self.tamanho = tamanho
        self.raio = int(self.tamanho / 8)
        self.ponto_x = 400
        self.ponto_y = 0
        self.calcular_regras()
        # velocidade
        self.vel_x = 30
        self.vel_y = 0

    def calcular_regras(self):
        # 600 = 400
        # 900 = 1000 ~ 800/700 tb serve
        if self.tipo == 0:
            bat.pontos = bat.pontos + 1
            self.vel_x = self.vel_x + 2
            if self.vel_x > 60:
                self.vel_x = self.vel_x - 1
            self.tipo = random.randint(1, 3)
        if self.tipo == 3:
            self.ponto_y = 400
            self.ponto_x = 1000
        if self.tipo == 2:
            self.ponto_y = 200
            self.ponto_x = 1000
        if self.tipo == 1:
            self.ponto_y = 0
            self.ponto_x = 1000

    def pintar(self, tela):
        if self.tipo == 3:
            # pygame.draw.circle(tela, CINZA, ( self.ponto_x + self.tamanho / 8, self.ponto_y + self.tamanho / 2),
            # self.raio)
            pedra = pygame.transform.scale(self.sprites.parse_sprite(3, 0), (250, 256))
            # pygame.display.flip()
            tela.blit(pedra, (self.ponto_x - 32, self.ponto_y))
        if self.tipo == 2:
            rest = pygame.draw.rect(screen, MARROMT, (
                self.ponto_x, self.ponto_y + self.tamanho * 0.8, self.tamanho - 13, self.tamanho * 1.2))
            tronco = pygame.transform.scale(self.sprites.parse_sprite(2, 0), (250, 256))
            # pygame.display.flip()
            tela.blit(tronco, (self.ponto_x - 32, self.ponto_y))
        if self.tipo == 1:
            pygame.draw.rect(tela, CINZAET, (self.ponto_x, self.ponto_y + self.tamanho * 0.7, self.tamanho - 28,
                                             self.tamanho * 2.3))
            pararaio = pygame.transform.scale(self.sprites.parse_sprite(4, 0), (250, 256))
            # pygame.display.flip()
            tela.blit(pararaio, (self.ponto_x - 32, self.ponto_y - 32))

    def processar_eventos(self, e):
        # 163 cabeça , 190 asa, -200 tras asa, -173?
        crash_sound = pygame.mixer.Sound("dirsom.wav")
        surge_sound = pygame.mixer.Sound("esqsom.wav")
        # self.processar_som(e)
        if self.ponto_x > -250 and self.tipo != 0:
            self.ponto_x = self.ponto_x - self.vel_x
            if self.ponto_x > -150:
                if bat.linha == self.tipo - 1:
                    self.processar_som(e)
                    # pygame.mixer.Sound.play(crash_sound)
                    if self.ponto_x < 163:
                        pygame.mixer.Sound.play(surge_sound)
                        exit()
        else:
            self.tipo = 0
            pygame.mixer.Sound.play(surge_sound)
            # pygame.mixer.Sound.play(crash_sound)
            self.calcular_regras()

    def processar_som(self, eventos):
        # pygame.mixer.music.load("dirsom.wav")
        crash_sound = pygame.mixer.Sound("dirsom.wav")
        surge_sound = pygame.mixer.Sound("esqsom.wav")
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    # pygame.mixer.Sound.play(surge_sound)
                    pygame.mixer.Sound.play(crash_sound)
                    '''if bat.linha == self.tipo - 1:
                        #pygame.time.delay(1000)
                        #pygame.mixer.Sound.play(surge_sound)
                        pygame.mixer.Sound.play(crash_sound)'''


if __name__ == "__main__":
    size = 600 // 3
    escuro = 0
    pause = 0
    spritesheet = Spritesheet('spritesheet.png')
    bat = Morcego(size, spritesheet)
    obstaculo = Inimigos(size, bat, spritesheet)
    cenario = Cenario(size, bat, spritesheet)
    # crash_sound = pygame.mixer.Sound("dirsom.wav")
    surge_sound = pygame.mixer.Sound("esqsom.wav")
    subir = pygame.mixer.Sound("subindo.wav")
    descer = pygame.mixer.Sound("descendo.wav")
    pygame.mixer.Sound.play(surge_sound)
    while True:
        # Calcular as Regras
        # obstaculo.calcular_regras()
        if pause == 0:
            bat.calcular_regras()
            cenario.calcular_regras(bat.coluna_intencao, bat.linha_intencao)
        # Pintar a tela
        screen.fill(PRETO)
        if escuro == 0:
            cenario.pintar(screen)
            obstaculo.pintar(screen)
            bat.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Captura de eventos
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if pause == 0:
                        pause = 1
                    else:
                        pause = 0
                if e.key == pygame.K_e:
                    if escuro == 0:
                        escuro = 1
                    else:
                        escuro = 0
            if e.type == pygame.QUIT:
                exit()
        if pause == 0:
            bat.processar_eventos(eventos)
            obstaculo.processar_eventos(eventos)
