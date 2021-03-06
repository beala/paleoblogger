import sys
import subprocess
import os
import codecs
import datetime

import procfiles
import readtemplatestage
import lamarkstage
import markdownstage
import navbargen
import htmlpagegen
import tocgen
import rssgenstage
import writerstage

import fileutils

args_dict = {
    "posts_dir": fileutils.add_slash_if_missing(sys.argv[1]),
    "output_dir": fileutils.add_slash_if_missing(sys.argv[2]),
    }

stages = [
            readtemplatestage.ReadTemplateStage,
            lamarkstage.LamarkStage,
            markdownstage.MarkdownStage,
            navbargen.NavbarGen,
            tocgen.TOCGen,
            htmlpagegen.HTMLPageGen,
            rssgenstage.RSSGenStage,
            writerstage.WriterStage
        ]

proc_posts = procfiles.ProcFiles(args_dict)
post_list, config_dict = proc_posts.process()
args_dict.update(config_dict)

for stage in stages:
    stage_obj = stage(args_dict)
    if not stage.single_item:
        post_list = stage_obj.process(post_list)
    else:
        for post_num in xrange(len(post_list)):
            if post_list[post_num]["regen"] == False:
                continue
            post_list[post_num] = stage_obj.process(
                    post_list,
                    post_list[post_num],
                    post_num)
