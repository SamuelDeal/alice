#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8:tabstop=4:softtabstop=4:shiftwidth=4:expandtab:textwidth=120
# PYTHON_ARGCOMPLETE_OK

"""
    Copyright 2019 Samuel Déal

    This file is part of Malice.

    Malice is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Core libs
import sys
import os
import argparse
import argcomplete
# import configparser
#

# Project specific libs
import malice.core.dev
import malice.core.self


def run():
    usage_str = """
    
    """
    try:
        # common_parser = argparse.ArgumentParser(prog="malice", add_help=False)
        parser = argparse.ArgumentParser(prog="malice",
                                         description='Manipulate docker for this project',
                                         #usage=usage_str,
                                         # parents=[common_parser]
                                         )
        parser.add_argument("--config", "-c", metavar='FILE', help="Configuration file location")

        subparsers = parser.add_subparsers(help='sub-command help', dest="command")
        parser_dev = subparsers.add_parser("dev")
        dev_subparsers = parser_dev.add_subparsers(help='sub-command help', dest="sub_command")
        dev_subparsers.add_parser("start")
        dev_subparsers.add_parser("restart")
        dev_subparsers.add_parser("stop")
        dev_subparsers.add_parser("kill")
        dev_subparsers.add_parser("clean")

        parser_self = subparsers.add_parser("self")
        self_subparsers = parser_self.add_subparsers(help='sub-command help', dest="sub_command")
        self_subparsers.add_parser("check")

        argcomplete.autocomplete(parser)
        args = parser.parse_args()
        if args.command is None:
            parser.error("No command provided")
        command = args.command
        if args.sub_command:
            command += ":" + args.sub_command

        if command == "dev":
            parser.error("Missing check sub command")
        elif command == "dev:start":
            malice.core.dev.start()
        elif command == "dev:restart":
            malice.core.dev.restart()
        elif command == "dev:stop":
            malice.core.dev.stop()
        elif command == "dev:kill":
            malice.core.dev.kill()
        elif command == "dev:clean":
            malice.core.dev.clean()
        elif command == "self":
            parser.error("Missing check sub command")
        elif command == "self:check":
            malice.core.self.check()
        else:
            parser.error("Missing check sub command")
    except KeyboardInterrupt:
        sys.stderr.write(os.linesep+"Aborted"+os.linesep)
        sys.stderr.flush()
        return 0
    except SystemExit as e:
        return e.code
    except Exception as e:
        sys.stderr.write(os.linesep + str(e) + os.linesep)
        sys.stderr.flush()
        return 1


def main():
    sys.exit(run())


if __name__ == '__main__':
    main()
