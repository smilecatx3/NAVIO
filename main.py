import time
import traceback
from pathlib import Path

from navio import env
from navio.downloader import Downloader
from navio.html_parser import HtmlParser
from navio.logger import logger


def download_all_pages() -> list[Path]:
    downloader = Downloader()
    start_page, end_page = env.config['pages']['start'], env.config['pages']['end']
    html_files = []

    for page in range(start_page, end_page+1):
        try:
            logger.info(f'Fetching page {page}...')
            html_file = downloader.download(page)
            html_files.append(html_file)
        except Exception:
            logger.error(f'Failed to download page {page}.')
            logger.error(traceback.format_exc())

        if page != end_page:
            time.sleep(1)

    return html_files


def parse_all_pages(html_files: list[Path]) -> list:
    parser = HtmlParser()
    combined_table_rows = []

    for html_file in html_files:
        try:
            table_rows = parser.parse(html_file)
            if table_rows:
                combined_table_rows += table_rows
            else:
                logger.warning(f'No circles found in "{html_file}".')

        except Exception:
            logger.error(f'Failed to parse "{html_file}".')
            logger.error(traceback.format_exc())

    return combined_table_rows


def generate_html_page(table_rows: list) -> Path:
    output_html = '''
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>サークル一覧</title>
  <link rel="stylesheet" type="text/css" href="styles.css">
</head>
<body>
<table>
  <tr>
    <th>CUT</th>
    <th>配置</th>
    <th>ジャンル</th>
    <th>傾向</th>
    <th>サークル名</th>
    <th>ペンネーム</th>
    <th>TAGS</th>
  </tr>
'''

    for row in table_rows:
        output_html += '  <tr>\n'
        for column in row:
            output_html += f'    <td>{column}</td>\n'
        output_html += '  </tr>\n'

    output_html += '''
</table>
</body>
</html>
'''

    html_file = env.current_dir/'html'/'index.html'
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(output_html)

    return html_file


def main():
    logger.info(f'Working directory: {env.working_dir}')

    html_files = download_all_pages()
    table_rows = parse_all_pages(html_files)
    output_html_file = generate_html_page(table_rows)

    logger.info(f'Generated HTML file in "{output_html_file}".')


if __name__ == '__main__':
    main()
