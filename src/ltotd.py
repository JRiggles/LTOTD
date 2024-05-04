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
