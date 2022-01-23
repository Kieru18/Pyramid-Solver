from typing_extensions import TypeAlias

sides = {
    0: 'up',
    1: 'down',
    2: 'left',
    3: 'right'
}

arr_row: TypeAlias = "list['set']"
board_array: TypeAlias = 'list["arr_row"]'
