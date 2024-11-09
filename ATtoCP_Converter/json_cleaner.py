import re
from pathlib import Path

class JsonCleaner:
    '''
    Cleans json files by: removing trailing commas, comments, and BOM chars
    
    Attributes
    path : Path (The directory path where the JSON files are located)
    '''
    def __init__(self, path):
        self.path = Path(path)

    def remove_comments_and_trailing_commas(self, content):
        """ Cleans up json file contents to avoid parsing errors when ingesting """
        content = re.sub(r'//.*', '', content)
        content = re.sub(r',\s*([\]}])', r'\1', content)
        return content

    def re_encode_clean_json(self, file_path):
        """ Opens json in utf-8-sig, cleans, and re-encodes in just utf-8 to get rid of the BOM """
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            content = file.read()
        cleaned_content = self.remove_comments_and_trailing_commas(content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

    def clean_json_files(self):
        """ Walks through the directory and it's sub-directories to find and process any json files """
        for file_path in self.path.rglob('*.json'):
            self.re_encode_clean_json(file_path)

# Test on bulk folders to break it
# json_cleaner = JsonCleaner('Test/Bulk_v07')
# json_cleaner.clean_json_files()
