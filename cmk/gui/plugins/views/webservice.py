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

import json
import time

from cmk.gui.i18n import _
from cmk.gui.globals import html

from . import (
    multisite_layouts,
    join_row,
    output_csv_headers,
)


def render_python_raw(data, view, group_cells, cells, num_columns, show_checkboxes):
    html.write(repr(data))


multisite_layouts["python-raw"] = {
    "title": _("Python raw data output"),
    "render": render_python_raw,
    "group": False,
    "hide": True,
}


def render_python(rows, view, group_cells, cells, num_columns, show_checkboxes):
    html.write_text("[\n")
    html.write(repr([cell.export_title() for cell in cells]))
    html.write_text(",\n")
    for row in rows:
        html.write_text("[")
        for cell in cells:
            joined_row = join_row(row, cell)
            _tdclass, content = cell.render_content(joined_row)
            html.write(repr(html.strip_tags(content)))
            html.write_text(",")
        html.write_text("],")
    html.write_text("\n]\n")


multisite_layouts["python"] = {
    "title": _("Python data output"),
    "render": render_python,
    "group": False,
    "hide": True,
}


def render_json(rows, view, group_cells, cells, num_columns, show_checkboxes, export=False):
    if export:
        filename = '%s-%s.json' % (view['name'],
                                   time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time())))
        if isinstance(filename, unicode):
            filename = filename.encode("utf-8")
        html.response.set_http_header("Content-Disposition",
                                      "Attachment; filename=\"%s\"" % filename)

    painted_rows = []

    header_row = []
    for cell in cells:
        header_row.append(html.strip_tags(cell.export_title()))
    painted_rows.append(header_row)

    for row in rows:
        painted_row = []
        for cell in cells:
            joined_row = join_row(row, cell)
            content = cell.render_content(joined_row)[1]
            if isinstance(content, (list, dict)):
                # Allow painters to return lists and dicts, then json encode them
                # as such data structures without wrapping them into strings
                pass

            else:
                if isinstance(content, unicode):
                    content = content.encode("utf-8")
                else:
                    content = "%s" % content
                content = html.strip_tags(content.replace("<br>", "\n"))

            painted_row.append(content)

        painted_rows.append(painted_row)

    html.write(json.dumps(painted_rows, indent=True))


multisite_layouts["json_export"] = {
    "title": _("JSON data export"),
    "render": lambda a, b, c, d, e, f: render_json(a, b, c, d, e, f, True),
    "group": False,
    "hide": True,
}

multisite_layouts["json"] = {
    "title": _("JSON data output"),
    "render": lambda a, b, c, d, e, f: render_json(a, b, c, d, e, f, False),
    "group": False,
    "hide": True,
}


def render_jsonp(rows, view, group_cells, cells, num_columns, show_checkboxes):
    html.write("%s(\n" % html.var('jsonp', 'myfunction'))
    render_json(rows, view, group_cells, cells, num_columns, show_checkboxes)
    html.write_text(");\n")


multisite_layouts["jsonp"] = {
    "title": _("JSONP data output"),
    "render": render_jsonp,
    "group": False,
    "hide": True,
}


def render_csv(rows, view, group_cells, cells, num_columns, show_checkboxes, export=False):
    if export:
        output_csv_headers(view)

    def format_for_csv(raw_data):
        # raw_data can also be int, float
        content = "%s" % raw_data
        stripped = html.strip_tags(content).replace('\n', '').replace('"', '""')
        return stripped.encode("utf-8")

    csv_separator = html.var("csv_separator", ";")
    first = True
    for cell in group_cells + cells:
        if first:
            first = False
        else:
            html.write(csv_separator)
        content = cell.export_title()
        html.write('"%s"' % format_for_csv(content))

    for row in rows:
        html.write_text("\n")
        first = True
        for cell in group_cells + cells:
            if first:
                first = False
            else:
                html.write(csv_separator)
            joined_row = join_row(row, cell)
            _tdclass, content = cell.render_content(joined_row)
            html.write('"%s"' % format_for_csv(content))


multisite_layouts["csv_export"] = {
    "title": _("CSV data export"),
    "render": lambda a, b, c, d, e, f: render_csv(a, b, c, d, e, f, True),
    "group": False,
    "hide": True,
}

multisite_layouts["csv"] = {
    "title": _("CSV data output"),
    "render": lambda a, b, c, d, e, f: render_csv(a, b, c, d, e, f, False),
    "group": False,
    "hide": True,
}
