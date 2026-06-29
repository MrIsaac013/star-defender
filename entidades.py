import pygame
import random
import math
from config import LARGURA, ALTURA, carregar_imagem


# ======================================================
# JOGADOR
# ======================================================
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = carregar_imagem("nave_jogador.png", (64, 64))
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA // 2
        self.rect.bottom = ALTURA - 20

        self.velocidade = 6
        self.vidas = 3
        self.pontuacao = 0

        self.cooldown_tiro = 250  # milissegundos entre tiros
        self.ultimo_tiro = 0

        # invulnerabilidade temporaria apos receber dano
        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.duracao_invulneravel = 1200

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            self.rect.y += self.velocidade

        # mantem o jogador dentro da tela
        self.rect.clamp_ip(pygame.Rect(0, 0, LARGURA, ALTURA))

    def pode_atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown_tiro:
            self.ultimo_tiro = agora
            return True
        return False

    def receber_dano(self):
        if self.invulneravel:
            return False
        self.vidas -= 1
        self.invulneravel = True
        self.tempo_invulneravel = pygame.time.get_ticks()
        return True

    def atualizar_invulnerabilidade(self):
        if self.invulneravel:
            agora = pygame.time.get_ticks()
            if agora - self.tempo_invulneravel >= self.duracao_invulneravel:
                self.invulneravel = False

    def desenhar_com_efeito(self, tela):
        """Pisca a nave enquanto estiver invulneravel."""
        if self.invulneravel:
            piscar = (pygame.time.get_ticks() // 100) % 2 == 0
            if piscar:
                tela.blit(self.image, self.rect)
        else:
            tela.blit(self.image, self.rect)


# ======================================================
# TIRO DO JOGADOR
# ======================================================
class TiroJogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = carregar_imagem("tiro_jogador.png", (8, 24))
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.velocidade = -11

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()


# ======================================================
# TIRO INIMIGO
# ======================================================
class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = carregar_imagem("tiro_inimigo.png", (8, 20))
        self.rect = self.image.get_rect(centerx=x, top=y)
        self.velocidade = 6

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.kill()


# ======================================================
# INIMIGO (drone ou caça)
# ======================================================
class Inimigo(pygame.sprite.Sprite):
    def __init__(self, tipo="drone", dificuldade=1.0):
        super().__init__()
        self.tipo = tipo

        if tipo == "drone":
            self.image = carregar_imagem("inimigo_drone.png", (48, 48))
            self.velocidade_y = random.uniform(1.5, 2.5) * dificuldade
            self.pontos = 10
            self.chance_atirar = 0.004
        else:  # caça (mais rápido, zigue-zague)
            self.image = carregar_imagem("inimigo_caca.png", (40, 40))
            self.velocidade_y = random.uniform(2.5, 3.5) * dificuldade
            self.pontos = 20
            self.chance_atirar = 0.008

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - self.rect.width)
        self.rect.y = random.randint(-150, -40)

        self.direcao_x = random.choice([-1, 1])
        self.amplitude = random.randint(40, 90)
        self.centro_x = self.rect.x
        self.angulo = random.uniform(0, math.pi * 2)

    def update(self):
        self.rect.y += self.velocidade_y

        if self.tipo == "caca":
            self.angulo += 0.05
            self.rect.x = self.centro_x + int(math.sin(self.angulo) * self.amplitude)

        if self.rect.top > ALTURA:
            self.kill()

    def tentar_atirar(self):
        return random.random() < self.chance_atirar


# ======================================================
# METEORO (obstaculo neutro, sem atirar)
# ======================================================
class Meteoro(pygame.sprite.Sprite):
    def __init__(self, dificuldade=1.0):
        super().__init__()
        tamanho = random.randint(32, 56)
        self.image = carregar_imagem("meteoro.png", (tamanho, tamanho))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, LARGURA - tamanho)
        self.rect.y = random.randint(-150, -40)

        self.velocidade_y = random.uniform(2.0, 4.0) * dificuldade
        self.velocidade_rotacao = random.uniform(-3, 3)
        self.angulo = 0
        self.imagem_original = self.image
        self.pontos = 5

    def update(self):
        self.rect.y += self.velocidade_y
        self.angulo += self.velocidade_rotacao
        centro = self.rect.center
        self.image = pygame.transform.rotate(self.imagem_original, self.angulo)
        self.rect = self.image.get_rect(center=centro)

        if self.rect.top > ALTURA:
            self.kill()


# ======================================================
# EFEITO DE EXPLOSAO (visual, sem colisao)
# ======================================================
class Explosao(pygame.sprite.Sprite):
    def __init__(self, centro, tamanho=50):
        super().__init__()
        img_base = carregar_imagem("explosao.png", (tamanho, tamanho))
        self.frames = []
        # cria efeito de "encolher e desaparecer" a partir da imagem base
        for i in range(6):
            escala = max(4, tamanho - i * 8)
            alpha_img = pygame.transform.scale(img_base, (escala, escala)).copy()
            alpha_img.set_alpha(255 - i * 40)
            self.frames.append(alpha_img)

        self.indice = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=centro)
        self.centro = centro
        self.contador_tempo = 0
        self.velocidade_animacao = 4  # frames do jogo por frame de animação

    def update(self):
        self.contador_tempo += 1
        if self.contador_tempo >= self.velocidade_animacao:
            self.contador_tempo = 0
            self.indice += 1
            if self.indice >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.indice]
                self.rect = self.image.get_rect(center=self.centro)
