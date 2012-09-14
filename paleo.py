import sys
import subprocess
import os
import codecs
import datetime

import procfiles
import lamarkstage
import markdownstage
import htmlpagegen
import tocgen
import rssgenstage
import writerstage

args_dict = {
    "posts_dir": sys.argv[1],
    "output_dir": sys.argv[2],
    }

stages = [
            lamarkstage.LamarkStage,
            markdownstage.MarkdownStage,
            htmlpagegen.HTMLPageGen,
            tocgen.TOCGen,
            rssgenstage.RSSGenStage,
            writerstage.WriterStage
        ]

proc_posts = procfiles.ProcFiles()
post_list, config_dict = proc_posts.process(args_dict["posts_dir"])
args_dict.update(config_dict)

for stage in stages:
    stage_obj = stage(args_dict)
    if not stage.single_item:
        post_list = stage_obj.process(post_list)
    else:
        for post_num in xrange(len(post_list)):
            post_list[post_num] = stage_obj.process(
                    post_list,
                    post_list[post_num],
                    post_num)
