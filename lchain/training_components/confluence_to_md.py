import argparse
import os
from atlassian import Confluence
from markdownify import MarkdownConverter


class MarkDownExe:

    def __init__(self, conf):
        self.conf = conf
        self.url = self.conf.user_conf["input_options"]["url"]
        self.space = self.conf.user_conf["input_options"]["space"]
        self.pages = self.conf.user_conf["input_options"]["pages"]
        self.url = self.conf.user_conf["input_options"]["url"]

    def get_dataset(self):
        confluence = Confluence(url=self.url, username=self.conf.jira_user, password=self.conf.jira_token)
        basepath = f"{os.getcwd()}/resources/markdown/{self.space}"
        if not os.path.exists(basepath):
            os.makedirs(basepath)

        total_tokens = 0
        output_paths = []

        for page in self.pages:

            try:
                print("Parsing page: ", page)
                page_id = confluence.get_page_id(self.space, page)
                content = confluence.get_page_by_id(page_id, expand="body.storage,version")
                markdown = AtlassianConverter().convert(content['body']['storage']['value'])
                total_tokens += len(markdown)
                file_path = f"{basepath}/{'_'.join(page.split())}"
                output_paths.append(file_path)
                with open(file_path, 'w') as f:
                    f.write(markdown)
            except Exception as e:
                print(e)

        print("Processing complete. Total count of words is:", total_tokens)
        return output_paths


class AtlassianConverter(MarkdownConverter):
    def __init__(self, **options):
        super().__init__(**options)
        setattr(self, 'convert_ac:structured-macro',self.convert_ac_structured_macro)
        setattr(self, 'convert_ac:parameter', self.convert_ac_parameter)
        setattr(self, 'convert_ac:plain-text-body',self.convert_ac_plain_text_body)

    def convert_ac_structured_macro(self, el, text, convert_as_inline):
        return text

    def convert_ac_parameter(self, el, text, convert_as_inline):
        if el.attrs['ac:name'] == 'title':
            return self.convert_h4(el, text, convert_as_inline)
        return ''

    def convert_ac_plain_text_body(self, el, text, convert_as_inline):
        if el.parent.attrs['ac:name'] == 'code':
            return self.convert_p(el, self.convert_code(el, text, convert_as_inline), convert_as_inline)
        else:
            return self.convert_p(el, text, convert_as_inline)
