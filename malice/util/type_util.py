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
import collections


def ll_float(var):
    """
    Check parameter can be cast as a valid float

    :param var:     The variable to check
    :type var:      any
    :return:        True if the value can be cast to float
    :rtype:         bool
    """
    try:
        float(var)
        return True
    except (ValueError, TypeError):
        return False


def ll_int(var):
    """
    Check parameter looks like a valid int

    :param var:     The variable to check
    :type var:      any
    :return:        True if the value can be cast to float
    :rtype:         bool
    """
    try:
        int(var)
        return True
    except (ValueError, TypeError):
        return False


def is_string(var):
    """
    Check if parameter is a string

    :param var:     The variable to test
    :type var:      any
    :return:        True is the variable is a string or unicode
    :rtype:         bool
    """
    return isinstance(var, str)


def is_int(var):
    """
    Check if parameter is an int

    :param var:     The variable to test
    :type var:      any
    :return:        True is the variable is a int
    :rtype:         bool
    """
    return isinstance(var, int)


def is_primitive(var):
    """
    Check if variable is primitive type, such as string or int

    :param var:     The variable to test
    :type var:      any
    :return:        True if given variable is primitive
    :rtype:         bool
    """
    return is_string(var) or is_int(var) or isinstance(var, (bool, float, bytes))


def is_array(var):
    if is_primitive(var):
        return False
    if isinstance(var, dict):
        return False
    return isinstance(var, collections.Iterable)


def is_dict(var):
    if is_primitive(var):
        return False
    return isinstance(var, dict)


def ll_bool(value):
    """
    Check if value looks like a bool

    :param value:       The value to check
    :type value:        any
    :return:            The boolean value
    :rtype:             bool
    """
    if value is None:
        return False
    if isinstance(value, bool):
        return True
    if ll_float(value):
        return int(float(value)) in (0, 1)
    try:
        value = to_str(value)
    except Exception:
        return False
    if value.lower() in ('yes', 'true', 't', 'y', '1', 'o', 'oui', 'on'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0', 'non', 'off'):
        return True
    else:
        return False


def to_bool(value):
    """
    Convert a string to bool
    Raise error if not a valid bool

    :param value:       The value to cast
    :type value:        any
    :return:            The boolean value
    :rtype:             bool
    """
    if value is None:
        raise TypeError("Not a boolean")
    if isinstance(value, bool):
        return value
    if ll_float(value):
        if not int(float(value)) in (0, 1):
            raise TypeError("Not a boolean")
        return int(float(value)) == 1
    try:
        value = to_str(value)
    except Exception:
        raise TypeError("Not a boolean")
    if value.lower() in ('yes', 'true', 't', 'y', '1', 'o', 'oui', 'on'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0', 'non', 'off'):
        return False
    else:
        raise TypeError("Not a boolean")


def to_bytes(var):
    """
    Convert a var to a byte string

    :param var:     The variable to convert
    :type var:      any
    :return:        The var converted to byte string
    :rtype:         bytes
    """
    if isinstance(var, bytes):
        return var
    elif isinstance(var, str):
        return var.encode("UTF-8")
    else:
        return str(var).encode("UTF-8")


def to_unicode(var):
    """
    Convert a var to a unicode string

    :param var:     The variable to convert
    :type var:      any
    :return:        The var converted to string
    :rtype:         str
    """
    if isinstance(var, str):
        return var
    elif isinstance(var, bytes):
        return var.decode("UTF-8")
    else:
        return str(var)


def to_str(var):
    """
    Convert a var to a string

    :param var:     The variable to convert
    :type var:      any
    :return:        The var converted to string
    :rtype:         str
    """
    return to_unicode(var)
