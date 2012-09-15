import datetime
import copy

class TOCGen(object):
    single_item=False

    def __init__(self, args_dict):
        self.template_vals = copy.copy(args_dict)

    def process(self, post_list):
        post_links = self._gen_post_links(post_list)
        #self.template_vals["page_links"] = self._gen_page_links(post_list)
        # Combine links with header and footer to make page.
        with open("body_head_toc") as header_file:
            header_str = header_file.read()
            header_str = header_str % self.template_vals
            body = header_str + post_links
        with open("body_footer") as footer_file:
            body += footer_file.read()
        post_list.append({
            'type': 'toc',
            'permalink': "index.html",
            'body': post_links,
            'cur_res': body,
            'regen': True,
            })

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

