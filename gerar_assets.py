import pygame
import math
import random

pygame.init()

PASTA = "assets/imagens"

def salvar(surface, nome):
    pygame.image.save(surface, f"{PASTA}/{nome}")
    print(f"Gerado: {nome}")

# ---------- NAVE DO JOGADOR ----------
def criar_nave_jogador():
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    # corpo principal (triangulo estilizado)
    pygame.draw.polygon(surf, (80, 200, 255), [(32, 4), (12, 56), (32, 44), (52, 56)])
    pygame.draw.polygon(surf, (20, 120, 200), [(32, 4), (12, 56), (32, 44), (52, 56)], 3)
    # cockpit
    pygame.draw.circle(surf, (255, 255, 255), (32, 26), 7)
    pygame.draw.circle(surf, (150, 220, 255), (32, 26), 5)
    # propulsores (brilho)
    pygame.draw.circle(surf, (255, 200, 80), (24, 54), 4)
    pygame.draw.circle(surf, (255, 200, 80), (40, 54), 4)
    salvar(surf, "nave_jogador.png")

# ---------- INIMIGO TIPO 1 (drone) ----------
def criar_inimigo_drone():
    surf = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (220, 70, 90), [(24, 44), (4, 8), (24, 18), (44, 8)])
    pygame.draw.polygon(surf, (150, 30, 50), [(24, 44), (4, 8), (24, 18), (44, 8)], 2)
    pygame.draw.circle(surf, (255, 230, 120), (24, 20), 5)
    salvar(surf, "inimigo_drone.png")

# ---------- INIMIGO TIPO 2 (caça rápido) ----------
def criar_inimigo_caca():
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (190, 100, 230), [(20, 38), (4, 4), (20, 14), (36, 4)])
    pygame.draw.polygon(surf, (110, 40, 150), [(20, 38), (4, 4), (20, 14), (36, 4)], 2)
    pygame.draw.circle(surf, (255, 255, 255), (20, 16), 4)
    salvar(surf, "inimigo_caca.png")

# ---------- METEORO ----------
def criar_meteoro():
    surf = pygame.Surface((56, 56), pygame.SRCALPHA)
    pontos = []
    cx, cy, r = 28, 28, 24
    random.seed(42)
    for i in range(10):
        ang = (math.pi * 2 / 10) * i
        raio = r + random.randint(-6, 4)
        x = cx + raio * math.cos(ang)
        y = cy + raio * math.sin(ang)
        pontos.append((x, y))
    pygame.draw.polygon(surf, (130, 110, 95), pontos)
    pygame.draw.polygon(surf, (80, 65, 55), pontos, 3)
    # crateras
    pygame.draw.circle(surf, (95, 80, 68), (20, 22), 5)
    pygame.draw.circle(surf, (95, 80, 68), (36, 30), 4)
    pygame.draw.circle(surf, (95, 80, 68), (26, 38), 3)
    salvar(surf, "meteoro.png")

# ---------- TIRO DO JOGADOR ----------
def criar_tiro_jogador():
    surf = pygame.Surface((8, 24), pygame.SRCALPHA)
    pygame.draw.rect(surf, (120, 230, 255), (2, 0, 4, 24), border_radius=3)
    pygame.draw.rect(surf, (255, 255, 255), (3, 0, 2, 10))
    salvar(surf, "tiro_jogador.png")

# ---------- TIRO INIMIGO ----------
def criar_tiro_inimigo():
    surf = pygame.Surface((8, 20), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255, 90, 90), (2, 0, 4, 20), border_radius=3)
    salvar(surf, "tiro_inimigo.png")

# ---------- ÍCONE DE VIDA ----------
def criar_icone_vida():
    surf = pygame.Surface((28, 28), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (80, 200, 255), [(14, 2), (5, 26), (14, 20), (23, 26)])
    salvar(surf, "icone_vida.png")

# ---------- EXPLOSÃO (sprite simples, 1 frame estilizado) ----------
def criar_explosao():
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    cores = [(255, 230, 120), (255, 160, 60), (255, 90, 50)]
    centro = (25, 25)
    for i, cor in enumerate(cores):
        raio = 22 - i * 6
        pygame.draw.circle(surf, cor, centro, raio)
    salvar(surf, "explosao.png")

# ---------- FUNDO ESTRELADO (imagem estática com estrelas) ----------
def criar_fundo():
    largura, altura = 800, 600
    surf = pygame.Surface((largura, altura))
    # gradiente vertical de azul escuro a preto
    for y in range(altura):
        t = y / altura
        r = int(8 + t * 5)
        g = int(8 + t * 5)
        b = int(30 + t * 15)
        pygame.draw.line(surf, (r, g, b), (0, y), (largura, y))
    random.seed(7)
    for _ in range(180):
        x = random.randint(0, largura - 1)
        y = random.randint(0, altura - 1)
        brilho = random.choice([120, 160, 200, 255])
        tam = random.choice([1, 1, 2])
        pygame.draw.circle(surf, (brilho, brilho, brilho), (x, y), tam)
    # algumas estrelas maiores com brilho
    for _ in range(15):
        x = random.randint(0, largura - 1)
        y = random.randint(0, altura - 1)
        pygame.draw.circle(surf, (255, 255, 255), (x, y), 2)
        pygame.draw.circle(surf, (180, 200, 255), (x, y), 4, 1)
    salvar(surf, "fundo_espaco.png")

if __name__ == "__main__":
    criar_nave_jogador()
    criar_inimigo_drone()
    criar_inimigo_caca()
    criar_meteoro()
    criar_tiro_jogador()
    criar_tiro_inimigo()
    criar_icone_vida()
    criar_explosao()
    criar_fundo()
    print("\nTodos os assets foram gerados em", PASTA)
