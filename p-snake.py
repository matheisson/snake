import curses
import time
import random
import sys

screen = curses.initscr()
title = ' !WELCOME TO PYTHON! '
screen.keypad(1)  # Enable keypad
dims = screen.getmaxyx()
# with this variable we can teg the max Y,X coords,
# equal to COLS-LEN


def game():
    # Setting the screen
    curses.noecho()
    curses.curs_set(0)
    screen.nodelay(1)
    head = [1, 1, ]  # Snake starts from the top left corner
    body = [head[:]] * 5  # Copy the head
    screen.border()
    direction = 0  # default direction = right

    curses.start_color()

    game_over = False  # by setting it false we can star a while Loop later
    screen.addstr(0, (curses.COLS - len(title)) // 2, title)
    deadcell = body[-1][:]
    foodmade = False
    body_part = "█"

    while not game_over:
        score = ("SCORE: " + str(len(body) - 5))
        screen.addstr(0, (curses.COLS - len(score)) // 7, score)
        while not foodmade:  # Generating food to random places on the screen
            y, x = random.randrange(
                1, dims[0] - 1), random.randrange(1, dims[1] - 1)
            if screen.inch(y, x) == ord(" "):  # within the border
                foodmade = True
                screen.addch(y, x, ord('@'))
        if deadcell not in body:
            screen.addch(deadcell[0], deadcell[1], " ")
        screen.addch(head[0], head[1], body_part)

        # Geeting key inputs, and pairing them with 4 directions
        action = screen.getch()
        if action == curses.KEY_UP and direction != 1:
            direction = 3
        elif action == curses.KEY_DOWN and direction != 3:
            direction = 1
        elif action == curses.KEY_RIGHT and direction != 2:
            direction = 0
        elif action == curses.KEY_LEFT and direction != 0:
            direction = 2
        # Giving directions, telling the head where to move on the Y,X coords
        if direction == 0:
            head[1] += 1
        elif direction == 2:
            head[1] -= 1
        elif direction == 1:
            head[0] += 1
        elif direction == 3:
            head[0] -= 1

        deadcell = body[-1][:]
        for z in range(len(body) - 1, 0, -1):
            body[z] = body[z - 1][:]

        body[0] = head[:]
        # defing game over and growth of the snake
        if screen.inch(head[0], head[1]) != ord(' '):
            if screen.inch(head[0], head[1]) == ord('@'):  # eating food, making the snake bigger
                foodmade = False
                body.append(body[-1])
            elif screen.inch(head[0], head[1]) == body_part:
                game_over = True
            else:
                game_over = True

        screen.move(dims[0] - 1, dims[1] - 1)
        screen.refresh()
        time.sleep(0.1)
        if len(body) <= 7:  # Here we added acceleratin to the game, based on the snakes length
            time.sleep(0.07)
        elif len(body) < 10:
            time.sleep(0.05)
        elif len(body) < 15:
            time.sleep(0.04)
        elif len(body) < 22:
            time.sleep(0.02)
        elif len(body) < 31:
            time.sleep(0.01)
        win = ("You have won the game. You don't have a life")  # :-)
        if len(body) == (curses.COLS * curses.LINES):
            game_over = True
    screen.clear()
    screen.nodelay(0)
    score = str(len(body) - 5)
    message = "GAME OVER"
    message2 = "You Got " + score + " Points"
    message3 = "Press SPACE to Play Again"
    message4 = "Press ENTER to Quit"
    if len(body) == (curses.COLS * curses.LINES):
        screen.addstr(6, (curses.COLS - len(win)) // 2, win)
    else:
        screen.addstr(6, (curses.COLS - len(message)) // 2, message)
    screen.addstr(7, (curses.COLS - len(message2)) // 2, message2)
    screen.addstr(8, (curses.COLS - len(message3)) // 2, message3)
    screen.addstr(9, (curses.COLS - len(message4)) // 2, message4)
    screen.refresh()
    k = 0  # here we can exit or play again by pressing the right key
    while k not in [32, 10]:
        k = screen.getch()
    if k == 32:
        screen.clear()
        game()
    if k == 10:
        screen.clear()
        exit()


def menu(stdscr):
    screen.nodelay(0)
    curses.noecho()
    curses.curs_set(0)
    selection = -1
    option = 0
    while selection < 0:  # change it by sel. in menu and hitting Enter
        graphics = [0] * 5
        graphics[option] = curses.A_REVERSE
        screen.addstr(0, dims[1] // 2 - 7, "WELCOME TO PYTHON")
        screen.addstr(6, dims[1] // 2 - 2, "PLAY", graphics[0])
        screen.addstr(7, dims[1] // 2 - 2, "EXIT", graphics[1])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1) % 5
        elif action == curses.KEY_DOWN:
            option = (option + 1) % 5
        elif action == ord('\n'):
            selection = option
    screen.clear()
    if selection == 0:
        game()

    elif selection == 1:
        screen.clear()
        screen.refresh()
        exit()

curses.wrapper(menu)

curses.endwin()
