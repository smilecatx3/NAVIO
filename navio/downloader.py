from pathlib import Path

import requests

from navio import env


class Downloader:

    def __init__(self):
        event_name = str(env.config['event_name'])
        self.base_url = f'https://www.b2-web-pamphlet.jp/{event_name}/circle/search'

        self.session = requests.Session()
        self.session.cookies.set(env.config['cookies']['name'], env.config['cookies']['value'])

    def download(self, page: int) -> Path:
        response = self.session.get(
            url=f'{self.base_url}?page={page}',
            timeout=30,
        )
        if not response.ok:
            raise RuntimeError(response.status_code)

        html_file = env.working_dir/f'page{page:03}.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(response.content.decode(encoding='utf-8'))
        return html_file
