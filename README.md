# Highlight

Simple tool to highlight and graph text files, especially log files like text log analyzer.

## Supports

- filter lines to include or exclude by text match
- colorize words or colorize whole line with text match
- create simple binary graph, based on START and END text match

### Filter lines

Print only lines with text ERROR and WARNING but exclude with text "open file" and "close file" (like `grep` or `grep -v` to exclude)

```
$ highlight -i ERROR -i WARNING -e "open file" -e "close file"
```

### Highlight lines

Colorize lines to `red` containing text `ERROR`, to `yellow` with WARNING

```
$ highlight -l r ERROR -l y WARNING
```

### Highlight word

Colorize word `socket.read` to `blue` socket.write to `pink`.

```
$ highlight -w b socket.read -l p socket.write
```

### Graph

Create vertical graph line with `cyan` character `C` where start is with text `connection.lock` and stops with `connection.unlock` and `yellow` `G` starting `gate open` ending `gate close`

```
$ highlight -g c C connection.lock connection.unlock -g y G "gate open" "gate close"
```

### Preview
<img width="933" alt="Screenshot 2023-10-16 at 22 58 54" src="https://github.com/pavelrevak/highlight/assets/9936533/574c6df7-3309-4ec5-8952-dbabf491382e">

## supported colors

    - k   black
    - r   red
    - y   yellow
    - g   green
    - c   cyan
    - b   blue
    - m   magenta
    - p   pink
    - w   white
    - gr  gray
    - lr  lred
    - ly  lyellow
    - lg  lgreen
    - lc  lcyan
    - lb  lblue
    - lm  lmagenta
    - lp  lpink
    - lw  lwhite

### COLOR format

    - foreground             lr   lred
    - :background            :g   :green
    - foreground:background  w:b  white:blue

## Help

```
$ highlight --help
usage: highlight.py [-h] [-i MATCH] [-e MATCH] [-l COLOR MATCH] [-w COLOR MATCH] [-g COLOR CHAR MATCH_START MATCH_END] [files ...]

positional arguments:
  files                 file names, or pipe

options:
  -h, --help            show this help message and exit
  -i MATCH, --include MATCH
                        include lines with match
  -e MATCH, --exclude MATCH
                        exclude lines with match
  -l COLOR MATCH, --line COLOR MATCH
                        colorize line with match
  -w COLOR MATCH, --word COLOR MATCH
                        colorize match
  -g COLOR CHAR MATCH_START MATCH_END, --graph COLOR CHAR MATCH_START MATCH_END
                        draw vertical binary graph on left side
```

## Installation

```
pip install git+https://github.com/pavelrevak/highlight.git
```

### Uninstall

```
pip uninstall log-highlighter
```
