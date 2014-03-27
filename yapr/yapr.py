"""
The layout of this application (and some code snippets) is inspired by BTC:
 - https://github.com/bittorrent/btc/blob/master/btc/btc.py


"""

__author__ = 'wallsr'

import atexit
import os
import re
import sys


def finish():
    try:
        sys.stdout.close()
    except:
        pass
    try:
        sys.stderr.close()
    except:
        pass

atexit.register(finish)


def error(msg, die=True):
    sys.stderr.write('%s: error: %s%s' % (os.path.basename(sys.argv[0]), msg, os.linesep))
    if die:
        exit(1)


def warning(msg):
    sys.stderr.write('%s: warning: %s%s' % (os.path.basename(sys.argv[0]), msg, os.linesep))


def usage(commands):
    print 'usage: yapr <command> [<args>]'
    print ''
    print 'commands are:' + os.linesep

    for c in sorted(commands.keys()):
        if hasattr(commands[c], '_description'):
            desc = commands[c]._description
        else:
            desc = 'NO _description DEFINED FOR SUBCOMMAND'
        print '    %-15s: %s' % (c, desc)
    print('')
    print("hint: use any command and --help if lost")


def __get_commands():
    """
    Returns a dictionary of command modules indexed by name.

    Commands should be in separate python scripts with the
    filename yapr_COMMAND.py
    """
    commands = {}

    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)

    for filepath in os.listdir(dirname):
        match = re.match(r'yapr_(.*)\.py', filepath)

        if not match:
            continue

        name = match.group(1)
        module_name = 'yapr_%s' % name
        module = getattr(__import__('yapr.%s' % module_name), module_name)
        commands[name] = module

    return commands


def main():
    commands = __get_commands()

    if len(sys.argv) < 2:
        usage(commands)
        exit(1)

    if sys.argv[1] not in commands:
        error('no such command: %s' % sys.argv[1], False)
        print('')
        usage(commands)
        exit(1)

    module = commands[sys.argv[1]]
    sys.argv[0] += ' %s' % sys.argv[1]
    del sys.argv[1]

    try:
        module.main()
    except KeyboardInterrupt:
        pass

    exit(0)


if __name__ == "__main__":
    main()



