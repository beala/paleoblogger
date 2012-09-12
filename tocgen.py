import datetime

class TocGen(object):
    single_item=False

    def __init__(self, args_dict):
        pass

    def process(self, post_list):
        post_links = ""
        for post in post_list:
            post_links += "<p>" + self._gen_link(post) + "\n"
        with open("body_head_toc") as header_file:
            header_str = header_file.read()
            header_str = header_str
            body = header_str + post_links
        with open("body_footer") as footer_file:
            body += footer_file.read()
        post_list.append({
            'title':"/usr/sbin/blog",
            'author':"Alex Beal",
            'date': datetime.datetime.now(),
            'permalink': "index.html",
            'body': post_links,
            'cur_res': body
            })

        return post_list

    def _gen_link(self, post):
        return '%s<br><a href="%s">%s</a>' % (
                post["date"].strftime("%m/%d/%Y"),
                post["permalink"],
                post["title"])
