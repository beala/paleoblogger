import datetime

import PyRSS2Gen as rssgen
from lamark import lamark

import fileutils
import markdown

class RSSGenStage(object):
    single_item = False

    def __init__(self, args_dict):
        self.blog_title = args_dict["title"]
        self.blog_url = args_dict["blog_base_url"]
        self.desc = args_dict["desc"]
        self.output_dir = args_dict["output_dir"]

    def process(self, post_list):
        post_rss = []
        for post in post_list:
            if post["type"] in ["post"]:
                post_rss.append(self._make_rss_item(post))
        rss = rssgen.RSS2(
                title=self.blog_title,
                link=self.blog_url,
                description=self.desc,
                lastBuildDate=datetime.datetime.now(),
                items=post_rss)
        post_list.append(
                {
                    "permalink": "rss.xml",
                    "body": rss.to_xml(),
                    "cur_res": rss.to_xml(),
                    "regen": True,
                })
        return post_list

    def _make_rss_item(self, post):
        desc = self._process_desc(post)
        link = fileutils.add_slash_if_missing(self.blog_url) + post["permalink"]
        return rssgen.RSSItem(
                title=post["title"],
                pubDate=post["date"],
                description=desc,
                guid=link,
                link=link)

    def _process_desc(self, post):
        if post["desc"] is None:
            desc_tmp = post["body"]
        else:
            desc_tmp = post["desc"]
        desc_tmp = lamark(desc_tmp,
                self.output_dir,
                post["permalink"],
                1500,
                self.blog_url,
                False
                )
        desc_tmp = markdown.markdown(
                desc_tmp,
                ['fenced_code', ' codehilite'])
        return desc_tmp

