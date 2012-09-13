import sys
import subprocess
import os
import codecs
import datetime

import lamarkstage
import markdownstage
import htmlpagegen
import tocgen
import writerstage

args_dict = {
    "posts_dir": sys.argv[1],
    "output_dir": sys.argv[2],
    }

stages = [
            lamarkstage.LamarkStage(args_dict),
            markdownstage.MarkdownStage(args_dict),
            htmlpagegen.HTMLPageGen(args_dict),
            tocgen.TocGen(args_dict),
            writerstage.WriterStage(args_dict)
        ]

def get_post_info(post_filename):
    post_info = {}
    with codecs.open(post_filename, encoding='utf-8') as post_file:
        whitespace_count=0
        while True:
            line = post_file.next().strip()
            if line == "":
                break
            colon_pos = line.find(":")
            if colon_pos == -1:
                raise Exception("Invalid header line: " + line)
            arg_name = line[:colon_pos]
            if arg_name not in ["title", "author", "date", "permalink"]:
                raise Exception("Unrecognized header argument: " + arg_name)
            post_info[arg_name] = line[colon_pos+1:].strip()
        post_info["date"] = datetime.datetime.strptime(post_info["date"], "%m-%d-%Y")
        post_info["permalink"] += ".html"
        body = ""
        while True:
            try:
                body += post_file.next()
            except StopIteration:
                break
        post_info["body"] = body.strip()
        post_info["cur_res"] = body.strip()
    return post_info

# TODO: Process post file path so that a "/" is appended if needed.

post_list = []
for post_filename in os.listdir(args_dict["posts_dir"]):
    if not post_filename.endswith(".lm"):
        continue
    post_info = get_post_info(args_dict["posts_dir"]+"/" + post_filename)
    post_list.append(post_info)
post_list.sort(key=lambda post_info: post_info['date'], reverse=True)

for stage in stages:
    if not stage.single_item:
        post_list = stage.process(post_list)
    else:
        for post_num in xrange(len(post_list)):
            post_list[post_num] = stage.process(
                    post_list,
                    post_list[post_num],
                    post_num)
