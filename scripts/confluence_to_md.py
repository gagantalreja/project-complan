import argparse
import os
from atlassian import Confluence
from markdownify import MarkdownConverter
from atlassian.errors import ApiError
from dotenv import load_dotenv

load_dotenv()



def parse_args():
    parser = argparse.ArgumentParser(description='Command line arguments for extracting Confluence page history into a git repository')

    parser.add_argument('-u', '--url', type=str, help="confluence url", required=True)
    parser.add_argument('-s', '--space', type=str, help="Key of the confluence space", required=True)
    parser.add_argument('-pg', '--pages', type=str, help="Title of the pages to extract separated by commas", required=True)

    return parser.parse_args()


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


def main():
    args = parse_args()

    confluence = Confluence(url=args.url, username=os.getenv("JIRA_USER"), password=os.getenv("JIRA_TOKEN"))

    basepath = f"./data/{args.space}"
    if not os.path.exists(basepath):
        os.mkdir(basepath)

    for page in args.pages.split(","):
        print("Parsing page: ", page)
        page_id = confluence.get_page_id(args.space, page)
        content = confluence.get_page_by_id(page_id, expand="body.storage,version")
        markdown = AtlassianConverter().convert(content['body']['storage']['value'])

        with open(f"{basepath}/{'_'.join(page.split())}", 'w') as f:
            f.write(markdown)


if __name__ == '__main__':
    main()
