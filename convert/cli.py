"""
mytools

Usage:
  mytools SOURCE_FILE [-t TYPE] [-o DEST_FILE]
  mytools -h 
  mytools -v

Options:
  -h                                Show this screen.
  -v                                Show version.
  -t TYPE                           Convert log to data type files
  -o DEST_FILE                      Output file path

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/williamchand/mytens-mytools
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import convert.commands

    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if k and v:
            convert.commands = getmembers(convert.commands.base, isclass)
            command = [command[1] for command in convert.commands][0]
            command = command(options)
            command.run()
            return
