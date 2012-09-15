import os
import codecs
import datetime
import fileutils

class ProcFiles(object):
    def __init__(self, args_dict):
        self.posts_dir = args_dict["posts_dir"]
        self.output_dir = args_dict["output_dir"]

    def process(self):
        """Given a directory of posts, return a dict representing those posts
           and a dict representing the blog's config.
           Return: (post_list, config_dict)
        """
        self.posts_dir = fileutils.add_slash_if_missing(self.posts_dir)
        post_list = []
        for post_filename in os.listdir(self.posts_dir):
            # Process config file
            if post_filename == "_config":
                config_dict = self._get_config_info(self.posts_dir+post_filename)
                continue
            # Process LaMark files
            if not post_filename.endswith(".lm"):
                continue
            post_info = self._get_post_info(self.posts_dir + post_filename)
            post_list.append(post_info)
        post_list.sort(key=lambda post_info: post_info['date'], reverse=True)
        return (post_list, config_dict)

    def _get_post_info(self,post_filename):
        """Given the filename of a post, populate a dict representing that post.
        """
        post_info = {
                "title": None,      # Post title
                "author": None,     # Post author
                "date": None,       # Date of post
                "type": None,       # Type: page, post, rss, toc
                "permalink": None,  # Permanent title of the post "my-post.html"
                "desc": None,       # Post description
                "body": None,       # Body of the post in LaMark
                "cur_res": None     # Output of each stage stored here
                }
        # Use utf-8, otherwise the markdown module chokes on it.
        with codecs.open(post_filename, encoding='utf-8') as post_file:
            whitespace_count=0
            while True:
                line = post_file.next().strip()
                if line == "":
                    break
                # Front matter can be surrounded by html comment tags if
                # needed.
                if line == "<!--" or line == "-->":
                    continue
                colon_pos = line.find(":")
                if colon_pos == -1:
                    raise Exception("Invalid front matter line: '%s'" % line)
                arg_name = line[:colon_pos]
                if arg_name not in post_info.keys():
                    raise Exception("Unrecognized front matter argument: '%s'" %
                            arg_name)
                post_info[arg_name] = line[colon_pos+1:].strip()
            # Body of post is the rest of the file.
            body = ""
            while True:
                try:
                    body += post_file.next()
                except StopIteration:
                    break
            post_info["body"] = body.strip()
            post_info["cur_res"] = body.strip()
            # Convert date string to datetime obj.
            post_info["date"] = datetime.datetime.strptime(
                    post_info["date"],
                    "%m-%d-%Y")
            # Post must end in .html
            post_info["permalink"] += ".html"
            # Check if the file needs to be regenerated. If the output dir has
            # a file that's the same name as 'permalink', and that file is
            # more recently modified than the '.lm' file, then set regen to
            # False. Else True.
            post_stat = os.stat(post_filename)
            try:
                output_stat = os.stat(self.output_dir + post_info["permalink"])
                if post_stat.st_mtime > output_stat.st_mtime:
                    post_info["regen"] = True
                else:
                    post_info["regen"] = False
            except OSError:
                # File could not be 'stat'd, so file probably doesn't exist yet,
                # meaning it needs to be generated.
                post_info["regen"] = True
            self._validate_post(post_info)
        return post_info

    def _validate_post(self, post):
        optionals = ["desc"]
        for key in post:
            if key in optionals:
                continue
            if post[key] is None:
                raise Exception("Post '%s' is missing front matter '%s'" %
                        (post['title'], key))

    def _get_config_info(self,config_filename):
        config_info={
                'home_url': None,
                'blog_base_url': None,
                'title': None,
                'desc': None,
                }
        with codecs.open(config_filename, encoding='utf-8') as config_file:
            for line in config_file:
                line = line.strip()
                # Skip empty lines or comments (lines beginning with #)
                if len(line) == 0 or line[0] == "#":
                    continue
                # Colon separates argument name from argument value.
                colon_pos = line.find(":")
                if colon_pos == -1:
                    continue
                arg_name = line[:colon_pos].strip()
                arg_val = line[colon_pos+1:].strip()
                config_info[arg_name] = arg_val
        required_args = [
                "home_url",
                "blog_base_url",
                "title",
                "desc",
                ]
        for arg_name in required_args:
            if config_info.get(arg_name, None) is None:
                raise Exception("Config file missing argument: '%s'" % arg_name)
        return config_info
