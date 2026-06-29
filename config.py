import pygame
import os
import sys


# ----------------------------------------------------------------
# CAMINHO BASE (relativo a este arquivo) - evita erro de URL/asset
# ----------------------------------------------------------------
def _detectar_base_dir():

    if getattr(sys, "frozen", False):
        # Executavel gerado pelo PyInstaller: usa a pasta onde o .exe esta.
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = _detectar_base_dir()


def caminho_asset(*partes):
    """Monta um caminho relativo seguro para qualquer asset do jogo."""
    return os.path.join(BASE_DIR, "assets", *partes)


# ----------------------------------------------------------------
# CONFIGURACOES GERAIS
# ----------------------------------------------------------------
LARGURA, ALTURA = 800, 600
FPS = 60

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL_CLARO = (80, 200, 255)
AMARELO = (255, 210, 60)
VERMELHO = (220, 70, 90)
VERDE = (90, 220, 130)
CINZA = (140, 150, 170)

PONTOS_PARA_VENCER = 500
VIDAS_INICIAIS = 3


pygame.init()

SOM_DISPONIVEL = True
try:
    pygame.mixer.init()
except pygame.error:
    SOM_DISPONIVEL = False
    print("Aviso: nao foi possivel inicializar o audio. O jogo vai rodar sem som.")

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Star Defender")
relogio = pygame.time.Clock()

# ----------------------------------------------------------------
# FONTES
# ----------------------------------------------------------------
fonte_titulo = pygame.font.SysFont("arial", 64, bold=True)
fonte_grande = pygame.font.SysFont("arial", 40, bold=True)
fonte_media = pygame.font.SysFont("arial", 26)
fonte_pequena = pygame.font.SysFont("arial", 20)


def carregar_imagem(nome, escala=None):
    caminho = caminho_asset("imagens", nome)
    img = pygame.image.load(caminho).convert_alpha()
    if escala:
        img = pygame.transform.scale(img, escala)
    return img


class SomFalso:
    """Objeto substituto usado quando o audio nao esta disponivel.
    Possui os mesmos metodos de um Sound, mas nao faz nada."""
    def play(self):
        pass

    def set_volume(self, valor):
        pass


def carregar_som(nome):
    if not SOM_DISPONIVEL:
        return SomFalso()
    try:
        caminho = caminho_asset("sons", nome)
        return pygame.mixer.Sound(caminho)
    except pygame.error:
        return SomFalso()
