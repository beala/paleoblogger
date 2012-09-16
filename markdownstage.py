import markdown

class MarkdownStage(object):
    single_item=True

    def __init__(self, args_dict):
        pass

    def process(self, post_list, post, post_num):
        if post['type'] not in ['page', 'post']:
            return post
        post["html_body"] = markdown.markdown(
                post["html_body"],
                ['fenced_code', 'codehilite'])
        # That was easy :-)
        return post
