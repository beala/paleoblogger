from lamark import lamark
import markdown

class LamarkStage(object):
    single_item = True

    def __init__(self, args_dict):
        self.output_dir = args_dict["output_dir"]

    def process(self, post_list, post, post_num):
        if post['type'] not in ['page', 'post']:
            return post
        body = post["html_body"]
        post["html_body"] = lamark(body, self.output_dir, post["permalink"], 1500)
        return post
