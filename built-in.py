# ------------------- "Libirariess"------------------- #
import os
import sys

# ------------------- "Built-in commandss"------------------- #
def execute_builtin(cmd):
    """
    Executes built-in commands:
    cd, pwd, exit, help
    Returns True if command is built-in, else False.
    """
    if not cmd or not cmd.get("argv"):
        return False
    command_name = cmd["argv"][0]
    args = cmd["argv"][1:]

    # --------- "Change directory"--------- #
    if command_name == "cd":
        if len(args) == 0:
            ### no argument soo go to home
            try:
                os.chdir(os.path.expanduser("~"))
            except Exception as e:
                print(f"cd: error: {e}")
        else:
            target_dir = args[0]
            try:
                os.chdir(target_dir)
            except FileNotFoundError:
                print(f"cd: {target_dir}: No such file or directory")
            except PermissionError:
                print(f"cd: {target_dir}: Permission denied")
            except Exception as e:
                print(f"cd: error: {e}")
        return True

    # --------- "Print current working directory"--------- #
    elif command_name == "pwd":
        print(os.getcwd())
        return True

    # --------- "Exit the shell"--------- #
    elif command_name == "exit":
        exit_code = 0
        if len(args) > 0:
            try:
                exit_code = int(args[0])
            except ValueError:
                print(f"exit: {args[0]}: numeric argument required")
        sys.exit(exit_code)

    # --------- "Show built-in commands"--------- #
    elif command_name == "help":
        print("Simple Shell - Built-in Commands:")
        print("  cd [directory]    Change the current directory")
        print("  pwd               Print the current working directory")
        print("  exit [code]       Exit the shell with optional exit code")
        print("  help              Display this help message")
        return True
    ### Not a built-in command
    return False

# ------------------- "Tokenizerrr"------------------- #
def tokenize(line):
    """Convert input line into list of tokens."""
    tokens = []
    i = 0
    L = len(line)

    while i < L:
        ch = line[i]
        # --------- "skip spaces"--------- #
        if ch.isspace():
            i += 1
            continue
        # --------- "append redirection"--------- #
        if ch == '>' and i + 1 < L and line[i+1] == '>':
            tokens.append('>>')
            i += 2
            continue
        # --------- "single-char specials"--------- #
        if ch in ['|', '<', '>', '&']:
            tokens.append(ch)
            i += 1
            continue
        # --------- "quoted stringgg"--------- #
        if ch in ['"', "'"]:
            quote = ch
            i += 1
            buf = []
            while i < L and line[i] != quote:
                buf.append(line[i])
                i += 1
            if i < L:
                i += 1  ### skip closing quote
            tokens.append(''.join(buf))
            continue
        # --------- "normal token"--------- #
        buf = []
        while (
            i < L and
            not line[i].isspace() and
            line[i] not in ['|', '<', '>', '&', '"', "'"]
        ):
            buf.append(line[i])
            i += 1
        tokens.append(''.join(buf))
    return tokens

# ------------------- "Parserrr"------------------- #
def parse_tokens(tokens):
    """
    convert list of tokens into command dic.
    Each command has:
      - argv: list of words
      - in: input redirection file
      - out: output redirection file
      - append: True if >>
      - bg: True if background (&)
    """
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
            if i + 1 < L:
                cur["in"] = tokens[i + 1]
            i += 2
            continue

        elif t == ">":
            if i + 1 < L:
                cur["out"] = tokens[i + 1]
                cur["append"] = False
            i += 2
            continue

        elif t == ">>":
            if i + 1 < L:
                cur["out"] = tokens[i + 1]
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
    """shortcut to tokenize and parse a line"""
    return parse_tokens(tokenize(line))

# ------------------- "Main Loopppppp"------------------- #
def main():
    while True:
        try:
            user_input = input("$ ").strip()
            if not user_input:
                continue ### skip empty lines

            # --------- "parse input into commandsss"--------- #
            commands = tokenize(user_input)
            if not commands:
                continue

            for cmd in commands:
                # --------- "check for built-in"--------- #
                if execute_builtin(cmd):
                    continue
            
                # --------- "placeholder for external commands / redirection / pipin"--------- #
                print(f"[External command not yet implemented: {' '.join(cmd['argv'])}]")

        except EOFError:
            ### Ctrl^D
            print()
            print("exit")
            break
        
        except KeyboardInterrupt:
            ### Ctrl^C 
            print()
            continue
        
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()