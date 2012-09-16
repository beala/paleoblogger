import copy

class HTMLPageGen(object):
    single_item=True

    def __init__(self, args_dict):
        self.template_vals = copy.copy(args_dict)
        pass

    def process(self, page_list, page, cur_page_num):
        cur_template_vals = {}
        cur_template_vals.update(self.template_vals)
        cur_template_vals.update(page)
        if "date" in cur_template_vals:
            cur_template_vals["date"] = cur_template_vals["date"].strftime("%B %d, %Y")
        # Select a template depending on type.
        page["html_template"] %= cur_template_vals
        return page
