import numpy as np
import wave
import struct
import os

PASTA = "assets/sons"
os.makedirs(PASTA, exist_ok=True)
SAMPLE_RATE = 44100

def salvar_wav(nome, amostras):
    amostras = np.clip(amostras, -1, 1)
    dados_int16 = (amostras * 32767).astype(np.int16)
    caminho = os.path.join(PASTA, nome)
    with wave.open(caminho, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(dados_int16.tobytes())
    print(f"Gerado: {nome}")

def envolope(n, ataque=0.05, release=0.3):
    env = np.ones(n)
    a = int(n * ataque)
    r = int(n * release)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    return env

def tiro_jogador():
    dur = 0.15
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    freq = np.linspace(1200, 400, len(t))
    onda = 0.4 * np.sin(2 * np.pi * freq * t)
    onda *= envolope(len(t), 0.02, 0.6)
    salvar_wav("tiro_jogador.wav", onda)

def tiro_inimigo():
    dur = 0.15
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    freq = np.linspace(700, 200, len(t))
    onda = 0.35 * np.sin(2 * np.pi * freq * t)
    onda *= envolope(len(t), 0.02, 0.6)
    salvar_wav("tiro_inimigo.wav", onda)

def explosao():
    dur = 0.4
    n = int(SAMPLE_RATE * dur)
    ruido = np.random.uniform(-1, 1, n)
    env = envolope(n, 0.01, 0.85)
    onda = ruido * env * 0.5
    salvar_wav("explosao.wav", onda)

def dano_jogador():
    dur = 0.25
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    freq = np.linspace(300, 100, len(t))
    onda = 0.5 * np.sin(2 * np.pi * freq * t)
    ruido = np.random.uniform(-0.2, 0.2, len(t))
    onda = (onda + ruido) * envolope(len(t), 0.01, 0.7)
    salvar_wav("dano_jogador.wav", onda)

def vitoria():
    notas = [523, 659, 784, 1046]
    partes = []
    for f in notas:
        dur = 0.18
        t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
        onda = 0.4 * np.sin(2 * np.pi * f * t)
        onda *= envolope(len(t), 0.05, 0.5)
        partes.append(onda)
    salvar_wav("vitoria.wav", np.concatenate(partes))

def derrota():
    notas = [400, 350, 300, 220]
    partes = []
    for f in notas:
        dur = 0.25
        t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
        onda = 0.4 * np.sin(2 * np.pi * f * t)
        onda *= envolope(len(t), 0.05, 0.6)
        partes.append(onda)
    salvar_wav("derrota.wav", np.concatenate(partes))

def clique_menu():
    dur = 0.08
    t = np.linspace(0, dur, int(SAMPLE_RATE * dur), False)
    onda = 0.35 * np.sin(2 * np.pi * 900 * t)
    onda *= envolope(len(t), 0.05, 0.6)
    salvar_wav("clique_menu.wav", onda)

if __name__ == "__main__":
    tiro_jogador()
    tiro_inimigo()
    explosao()
    dano_jogador()
    vitoria()
    derrota()
    clique_menu()
    print("\nTodos os sons foram gerados em", PASTA)
