# DO NOT EDIT THE FOLLOWING LINES
# COURSE CPSC 231 FALL 2021
# INSTRUCTOR: Jonathan Hudson
# Wi52C3g7ZzkJ7XBcVRHY
# DO NOT EDIT THE ABOVE LINES

# INFORMATION FOR YOUR TA

import sys
import os
import turtle

# STARTER CONSTANTS
BACKGROUND_COLOR = "black"
WIDTH = 600
HEIGHT = 600
# AXIS CONSTANTS
AXIS_COLOR = "blue"
# STAR CONSTANTS
STAR_COLOR = "white"
STAR_COLOR2 = "grey"
NAME_OFFSET = 10
NAME_FONT = ("Arial", 5, "normal")
RATIO = 300
START = -1
END = 1
TICK_DIS = 0.25
TIK_LENGTH = 8
DISTANCE_LABEL = 25
ALPHA = 6


def get_color(quantifier):
    """
    :param quantifier: it as a quantifier in our main while loop to change color
    :return: a string for color
    """
    if (quantifier % 3) == 0:
        color = "red"
    if (quantifier % 3) == 1:
        color = "green"
    if (quantifier % 3) == 2:
        color = "yellow"
    return color


def calc_to_screen_coord(x, y):
    """
    Convert a calculator (x,y) to a pixel (screen_x, screen_y) based on ratio
    :param x: Calculator x
    :param y: Calculator y
    :return: (screen_x, screen_y) pixel version of calculator (x,y)
    """
    # screen_y and screen_x are local variables
    x = float(x)
    y = float(y)
    screen_x = (RATIO * x) + (WIDTH/2)
    screen_y = (RATIO * y) + (HEIGHT/2)
    return screen_x, screen_y


def draw_dot_name(pointer, x, y, mag, name, flag_name):
    """
    this function draws stars that are named
    :param pointer: turtle pointer
    :param x: pixel x (location)
    :param y: pixel y (location)
    :param mag: given magnitude
    :param name: the name of the star
    :param flag_name: this is a flag that indicates if the user wants names to be shown
    :return: nothing it just passes
    """
    pointer.penup()
    mag = float(mag)
    diameter = 10 / (mag + 2)
    pointer.color(STAR_COLOR)
    screen_x, screen_y = calc_to_screen_coord(x,y)
    pointer.goto(screen_x, screen_y)
    pointer.pendown
    pointer.dot(diameter)
    pointer.penup
    pointer.goto(screen_x, screen_y - NAME_OFFSET)
    pointer.penup
    if flag_name is True:
        pointer.pendown
        pointer.write(name, NAME_FONT)
        pointer.penup
    pass


def draw_dot(pointer, x, y, mag):
    """
    this function draws stars that are not named
    :param pointer: turtle pointer
    :param x: pixel x (location)
    :param y: pixel y (location)
    :param mag: given magnitude
    :return: nothing it just passes
    """
    pointer.penup()
    mag = float(mag)
    diameter = 10 / (mag + 2)
    pointer.color(STAR_COLOR2)
    screen_x, screen_y = calc_to_screen_coord(x,y)
    pointer.goto(screen_x, screen_y)
    pointer.pendown
    pointer.dot(diameter)
    pointer.penup
    pointer.goto(screen_x, screen_y - NAME_OFFSET)
    pointer.penup


def draw_line(pointer, screen_x1, screen_y1, screen_x2, screen_y2, color):
    """
    Draw a line between tow pixel coordinates (screen_x_1, screen_y_1) to (screen_x_2, screen_y_2)
    :param pointer: Turtle pointer to draw with
    :param screen_x1: The pixel x of line start
    :param screen_y1: The pixel y of line start
    :param screen_x2: The pixel x of line end
    :param screen_y2: The pixel y of line end
    :return: None (just draws in turtle)
    """
    pointer.color(color)
    pointer.penup()
    pointer.goto(screen_x1, screen_y1)
    pointer.pendown()
    pointer.goto(screen_x2, screen_y2)
    pointer.penup()
    pass


def handle():
    """
    this function deals with the arguments and the input of first file
    i have divided to four posibleities firs if there are no arguments
    second if there is only one argument ,third if there are two arguments
    fourth if there are more than two arguments
    :return: filename for the star information file , flag_names if the user wants the names
    """
    flag_names = False
    if len(sys.argv) == 1:
        filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
        if filename == "":
            sys.exit("no file was entered. program exiting!")
    if len(sys.argv) == 2:
        if sys.argv[1] == "-names":
            flag_names = True
            filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
            while not (os.path.isfile(filename)):
                filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
                if filename == "":
                    sys.exit("no file was entered. program exiting!")
        if not os.path.isfile(sys.argv[1]) and sys.argv[1] != "-names":
            filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
            while not (os.path.isfile(filename)):
                filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
                if filename == "":
                    sys.exit("no file was entered. program exiting!")
        if os.path.isfile(sys.argv[1]):
            filename = sys.argv[1]
    if len(sys.argv) == 3:
        if (os.path.isfile(sys.argv[1]) or os.path.isfile(sys.argv[2])) and not(os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2])):
            if sys.argv[1] == "-name" or sys.argv[2] == "-name":
                flag_names = True
            if os.path.isfile(sys.argv[1]):
                filename = sys.argv[1]
            if os.path.isfile(sys.argv[2]):
                filename = sys.argv[2]
        if os.path.isfile(sys.argv[1]) and os.path.isfile(sys.argv[2]):
            sys.exit("If there are two arguments, then one should be the -names flag")
        if (os.path.isfile(sys.argv[1]) is False) and (os.path.isfile(sys.argv[2]) is False):
            filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
            while not os.path.isfile(filename):
                filename = input("Enter the name of the input file with star information (ex. stars_all.dat):")
                if filename == "":
                    sys.exit("no file was entered. program exiting!")
    # Handle arguments
    if len(sys.argv) > 3:
        sys.exit("you entered too many arguments !")
    return filename, flag_names


def read_star(filename):
    """

    :param filename: it gets the file from user
    :return: a list of lists including needed information and a dictionary which the names are keys and
    values are needed information
    """
    full_star_list = []
    dict_star_name = {}
    file_handler = open(filename)
    lines = file_handler.readlines()
    #########################################################################
    """
    the first if statement checks each line of the file if there is more information than needed or less
    and it stops the program
    there are some stars with more than one name so i have divided the posiblities (one name, two names
    three names)
    """
    try:
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
            if len(line) > 7 or len(line) < 6:
                sys.exit("lines in the file contain too much information or not enough information")
            line.pop(2)
            line.pop(2)
            line.pop(3)
            if line[3] == '':
                line = line[:3]
            a = line[0]
            a = float(a)
            full_star_list.append(line)
            if len(line) == 4:
                names = line[-1:]
                names_list = names[0].split(";")
                if len(names_list) == 3:
                    dict_star_name[names_list[0]] = line[:3]
                    dict_star_name[names_list[1]] = line[:3]
                    dict_star_name[names_list[-1]] = line[:3]
                    print("%s is at (%s,%s) with magnitude %s" % (names_list[0], line[0], line[1], line[2]))
                    print("%s is at (%s,%s) with magnitude %s" % (names_list[1], line[0], line[1], line[2]))
                    print("%s is at (%s,%s) with magnitude %s" % (names_list[-1], line[0], line[1], line[2]))
                if len(names_list) == 2:
                    dict_star_name[names_list[0]] = line[:3]
                    dict_star_name[names_list[-1]] = line[:3]
                    print("%s is at (%s,%s) with magnitude %s" % (names_list[0], line[0], line[1], line[2]))
                    print("%s is at (%s,%s) with magnitude %s" % (names_list[-1], line[0], line[1], line[2]))
                if len(names_list) == 1:
                    dict_star_name[names_list[0]] = line[:3]
                    print("%s is at (%s,%s) with magnitude %s" % (names_list[0], line[0], line[1], line[2]))

        return full_star_list, dict_star_name
    except TypeError as type_error:
        sys.exit("the file data is not the correct type")


def draw_axis(pointer):
    """
    :param pointer: turtle pointer
    :return: just draws the axis
    """
    pointer.color("blue")
    def draw_x_axis_tick(pointer, screen_x, screen_y):
        """
        Draw an x-axis tick for location (screen_x, screen_y)
        :param pointer: Turtle pointer to draw with
        :param screen_x: The pixel x of tick location on axis
        :param screen_y: The pixel y of tick location on axis
        :return: None (just draws in turtle)
        """
        pointer.penup()
        pointer.goto(screen_x, screen_y - TIK_LENGTH)
        pointer.pendown()
        pointer.goto(screen_x, screen_y + TIK_LENGTH)
        pointer.penup
        pass

    def draw_x_axis_label(pointer, screen_x, screen_y, label_text):
        """
        Draw an x-axis label for location (screen_x, screen_y), label is label_text
        :param pointer: Turtle pointer to draw with
        :param screen_x: The pixel x of tick location on axis
        :param screen_y: The pixel y of tick location on axis
        :param label_text: The string label to draw
        :return: None (just draws in turtle)
        """
        pointer.penup()
        pointer.goto(screen_x - ALPHA, screen_y - DISTANCE_LABEL)
        pointer.pendown()
        pointer.write(label_text)
        pointer.penup
        pass

    def draw_y_axis_tick(pointer, screen_x, screen_y):
        """
        Draw an y-axis tick for location (screen_x, screen_y)
        :param pointer: Turtle pointer to draw with
        :param screen_x: The pixel x of tick location on axis
        :param screen_y: The pixel y of tick location on axis
        :return: None (just draws in turtle)
        """

        pointer.penup()
        pointer.goto(screen_x - TIK_LENGTH, screen_y)
        pointer.pendown()
        pointer.goto(screen_x + TIK_LENGTH, screen_y)
        pointer.penup
        pass

    def draw_y_axis_label(pointer, screen_x, screen_y, label_text):
        """
        Draw an y-axis label for location (screen_x, screen_y), label is label_text
        :param pointer: Turtle pointer to draw with
        :param screen_x: The pixel x of tick location on axis
        :param screen_y: The pixel y of tick location on axis
        :param label_text: The string label to draw
        :return: None (just draws in turtle)
        """
        pointer.penup()
        pointer.goto(screen_x - DISTANCE_LABEL, screen_y - ALPHA)
        pointer.pendown()
        pointer.write(label_text)
        pointer.penup
        pass

    draw_line(pointer, 0, HEIGHT/2, WIDTH, HEIGHT/2, AXIS_COLOR)
    label_quantifier = START
    while START <= label_quantifier <= END:
        label_text = label_quantifier
        pixel_label_quantifier, y = calc_to_screen_coord(label_quantifier, HEIGHT/2)
        draw_x_axis_tick(pointer, pixel_label_quantifier, HEIGHT/2)
        draw_x_axis_label(pointer, pixel_label_quantifier, HEIGHT/2, label_text)
        label_quantifier += TICK_DIS

    draw_line(pointer, WIDTH/2, 0, WIDTH/2, HEIGHT, AXIS_COLOR)
    label_quantifier = START
    while START <= label_quantifier <= END:
        label_text = label_quantifier
        x, pixel_label_quantifier = calc_to_screen_coord(WIDTH/2, label_quantifier)
        draw_y_axis_tick(pointer, WIDTH/2, pixel_label_quantifier)
        draw_y_axis_label(pointer, WIDTH/2, pixel_label_quantifier, label_text)
        label_quantifier += TICK_DIS


def draw_star(pointer, full_star_list, dict_star_name, flag_names):
    """
    :param pointer: turtle pointer
    :param full_star_list:
    :param dict_star_name:
    :param flag_names:
    :return:
    """
    for i in range(len(full_star_list)):
        info_list = full_star_list[i]
        x_star = info_list[0]
        y_star = info_list[1]
        mag_star = info_list[2]
        draw_dot(pointer, x_star, y_star, mag_star)
    for name in dict_star_name.keys():
        info_list = dict_star_name[name]
        x_star = info_list[0]
        y_star = info_list[1]
        mag_star = info_list[2]
        draw_dot_name(pointer, x_star, y_star, mag_star, name, flag_names)


def read_cons():
    """

    :return: it returns a list of tuples with the name of each edge,and the name of constelation
    """
    try:
        full_con_star_list = []
        mes_full_con_star_list = []
        con_filename = input("Enter a constellation file (Ex. BigDipper.dat):")
        if con_filename == "":
            sys.exit("no file was entered. program exiting!")
        con_file_handler = open(con_filename)
        lines = con_file_handler.readlines()
        for line in lines:
            line = line.rstrip()
            line = line.split(",")
            full_con_star_list.append(line)
        constellation_name = full_con_star_list[0]
        full_con_star_list_c = full_con_star_list[:]
        full_con_star_list_c.pop(0)
        for i in range(len(full_con_star_list_c)):
            x = full_con_star_list_c[i]
            m_1 = x[0]
            m_2 = x[1]
            mes_full_con_star_list.append(m_1)
            mes_full_con_star_list.append(m_2)
        print((str(constellation_name)[1:-1])+" constellation contains {"+(str(mes_full_con_star_list)[1:-1])+"}")
        return (str(constellation_name)[1:-1]), full_con_star_list_c
    except FileNotFoundError as file_not_found:
        print("The path entered isn't a valid filename:"+con_filename)

    except TypeError as type_error:
        print("the file data is not the correct type:"+con_filename)


def draw_cons(pointer, full_con_star_list_c, dict_star_name, color):
    """
    :param pointer: turtle pointer
    :param full_con_star_list_c: the list of tuples of each edge
    :param dict_star_name: the dictionary of named stars
    :param color: the color of edges
    :return: it just draws the constelation
    """
    for i in range(len(full_con_star_list_c)):
        x = full_con_star_list_c[i]
        m_1 = x[0]
        m_2 = x[1]
        info_list_1 = dict_star_name[m_1]
        info_list_2 = dict_star_name[m_2]
        x_1 = info_list_1[0]
        y_1 = info_list_1[1]
        x_2 = info_list_2[0]
        y_2 = info_list_2[1]
        screen_x_1, screen_y_1 = calc_to_screen_coord(x_1, y_1)
        screen_x_2, screen_y_2 = calc_to_screen_coord(x_2, y_2)
        draw_line(pointer, screen_x_1, screen_y_1, screen_x_2, screen_y_2, color)
    pass


def setup():
    """
    Setup the turtle window and return drawing pointer
    :return: Turtle pointer for drawing
    """
    turtle.bgcolor(BACKGROUND_COLOR)
    turtle.setup(WIDTH, HEIGHT, 0, 0)
    screen = turtle.getscreen()
    screen.delay(delay=0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer = turtle
    pointer.hideturtle()
    pointer.speed(0)
    pointer.up()
    return pointer


def main():
    """
    Main constellation program
    :return: None
    """
    # Handle arguments

    filename, flag_names = handle()
    pointer = setup()

    # Read star information from file (function)

    full_star_list, dict_star_name = read_star(filename)

    # Draw Axes (function)

    draw_axis(pointer)

    # Draw Stars (function)

    draw_star(pointer, full_star_list, dict_star_name, flag_names)

    # Loop getting filenames
    # Read constellation file (function)
    quantifier = 0
    while True:
        color = get_color(quantifier)
        constellation_name, full_con_star_list_c = read_cons()
        # Draw Constellation (function)
        draw_cons(pointer, full_con_star_list_c, dict_star_name, color)
        quantifier += 1
        # Draw bounding box (Bonus) (function)

        pass


main()

print("\nClick on window to exit!\n")
turtle.exitonclick()
