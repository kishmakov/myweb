#!/usr/bin/env python
import markdown
import os
import re
import shutil
from pathlib import Path

mds_dir = "notes"
templates_dir = "app/templates/n"
index_file = "app/index.py"

################################################################


def is_meta_for(key, line, result):
    match = re.search("^<!-- {0}: (.+) -->$".format(key), line)
    if match:
        result.append(match.group(1))
        return True

    return False


def parse_input(file_name):
    header = ""
    tags = list()
    summary = list()
    text = ""

    input_file = open(file_name, "r", encoding="utf-8")

    for line in input_file:
        result = list()
        if is_meta_for("Header", line, result):
            header = result[0]
        elif is_meta_for("Summary", line, result):
            summary.append(result[0])
        elif is_meta_for("Tag", line, result):
            tags.append(result[0])
        else:
            text += line

    return header, tags, '\n'.join(summary), text

################################################################


def header_by_name(relative_name):
    words = [s.capitalize() for s in relative_name.split('_')]
    return ' '.join(words[1:])


def write_template(relative_name, header, raw_text):
    text = '{% extends "base.html" %}\n'

    text += '{% block title %}' + header + '{% endblock %}\n'

    text += '{% block container %}\n'
    text += markdown.markdown("# " + header + raw_text)
    text += '\n{% endblock %}\n'

    output_name = os.path.join(templates_dir, relative_name + ".html")

    output_file = open(output_name, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(text)


def process(file_name):
    relative_name = Path(file_name).stem

    header, tags, summary, text = parse_input(file_name)

    if len(header) == 0:
        header = header_by_name(relative_name)

    write_template(relative_name, header, text)


def clean_up():
    shutil.rmtree(templates_dir, ignore_errors=True)
    os.mkdir(templates_dir)


if __name__ == "__main__":
    clean_up()

    for file in os.listdir(mds_dir):
        if file.endswith(".md"):
            process(os.path.join(mds_dir, file))
