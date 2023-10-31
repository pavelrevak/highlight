"""Text or log files highlighter and or analyzer"""

import fileinput as _fileinput
import argparse as _argparse


COLORS = {
    ('black', '', '\033[30m', '\033[40m'),
    ('red', 'r', '\033[31m', '\033[41m'),
    ('yellow', 'y', '\033[33m', '\033[43m'),
    ('green', 'g', '\033[32m', '\033[42m'),
    ('cyan', 'c', '\033[36m', '\033[46m'),
    ('blue', 'b', '\033[34m', '\033[44m'),
    ('magenta', 'm', '\033[35m', '\033[45m'),
    ('pink', 'p', '\033[35m', '\033[45m'),
    ('white', 'w', '\033[37m', '\033[47m'),
    ('gray', 'gr', '\033[90m', '\033[100m'),
    ('lred', 'lr', '\033[91m', '\033[101m'),
    ('lyellow', 'ly', '\033[93m', '\033[103m'),
    ('lgreen', 'lg', '\033[92m', '\033[102m'),
    ('lcyan', 'lc', '\033[96m', '\033[106m'),
    ('lblue', 'lb', '\033[94m', '\033[104m'),
    ('lmagenta', 'lm', '\033[95m', '\033[105m'),
    ('lpink', 'lp', '\033[95m', '\033[105m'),
    ('lwhite', 'lw', '\033[97m', '\033[107m'),
    ('black', 'k', '\033[30m', '\033[40m'),
}

COLOR_RESET = '\033[0m'


class UnknowColor(Exception):
    """Unknown color error"""
    def __init__(self, color):
        super().__init__("Unknown color: " + color)


def get_color_code(color):
    """Return color value based on color name"""
    for name, short, fg, bg in COLORS:
        if color in (name, short):
            return fg, bg
    raise UnknowColor(color)


def get_color(color):
    if ':' in color:
        fg, bg = color.split(':')
        return get_color_code(bg)[1] + get_color_code(fg)[0]
    return COLOR_RESET + get_color_code(color)[0]


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
                    graph[index] = color_value + mark + COLOR_RESET
                elif stop in line:
                    graph[index] = color_value + '.' * len(mark) + COLOR_RESET
        line_color = None
        if args.line:
            for color, patterns in highlight_line.items():
                for pattern in patterns:
                    if pattern in line:
                        line_color = color
                        break
                if line_color:
                    colored_line = line_color + colored_line + COLOR_RESET
                    break
        if args.word:
            if line_color is None:
                line_color = COLOR_RESET
            for color, patterns in highlight_word.items():
                for pattern in patterns:
                    if pattern in line:
                        colored_line = colored_line.replace(
                            pattern, color + pattern + COLOR_RESET + line_color)
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
