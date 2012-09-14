class HTMLPageGen(object):
    single_item=True

    def __init__(self, args_dict):
        pass

    def process(self, page_list, page, cur_page_num):
        body = page["cur_res"]
        with open("body_head") as header_file:
            header_str = header_file.read()
            template_vals={}
            # Copy dict to template vals so "date" can be modified.
            template_vals.update(page)
            template_vals["date"] = template_vals["date"].strftime("%B %d, %Y")
            header_str = header_str % template_vals
            body = header_str + body
        with open("body_footer") as footer_file:
            body += footer_file.read()
        page["cur_res"] = body
        return page
