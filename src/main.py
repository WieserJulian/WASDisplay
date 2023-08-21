from src.tool_frames.Display import Display
from src.utils.config import Config
import logging

if __name__ == '__main__':
    Config()
    # logging.basicConfig(filename='log/wasApp.log', encoding='utf-8', level=logging.DEBUG)
    logging.info("Start application")
    app = Display()
    app.mainloop()