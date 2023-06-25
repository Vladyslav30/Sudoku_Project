# Pygame is a library for making games in Python
import pygame

# The following are custom modules containing Sudoku related functions such as
# validating Sudoku rules, solving the Sudoku, creating the Sudoku matrix etc.
from test import valid, solve, create_matrix, print_sudoku, find_empty

# Time and numpy are general purpose libraries
import time
import numpy as np
import sys

# Initializes pygame's font module
pygame.font.init()

class Grid:
    # Predefined Sudoku board that this code will solve.
    board = [
        [0, 7, 1, 0, 6, 9, 5, 0, 0],
        [0, 0, 9, 0, 0, 0, 6, 0, 0],
        [0, 0, 6, 7, 0, 0, 0, 9, 0],
        [0, 9, 8, 0, 0, 7, 2, 6, 0],
        [1, 3, 2, 8, 0, 0, 0, 7, 4],
        [0, 0, 4, 1, 9, 2, 8, 3, 0],
        [0, 0, 7, 0, 8, 0, 0, 0, 0],
        [9, 1, 0, 4, 0, 3, 7, 8, 0],
        [0, 8, 0, 0, 0, 1, 0, 0, 2]
    ]
    # Converts the board list to a numpy array for more convenient manipulation
    board = np.array(board)

    # Initializes the Grid object with dimensions, creates 'Cube' objects for each cell of the Sudoku
    def __init__(self, rows, cols, width, height,):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.update_model()
        self.solve = False
        self.solve_time = 0

    # Updates the current Sudoku board model from the 'Cube' objects
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # Place a value on the board at the selected location
    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            # If the new value is valid and the board can be solved, return True
            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                # If not, reset the value of the cube and return False
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    # Temporary sketch value on the board at the selected location
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)  # This function is used to sketch or "pencil in" a value without confirming it

    # Draws the current state of the board on the pygame window
    def draw(self, win):
        gap = self.width / 9  # Calculate the width of each Sudoku cell (the board is divided into 9 parts)

        # Draw lines to make the grid. Every third line is thicker to separate the 3x3 subgrids
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw each individual cell/cube on the grid
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    # Method to select a cell on the grid. All other cells are deselected.
    def select(self, row, col):
        # Deselect all cubes first
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        # Select the clicked cube
        self.cubes[row][col].selected = True
        self.selected = (row, col)  # Save the selected cell's coordinates

    # Method to clear the selected cell's temporary value
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:  # Only clears the cell if the value is 0 (not a given number)
            self.cubes[row][col].set_temp(0)  # Resets the temporary value to 0

    # Method to convert a screen space click into grid coordinates
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:  # If the click is within the bounds of the grid
            gap = self.width / 9  # Calculate the width of each Sudoku cell (the board is divided into 9 parts)
            x = pos[0] // gap  # Determine the X coordinate in grid space
            y = pos[1] // gap  # Determine the Y coordinate in grid space

            return (int(y), int(x))  # Return the grid space coordinates
        else:
            return None  # If the click was outside the grid, return None


    # Method to check if the Sudoku puzzle has been solved. If any cell is still 0, it returns False.
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:  # If a cell's value is still 0, the puzzle is not solved
                    return False
        return True  # If no cell is 0, the puzzle is solved

    # Method to solve the Sudoku puzzle using a backtracking algorithm. It also updates the GUI with the progress.
    def solve_gui(self, win):
        self.update_model()  # Update the model to the current state
        find = find_empty(self.model)  # Find an empty cell in the puzzle
        if not find:  # If there are no empty cells, the puzzle is solved
            return True
        else:  # If there are empty cells, try to solve for them
            row, col = find  # Get the coordinates of the empty cell

        # Try each number from 1 to 9
        for i in range(1, 10):
            # If the number is valid according to Sudoku rules, try to solve with that number
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i  # Set the cell to the number
                self.cubes[row][col].set(i)  # Update the GUI with the new number
                self.cubes[row][col].draw_change(win, True)  # Highlight the change in the GUI
                self.update_model()  # Update the model to the current state
                pygame.display.update()  # Update the display
                pygame.time.delay(100)  # Delay to slow down the solving process for visibility

                # Recursive call to continue solving
                if self.solve_gui(win):
                    return True

                # If the number doesn't lead to a solution, reset the cell and backtrack
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(win, False)  # Show the backtrack in the GUI
                pygame.display.update()
                pygame.time.delay(100)

        # If no number leads to a solution, return False to trigger backtracking
        return False



# The Cube class represents a cell in the Sudoku grid
class Cube:
    rows = 9  # Number of rows in a Sudoku grid
    cols = 9  # Number of columns in a Sudoku grid

    # Constructor for the Cube class
    def __init__(self, value, row, col, width, height):
        self.value = value  # Value in the cell (0 if the cell is empty)
        self.temp = 0  # Temporary value penciled in
        self.row = row  # Row index of the cell in the grid
        self.col = col  # Column index of the cell in the grid
        self.width = width  # Width of the cell
        self.height = height  # Height of the cell
        self.selected = False  # Whether the cell is selected
        self.gap = self.width / 9  # The gap between cells
        self.x = self.col * self.gap  # The x-coordinate of the top left corner of the cell
        self.y = self.row * self.gap  # The y-coordinate of the top left corner of the cell

    # Draws the Cube on the pygame window
    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        # If a temporary value is entered, show it in light grey
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (self.x + 5, self.y + 5))
        # If a final value is entered, show it in black
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (self.x + (self.gap/2 - text.get_width()/2), self.y + (self.gap/2 - text.get_height()/2)))

        # If the cell is selected, highlight it with a red border
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.gap, self.gap), 3)

    # Highlights the cell in green or red, depending on the value of g
    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)

        # Clear the cell
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.gap, self.gap), 0)

        # Draw the value of the cell
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (self.x + (self.gap/2 - text.get_width()/2), self.y + (self.gap/2 - text.get_height()/2)))

        # If g is True, draw a green border; otherwise, draw a red border
        if g:
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.gap, self.gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.gap, self.gap), 3)

    # Sets the final value of the cell
    def set(self, val):
        self.value = val

    # Sets a temporary value for the cell
    def set_temp(self, val):
        self.temp = val  # Sets a temporary value for the cell

# Redraws the entire game window
def redraw_window(win, board, time, strickers):
    win.fill((255, 255, 255))  # Fills the window with white color

    # Sets the font for the text
    fnt = pygame.font.SysFont("comicsans", 40)

    # Creates a text surface displaying the time and blits it onto the window
    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (300, 540))  # Blit is a pygame function to draw one image onto another

    # Creates a text surface displaying the number of mistakes (strickers) and blits it onto the window
    text = fnt.render("Strickers: " + str(strickers), 1, (255, 0, 0))
    win.blit(text, (20, 540))

    # Draw the Sudoku board on the window
    board.draw(win)


def draw_text(text, size, x, y ,win):
    # Defines the font and size for the text
    font = pygame.font.SysFont("comicsans", size, bold=True)
    # Renders the text
    text = font.render(text, True, (0, 0, 0))
    # Creates a rectangle object for the text surface object
    text_rect = text.get_rect()
    # Positions the center of the rectangle at specified coordinates
    text_rect.midtop = (x, y)
    # Blits the text onto the window at the specified location
    win.blit(text, text_rect)

def draw_button(text, color, x, y, w, h, win):
    # Draws a button as a rectangle onto the window
    pygame.draw.rect(win, color, (x, y, w, h))
    # Calls draw_text function to draw text onto the button
    draw_text(text, 30, x + w/2, y, win)

def button_clicked(x, y, w, h):
    # Gets the current position of the mouse
    mouse = pygame.mouse.get_pos()
    # Gets the state of the mouse buttons
    click = pygame.mouse.get_pressed()
    # Checks if the mouse is within the dimensions of the button and if it has been clicked
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            return True
    return False

def ask_quit(win):
    while True:
        # Checks for a QUIT event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quits the game and exits the program
                pygame.quit()
                sys.exit()
        # Fills the window with white color
        win.fill((255, 255, 255))
        # Draws the quit confirmation text onto the window
        draw_text("Do you want to quit?", 30, win.get_width()/2, win.get_height()/2 - 60, win)
        # Draws the "Yes" button onto the window
        draw_button("Yes", (0, 255, 0), win.get_width()/2 - 100, win.get_height()/2 , 80, 40, win)
        # Draws the "No" button onto the window
        draw_button("No", (255, 0, 0),  win.get_width()/2 + 20, win.get_height()/2 , 80, 40, win)

        # Checks if the "Yes" button is clicked
        if button_clicked(win.get_width()/2 - 100, win.get_height()/2 , 80, 40):
            return True
        # Checks if the "No" button is clicked
        elif button_clicked(win.get_width()/2 + 20, win.get_height()/2 , 80, 40):
            return False
        # Updates the contents of the display
        pygame.display.update()


def lost(win):
    while True:
        # Checks for a QUIT event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quits the game and exits the program
                pygame.quit()
                sys.exit()
        # Fills the window with white color
        win.fill((255, 255, 255))
        # Draws the game over text onto the window
        draw_text("You lost!", 30, win.get_width()/2, win.get_height()/2 - 60, win)
        # Draws the "Play again" button onto the window
        draw_button("Play again", (0, 255, 0), win.get_width()/2 - 200, win.get_height()/2 , 160, 50, win)
        # Draws the "Quit" button onto the window
        draw_button("Quit", (255, 0, 0),  win.get_width()/2 + 60, win.get_height()/2 , 160, 50, win)

        # Checks if the "Play again" button is clicked
        if button_clicked(win.get_width()/2 - 200, win.get_height()/2 , 160, 50):
            return True
        # Checks if the "Quit" button is clicked
        elif button_clicked(win.get_width()/2 + 60, win.get_height()/2 , 160, 50):
            return False
        # Updates the contents of the display
        pygame.display.update()

def format_time(secs):
    # Converts the time in seconds to hours, minutes, and seconds format
    sec = secs % 60  # Gets the remaining seconds
    minute = secs // 60  # Converts the seconds to minutes
    hour = minute // 60  # Converts the minutes to hours

    # Returns the formatted time as a string
    mat = " " + str(minute) + ":" + str(sec)
    return mat

def main():
    # Initialize the window with a specific size and set the caption as "Sudoku"
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")
    # Create a new Grid object with 9 rows, 9 columns, and a specific size
    board = Grid(9, 9, 540, 540)
    # Initialize the key variable that will hold the number entered by the user
    key = None
    # Control variable for the main loop
    run = True
    # Track the start time of the game
    start = time.time()
    # Counter for mistakes made by the player
    strickers = 0

    # Main loop
    while run:
        # Calculate the elapsed time
        play_time = round(time.time() - start)

        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Ask the player if they want to quit when they close the window
                if ask_quit(win):
                    run = False
                else:
                    continue
            # If a key is pressed
            if event.type == pygame.KEYDOWN:
                # Check for number keys 1-9 and numpad keys 1-9
                # If any of these keys is pressed, assign its value to key
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                    # If the space key is pressed, solve the board
                if event.key == pygame.K_SPACE:
                    board.solve_gui(win)
                    # If the return key is pressed
                if event.key == pygame.K_RETURN:
                    # If there's a temporary value on the selected square
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        # Try to place the temp value on the board
                        if board.place(board.cubes[i][j].temp):
                            continue
                        # If the value cannot be placed, increase the strikes
                        else:
                            strickers += 1
                            # If the player has made 3 mistakes, end the game
                            if strickers == 3:
                                if lost(win):
                                    # If the player wants to play again, reset the game
                                    board.clear()
                                    strickers = 0
                                    start = time.time()
                                # Otherwise, exit the game
                                else:
                                    run = False

                        # Reset the key after the value is placed
                        key = None

            # If the mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position where the mouse was clicked
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                # If a square was clicked, select that square and reset the key
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
        # If a square is selected and a number key was pressed, sketch that number on the square
        if board.selected and key != None:
            board.sketch(key)
        # Redraw the window and update the display
        redraw_window(win, board, play_time, strickers)
        pygame.display.update()

# Run the main function
main()
# Quit Pygame when the main function returns
pygame.quit()