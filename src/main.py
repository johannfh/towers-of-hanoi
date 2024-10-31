import logging

from view.app import SCREEN_HEIGHT, SCREEN_WIDTH, App

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app = App((SCREEN_WIDTH, SCREEN_HEIGHT))
    app.run()
