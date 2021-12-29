import os
import sys
from ..converter_utils import validate_path, print_message, run_convert


class Base(object):
    """A base command."""

    def __init__(self, options, *args, **kwargs):
        """Create the Base object (a command object).

        :param options: command options
        :type options: dict
        """

        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.extension_path_map = {"text": ".txt", "json": ".json"}

    def get_user_input(self):
        """Set all needed variables via user input for the conversion.
        :returns: source_paths
                  output_paths
                  conversion_data_type
        :rtype: string
                string
                string
        """
        source_path = self.options["SOURCE_FILE"]
        source_path = validate_path(source_path)
        data_type = self.options["-t"]
        destination_path = self.options["-o"]
        if data_type == None:
            data_type = "text"
        if destination_path == None:
            destination_path = (
                os.path.splitext(source_path)[0] + self.extension_path_map[data_type]
            )
        return source_path, destination_path, data_type

    def run(self):
        """All commands must implement this method."""
        source_path, destination_path, data_type = self.get_user_input()
        try:
            run_convert(source_path, destination_path, data_type)
            print_message("completed")
        except Exception as exc:
            print_message("exception", **{"exc": exc})
            sys.exit(1)
