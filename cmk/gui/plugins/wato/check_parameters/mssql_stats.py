#!/usr/bin/python
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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Float,
    TextAscii,
    Tuple,
)
from cmk.gui.plugins.wato import (
    RulespecGroupCheckParametersApplications,
    register_check_parameters,
)

register_check_parameters(
    RulespecGroupCheckParametersApplications,
    "mssql_stats",
    _("MSSQL Statistics"),
    Dictionary(
        elements=[
            ("batch_requests/sec",
             Tuple(
                 title=_("Batch Requests/sec"),
                 elements=[
                     Float(title=_("warning at"), unit=_("/sec"), default_value=100000.0),
                     Float(title=_("critical at"), unit=_("/sec"), default_value=200000.0),
                 ])),
            ("sql_compilations/sec",
             Tuple(
                 title=_("SQL Compilations/sec"),
                 elements=[
                     Float(title=_("warning at"), unit=_("/sec"), default_value=10000.0),
                     Float(title=_("critical at"), unit=_("/sec"), default_value=20000.0),
                 ])),
            ("sql_re-compilations/sec",
             Tuple(
                 title=_("SQL Re-Compilations/sec"),
                 elements=[
                     Float(title=_("warning at"), unit=_("/sec"), default_value=10000.0),
                     Float(title=_("critical at"), unit=_("/sec"), default_value=200.0),
                 ])),
            ("locks_per_batch",
             Tuple(
                 title=_("Locks/Batch"),
                 elements=[
                     Float(title=_("warning at"), default_value=1000.0),
                     Float(title=_("critical at"), default_value=3000.0),
                 ])),
        ],),
    TextAscii(title=_("Counter ID"),),
    "dict",
)