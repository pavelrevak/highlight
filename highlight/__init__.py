"""Text or log files highlighter and or analyzer"""

import fileinput as _fileinput
import argparse as _argparse


COLORS = {
    'default': '\033[0m',
    'black': '\033[30m',
    'red': '\033[31m',
    'yellow': '\033[33m',
    'green': '\033[32m',
    'cyan': '\033[36m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'pink': '\033[35m',
    'white': '\033[37m',

    'gray': '\033[90m',
    'lred': '\033[91m',
    'lyellow': '\033[93m',
    'lgreen': '\033[92m',
    'lcyan': '\033[96m',
    'lblue': '\033[94m',
    'lmagenta': '\033[95m',
    'lpink': '\033[95m',
    'lwhite': '\033[97m',

    'iblack': '\033[40m\033[97m',
    'ired': '\033[41m\033[97m',
    'iyellow': '\033[43m\033[97m',
    'igreen': '\033[42m\033[97m',
    'icyan': '\033[46m\033[97m',
    'iblue': '\033[44m\033[97m',
    'imagenta': '\033[45m\033[97m',
    'ipink': '\033[45m\033[97m',
    'iwhite': '\033[47m\033[30m',

    'igray': '\033[100m\033[97m',
    'ilred': '\033[101m\033[30m',
    'ilyellow': '\033[103m\033[30m',
    'ilgreen': '\033[102m\033[30m',
    'ilcyan': '\033[106m\033[30m',
    'ilblue': '\033[104m\033[30m',
    'ilmagenta': '\033[105m\033[30m',
    'ilpink': '\033[105m\033[30m',
    'ilwhite': '\033[107m\033[30m',
}

DEFAULT_COLOR = COLORS['default']


class UnknowColor(Exception):
    """Unknown color error"""
    def __init__(self, color):
        super().__init__("Unknown color: " + color)


def get_color(color):
    """Return color value based on color name"""
    for name, value in COLORS.items():
        if name.startswith(color.lower()):
            return value
    raise UnknowColor(color)


def action_decode(actions):
    """Decode actions for line or word highlighting"""
    color_map = {}
    for color, pattern in actions:
        color_value = get_color(color)
        if color_value not in color_map:
            color_map[color_value] = [pattern]
        else:
            color_map[color_value].append(pattern)
    return color_map


def match_pattern(line, matchs):
    """Match pattern in line"""
    for match in matchs:
        if match in line:
            return True
    return False


def process(args):
    """Process text file"""
    if args.line:
        highlight_line = action_decode(args.line)
    if args.word:
        highlight_word = action_decode(args.word)

    graph = []
    if args.graph:
        for color, mark, start, stop in args.graph:
            graph.append(' ' * len(mark))

    for line in _fileinput.input(args.files):
        colored_line = line.strip()
        if args.include and not match_pattern(colored_line, args.include):
            continue
        if args.exclude and match_pattern(colored_line, args.exclude):
            continue
        if graph:
            for index, params in enumerate(args.graph):
                color, mark, start, stop = params
                color_value = get_color(color)
                if start in line:
                    graph[index] = color_value + mark + DEFAULT_COLOR
                elif stop in line:
                    graph[index] = color_value + '.' * len(mark) + DEFAULT_COLOR
        line_color = None
        if args.line:
            for color, patterns in highlight_line.items():
                for pattern in patterns:
                    if pattern in line:
                        line_color = color
                        break
                if line_color:
                    colored_line = line_color + colored_line + DEFAULT_COLOR
                    break
        if args.word:
            if line_color is None:
                line_color = DEFAULT_COLOR
            for color, patterns in highlight_word.items():
                for pattern in patterns:
                    if pattern in line:
                        colored_line = colored_line.replace(
                            pattern, color + pattern + line_color)
        print(' '.join(graph) + '  ' + colored_line)


def main():
    """Main"""
    parser = _argparse.ArgumentParser()
    parser.add_argument(
        'files', nargs='*', help="file names, or stdin")
    parser.add_argument(
        '-i', '--include', metavar='MATCH', action='append',
        help="include lines with match")
    parser.add_argument(
        '-e', '--exclude', metavar='MATCH', action='append',
        help="exclude lines with match")
    parser.add_argument(
        '-l', '--line', nargs=2, metavar=('COLOR', 'MATCH'),
        action='append', help="colorize line with match")
    parser.add_argument(
        '-w', '--word', nargs=2, metavar=('COLOR', 'MATCH'),
        action='append', help="colorize match")
    parser.add_argument(
        '-g', '--graph', nargs=4,
        metavar=('COLOR', 'CHAR', 'MATCH_START', 'MATCH_END'),
        action='append', help="draw vertical binary graph on left side")
    process(parser.parse_args())
