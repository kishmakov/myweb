#!/usr/bin/env python
import markdown
import os
import re
import shutil
import textwrap
from pathlib import Path

mds_dir = "notes"
templates_dir = "app/templates/n"
index_file_name = "app/index.py"

################################################################


def is_meta_for(key, line, result):
    match = re.search(f"^<!-- {key}: (.+) -->$", line)
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

    return header, tags, " ".join(summary).replace("  ", " "), text

################################################################


def header_by_name(relative_name):
    words = [s.capitalize() for s in relative_name.split('_')]
    return ' '.join(words[1:])


def write_template(relative_name, header, raw_text):
    text = '{% extends "note.html" %}\n\n'

    text += '{% block title %}' + header + '{% endblock %}\n\n'

    text += '{% block div %}\n'
    text += markdown.markdown("# " + header + raw_text, extensions=['smarty'])
    text += '\n{% endblock %}\n'

    output_name = os.path.join(templates_dir, relative_name + ".html")

    output_file = open(output_name, "w", encoding="utf-8", errors="xmlcharrefreplace")
    output_file.write(text)


def escape(line):
    return line.replace('"', '\\"').replace("'", "\\'")


def append_index(relative_name, header, tags, summary):
    index_file = open(index_file_name, "a", encoding="utf-8")
    index_file.write("\nnotes_records.append(NoteRecord(\n")
    index_file.write(f'    "{relative_name}",\n')
    index_file.write(f'    "{header}",\n')
    index_file.write(f'    {tags},\n')
    index_file.write(f'    "{escape(summary)}"\n')
    index_file.write("))\n")


def process(file_name):
    relative_name = Path(file_name).stem

    header, tags, summary, text = parse_input(file_name)

    if len(header) == 0:
        header = header_by_name(relative_name)

    write_template(relative_name, header, text)
    append_index(relative_name, header, tags, summary)


def prepare():
    shutil.rmtree(templates_dir, ignore_errors=True)
    os.mkdir(templates_dir)

    index_begin = textwrap.dedent("""\
        from note_record import NoteRecord

        notes_records = list()
        """)

    index_file = open(index_file_name, "w", encoding="utf-8")
    index_file.write(index_begin)


if __name__ == "__main__":
    prepare()

    for file in os.listdir(mds_dir):
        if file.endswith(".md"):
            process(os.path.join(mds_dir, file))
