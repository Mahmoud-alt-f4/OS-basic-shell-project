def tokenize(line):
    """Convert input line into list of tokens."""
    tokens = []
    i = 0
    L = len(line)

    while i < L:
        ch = line[i]

        # skip spaces
        if ch.isspace():
            i += 1
            continue

        # >>
        if ch == '>' and i + 1 < L and line[i+1] == '>':
            tokens.append('>>')
            i += 2
            continue

        # single-char specials
        if ch in ['|', '<', '>', '&']:
            tokens.append(ch)
            i += 1
            continue

        # quoted string
        if ch in ['"', "'"]:
            quote = ch
            i += 1
            buf = []
            while i < L and line[i] != quote:
                buf.append(line[i])
                i += 1
            i += 1  # skip closing quote
            tokens.append(''.join(buf))
            continue

        # normal token
        buf = []
        while (
            i < L 
            and not line[i].isspace() 
            and line[i] not in ['|', '<', '>', '&', '"', "'"]
        ):
            buf.append(line[i])
            i += 1

        tokens.append(''.join(buf))

    return tokens


def parse_tokens(tokens):
    """Group tokens into dict describing each command."""
    cmds = []
    cur = {"argv": [], "in": None, "out": None, "append": False, "bg": False}

    i = 0
    L = len(tokens)
    while i < L:
        t = tokens[i]

        if t == "|":
            cmds.append(cur)
            cur = {"argv": [], "in": None, "out": None, "append": False, "bg": False}
            i += 1
            continue

        elif t == "<":
            cur["in"] = tokens[i+1]
            i += 2
            continue

        elif t == ">":
            cur["out"] = tokens[i+1]
            cur["append"] = False
            i += 2
            continue

        elif t == ">>":
            cur["out"] = tokens[i+1]
            cur["append"] = True
            i += 2
            continue

        elif t == "&":
            cur["bg"] = True
            i += 1
            continue

        else:
            cur["argv"].append(t)
            i += 1

    if cur["argv"] or cur["in"] or cur["out"] or cur["bg"]:
        cmds.append(cur)

    return cmds


def parse_line(line):
    """Shortcut: tokenize then parse."""
    return parse_tokens(tokenize(line))


if __name__ == "__main__":
    while True:
        line = input("$ ")
        print(parse_line(line))

