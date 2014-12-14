#!/usr/bin/python

import markdown
import re
import sys

def convert(text):
    html_head = '{% extends "base.html" %}\n\n'
    html_head += '{% block container %}\n'
    html_body = markdown.markdown(text)
    html_tail = '\n{% endblock %}\n'

    return html_head + html_body + html_tail

def convert_and_parse(input_name, output_name):
    tags_num = 0
    header_num = 1
    summary_num = 2
    body_num  = 3

    lines = ['', '', '', '']

    current_num = -1
    separator = re.compile('^===+ [A-Za-z]+ ===+$')

    input = open(input_name, 'r')

    for line in input:
        mode = ''
        if separator.match(line):
            mode = line[:-1].strip('= ').lower()

        if mode == 'tags':
            current_num = tags_num
        elif mode == 'header':
            current_num = header_num
        elif mode == 'summary':
            current_num = summary_num
        elif mode == 'body':
            current_num = body_num
        elif current_num >= 0:
            lines[current_num] += line

    output = open(output_name, 'w')
    output.write(convert(lines[body_num]))

    tags = filter(bool, lines[tags_num].translate(None, '\n').split(';'))
    header = lines[header_num][0:lines[header_num].find('\n')]

    return tags, header, lines[summary_num]

if len(sys.argv) < 3:
    raise Exception('convert.py expects 2 arguments, {0} provided'.format(len(sys.argv) - 1))

tags, header, summary = convert_and_parse(sys.argv[1], sys.argv[2])
