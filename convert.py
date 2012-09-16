import re
import os
import sys
import datetime
import codecs

post_list = []
for post_filename in os.listdir(sys.argv[1]):
    print post_filename
    if not post_filename.endswith(".markdown"):
        continue
    post_dict = {}
    dash_count = 0
    with codecs.open(sys.argv[1] + post_filename, encoding="utf-8") as post_file:
        while dash_count < 2:
            line = post_file.next().strip()
            if line == "---":
                dash_count += 1
                continue
            if line[0] == "-":
                continue
            colon_pos = line.find(":")
            arg_name = line[:colon_pos].strip()
            arg_val = line[colon_pos+1:].strip()
            post_dict[arg_name] = arg_val
        body = ""
        while True:
            try:
                body += post_file.next()
            except StopIteration:
                break
        post_dict["body"] = body
        post_dict["filename"] = post_filename
        post_list.append(post_dict)

for post in post_list:
    period_pos = post["filename"].rfind(".")
    new_post_filename = post["filename"][:period_pos] + ".lm"
    post["date"] = datetime.datetime.strptime(post["date"], "%Y-%m-%d %H:%M")
    post["title"] = post["title"].strip('"')
    post["permalink"] = re.sub(r'[^\w]', '-', post["title"])
    with codecs.open(sys.argv[2] + new_post_filename, encoding="utf-8", mode="w") as new_post:
        new_post.write("title: %s\n" % post["title"].strip('"'))
        new_post.write("author: Alex Beal\n")
        new_post.write("date: %s\n" % post["date"].strftime("%m-%d-%Y"))
        new_post.write("type: post\n")
        new_post.write("desc: \n")
        new_post.write("permalink: %s\n" % post["permalink"])
        new_post.write("\n")
        new_post.write(post["body"])
