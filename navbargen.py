class NavbarGen(object):
    single_item = False

    def __init__(self, args_dict):
        self.global_args_dict = args_dict

    def process(self, post_list):
        page_links_html = self._gen_page_links(post_list)
        for post in post_list:
            post["page_links"] = page_links_html
        return post_list

    def _gen_page_links(self, post_list):
        # Generate navigation header
        page_links_html = ""
        for post in post_list:
            if post["type"] == "page":
                page_links_html += '<li>'+self._gen_page_link(post)+"</li>"
        return page_links_html

    def _gen_page_link(self, post):
        return '<a href="%s">%s</a>' % (
                post["permalink"],
                post["title"])
