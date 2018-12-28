import neovim
import re

# todo : on )

@neovim.plugin
class SurroundPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim
        self.surroundings = [['(', ')'], ['[', ']'], ['{', '}'], ['<', '>'],
                ['\'', '\''], ['"', '"'], ['`', '`']]

    def echo(self, msg):
        self.nvim.out_write(msg + "\n")

    # look up a pair of surroundings corresponding to an argument.
    def lookup_surrounding(self, arg):
        for surrounding in self.surroundings:
            if surrounding[0] == arg or surrounding[1] == arg:
                return surrounding

    # search a pair of surroundings from buffer.
    def search_surroundings(self, surrounding, row, starting_point):
        # ] is must be placed at the beginning of the character set.
        match = re.search('[' + surrounding[1] + surrounding[0] + ']',
                    self.nvim.current.buffer[row][starting_point:])
        if match == None: # Next line
            if (len(self.nvim.current.buffer) - 1) \
                    <= row or self.nvim.current.buffer[row+1] == '':
                # End line or Blank line
                return
            return self.search_surroundings(surrounding, row + 1, 0)
        elif match[0] == surrounding[1]:
            return row, starting_point + match.start()
        elif match[0] == surrounding[0]:
            index = self.search_surroundings(
                        surrounding, row, starting_point + match.start() + 1
                    )
            return self.search_surroundings(surrounding, index[0], index[1] + 1)
        return

    @neovim.command('RmSurround', range='', nargs='0', sync=True)
    def remove_surround(self, args, range):
        cursor = self.nvim.current.window.cursor
        surrounding = self.lookup_surrounding(self.nvim.current.line[cursor[1]])
        if not surrounding:
            self.echo('Not surrounding character')
            return
        index = self.search_surroundings(surrounding, cursor[0]-1, cursor[1]+1)
        if index == None:
            self.echo('Do\'t find surrounding character')
            return
        endLine = self.nvim.current.buffer[index[0]]
        self.nvim.current.buffer[index[0]] \
            = endLine[:index[1]] + endLine[index[1]+1:]
        self.nvim.current.line \
            = self.nvim.current.line[:cursor[1]] \
                + self.nvim.current.line[cursor[1]+1:]

    @neovim.function('ChSurround', sync=True)
    def change_surround(self, args):
        cursor = self.nvim.current.window.cursor
        before_surrounding = self.lookup_surrounding(self.nvim.current.line[cursor[1]])
        after_surrounding = self.lookup_surrounding(args[0])

        if before_surrounding == None or after_surrounding == None:
            self.echo('Not surrounding character')
            return
        index = self.search_surroundings(before_surrounding, cursor[0]-1, cursor[1]+1)
        if index == None:
            self.echo('Do\'t find surrounding character')
            return

        endLine = self.nvim.current.buffer[index[0]]
        self.nvim.current.buffer[index[0]] \
            = endLine[:index[1]] + after_surrounding[1] + endLine[index[1]+1:]
        self.nvim.current.line \
            = self.nvim.current.line[:cursor[1]] \
                + after_surrounding[0] + self.nvim.current.line[cursor[1]+1:]

    def getInsertedLine(self, surrounding):
        match = re.search('\S', self.nvim.current.line)
        return self.nvim.current.line[:match.start()] \
                + surrounding[0] \
                + self.nvim.current.line[match.start():] \
                + surrounding[1]

    @neovim.function('SurroundLine', sync=True)
    def surround_line(self, args):
        surrounding = self.lookup_surrounding(args[0])
        if surrounding:
            self.nvim.current.line = self.getInsertedLine(surrounding)

    def getInsertedWord(self, surrounding):
        line = self.nvim.current.line
        cursor = self.nvim.current.window.cursor[1]
        right = self.nvim.current.line.find(' ', cursor)
        if right < 0:
            right = len(self.nvim.current.line)
        left = self.nvim.current.line.rfind(' ', 0, cursor)
        return line[:left+1] \
                + surrounding[0] \
                + line[left+1:right] \
                + surrounding[1] \
                + line[right:]

    @neovim.function('SurroundWord', sync=True)
    def surround_word(self, args):
        surrounding = self.lookup_surrounding(args[0])
        if surrounding:
            self.nvim.current.line = self.getInsertedWord(surrounding)
