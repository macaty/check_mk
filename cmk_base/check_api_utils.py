#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2014             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# NOTE: This module is for dependency-breaking purposes only, and its contents
# should probably moved somewhere else when there are no import cycles anymore.
# But at the current state of affairs we have no choice, otherwise an
# incremental cleanup is impossible.

import cmk_base.console as console


# Symbolic representations of states in plugin output
state_markers = ["", "(!)", "(!!)", "(?)"]


# The function no_discovery_possible is as stub function used for
# those checks that do not support inventory. It must be known before
# we read in all the checks
def no_discovery_possible(check_plugin_name, info):
    """In old checks we used this to declare that a check did not support
    a service discovery. Please don't use this for new checks. Simply
    skip the "inventory_function" argument of the check_info declaration."""
    console.verbose("%s does not support discovery. Skipping it.\n", check_plugin_name)
    return []


# Management board checks
MGMT_PRECEDENCE = "mgmt_precedence" # Use management board address/credentials when it's a SNMP host
MGMT_ONLY       = "mgmt_only"       # Use host address/credentials when it's a SNMP HOST
HOST_PRECEDENCE = "host_precedence" # Check is only executed for mgmt board (e.g. Managegment Uptime)
HOST_ONLY       = "host_only"       # Check is only executed for real SNMP host (e.g. interfaces)


# Is set before check/discovery function execution
_hostname = "unknown" # Host currently being checked


def set_hostname(hostname):
    global _hostname
    _hostname = hostname


def host_name():
    """Returns the name of the host currently being checked or discovered."""
    return _hostname


# Is set before check execution
_check_type = None
_service_description = None


def set_service(check_type, service_description):
    global _check_type, _service_description
    _check_type = check_type
    _service_description = service_description


def check_type():
    """Returns the name of the check type currently being checked."""
    return _check_type


# TODO: Is this really needed? Could not find a call site.
def service_description():
    """Returns the name of the service currently being checked."""
    return _service_description