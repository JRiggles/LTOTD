<img src="src/appicon.png" alt="app icon - a stylized pixel-art image of a lightbulb"/>

# LTOTD
### "Lospec Tag of the Day"

A Mac OS menu bar app that displays the "Tag of the Day" from [Lospec](https://lospec.com)

> Current Version: 0.2.3

### Latest Changes:
- *v0.2.3* New app icon, clean up imports, better "No Tag Found" message, light cleanup/refactoring
- *v0.2.2* Patch: fix bad refresh time from v0.2.1 (oops!)
- *v0.2.1* Patch: fix async call in `_refresh_handler()`

## Getting Started

<img src="screenshots/main.png" alt="a screenshot of the main application menu" />

Start the app and it will automatically fetch the Tag of the Day

The app will refresh every hour while running, but you can also click on "Refresh" in the menu to refresh manually

You'll get a notification from the app when the `#tag` changes

<img src="screenshots/notification.png" alt="a screenshot of a typical notification from this app" />

## Installation

NOTE: Official release is on hold pending updates to the [Lospec API](https://lospec.com/palettes/api), at which point I will update the app to make use of the official endpoint instead of scraping. This app should be considered only as a proof-of-concept.

    TODO

### Build it Yourself

In lieu of a proper release for now, you can build the app yourself!

> [!NOTE]
> You'll need Python installed (this app was built using Python 3.12)

1. Clone this repo
2. Open a terminal and navigate to the root of the cloned directory, **LTOTD**
3. Run the command `pip install -r requirements.txt` to install the necessary dependencies
4. Run the command `python setup.py py2app` to build the app

If everything worked, you'll find the app here:

`{wherever you cloned the repo}/LTOTD/dist/LTOTD`

## Built With Python

  Using...
  - [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/)
  - [py2app](https://py2app.readthedocs.io/en/latest/index.htm)
  - [Requests](https://requests.readthedocs.io/en/latest/)
  - [Rumps](https://github.com/jaredks/rumps?tab=readme-ov-file)
## Versioning

This project follows [Semantic Versioning](http://semver.org/), a.k.a SEMVER

## Acknowledgements

Lospec was created and is maintained by Sam Keddy, a.k.a [Skeddles](https://github.com/Skeddles)

- [Lospec on Patreon](https://www.patreon.com/lospec)
- [Lospec on GitHub](https://github.com/lospec)

*All copyrights are property of their respective owners*
