"""
MIT License

Copyright (c) 2024 John Riggles [sudo_whoami]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import requests
import rumps
from bs4 import BeautifulSoup


class LTOTD(rumps.App):
    SIX_HOURS = 21_600  # seconds

    def __init__(self) -> None:
        """
        Show the Lospec Tag of the Day in the menu bar (set as app's title)
        """
        super().__init__('LTOTD', menu=['Lospec Tag of the Day', 'Refresh'])
        self.refresh_timer = rumps.Timer(
            self.refresh,
            self.SIX_HOURS,
        ).start()

    @rumps.clicked('Refresh')
    def refresh(self, _sender=None) -> None:
        """Manually refresh on menu item click"""
        asyncio.run(self._refresh_handler())

    async def _refresh_handler(self) -> None:
        self.title = 'Refreshing...'
        self.title = await asyncio.create_task(self.get_tag())

    @staticmethod
    async def get_tag() -> str:
        URL = 'https://lospec.com/dailies/'
        response = requests.get(URL)

        if (status := response.status_code) == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # find the <div> with class='daily tag' and get its text
            if tag_div := soup.find('div', class_='daily tag'):
                return tag_div.text.strip()
            else:
                return 'Not Today!'
        else:
            return f'ERROR: {status}'


if __name__ == '__main__':
    app = LTOTD()
    app.run()
