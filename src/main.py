from src.Display import Display
from src.config import Config

if __name__ == '__main__':
    Config()
    app = Display()
    app.mainloop()