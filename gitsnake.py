import csv
import curses
from curses import wrapper
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
import time
import random
from operator import itemgetter
import math


screen = curses.initscr()
dims = screen.getmaxyx()

title = " !WELCOME TO PYTHON! "
start_length = 5
growby = 1
speed = {"Easy": 0.2, "Medium": 0.09, "Hard": 0.05}
difficulty = "Medium"
accel = True
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)


def game(screen):
    screen.clear()
    dims = screen.getmaxyx()
    curses.use_default_colors()
    screen.nodelay(1)
    curses.curs_set(0)
    screen.keypad(1)
    curses.start_color()
    head = [1, 1]
    body = ([head[:]] * start_length)
    screen.border()
    screen.addstr(0, (dims[1] - len(title)) // 2, title)
    direction = 0  # 0-right, 1-down, 2-left, 3, up
    game_over = False
    foodmade = False
    deadcell = body[-1][:]

    while not game_over:
        while not foodmade:
            y, x = random.randrange(
                1, dims[0] - 1), random.randrange(1, dims[1] - 1)
            if screen.inch(y, x) == ord(" "):
                foodmade = True
                food_type = ["🐥", "🔰", "🍦"]
                food_type_index = random.randint(0, 2)
                screen.addch(y, x, food_type[food_type_index])
        if deadcell not in body:
            screen.addch(deadcell[0], deadcell[1], " ")
        screen.addch(head[0], head[1], "🏮", curses.color_pair(2))

        action = screen.getch()
        if action == curses.KEY_UP and direction != 1:
            direction = 3
        if action == curses.KEY_DOWN and direction != 3:
            direction = 1
        if action == curses.KEY_LEFT and direction != 0:
            direction = 2
        if action == curses.KEY_RIGHT and direction != 2:
            direction = 0
        if action == 27:
            break

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

        if head[0] == dims[0] - 1 and head[1] == dims[1] - len(body):
            if direction == 0:
                y -= 1
            elif direction == 1:
                x -= 1

        if screen.inch(head[0], head[1]) != ord(" "):
            if screen.inch(head[0], head[1]) == ord(food_type[food_type_index]):
                foodmade = False
                screen.addstr(head[0], head[1], "*", curses.color_pair(3))
                for g in range(growby):
                    body.append(body[-1])
            else:
                game_over = True
        screen.refresh()
        if not accel:
            time.sleep(speed[difficulty])
        else:
            time.sleep(15.0 * speed[difficulty] / len(body))
        score = int(len(body) - start_length)
        score_str = "SCORE: " + str(score)
        screen.addstr(0, (curses.COLS - len(score_str)) // 7, score_str)
    screen.clear()
    screen.nodelay(0)

    message1 = "GAME OVER"
    message2 = "You got " + str(score) + " points."
    message3 = "Press SPACE to play again."
    message4 = "Press ESC to quit."
    message5 = "Press M to go back to the menu."
    screen.addstr(dims[0] // 2 - 3, (dims[1] - len(message1)) // 2, message1)
    screen.addstr(dims[0] // 2 - 2, (dims[1] - len(message2)) // 2, message2)
    screen.addstr(dims[0] // 2, (dims[1] - len(message3)) // 2, message3)
    screen.addstr(dims[0] // 2 + 1, (dims[1] - len(message4)) // 2, message4)
    screen.addstr(dims[0] // 2 + 2, (dims[1] - len(message5)) // 2, message5)
    with open("high_score.txt", 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(str(score))
    screen.refresh()
    q = 0
    while q not in [32, 27, 77, 109]:
        q = screen.getch()
    if q == 32:
        game(screen)
    elif q == 27:
        exit()
    elif q == 77 or q == 109:
        menu(screen)


def menu(screen):
    curses.curs_set(0)
    screen.nodelay(0)
    screen.border()
    curses.use_default_colors()
    screen.clear()
    selection = -1
    option = 0
    while selection < 0:
        graphics = [0] * 5
        graphics[option] = curses.A_REVERSE
        screen.addstr(dims[0] // 2 - 2, dims[1] // 2 - 2, "PLAY", graphics[0])
        screen.addstr(dims[0] // 2 - 1, dims[1] // 2 - 2, "INFO", graphics[1])
        screen.addstr(dims[0] // 2, dims[1] // 2 - 6, "GAME OPTIONS", graphics[2])
        screen.addstr(dims[0] // 2 + 1, dims[1] // 2 - 5, "HIGH SCORE", graphics[3])
        screen.addstr(dims[0] // 2 + 2, dims[1] // 2 - 2, "EXIT", graphics[4])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1) % 5
        elif action == curses.KEY_DOWN:
                option = (option + 1) % 5
        elif action == ord("\n"):
            selection = option
    if selection == 0:
        game(screen)
    elif selection == 1:
        info(screen)
    elif selection == 2:
        gameOptions(screen)
    elif selection == 3:
        high_scores(screen)


def info(screen):
    screen.clear()
    screen.nodelay(0)
    screen.border()
    infos_top = [" !WELCOME TO PYTHON! "]
    infos_center = [
        "Use the arrow keys to move.", "Don't run into the wall, title, or yourself.",
        "Collect food to grow.", "\n", "And remember, that the snake gets longer as well as FASTER."]
    infos_bottom = ["Press any key to go back."]
    for t in range(len(infos_top)):
        screen.addstr(t + 1, (dims[1] - len(infos_top[t])) // 2, infos_top[t])
    for z in range(len(infos_center)):
        screen.addstr((dims[0] - len(infos_center)) // 2 + z, (
            dims[1] - len(infos_center[z])) // 2, infos_center[z])
    for b in range(len(infos_bottom)):
        screen.addstr(dims[0] + b - 1 - len(infos_bottom), (
            dims[1] - len(infos_bottom[b])) // 2, infos_bottom[b])
    screen.refresh()
    screen.getch()
    menu(screen)


def gameOptions(screen):
    global start_length, growby, difficulty, accel
    screen.clear()
    screen.border()
    selection = -1
    option = 0
    while selection < 4:
        screen.clear()
        graphics = [0] * 5
        graphics[option] = curses.A_BOLD
        strings = ["Starting snake length? " + str(start_length), "Snake growth rate: " +
                   str(growby), "Difficulty: " +
                   str(difficulty), "Acceleration: " + str(accel),
                   "Exit"]
        for z in range(len(strings)):
            screen.addstr((dims[0] - len(strings)) // 2 + z, (
                dims[1] - len(strings[z])) // 2, strings[z], graphics[z])
        screen.refresh()
        action = screen.getch()
        if action == curses.KEY_UP:
            option = (option - 1) % 5
        elif action == curses.KEY_DOWN:
            option = (option + 1) % 5
        elif action == ord("\n"):
            selection = option
        elif action == curses.KEY_RIGHT and option in [0, 1]:
            if option == 0 and start_length < 20:
                start_length += 1
            elif option == 1 and growby < 10:
                growby += 1
        elif action == curses.KEY_LEFT:
            if option == 0 and start_length > 3:
                start_length -= 1
            elif option == 1 and growby > 1:
                growby -= 1
        elif action == 27:
            menu(screen)
        if selection == 2:
            if difficulty == "Easy":
                difficulty = "Medium"
            elif difficulty == "Medium":
                difficulty = "Hard"
            else:
                difficulty = "Easy"
        elif selection == 3:
            accel = not accel
        if selection < 4:
            selection = -1
    menu(screen)


def high_scores(screen):
    screen.clear()
    screen.nodelay(0)
    screen.border()
    high_score_top = [" !WELCOME TO PYTHON! "]
    for t in range(len(high_score_top)):
        screen.addstr(t + 1, (dims[1] - len(high_score_top[t])) // 2, high_score_top[t])
    with open("high_score.txt") as csvfile:
        readCSV = csv.reader(csvfile)
        highest = []
        for row in readCSV:
            row = int(row[0])
            highest.append(row)
    highest = (sorted(highest, reverse=True))[:10]
    for i in range(len(highest)):
        s = str(i + 1) + "."
        g = int(highest[i])
        screen.addstr(i+5, (dims[1] - len(str(highest[i]))) // 2-2, "{0} {1}".format(s, g))
        screen.refresh()
    screen.refresh()
    screen.getch()
    menu(screen)

wrapper(menu)
