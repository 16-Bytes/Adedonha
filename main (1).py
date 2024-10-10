import curses
import pyfiglet
import time
import random
import numpy as np

def gerar_letra():
    letras = np.array([chr(i) for i in range(65, 91)])
    return np.random.choice(letras)

def calcular_pontuacao(respostas):
    pontuacao = 0
    for resposta in respostas:
        if resposta.strip():
            pontuacao += 10
    return pontuacao

def jogar(stdscr, tempo_limite):
    curses.curs_set(1)
    stdscr.clear()
    stdscr.addstr(2, 1, "Sorteando letra...")
    stdscr.refresh()
    time.sleep(1)
    letra = gerar_letra()
    stdscr.addstr(4, 1, f"Letra sorteada: {letra}")

    categorias = ["Frutas", "Animais", "Países", "Cores", "Objetos", "Filmes", 
                  "Partes do Corpo", "Carros", "Comidas", "Super Heróis"]

    stdscr.addstr(6, 1, "Categorias:")
    for i, categoria in enumerate(categorias, 1):
        stdscr.addstr(6 + i, 1, f"{i}. {categoria}")

    inicio = time.time()
    respostas = []
    stdscr.addstr(17, 1, "Preencha as respostas (pressione Enter após cada uma):")

    for i, categoria in enumerate(categorias):
        stdscr.addstr(19 + i, 1, f"{categoria}: ")
        stdscr.refresh()

        resposta = ''
        stdscr.move(19 + i, len(categoria) + 3)
        while True:
            key = stdscr.getch()
            if key == ord('\n'):
                break
            elif key == 127:
                resposta = resposta[:-1]
                stdscr.addstr(19 + i, len(categoria) + 3, resposta + ' ')
            else:
                resposta += chr(key)
                stdscr.addstr(19 + i, len(categoria) + 3, resposta + ' ')

            stdscr.refresh()
            stdscr.move(19 + i, len(categoria) + 3 + len(resposta))

        respostas.append(resposta)

        if time.time() - inicio > tempo_limite * 60:
            break

    stdscr.clear()
    pontuacao = calcular_pontuacao(respostas)
    stdscr.addstr(2, 1, f"Tempo esgotado ou jogo finalizado!")
    stdscr.addstr(4, 1, f"Pontuação final: {pontuacao}")

    stdscr.addstr(6, 1, "Pressione Enter para voltar ao menu.")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('\n'):
            main_menu(stdscr)
            break

def main_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    title = pyfiglet.figlet_format("STOP", font='slant')
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(1, 1, title)
    stdscr.attroff(curses.color_pair(1))

    menu_options = ["1. Jogar Offline", "2. Sair"]
    start_y_menu = 10

    for i, option in enumerate(menu_options):
        stdscr.addstr(start_y_menu + i, 1, option)

    stdscr.addstr(start_y_menu + len(menu_options) + 1, 1, "Escolha uma opção: ")
    stdscr.refresh()

    choice = stdscr.getch()

    if choice == ord('1'):
        stdscr.clear()
        curses.echo()
        stdscr.move(1, 30)
        tempo_str = '1'
        try:
            tempo_limite = int(tempo_str)
        except ValueError:
            tempo_limite = 1
        curses.noecho()
        jogar(stdscr, tempo_limite)
    elif choice == ord('2'):
        stdscr.addstr(start_y_menu + len(menu_options) + 3, 1, "Saindo do jogo...")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main_menu)