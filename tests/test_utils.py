import os

import mock
import pytest
from converter_utils import validate_path, run_convert
from convert.commands.base import Base
import json


class TestUserInput(object):
    def setup(self):
        self.file_path = os.path.abspath(__file__)
        self.options = {
            "-t": "text",
            "-o": self.file_path,
            "SOURCE_FILE": self.file_path,
        }

    def test_get_user_input_source_file_complete(self):
        source_path, destination_path, data_type = Base(self.options).get_user_input()
        assert source_path == self.file_path
        assert destination_path == self.file_path
        assert data_type == "text"

    def test_get_user_input_source_file_type_none(self):
        self.options["-t"] = None
        source_path, destination_path, data_type = Base(self.options).get_user_input()
        assert source_path == self.file_path
        assert destination_path == self.file_path
        assert data_type == "text"

    def test_get_user_input_source_file_type_json(self):
        self.options["-t"] = "json"
        source_path, destination_path, data_type = Base(self.options).get_user_input()
        assert source_path == self.file_path
        assert destination_path == self.file_path
        assert data_type == "json"

    def test_get_user_input_source_destination_none_type_text(self):
        self.options["-o"] = None
        source_path, destination_path, data_type = Base(self.options).get_user_input()
        assert source_path == self.file_path
        assert destination_path == os.path.splitext(source_path)[0] + ".txt"
        assert data_type == "text"

    def test_get_user_input_source_destination_none_type_json(self):
        self.options["-t"] = "json"
        self.options["-o"] = None
        source_path, destination_path, data_type = Base(self.options).get_user_input()
        assert source_path == self.file_path
        assert destination_path == os.path.splitext(source_path)[0] + ".json"
        assert data_type == "json"


class TestConvert(object):
    def setup(self):
        self.file_path = os.path.abspath(__file__)
        self.options = {
            "-t": "text",
            "-o": self.file_path,
            "SOURCE_FILE": self.file_path,
        }
        self.open_name = "%s.open" % __name__

    def test_convert_success_json(self):
        self.options["-t"] = "json"
        with mock.patch(
            "builtins.open",
            mock.mock_open(
                read_data="""2017/10/05 14:30:14 [emerg] 26048#0: unexpected end of file, expecting "}" in /home/andrey_murzich/nginx/conf/hosts.conf:23\n2017/10/05 14:34:27 [error] 26174#0: *1 open() "/home/andrey_murzich/nginx/html/favicon.ico" failed (2: No such file or directory), client: 127.0.0.1, server: 192.168.122.73, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8080"""
            ),
        ) as mock_file:
            Base(self.options).run()
            mock_file.assert_called_with(self.file_path, "w")
            assert_write = [
                {
                    "timestamp": "2017/10/05 14:30:14",
                    "severity": "emerg",
                    "process_id": "26048",
                    "thread_id": "0",
                    "connection_id": None,
                    "error": 'unexpected end of file, expecting "}" in /home/andrey_murzich/nginx/conf/hosts.conf:23',
                    "context": None,
                    "client_ip": None,
                    "server": None,
                    "request_method": None,
                    "request_path": None,
                    "request_protocol": None,
                    "upstream": None,
                    "host": None,
                    "referrer": None,
                },
                {
                    "timestamp": "2017/10/05 14:34:27",
                    "severity": "error",
                    "process_id": "26174",
                    "thread_id": "0",
                    "connection_id": "1",
                    "error": 'open() "/home/andrey_murzich/nginx/html/favicon.ico" failed (2: No such file or directory)',
                    "context": None,
                    "client_ip": "127.0.0.1",
                    "server": '192.168.122.73, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8080',
                    "request_method": None,
                    "request_path": None,
                    "request_protocol": None,
                    "upstream": None,
                    "host": None,
                    "referrer": None,
                },
            ]
            handle = mock_file()
            handle.write.assert_called_once_with(json.dumps(assert_write, indent=4))

    def test_convert_success_text(self):
        with mock.patch(
            "builtins.open",
            mock.mock_open(
                read_data="""2017/10/05 14:30:14 [emerg] 26048#0: unexpected end of file, expecting "}" in /home/andrey_murzich/nginx/conf/hosts.conf:23\n2017/10/05 14:34:27 [error] 26174#0: *1 open() "/home/andrey_murzich/nginx/html/favicon.ico" failed (2: No such file or directory), client: 127.0.0.1, server: 192.168.122.73, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8080"""
            ),
        ) as mock_file:
            Base(self.options).run()
            mock_file.assert_called_with(self.file_path, "w")
            handle = mock_file()
            handle.write.assert_called_once_with(
                '2017/10/05 14:30:14 [emerg] 26048#0: unexpected end of file, expecting "}" in /home/andrey_murzich/nginx/conf/hosts.conf:23\n2017/10/05 14:34:27 [error] 26174#0: *1 open() "/home/andrey_murzich/nginx/html/favicon.ico" failed (2: No such file or directory), client: 127.0.0.1, server: 192.168.122.73, request: "GET /favicon.ico HTTP/1.1", host: "localhost:8080'
            )
