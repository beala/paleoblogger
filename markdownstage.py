import markdown

class MarkdownStage(object):
    single_item=True

    def __init__(self, args_dict):
        pass

    def process(self, post_list, post, post_num):
        post["cur_res"] = markdown.markdown(
                post["cur_res"],
                ['fenced_code', 'codehilite'])
        # That was easy :-)
        return post
