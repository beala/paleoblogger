import codecs

class ReadTemplateStage(object):
    single_item = False

    template_dict = {
            'post': 'post_template.html',
            'page': 'page_template.html',
            'toc':  'toc_template.html',
            }

    def __init__(self, args_dict):
        pass

    def process(self, content_list):
        template_dict = self._read_templates()
        for content in content_list:
            content["html_template"] = template_dict[content["type"]]
        return content_list

    def _read_templates(self):
        for template_type in self.template_dict:
            with codecs.open(
                    self.template_dict[template_type],
                    encoding="utf-8") as template_f:
                 self.template_dict[template_type] = template_f.read()
        return self.template_dict
