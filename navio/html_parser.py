import html
from pathlib import Path

from bs4 import BeautifulSoup, Tag


class HtmlParser:

    def parse(self, input_html: Path) -> list:
        with open(input_html, encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')
        circle_blocks = soup.find_all('div', class_='circle_cut_img_area')
        table_rows = []

        for circle_block in circle_blocks:
            parent = circle_block.parent

            cut_img_tag = circle_block.find('img', class_='CircleCut')
            if cut_img_tag:
                img_link = html.escape(cut_img_tag['src'])
                cut_img = f'<img src="{img_link}" loading="lazy" alt="cut"/>'
            else:
                cut_img = ''

            space_tag = parent.find('span', class_='CircleSpace')
            space = space_tag.get_text(strip=True) if space_tag else ''

            genre_tag = parent.find('span', class_='ArtifactTitle')
            genre = genre_tag.get_text(strip=True) if genre_tag else ''

            tendency_tag = parent.find('span', class_='ArtifactTendency')
            tendency = tendency_tag.get_text(strip=True) if tendency_tag else ''

            circle_name_tag = parent.find('div', class_='CircleName')
            circle_name = circle_name_tag.get_text(strip=True) if circle_name_tag else ''

            pen_name_tag = parent.find('span', class_='CirclePenname')
            pen_name = pen_name_tag.get_text(strip=True) if pen_name_tag else ''

            tags = self._get_tags(parent, [
                ('CircleR18', '🔞'),
                ('CircleIsManga', '🏷️マンガ'),
                ('CircleIsNovel', '🏷️小説'),
            ])

            row = [cut_img, space, genre, tendency, circle_name, pen_name, tags]
            table_rows.append(row)

        return table_rows

    def _get_tags(self, parent_tag: Tag, tuples: list) -> str:
        tag_list = []
        for class_name, tag_name in tuples:
            tag = parent_tag.find('div', class_=class_name)
            if tag and tag.get_text(strip=True) == '1':
                tag_list.append(tag_name)
        return ' | '.join(tag_list)
