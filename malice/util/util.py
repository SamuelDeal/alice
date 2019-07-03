# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8:tabstop=4:softtabstop=4:shiftwidth=4:expandtab:textwidth=120

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

# Python core libraries
import json
import os
import signal
import contextlib
import socket
import string
import random
import datetime
import uuid
import configparser
import subprocess

# Project specific libs
from util.type_util import *


PATH_TYPE_UNIX = 1
PATH_TYPE_WINDOWS = 2


def path_join(first, *args, **kwargs):
    """
    Concatenate path for other system.
    You could provide the "os" param to specify the os.
    If you wanrt to calculate a path for the current machine, you should use os.path.join instead

    :param first:   The first path element
    :type first:    str
    :param args:    The other path parts
    :type args:     str
    :param os:      Which kind of os you want to join. Optional, default PATH_TYPE_UNIX
    :type os:       int
    :return:        A valid unix path
    :rtype:         str
    """
    os_type = PATH_TYPE_UNIX
    if "os" in kwargs:
        if kwargs['os'] not in (PATH_TYPE_UNIX, PATH_TYPE_WINDOWS):
            raise RuntimeError("unknown os type "+repr(kwargs['os']))
        os_type = kwargs['os']

    if os_type == PATH_TYPE_UNIX:
        result = first.rstrip("/")
        for arg in args:
            result += "/" + arg.strip("/")
        return result
    else:  # os_type == PATH_TYPE_WINDOWS:
        result = first.rstrip("/").rstrip("\\")
        for arg in args:
            result += "\\" + arg.strip("/").rstrip("\\")
        return result


def float_equals(val1, val2):
    """
    Check if 2 float values are equals

    :param val1:    The first value
    :type val1:     float
    :param val2:    The second value
    :type val2:     float
    :return:        True if the values can be considered as equal
    :rtype:         bool
    """
    return abs(val1 - val2) < 1e-07


def round_int(value, round_to):
    """
    Round a value by an arbitrary integer

    :param value:       The value you want to round
    :type value:        float|int
    :param round_to:    The value you want the result to be a multiple of
    :type round_to:     int
    :return:            the rounded value (ex: round_int(67, 5) => 65)
    :rtype:             int
    """
    return int((value + int(round_to)/2) // round_to * round_to)


def format_float(value, precision=4):
    str_format = "{:."+to_str(precision)+'f}'
    result = str_format.format(float(value)).rstrip('0').rstrip('.')
    if result == "" or result == "-" or result == "-0":
        return "0"
    return result


def has_flag(value, flag):
    """
    Check if a value contains specific bits

    :param value:       A numerical value (usually a status)
    :type value:        int
    :param flag:        A flag, usually one or an addition of powers of two
    :type flag:         int
    :return:            True if the value contains all bits of flag
    :rtype:             bool
    """
    return (value & flag) == flag


def has_filled_value(dictionary, key):
    """
    Check if a dictionary has a valid non empty value for given key

    :param dictionary:      The dictionary to check
    :type dictionary:       dict[str, any]
    :param key:             The key to check
    :type key:              str
    :return:                True if there is a non empty value
    :rtype:                 bool
    """
    if key not in dictionary.keys():
        return False
    if not dictionary[key]:
        return False
    if is_string(dictionary[key]) and not dictionary[key].strip():
        return False
    return True


def env_is_on(key):
    """
    Check if an environment variable is on

    :param key:     The environment variable name
    :type key:      str
    :return:        True if the environment variable is on
    :rtype:         bool
    """
    if key not in os.environ.keys():
        return False
    if not os.environ[key]:
        return False
    if is_string(os.environ[key]) and not os.environ[key].strip():
        return False
    return to_str(os.environ[key]).strip().lower() in ('yes', 'true', 't', 'y', '1', 'o', 'oui', 'on')


def env_is_off(key):
    """
    Check if an environment variable is off

    :param key:     The environment variable name
    :type key:      str
    :return:        True if the environment variable is on
    :rtype:         bool
    """
    if key not in os.environ.keys():
        return False
    if not os.environ[key]:
        return False
    if is_string(os.environ[key]) and not os.environ[key].strip():
        return False
    return to_str(os.environ[key]).strip().lower() in ('no', 'false', 'f', 'n', '0', 'non', 'off')


class TimeoutError(RuntimeError):
    pass


def _raise_timeout(*unused):
    raise TimeoutError()


@contextlib.contextmanager
def using_timeout(timeout):
    """
    This method should be used via the 'with' keyword
    This method raise a TimeoutError after timeout seconds if we didn't exit the 'with'

    :param timeout:     The timeout, in seconds
    :type timeout:      int|datetime.timedelta
    """
    if ll_float(timeout):
        timeout = int(float(timeout))
    else:
        timeout = timeout.seconds

    try:
        signal.signal(signal.SIGALRM, _raise_timeout)
        signal.alarm(timeout)
        yield
    finally:
        signal.alarm(0)


def tcp_port_status(host, port):
    """
    Ping a tcp port

    :param host:    The hostname or ip of a distant machine
    :type host:     str
    :param port:    The port to ping
    :type port:     int|str
    :return:        True if we successfully ping the server, False otherwise
    :rtype:         bool
    """
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((host, int(port)))
        s.shutdown(2)
        return True
    except Exception:
        return False


class SaltChars(object):
    chars = string.ascii_letters + string.digits


def generate_salt(length=12):
    """
    Generate a new salt string

    :param length:      The length of the salt to generate. Optional, default 12
    :type length:       int
    :return:            the generated salt
    :rtype:             str
    """
    salt = ''
    for i in range(length):
        salt += SaltChars.chars[random.randint(0, len(SaltChars.chars) - 1)]
    return salt


def write_conf(filename, data, section="Job"):
    """
    Write a dictionary as config file> For complex objects, values are saved as json dump

    :param filename:    The config file name and path
    :type filename:     str
    :param data:        The data to save
    :type data:         dict[str, str]
    :param section:     The config file main section. Optional, default "Job"
    :type section:      str
    """
    conf = configparser.RawConfigParser()

    conf.add_section(section)
    for key, value in data.items():
        if is_primitive(value):
            conf.set(section, to_str(key), to_str(value))
        else:
            conf.set(section, to_str(key), json.dumps(value))

    with open(filename, 'wb') as configfile:
        conf.write(configfile)


def load_ini_file(filename):
    conf = configparser.ConfigParser()
    conf.read(filename)
    return conf


def compute_variance(data):
    y_squared_dot = sum(i * i for i in data)
    y_dot_squared = sum(data) ** 2
    return (y_squared_dot - y_dot_squared / len(data)) / (len(data) - 1)


def json_encode(val):
    if val is None:
        return None
    return json.dumps(cast_for_json(val))


def dt_to_timestamp(dt, default=None):
    """
    Convert a datetime object to a timestamp

    :param dt:          The input datetime
    :type dt:           datetime.datetime|None
    :param default:     What to return if the input is invalid. Optional, default None
    :type default:      int|None
    :return:            The timestamp
    :rtype:             int|None
    """
    if dt is None:
        return default
    epoch = datetime.datetime.utcfromtimestamp(0)
    return(dt - epoch).total_seconds()


def cast_for_json(val):
    if val is None:
        return None
    if is_primitive(val):
        return val
    if isinstance(val, collections.Mapping):
        return {cast_for_json(key): cast_for_json(subval) for key, subval in val.items()}
    elif isinstance(val, collections.Iterable):
        return [cast_for_json(subval) for subval in val]
    elif isinstance(val, datetime.datetime):
        return dt_to_timestamp(val)
    elif isinstance(val, uuid.UUID):
        return to_str(val)
    else:
        return to_str(val)


def is_json(var):
    """
    Check if parameter is a valid json string

    :param var:     The variable to test
    :type var:      any
    :return:        True is the variable is a valid json string
    :rtype:         bool
    """
    if not is_string(var):
        return False
    try:
        _ = json.loads(var)
        return True
    except Exception:
        return False


def log_error(log, e):
    log.exception(e)
    if isinstance(e, subprocess.CalledProcessError) and e.output:
        log.error("Output:  \n"+to_str(e.output).strip())
