import datetime

class TOCGen(object):
    single_item=False

    def __init__(self, args_dict):
        self.template_vals = args_dict
        pass

    def process(self, post_list):
        post_links = ""
        for post in post_list:
            post_links += "<p>" + self._gen_link(post) + "\n"
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
            'skip': False,
            })

        return post_list

    def _gen_link(self, post):
        return '%s<br><a href="%s">%s</a>' % (
                post["date"].strftime("%m/%d/%Y"),
                post["permalink"],
                post["title"])
