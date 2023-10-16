# Highlight

Simple tool to highlight and graph text files, especially log files like text log analyzer.

## Supports

- filter lines to include or exclude by text match
- colorize words or colorize whole line with text match
- create simple binary graph, based on START and END text match

### filter lines

Print only lines with text ERROR and WARNING but exclude with text "open file" and "close file" (like `grep` or `grep -v` to exclude)

```
$ highlight -i ERROR -i WARNING -e "open file" -e "close file"
```

### highlight lines

Colorize lines to `red` containing text `ERROR`, to `yellow` with WARNING

```
$ highlight -l r ERROR -l y WARNING
```

### highlight word

Colorize word `socket.read` to `blue` socket.write to `pink`.

```
$ highlight -w b socket.read -l p socket.write
```

### graph

Create vertical graph line with `cyan` character `C` where start is with text `connection.lock` and stops with `connection.unlock` and `yellow` `G` starting `gate open` ending `gate close`

```
$ highlight -g c C connection.lock connection.unlock -g y G "gate open" "gate close"
```

## supported colors

- `default` - default terminal color
- `red`
- `yellow`
- `green`
- `cyan`
- `blue`
- `pink`
- `white`

As color you can use any case and also only first character(s) like `Green`, `GRE` or `g`

## help

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
