from PIL import Image, ImageDraw, ImageFont
from conf import PATH, user_path
from conf import OUTLINE_WIDTH, INLINE_WIDTH, SMALLEST_STRING
from conf import C_RED, C_GREEN, C_GREY
from conf import RED_TAGS, GREEN_TAGS, GREY_TAGS


class TableDrawer:
    @staticmethod
    def draw_table(board, font_size, color_matrix=None, empty_matrix=None):
        # PATH is defined in project, user_path is user's path to project directory
        path = user_path + PATH

        # calculates the width and height of image
        params = TableDrawer.board_params(board, font_size)
        x_size = len(params[0])
        y_size = len(params[1])
        width = OUTLINE_WIDTH * 2 + INLINE_WIDTH * (len(params[0]) - 1)
        height = OUTLINE_WIDTH * 2 + INLINE_WIDTH * (len(params[1]) - 1)
        for cell_width in params[0]:
            width += cell_width
        for cell_height in params[1]:
            height += cell_height
        img = Image.new('RGB', (width, height), color='white')

        # region drawing outlines (borders) and inlines
        # outlines
        indent = (OUTLINE_WIDTH - 1) / 2
        draw = ImageDraw.Draw(img)
        draw.line((0, indent, width, indent), fill=0, width=OUTLINE_WIDTH)
        draw.line((0, height - indent - 1, width, height - indent - 1), fill=0, width=OUTLINE_WIDTH)
        draw.line((indent, 0, indent, height), fill=0, width=OUTLINE_WIDTH)
        draw.line((width - indent - 1, 0, width - indent - 1, height), fill=0, width=OUTLINE_WIDTH)

        # inlines
        start_pix = OUTLINE_WIDTH - int((INLINE_WIDTH + 1) / 2)
        shift = 0
        for x in range(x_size - 1):
            shift += params[0][x] + INLINE_WIDTH
            draw.line((start_pix + shift, 0, start_pix + shift, height), fill=0, width=INLINE_WIDTH)
        shift = 0
        for y in range(y_size - 1):
            shift += params[1][y] + INLINE_WIDTH
            draw.line((0, start_pix + shift, width, start_pix + shift), fill=0, width=INLINE_WIDTH)
        # endregion

        # region coloring cells if board_color is not None
        if color_matrix is not None:
            if color_matrix == 'default':
                color_matrix = TableDrawer.create_default_color_matrix(board)
            start_pix = OUTLINE_WIDTH
            shift_x = 0
            shift_y = 0
            for x in range(x_size):
                shift_y = 0
                for y in range(y_size):
                    seed = (start_pix + shift_x, start_pix + shift_y)
                    shift_y += params[1][y] + INLINE_WIDTH
                    if (color_matrix[y][x] is tuple) and (len(color_matrix[y][x]) == 3):
                        ImageDraw.floodfill(img, seed, color_matrix[y][x])
                        continue
                    if color_matrix[y][x] in GREY_TAGS:
                        ImageDraw.floodfill(img, seed, C_GREY)
                    if color_matrix[y][x] in GREEN_TAGS:
                        ImageDraw.floodfill(img, seed, C_GREEN)
                    if color_matrix[y][x] in RED_TAGS:
                        ImageDraw.floodfill(img, seed, C_RED)
                shift_x += params[0][x] + INLINE_WIDTH
        # endregion

        # region printing text
        if empty_matrix is None:
            empty_matrix = [[1 for i in range(len(params[0]))] for j in range(len(params[1]))]
        if empty_matrix == 'default':
            empty_matrix = TableDrawer.create_default_empty_matrix(board)
        fnt = ImageFont.truetype('times.ttf', font_size)
        start_pix = OUTLINE_WIDTH
        shift_x = 0
        shift_y = 0
        for x in range(x_size):
            shift_y = 0
            for y in range(y_size):
                fnt_seed = (start_pix + shift_x + params[0][x] / 2, start_pix + shift_y + params[1][y] / 2)
                shift_y += params[1][y] + INLINE_WIDTH
                if empty_matrix[y][x] == 1:
                    draw.text(fnt_seed, str(board[y][x]), font=fnt, fill=0, anchor='mm')
            shift_x += params[0][x] + INLINE_WIDTH
        # endregion

        img.show()
        img.save(path + 'abaka_table.png', 'PNG')

    @staticmethod
    def board_params(board, font_size):
        # first array in params stands for x-size of cells, second for y-size
        # x and y are inverted because board is transposed to x-y basis
        params = [[], []]
        fnt = ImageFont.truetype('times.ttf', font_size)
        x_len = len(board)
        y_len = len(board[0])
        for y in range(y_len):
            box = fnt.getbbox(str(board[0][y]))
            params[0].append(box[2])
        for x in range(x_len):
            if fnt.getbbox(str(board[x][0]))[1] < fnt.getbbox(SMALLEST_STRING)[1]:
                box = fnt.getbbox(SMALLEST_STRING)
            else:
                box = fnt.getbbox(str(board[x][0]))
            params[1].append(box[3])

        # resizes params arrays to make cells square if they look like high rectangle (x < y)
        min_y = 1000000
        for x in range(x_len):
            if params[1][x] < min_y:
                min_y = params[1][x]
        for y in range(y_len):
            if params[0][y] < min_y:
                params[0][y] = min_y

        # makes cells larger to fit the text with gaps
        for y in range(y_len):
            params[0][y] += 2 * int(font_size / 4)
        for x in range(x_len):
            params[1][x] += 2 * int(font_size / 4)

        return params

    # default coloring - colors in green, red or gey and works only for int
    # >0 - green, ==0 - grey, <0 - red, else - grey
    @staticmethod
    def create_default_color_matrix(board):
        color_matrix = [[0 for i in range(len(board[0]))] for j in range(len(board))]
        for x in range(len(board)):
            for y in range(len(board[0])):
                if type(board[x][y]) is int:
                    if board[x][y] < 0:
                        color_matrix[x][y] = C_RED
                    if board[x][y] > 0:
                        color_matrix[x][y] = C_GREEN
                else:
                    color_matrix[x][y] = C_GREY
        return color_matrix

    # default empty matrix: 0 - empty, 1 - print text
    # in default '' or ' ' in board stands for empty
    @staticmethod
    def create_default_empty_matrix(board):
        empty_matrix = [[0 for i in range(len(board[0]))] for j in range(len(board))]
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] in ['', ' ']:
                    empty_matrix[x][y] = 0
                else:
                    empty_matrix[x][y] = 1
        return empty_matrix


board_mask = [["hello", '', '', '', ''],
              [1, 1, 1, '', ''],
              [1, 1, -1, -1, -1],
              ['', '', -1, -1, 1],
              ['', '', '', '', '']]
board_color_mask = [[0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0],
                    [1, 1, -1, -1, -1],
                    [0, 0, -1, -1, 1],
                    [0, 0, 0, 0, 0]]
TableDrawer.draw_table(board_mask, 40, color_matrix=board_color_mask, empty_matrix='default')
