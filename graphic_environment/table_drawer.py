from PIL import Image, ImageDraw, ImageFont
from conf import PATH, user_path
from conf import OUTLINE_WIDTH, INLINE_WIDTH
from conf import C_RED, C_GREEN, C_GREY
from conf import RED_TAGS, GREEN_TAGS, GREY_TAGS


class TableDrawer:
    @staticmethod
    def draw_table(board, font_size, board_color=None):
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
        print(start_pix)
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
        if board_color is not None:
            start_pix = OUTLINE_WIDTH
            shift_x = 0
            shift_y = 0
            for x in range(x_size):
                shift_y = 0
                for y in range(y_size):
                    seed = (start_pix + shift_x, start_pix + shift_y)
                    if board_color[y][x] in GREY_TAGS:
                        ImageDraw.floodfill(img, seed, C_GREY)
                    if board_color[y][x] in GREEN_TAGS:
                        ImageDraw.floodfill(img, seed, C_GREEN)
                    if board_color[y][x] in RED_TAGS:
                        ImageDraw.floodfill(img, seed, C_RED)
                    shift_y += params[1][y] + INLINE_WIDTH
                shift_x += params[0][x] + INLINE_WIDTH
        # endregion

        # region printing text
        fnt = ImageFont.truetype('times.ttf', font_size)
        start_pix = OUTLINE_WIDTH
        shift_x = 0
        shift_y = 0
        for x in range(x_size):
            shift_y = 0
            for y in range(y_size):
                fnt_seed = (start_pix + shift_x + params[0][x] / 2, start_pix + shift_y + params[1][y] / 2)
                draw.text(fnt_seed, str(board[y][x]), font=fnt, fill=0, anchor='mm')
                shift_y += params[1][y] + INLINE_WIDTH
            shift_x += params[0][x] + INLINE_WIDTH
        # endregion

        img.show()
        img.save(path + 'abaka_table.png', 'PNG')

        # old code
        # with Image.open(path + 'BlankTable.png') as im:
        #     draw = ImageDraw.Draw(im)
        #     size = im.size[0]
        #     color = 0
        #     # region drawing box
        #     draw.line((2, 0, 2, size), fill=color, width=5)
        #     draw.line((0, 2, size, 2), fill=color, width=5)
        #     draw.line((size - 3, 0, size - 3, size), fill=color, width=5)
        #     draw.line((0, size - 3, size, size - 3), fill=color, width=5)
        #     # endregion
        #     # region drawing lines for cells
        #     start_coord = 3
        #     shift = 63
        #     for x in range(1, 5):
        #         x_coord = start_coord + shift * x
        #         draw.line((x_coord, 0, x_coord, size), fill=color, width=3)
        #     for y in range(1, 5):
        #         y_coord = start_coord + shift * y
        #         draw.line((0, y_coord, size, y_coord), fill=color, width=3)
        #     # endregion
        #     # region filling cells with colors and drawing cell values
        #     start_coord = 5
        #     shift = 63
        #     replace_red = (244, 113, 116)
        #     replace_green = (137, 232, 148)
        #     replace_grey = (209, 207, 200)
        #     fnt = ImageFont.truetype('times.ttf', 40)
        #     for x in range(5):
        #         for y in range(5):
        #             seed = (start_coord + x * shift, start_coord + y * shift)
        #             fnt_seed = (20 + seed[0], 10 + seed[1])
        #             if final_board[x][y] < 0:
        #                 ImageDraw.floodfill(im, seed, replace_red)
        #                 draw.text(fnt_seed, '0', font=fnt, fill=0)
        #             if final_board[x][y] > 0:
        #                 ImageDraw.floodfill(im, seed, replace_green)
        #                 draw.text(fnt_seed, str(final_board[x][y]), font=fnt, fill=0)
        #             if final_board[x][y] == 0:
        #                 ImageDraw.floodfill(im, seed, replace_grey)
        #     # endregion
        #     # im.show()
        #     im.save(path + 'CompleteTable.png', 'PNG')
        #     return path + 'CompleteTable.png'

    @staticmethod
    def get_cell_value(board, x, y):
        if board[x][y] < 1:
            return board[x][y]
        value = 1
        check_x = [-1, 1]
        check_y = [-1, 1]
        if x == 0 and x != 4:
            check_x = [1]
        if x == 4 and x != 0:
            check_x = [-1]
        if y == 0 and y != 4:
            check_y = [1]
        if y == 4 and y != 0:
            check_y = [-1]
        for ind_x in check_x:
            if board[x + ind_x][y] == 1:
                value += 1
        for ind_y in check_y:
            if board[x][y + ind_y] == 1:
                value += 1
        return value

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


board_mask = [["hello", 0, 0, 0, 0],
              [1, 1, 1, 0, 0],
              [1, 1, -1, -1, -1],
              [0, 0, -1, -1, 1],
              [0, 0, 0, 0, 0]]
board_color_mask = [[0, 0, 0, 0, 0],
               [1, 1, 1, 0, 0],
               [1, 1, -1, -1, -1],
               [0, 0, -1, -1, 1],
               [0, 0, 0, 0, 0]]
TableDrawer.draw_table(board_mask, 40, board_color_mask)
