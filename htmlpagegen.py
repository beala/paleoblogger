import copy

class HTMLPageGen(object):
    single_item=True

    def __init__(self, args_dict):
        self.template_vals = copy.copy(args_dict)
        pass

    def process(self, page_list, page, cur_page_num):
        # Select a template depending on type.
        if page["type"] == "post":
            header = "body_head"
        elif page["type"] == "page":
            header = "body_head_page"
        else:
            raise Exception("Unknown page type: '%s'" % page["type"])
        body = page["cur_res"]
        with open(header) as header_file:
            header_str = header_file.read()
            # Copy dict to template vals so "date" can be modified.
            self.template_vals.update(page)
            self.template_vals["date"] = self.template_vals["date"].strftime("%B %d, %Y")
            header_str = header_str % self.template_vals
            body = header_str + body
        with open("body_footer") as footer_file:
            body += footer_file.read()
        page["cur_res"] = body
        return page
