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
import datetime as dt
import requests
import rumps
from bs4 import BeautifulSoup


class LTOTD(rumps.App):
    def __init__(self) -> None:
        """
        Show the Lospec Tag of the Day in the menu bar (set as app's title)
        """
        super().__init__('LTOTD', menu=['Lospec Tag of the Day', 'Refresh'])
        self.refresh_timer = rumps.Timer(
            self.refresh,
            3600  # refresh every hour (3600 seconds)
        ).start()
        self.latest_tag: str | None = None

    @rumps.clicked('Refresh')
    def refresh(self, _sender=None) -> None:
        """Manually refresh on menu item click"""
        asyncio.run(self._refresh_handler())

    async def _refresh_handler(self) -> None:
        """Handle running `self.get_tag` asynchronously"""
        self.title = 'Refreshing...'
        self.title = await self.get_tag()
        self.notify_on_change()

    def notify_on_change(self) -> None:
        """Check to see if the tag has been updated, notify on changes"""
        if self.title != self.latest_tag:
            timestamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rumps.notification(
                title='Lospec Tag of the Day:',
                subtitle=f'{self.title}',
                message=f'Last checked at {timestamp}',
                action_button='Close',
            )
        # store the latest tag for comparison later
        self.latest_tag = self.title

    @staticmethod
    async def get_tag() -> str:
        """Parse `'https://lospec.com/dailies/'` for the tag of the day

        Returns:
            str: the tag of the day `#tag` -or-
            str: `Not Today!` if no tag is found -or-
            str: `Error: <HTTP status code>` for any response code other
                than 200
        """
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
