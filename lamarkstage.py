from lamark import *
class LamarkStage(object):
    single_item = True

    def __init__(self, args_dict):
        self.output_dir = args_dict["output_dir"]

    def process(self, post_list, post, post_num):
        body = post["cur_res"]
        post["cur_res"] = lamark.lamark(body, self.output_dir)
        return post
