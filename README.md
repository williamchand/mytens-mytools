# mytens-mytools-cli

_A linux file log converter command line program in Python._

## Purpose

This is a custom Python (3) CLI for linux file log

I've done this to make it easy to convert my linux file log into different
formats plaintext and json

## Install

Plug & Play:

    $ git clone https://github.com/williamchand/mytens-mytools.git
    $ cd mytens-mytools
    $ pip3 install -r requirements.txt
    $ pip3 install .

If you want to play around with the code I'd recommend creating a virtual environment first (with python3):
$ pip install -r requirements-dev.txt
$ python setup.py develop

## Usage

The idea is for the CLI to ask you for the necessary information in order to work,
the only thing you should know is that if what you are interested in is converting JSON
you should use the flag `-t json` command:

    $ mytools /var/log/nginx/error.log -t json

If you are interested in converting Plaintext then
use command flag `-t text`:

    $ mytools /var/log/nginx/error.log -t text

Full command list follows:

    Usage:
        mytools /var/log/nginx/error.log
        mytools /var/log/nginx/error.log -t text
        mytools /var/log/nginx/error.log -t json
        mytools /var/log/nginx/error.log -o /User/johnmayer/Desktop/nginxlog.txt
        mytools /var/log/nginx/error.log -t json -o /User/johnmayer/Desktop/nginxlog.json
        mytools -h | --help
        mytools -v | --version

    Options:
        -h --help                         Show this screen.
        -v --version                      Show version.
        -t --type                         Convert log to data type files
        -o --output                       Output file path

Notice if you enter without specifying any path then the output file will
be in the same directory as the source file `/var/log/nginx/`
nginx file example `error.log`

## Dependencies

- [docopt](https://github.com/docopt/docopt)

## Contributing

Feel free to report any bugs or submit feature requests.

Pull requests are welcome as well.
