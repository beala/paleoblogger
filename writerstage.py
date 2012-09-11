import re

class WriterStage(object):
    single_item=True

    def __init__(self, args_dict):
        self.output_dir = args_dict["output_dir"]
        pass

    def process(self, post_list, post, post_num):
        with open(self._make_file_name(self.output_dir, post), 'w') as post_file:
            post_file.write(post["cur_res"])
        return post

    def _make_file_name(self, output_dir, post):
        if output_dir[-1] != "/":
            output_dir += "/"
        post_file_name = re.sub(r"[\s]", "-", post["permalink"])
        return output_dir + post_file_name
