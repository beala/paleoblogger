import sys
import subprocess
import os
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
    with open(post_filename) as post_file:
        title = post_file.next().strip()
        author = post_file.next().strip()
        date = datetime.datetime.strptime(post_file.next().strip(), "%m-%d-%Y")
        permalink = post_file.next().strip() + ".html"
        body = ""
        while True:
            try:
                body += post_file.next()
            except StopIteration:
                break
        body = body.strip()
    return {
            'title': title,
            'author':author,
            'date':date,
            'permalink':permalink,
            'body':body,
            'cur_res': body,
            }

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
