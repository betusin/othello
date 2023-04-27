from typing import Optional, List, Tuple


def new_playground(size: int) -> List[List[str]]:
    playground = []
    for row in range(size):
        line = []
        for col in range(size):
            line.append(" ")
        playground.append(line)
    return playground


def init_playground(playground: List[List[str]]) -> List[List[str]]:
    middle_pos = len(playground) // 2 - 1
    set_symbol(playground, middle_pos, middle_pos, "O")
    set_symbol(playground, middle_pos + 1, middle_pos + 1, "O")
    set_symbol(playground, middle_pos + 1, middle_pos, "X")
    set_symbol(playground, middle_pos, middle_pos + 1, "X")
    return playground


def get(playground: List[List[str]], row: int, col: int) -> str:
    return playground[row][col]


def set_symbol(playground: List[List[str]],
               row: int, col: int, symbol: str) -> None:
    playground[row][col] = symbol


def spaces_fill(n: str) -> str:
    return (len(str(26)) - len(n)) * " "


def draw_head(playground: List[List[str]], separate_line: str) -> None:
    print(" ", spaces_fill(""), end="")
    for i in range(0, len(playground)):
        print(" ", chr(ord('A') + i), end="  ", sep="")
    print()
    print(separate_line)


def draw_body(playground: List[List[str]], separate_line: str) -> None:
    for row in range(len(playground)):
        print(spaces_fill(str(row)),
              row, " | ", sep="", end="")
        for col in range(len(playground)):
            print(playground[row][col], " | ", sep="", end="")
        print()
        print(separate_line)


def draw(playground: List[List[str]]) -> None:
    separate_line = spaces_fill("") + " +" + len(playground) * "---+"

    draw_head(playground, separate_line)
    draw_body(playground, separate_line)


def count_rocks_to_dye(row_move: int, col_move: int,
                       row: int, col: int, playground: List[List[str]],
                       symbol: str) -> int:
    symbols = ""
    while 0 <= row + row_move < len(playground) \
            and 0 <= col + col_move < len(playground) \
            and get(playground, row + row_move, col + col_move) != " ":
        row = row + row_move
        col = col + col_move
        symbols += get(playground, row, col)

    position = 0
    dyed = 0

    if symbol in symbols:
        while symbols[position] != symbol:
            dyed += 1
            position += 1

    return dyed


def dying(dyed: int, row_move: int, col_move: int,
          row: int, col: int, playground: List[List[str]],
          symbol: str) -> None:
    for i in range(1, dyed + 1):
        set_symbol(playground, row + row_move * i, col + col_move * i, symbol)


def play(playground: List[List[str]], row: int, col: int,
         symbol: str) -> Optional[int]:
    if get(playground, row, col) != " ":
        return None

    dyed_rocks = count_all_dyed(row, col, playground, symbol, True)
    if dyed_rocks == 0:
        return None

    set_symbol(playground, row, col, symbol)
    return dyed_rocks


def count_all_dyed(row: int, col: int,
                   playground: List[List[str]],
                   symbol: str, to_dye: bool) -> int:
    dyed_rocks = 0
    all_directions = [(0, 1), (0, -1), (1, 1), (1, 0),
                      (1, -1), (-1, 1), (-1, 0), (-1, -1)]

    for direction in all_directions:
        now_dyed = count_rocks_to_dye(direction[0], direction[1],
                                      row, col, playground, symbol)
        dyed_rocks += now_dyed
        if to_dye:
            dying(now_dyed, direction[0], direction[1],
                  row, col, playground, symbol)

    return dyed_rocks


def game_over(playground: List[List[str]], current_symbol: str) -> bool:
    for row in range(len(playground)):
        for col in range(len(playground)):
            if get(playground, row, col) == " ":
                dyed_rocks = count_all_dyed(
                    row, col, playground, current_symbol, False)
                if dyed_rocks != 0:
                    return False
    return True


def count(playground: List[List[str]]) -> Tuple[int, int]:
    count_x = 0
    count_o = 0
    for row in range(len(playground)):
        for col in range(len(playground)):
            if playground[row][col] == "X":
                count_x += 1
            if playground[row][col] == "O":
                count_o += 1
    return count_x, count_o


def get_size() -> Optional[int]:
    size = input("Enter size of playground: ")
    if not size.isdigit():
        print("You didn't enter a number.")
        return get_size()
    if int(size) < 4:
        print("Number is too small. Try at least 4.")
        return get_size()
    if int(size) > 26:
        print("Number is too big. It will work just with number up to 26.")
        return get_size()
    if int(size) % 2 != 0:
        print("Entered number cannot be divided by two.")
        return get_size()
    return int(size)


def get_row_pos(size: int) -> int:
    row = input("Enter the line number where "
                "you want to place your character:")

    while not check_row(size, row):
        row = input("Enter the letter of the column where"
                    " you want to place your character:")
    return int(row)


def check_row(size: int, row: str) -> bool:
    if not row.isdigit():
        print("You didn't enter a number. You can"
              " only enter numbers from 0 to", size - 1)
        return False

    if size - 1 < int(row) or int(row) < 0:
        print("You entered a position outside the game board."
              " You can only enter numbers from 0 to", size - 1)
        return False

    return True


def get_col_pos(size: int) -> int:
    char_col = input("Enter the letter of the column where"
                     " you want to place your character:").upper()

    while not check_col(size, char_col):
        char_col = input("Enter the letter of the column where"
                         " you want to place your character:").upper()
    col = ord(char_col) - ord('A')
    return int(col)


def check_col(size: int, char_col: str) -> bool:
    if len(char_col) > 1:
        print("You didn't enter a letter, but text. You can only"
              " enter one letter from A to", chr(ord('A') + size - 1))
        return False

    if char_col.isdigit():
        print("You entered a number. You can only"
              " enter letters from A to", chr(ord('A') + size - 1))
        return False

    if not char_col.isalpha():
        print("You entered an invalid character. You can only"
              " enter letters from A to", chr(ord('A') + size - 1))
        return False

    col = ord(char_col) - ord('A')

    if size - 1 < int(col) or int(col) < 0:
        print("You entered a position outside the game board. "
              "You can only enter letters from A to", chr(ord('A') + size - 1))
        return False

    return True


def get_coordinates(playground: List[List[str]]) -> Tuple[int, int]:
    row = get_row_pos(len(playground))
    col = get_col_pos(len(playground))

    while get(playground, row, col) != " ":
        print("You have entered a position where there is another character."
              " You can only enter stones to empty spaces.")
        row, col = get_coordinates(playground)

    return int(row), int(col)


def turn(playground: List[List[str]], symbol: str) -> None:
    print("*** ", symbol, "`s turn ***", sep="")
    row, col = get_coordinates(playground)

    while count_all_dyed(row, col, playground, symbol, False) == 0:
        print("Your move is invalid because it will not color a single stone.")
        row, col = get_coordinates(playground)

    play(playground, row, col, symbol)


def print_status(playground: List[List[str]]) -> None:
    print(60 * "\n")
    status = count(playground)
    print("*** Actual status (X:O) is: ", status[0],
          ":", status[1], " ***", sep="")
    draw(playground)
    print()


def print_result(playground: List[List[str]]) -> None:
    print("Game over. Other moves are not possible.")
    status = count(playground)
    print("Final status (X:O) is: ", status[0],
          ":", status[1], sep="")

    if status[0] > status[1]:
        print("The winner is 'X'.")
    if status[0] < status[1]:
        print("The winner is 'O'.")
    if status[0] == status[1]:
        print("Game finished in a draw.")


def game() -> None:
    print("WELCOME TO GAME REVERSI")
    size = get_size()

    print("*** Player X is starting ***")

    playground = init_playground(new_playground(size))
    draw(playground)
    current_player, opposite_player = 'X', 'O'

    while not game_over(playground, 'X') and not game_over(playground, 'O'):
        turn(playground, current_player)
        print_status(playground)
        opposite_player, current_player = current_player, opposite_player

    print_result(playground)


if __name__ == '__main__':
    game()
