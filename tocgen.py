import datetime
import copy

class TOCGen(object):
    single_item=False

    def __init__(self, args_dict):
        self.template_vals = copy.copy(args_dict)

    def process(self, post_list):
        for post in post_list:
            if post['type'] == 'toc':
                toc = post
                break
        toc['toclinks'] = self._gen_post_links(post_list)
        return post_list

    def _gen_post_links(self,post_list):
        post_links_html = ""
        # Generate a link in the TOC for each post.
        for post in post_list:
            if post["type"] != "post":
                continue
            post_links_html += "<p>" + self._gen_post_link(post) + "\n"
        return post_links_html

    def _gen_post_link(self, post):
        return '%s<br><a href="%s">%s</a>' % (
                post["date"].strftime("%m/%d/%Y"),
                post["permalink"],
                post["title"])

