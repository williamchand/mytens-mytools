import os
import sys
import json
import re
import pathlib


def print_message(msg_type, **kwargs):
    """"""
    if msg_type == "exception":
        print("\nAn exception ocurred:", "{}".format(kwargs["exc"]))

    elif msg_type == "invalid_path":
        print(
            "\nGiven path is not valid, please confirm",
            kwargs["path"],
            "has no typos.\n",
        )

    elif msg_type == "completed":
        print("\n(っ◕‿◕)っ   ", "Conversion completed", "   ⊂(´･◡･⊂ )∘˚\n")


def validate_path(path):
    valid = True
    if not os.path.isfile(path):
        valid = False

    if not valid:
        print_message("invalid_path", **{"path": path})
        sys.exit(2)

    return path


def run_convert(source_path, output_path, type_data):
    """Trigger conver command based given params.

    :param source_path: source file path
    :type source_path: string
    :param output_path: output file path
    :type type_data: string
    :param type_data: ffmpeg command options
    """

    # Using readlines()
    source_file = open(source_path, "r")
    lines = source_file.readlines()

    count = 0
    # Strips the newline character
    result = []
    for line in lines:
        result.append(line.strip())
    source_file.close()
    if type_data == "text":
        result = "\n".join(result)
    elif type_data == "json":
        result = json_map_log(result)
    pathlib.Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)
    dest_file = open(output_path, "w")
    dest_file.write(result)
    dest_file.close()


def json_map_log(logs):
    result = []
    lineformat = re.compile(
        r"""^(?P<timestamp>\d{4}/\d{2}/\d{2}\ \d{2}:\d{2}:\d{2})
    \ \[(?P<severity>emerg|alert|crit|error|warn|notice|info)\]
    \ (?P<process_id>\d+)
    \#(?P<thread_id>\d+):
    (\ \*(?P<connection_id>\d+))?
    \ (?P<error>.+?)
    (?:\ while\ (?P<context>.+?))?
    (?:,\ client:\ (?P<client_ip>\d+\.\d+\.\d+\.\d+)
    ,\ server:\ (?P<server>.+?))?
    (?:,\ request:\ \"(?P<request_method>[A-Z]+?)
        \ (?P<request_path>\/.*?)
        \ (?P<request_protocol>.+?)\")?
    (?:,\ upstream:\ \"(?P<upstream>.+?)\")?
    (?:,\ host:\ \"(?P<host>.+?)\")?
    (?:,\ referrer:\ \"(?P<referrer>.+?)\")?
    $
    """,
        re.IGNORECASE | re.VERBOSE,
    )
    for log in logs:
        m = re.search(lineformat, log)
        result.append(m.groupdict())
    return json.dumps(result, indent=4)
