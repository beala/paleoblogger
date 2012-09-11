class HTMLPageGen(object):
    single_item=True

    def __init__(self, args_dict):
        pass

    def process(self, page_list, page, cur_page_num):
        body = page["cur_res"]
        with open("body_head") as header_file:
            header_str = header_file.read()
            header_str = header_str % (
                    page["title"],
                    page["title"],
                    page["author"],
                    page["date"].strftime("%B %d, %Y"))
            body = header_str + body
        with open("body_footer") as footer_file:
            body += footer_file.read()
        page["cur_res"] = body
        return page
