"""
MIT License

Copyright (c) 2024-25 John Riggles [sudo_whoami]

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
import datetime as dt
from asyncio import run
from json import dump, load
from pathlib import Path

import rumps
from httpx import get


class LTOTD(rumps.App):
    def __init__(self) -> None:
        """Show the Lospec Tag of the Day in the menu bar (as app's title)"""
        super().__init__(
            'LTOTD',
            menu=[
                'Lospec Tag of the Day',  # disabled, used as title
                rumps.separator,
                'Refresh',
                'Show Notifications',
                # 'Quit' is added automatically
            ]
        )
        # refresh every hour (3600 seconds)
        rumps.Timer(self.refresh, 3600).start()
        # initialize latest_tag for comparison
        self.latest_tag: str | None = None
        # create data.json in Application Support directory if it doesn't exist
        self._create_app_storage()
        # load user's notification preference from Application Support
        self.menu['Show Notifications'].state = (
            self.load_notification_preference()
        )

    def _create_app_storage(self) -> None:
        data_file = Path(rumps.application_support('LTOTD')) / 'data.json'
        if not data_file.exists():
            with data_file.open('w') as prefs:
                dump({'notifications_enabled': True}, prefs)

    @rumps.clicked('Refresh')
    def refresh(self, _sender=None) -> None:
        """Manually refresh on menu item click"""
        run(self._refresh_handler())

    async def _refresh_handler(self) -> None:
        """Handle running `self.get_tag` asynchronously"""
        self.title = 'Refreshing...'
        self.title = await self.get_tag()
        if self.menu['Show Notifications'].state:
            self.notify_on_change()

    @rumps.clicked('Show Notifications')
    def show_notifications(self, sender) -> None:
        """Enable or disable notifications on menu item click"""
        # NOTE: due to limitations in rumps, changing this state won't update
        # the notification permssions in macOS System Settings
        sender.state = not sender.state
        self.save_notification_preference()

    def load_notification_preference(self) -> bool:
        """
        Load the user's notification preference from persistent storage in the
        Application Support directory
        """
        with self.open('data.json', 'r') as prefs:
            data = load(prefs)
            return data.get('notifications_enabled', False)

    def save_notification_preference(self) -> None:
        """
        Save the user's notification preference to persistent storage in the
        Application Support directory
        """
        with self.open('data.json', 'w') as prefs:
            state = self.menu['Show Notifications'].state
            dump({'notifications_enabled': state}, prefs)

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
        """Query `https://lospec.com/dailies/current-daily-tag.txt` for the tag
        of the day

        Returns:
            str: the tag of the day `#tag` -or-
            str: `No Tag Found` if no tag is found -or-
            str: `Error: <HTTP status code>` for any response code other
            than 200
        """
        URL = 'https://lospec.com/dailies/current-daily-tag.txt'
        # FIXME: AsyncClient doesn't seem to work in the built app, despite
        # working when just running the script...fix TBD, for now, 'get' works
        # async with AsyncClient() as client:
            # response = await client.get(URL)
        response = get(URL)

        if (status := response.status_code) == 200:
            if tag := response.text.strip():
                return f'#{tag}'
            else:
                return 'No Tag Found'
        else:
            return f'ERROR: {status}'


if __name__ == '__main__':
    app = LTOTD()
    app.run()
