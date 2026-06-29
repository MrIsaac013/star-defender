"""
STAR DEFENDER - main.py
Ponto de entrada do jogo. Contem o loop principal e as telas:
MENU -> JOGANDO -> VITORIA / DERROTA -> (voltar ao MENU)
"""
import pygame
import random
import sys

from config import (
    LARGURA, ALTURA, FPS,
    BRANCO, PRETO, AZUL_CLARO, AMARELO, VERMELHO, VERDE, CINZA,
    PONTOS_PARA_VENCER, VIDAS_INICIAIS,
    tela, relogio,
    fonte_titulo, fonte_grande, fonte_media, fonte_pequena,
    carregar_imagem, carregar_som,
)
from entidades import Jogador, TiroJogador, TiroInimigo, Inimigo, Meteoro, Explosao


# ----------------------------------------------------------------
# ESTADOS DO JOGO
# ----------------------------------------------------------------
MENU = "menu"
JOGANDO = "jogando"
VITORIA = "vitoria"
DERROTA = "derrota"


class Jogo:
    def __init__(self):
        self.estado = MENU
        self.fundo = carregar_imagem("fundo_espaco.png", (LARGURA, ALTURA))
        self.icone_vida = carregar_imagem("icone_vida.png", (28, 28))

        # sons
        self.som_tiro_jogador = carregar_som("tiro_jogador.wav")
        self.som_tiro_inimigo = carregar_som("tiro_inimigo.wav")
        self.som_explosao = carregar_som("explosao.wav")
        self.som_dano = carregar_som("dano_jogador.wav")
        self.som_vitoria = carregar_som("vitoria.wav")
        self.som_derrota = carregar_som("derrota.wav")
        self.som_clique = carregar_som("clique_menu.wav")

        for som in (self.som_tiro_jogador, self.som_tiro_inimigo):
            som.set_volume(0.35)
        self.som_explosao.set_volume(0.5)
        self.som_dano.set_volume(0.6)

        self.tempo_jogo_iniciado = 0
        self.reiniciar_jogo()

    # ------------------------------------------------------------
    def reiniciar_jogo(self):
        self.jogador = Jogador()
        self.jogador.vidas = VIDAS_INICIAIS
        self.jogador.pontuacao = 0

        self.grupo_jogador = pygame.sprite.GroupSingle(self.jogador)
        self.tiros_jogador = pygame.sprite.Group()
        self.tiros_inimigo = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.meteoros = pygame.sprite.Group()
        self.explosoes = pygame.sprite.Group()

        self.tempo_ultimo_spawn_inimigo = 0
        self.tempo_ultimo_spawn_meteoro = 0
        self.intervalo_spawn_inimigo = 1100  # ms
        self.intervalo_spawn_meteoro = 900   # ms
        self.dificuldade = 1.0
        self.tempo_inicio = pygame.time.get_ticks()

    # ------------------------------------------------------------
    # TELA DE MENU
    # ------------------------------------------------------------
    def desenhar_menu(self):
        tela.blit(self.fundo, (0, 0))

        titulo = fonte_titulo.render("STAR DEFENDER", True, AZUL_CLARO)
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 110)))

        subtitulo = fonte_media.render(
            "Defenda seu setor contra a invasao espacial!", True, BRANCO
        )
        tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA // 2, 165)))

        # Caixa de instrucoes
        caixa = pygame.Rect(LARGURA // 2 - 250, 220, 500, 230)
        pygame.draw.rect(tela, (15, 20, 40), caixa, border_radius=14)
        pygame.draw.rect(tela, AZUL_CLARO, caixa, width=2, border_radius=14)

        linhas = [
            ("CONTROLES", AMARELO, fonte_media, True),
            ("Setas / WASD  -  Mover a nave", BRANCO, fonte_pequena, False),
            ("ESPACO  -  Atirar", BRANCO, fonte_pequena, False),
            ("ESC  -  Sair do jogo", BRANCO, fonte_pequena, False),
            ("", BRANCO, fonte_pequena, False),
            ("OBJETIVO", AMARELO, fonte_media, True),
            (f"Marque {PONTOS_PARA_VENCER} pontos para vencer", BRANCO, fonte_pequena, False),
            (f"Voce tem {VIDAS_INICIAIS} vidas. Boa sorte!", BRANCO, fonte_pequena, False),
        ]
        y = caixa.top + 18
        for texto, cor, fonte, centralizado in linhas:
            if texto == "":
                y += 10
                continue
            render = fonte.render(texto, True, cor)
            if centralizado:
                rect = render.get_rect(centerx=LARGURA // 2, top=y)
            else:
                rect = render.get_rect(centerx=LARGURA // 2, top=y)
            tela.blit(render, rect)
            y += render.get_height() + 6

        # Botao iniciar (piscando)
        piscar = (pygame.time.get_ticks() // 500) % 2 == 0
        cor_botao = VERDE if piscar else (60, 150, 90)
        texto_inicio = fonte_grande.render("Pressione ENTER para iniciar", True, cor_botao)
        tela.blit(texto_inicio, texto_inicio.get_rect(center=(LARGURA // 2, 510)))

        rodape = fonte_pequena.render(
            "Atividade Pratica - Linguagem de Programacao Aplicada", True, CINZA
        )
        tela.blit(rodape, rodape.get_rect(center=(LARGURA // 2, 575)))

    # ------------------------------------------------------------
    # SPAWN DE INIMIGOS E METEOROS
    # ------------------------------------------------------------
    def atualizar_spawns(self):
        agora = pygame.time.get_ticks()

        # dificuldade aumenta com o tempo de jogo
        segundos_decorridos = (agora - self.tempo_inicio) / 1000
        self.dificuldade = 1.0 + min(segundos_decorridos / 40, 1.8)

        if agora - self.tempo_ultimo_spawn_inimigo >= self.intervalo_spawn_inimigo:
            self.tempo_ultimo_spawn_inimigo = agora
            tipo = random.choices(["drone", "caca"], weights=[0.65, 0.35])[0]
            inimigo = Inimigo(tipo=tipo, dificuldade=self.dificuldade)
            self.inimigos.add(inimigo)
            # intervalo de spawn diminui (jogo fica mais dificil)
            self.intervalo_spawn_inimigo = max(450, 1100 - segundos_decorridos * 8)

        if agora - self.tempo_ultimo_spawn_meteoro >= self.intervalo_spawn_meteoro:
            self.tempo_ultimo_spawn_meteoro = agora
            meteoro = Meteoro(dificuldade=self.dificuldade)
            self.meteoros.add(meteoro)
            self.intervalo_spawn_meteoro = max(400, 900 - segundos_decorridos * 6)

    # ------------------------------------------------------------
    # LOGICA DO JOGO (uma rodada de update)
    # ------------------------------------------------------------
    def atualizar_jogando(self):
        teclas = pygame.key.get_pressed()
        self.jogador.mover(teclas)
        self.jogador.atualizar_invulnerabilidade()

        if teclas[pygame.K_SPACE] and self.jogador.pode_atirar():
            tiro = TiroJogador(self.jogador.rect.centerx, self.jogador.rect.top)
            self.tiros_jogador.add(tiro)
            self.som_tiro_jogador.play()

        self.atualizar_spawns()

        self.tiros_jogador.update()
        self.tiros_inimigo.update()
        self.inimigos.update()
        self.meteoros.update()
        self.explosoes.update()

        # inimigos podem atirar
        for inimigo in self.inimigos:
            if inimigo.tentar_atirar():
                tiro = TiroInimigo(inimigo.rect.centerx, inimigo.rect.bottom)
                self.tiros_inimigo.add(tiro)
                self.som_tiro_inimigo.play()

        self.verificar_colisoes()

        # condicao de vitoria
        if self.jogador.pontuacao >= PONTOS_PARA_VENCER:
            self.estado = VITORIA
            self.som_vitoria.play()

        # condicao de derrota
        if self.jogador.vidas <= 0:
            self.estado = DERROTA
            self.som_derrota.play()

    # ------------------------------------------------------------
    def verificar_colisoes(self):
        # tiro do jogador atinge inimigo
        for tiro in list(self.tiros_jogador):
            atingidos = pygame.sprite.spritecollide(tiro, self.inimigos, dokill=True)
            if atingidos:
                tiro.kill()
                for inimigo in atingidos:
                    self.jogador.pontuacao += inimigo.pontos
                    self.explosoes.add(Explosao(inimigo.rect.center, tamanho=50))
                    self.som_explosao.play()

        # tiro do jogador atinge meteoro
        for tiro in list(self.tiros_jogador):
            atingidos = pygame.sprite.spritecollide(tiro, self.meteoros, dokill=True)
            if atingidos:
                tiro.kill()
                for meteoro in atingidos:
                    self.jogador.pontuacao += meteoro.pontos
                    self.explosoes.add(Explosao(meteoro.rect.center, tamanho=40))
                    self.som_explosao.play()

        # tiro inimigo atinge jogador
        atingiu = pygame.sprite.spritecollide(
            self.jogador, self.tiros_inimigo, dokill=True
        )
        if atingiu and self.jogador.receber_dano():
            self.explosoes.add(Explosao(self.jogador.rect.center, tamanho=60))
            self.som_dano.play()

        # inimigo colide diretamente com o jogador
        atingiu_inimigo = pygame.sprite.spritecollide(
            self.jogador, self.inimigos, dokill=True
        )
        if atingiu_inimigo and self.jogador.receber_dano():
            self.explosoes.add(Explosao(self.jogador.rect.center, tamanho=60))
            self.som_dano.play()

        # meteoro colide diretamente com o jogador
        atingiu_meteoro = pygame.sprite.spritecollide(
            self.jogador, self.meteoros, dokill=True
        )
        if atingiu_meteoro and self.jogador.receber_dano():
            self.explosoes.add(Explosao(self.jogador.rect.center, tamanho=60))
            self.som_dano.play()

    # ------------------------------------------------------------
    # DESENHO DA TELA DE JOGO
    # ------------------------------------------------------------
    def desenhar_jogando(self):
        tela.blit(self.fundo, (0, 0))

        self.meteoros.draw(tela)
        self.inimigos.draw(tela)
        self.tiros_jogador.draw(tela)
        self.tiros_inimigo.draw(tela)
        self.explosoes.draw(tela)
        self.jogador.desenhar_com_efeito(tela)

        self.desenhar_hud()

    def desenhar_hud(self):
        # pontuacao
        texto_pontos = fonte_media.render(
            f"Pontos: {self.jogador.pontuacao} / {PONTOS_PARA_VENCER}", True, BRANCO
        )
        tela.blit(texto_pontos, (16, 14))

        # vidas (icones)
        for i in range(self.jogador.vidas):
            tela.blit(self.icone_vida, (LARGURA - 40 - i * 34, 14))

        # barra de progresso de pontuacao
        largura_barra = 300
        progresso = min(self.jogador.pontuacao / PONTOS_PARA_VENCER, 1.0)
        pygame.draw.rect(tela, (40, 40, 60), (LARGURA // 2 - largura_barra // 2, 16, largura_barra, 14), border_radius=6)
        pygame.draw.rect(
            tela, VERDE,
            (LARGURA // 2 - largura_barra // 2, 16, int(largura_barra * progresso), 14),
            border_radius=6,
        )

    # ------------------------------------------------------------
    # TELAS DE FIM DE JOGO
    # ------------------------------------------------------------
    def desenhar_fim_de_jogo(self, vitoria: bool):
        tela.blit(self.fundo, (0, 0))
        overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        tela.blit(overlay, (0, 0))

        if vitoria:
            titulo = fonte_titulo.render("VITORIA!", True, VERDE)
            mensagem = "Voce defendeu o setor com sucesso!"
        else:
            titulo = fonte_titulo.render("FIM DE JOGO", True, VERMELHO)
            mensagem = "Sua nave foi destruida..."

        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 200)))

        texto_msg = fonte_media.render(mensagem, True, BRANCO)
        tela.blit(texto_msg, texto_msg.get_rect(center=(LARGURA // 2, 270)))

        texto_pontos = fonte_grande.render(
            f"Pontuacao final: {self.jogador.pontuacao}", True, AMARELO
        )
        tela.blit(texto_pontos, texto_pontos.get_rect(center=(LARGURA // 2, 330)))

        piscar = (pygame.time.get_ticks() // 500) % 2 == 0
        cor = BRANCO if piscar else CINZA
        texto_acao = fonte_media.render(
            "Pressione ENTER para jogar novamente  |  ESC para sair", True, cor
        )
        tela.blit(texto_acao, texto_acao.get_rect(center=(LARGURA // 2, 420)))

    # ------------------------------------------------------------
    # LOOP PRINCIPAL
    # ------------------------------------------------------------
    def executar(self):
        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado == JOGANDO:
                            self.estado = MENU
                        else:
                            rodando = False

                    if evento.key == pygame.K_RETURN:
                        if self.estado == MENU:
                            self.som_clique.play()
                            self.reiniciar_jogo()
                            self.estado = JOGANDO
                        elif self.estado in (VITORIA, DERROTA):
                            self.som_clique.play()
                            self.reiniciar_jogo()
                            self.estado = MENU

            # ----- atualizacao + desenho conforme o estado -----
            if self.estado == MENU:
                self.desenhar_menu()
            elif self.estado == JOGANDO:
                self.atualizar_jogando()
                self.desenhar_jogando()
            elif self.estado == VITORIA:
                self.desenhar_fim_de_jogo(vitoria=True)
            elif self.estado == DERROTA:
                self.desenhar_fim_de_jogo(vitoria=False)

            pygame.display.flip()
            relogio.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
