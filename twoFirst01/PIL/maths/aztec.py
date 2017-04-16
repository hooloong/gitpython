import argparse
import random
import cairo


# 4 colors for the 4 types of dominoes
N_COLOR = (1, 0.25, 0.5)
S_COLOR = (0.75, 0.5, 0.25)
W_COLOR = (0.1, 0.25, 0.75)
E_COLOR = (0.25, 0.8, 0.5)


class AzGraph(object):
    '''
    Use a dict to represent a tiling of an az graph.
    Each cell (a 1x1 square) is specified by the coordinate of its left-bottom corner.
    A cell has five possible types: 'n', 's', 'w', 'e', None,
    where None means it's an empty cell.
    Be careful that one should always start from the boundary when
    deleting or filling blocks, this is an implicit but important part in the algorithm.
    '''

    def __init__(self, n):
        self.order = n

        self.cells = []
        for j in range(-n, n):
            k = min(n+1+j, n-j)
            for i in range(-k, k):
                self.cells.append((i, j))

        self.tile = {cell: None for cell in self.cells}


    @staticmethod
    def block(i, j):
        '''
        Return the 2x2 block with its bottom-left cell at (i, j)
        '''
        return [(i, j), (i+1, j), (i, j+1), (i+1, j+1)]


    def is_black(self, i, j):
        '''
        Check if cell (i, j) is colored black.
        Note that the chessboard is colored so that the leftmost cell in the top row is white.
        '''
        return (i + j + self.order) % 2 == 1


    def check_block(self, i, j, dominoes):
        '''
        Check whether a block is filled with dominoes of given orientations.
        '''
        return all(self.tile[cell] == fill for cell, fill in zip(self.block(i, j), dominoes))


    def fill_block(self, i, j, dominoes):
        '''
        Fill a block with two dominoes of given orientations.
        '''
        for cell, fill in zip(self.block(i, j), dominoes):
            self.tile[cell] = fill


    def delete(self):
        '''
        Delete all bad blocks in a tiling.
        A block is called bad if it contains a pair of parellel dominoes that
        has orientations toward each other.
        '''
        for i, j in self.cells:
            try:
                if (self.check_block(i, j, ['n', 'n', 's', 's'])
                        or self.check_block(i, j, ['e', 'w', 'e', 'w'])):
                    self.fill_block(i, j, [None]*4)
            except KeyError:
                pass
        return self


    def slide(self):
        '''
        Move all dominoes one step according to their orientations.
        '''
        new_board = AzGraph(self.order + 1)
        for (i, j) in self.cells:
            if self.tile[(i, j)] == 'n':
                new_board.tile[(i, j+1)] = 'n'
            if self.tile[(i, j)] == 's':
                new_board.tile[(i, j-1)] = 's'
            if self.tile[(i, j)] == 'w':
                new_board.tile[(i-1, j)] = 'w'
            if self.tile[(i, j)] == 'e':
                new_board.tile[(i+1, j)] = 'e'
        return new_board


    def create(self):
        '''
        Fill all holes with pairs of dominoes that leaving each other.
        This is a somewhat subtle step in this program since after the sliding step
        we are working on a larger (hence different) chessboard now!
        '''
        for i, j in self.cells:
            try:
                if self.check_block(i, j, [None]*4):
                    if random.random() > 0.5:
                        self.fill_block(i, j, ['s', 's', 'n', 'n'])
                    else:
                        self.fill_block(i, j, ['w', 'e', 'w', 'e'])

            except KeyError:
                pass
        return self


    def render(self, size, extent, filename, bg_color=(1, 1, 1)):
        '''
        Draw current tiling (might have holes) to a png image with cairo.
        size:
            image size in pixels, e.g. size = 600 means 600x600
        extent:
            range of the axis: [-extent, extent] x [-extent, extent]
        filename:
            output filename, must be a .png image.
        bg_color:
            background color, default to white.
            If set to None then transparent background will show through.
        '''
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
        ctx = cairo.Context(surface)
        ctx.scale(size/(2.0*extent), -size/(2.0*extent))
        ctx.translate(extent, -extent)

        if bg_color:
            ctx.set_source_rgb(*bg_color)
            ctx.paint()

        margin = 0.1

        for (i, j) in self.cells:
            if self.is_black(i, j) and self.tile[(i, j)]:
                if self.tile[(i, j)] == 'n':
                    ctx.rectangle(i - 1 + margin, j + margin,
                                  2 - 2 * margin, 1 - 2 * margin)
                    ctx.set_source_rgb(*N_COLOR)

                if self.tile[(i, j)] == 's':
                    ctx.rectangle(i + margin, j + margin,
                                  2 - 2 * margin, 1 - 2 * margin)
                    ctx.set_source_rgb(*S_COLOR)

                if self.tile[(i, j)] == 'w':
                    ctx.rectangle(i + margin, j + margin,
                                  1 - 2 * margin, 2 - 2 * margin)
                    ctx.set_source_rgb(*W_COLOR)

                if self.tile[(i, j)] == 'e':
                    ctx.rectangle(i + margin, j - 1 + margin,
                                  1 - 2 * margin, 2 - 2 * margin)
                    ctx.set_source_rgb(*E_COLOR)

                ctx.fill()

        surface.write_to_png(filename)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-size', metavar='s', type=int,
                        default=600, help='image size')
    parser.add_argument('-order', metavar='o', type=int,
                        default=60, help='order of az graph')
    parser.add_argument('-filename', metavar='f',
                        default='randomtiling.png', help='output filename')
    args = parser.parse_args()

    az = AzGraph(0)
    for _ in range(args.order):
        az = az.delete().slide().create()
    az.render(args.size, args.order + 1, args.filename)


if __name__ == '__main__':
    main()