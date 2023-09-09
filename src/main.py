if __name__ == '__main__':
    try:
        import sys
        from tool_frames.Display import Display
        from utils.config import Config
        import logging

        if getattr(sys, 'frozen', False):
            import pyi_splash
        Config()
        # logging.basicConfig(filename='log/wasApp.log', encoding='utf-8', level=logging.DEBUG)
        logging.info("Start application")
        app = Display()
        if getattr(sys, 'frozen', False):
            pyi_splash.close()
        app.mainloop()
    except Exception as e:
        print("Error", e)
        input()
