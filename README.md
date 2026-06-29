# Star Defender

Jogo 2D do tipo *shoot 'em up* (atirador espacial), desenvolvido em **Python + Pygame**

## Sobre o jogo

Você controla uma nave espacial que deve defender seu setor contra uma invasão de
drones, caças inimigos e meteoros. Destrua os inimigos para ganhar pontos, mas
cuidado: colisões e tiros inimigos tiram suas vidas!

- **Controle do jogador**: movimento livre em 2D (setas / WASD) + tiro (espaço)
- **Desafio**: ondas crescentes de inimigos e meteoros, dificuldade progressiva
- **Condição de vitória**: alcançar 500 pontos
- **Condição de derrota**: perder as 3 vidas

### Controles
| Tecla | Ação |
|---|---|
| Setas ou `WASD` | Mover a nave |
| `Espaço` | Atirar |
| `Enter` | Iniciar / Reiniciar (nos menus) |
| `Esc` | Voltar ao menu / Sair |

Os controles também aparecem na tela de menu do jogo, como exigido na atividade.

## Estrutura do projeto

```
star_defender/
├── main.py              # Loop principal e telas (menu, jogo, vitória, derrota)
├── entidades.py          # Classes: Jogador, Inimigo, Meteoro, Tiros, Explosão
├── config.py              # Configurações globais e funções de carregamento de assets
├── gerar_assets.py        # Script que gerou as imagens 
├── gerar_sons.py           # Script que gerou os sons 
├── requirements.txt
└── assets/
    ├── imagens/   (.png gerados proceduralmente — sem direitos de terceiros)
    └── sons/      (.wav sintetizados — sem direitos de terceiros)
```
