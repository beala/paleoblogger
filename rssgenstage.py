import PyRSS2Gen as rssgen
import datetime
import fileutils

class RSSGenStage(object):
    single_item = False

    def __init__(self, args_dict):
        self.blog_title = args_dict["title"]
        self.blog_url = args_dict["blog_base_url"]
        self.desc = args_dict["desc"]

    def process(self, post_list):
        post_rss = []
        for post in post_list:
            if post["type"] == "post":
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
                    "date": datetime.datetime.now(),
                    "body": rss.to_xml(),
                    "cur_res": rss.to_xml(),
                    "skip": False,
                })
        return post_list

    def _make_rss_item(self, post):
        link = fileutils.add_slash_if_missing(self.blog_url) + post["permalink"]
        return rssgen.RSSItem(
                title=post["title"],
                pubDate=post["date"],
                description=post["desc"],
                guid=link,
                link=link
        )
