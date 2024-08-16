from customtkinter import set_appearance_mode, set_default_color_theme, CTk
from interface.interface import create_widgets
from static.languages import ACTIVE_LANGUAGE

class AppWindow:
    """ creates main GUI window with widgets"""
    
    # default configs
    DEFAULT_BACKGROUND_THEME = 'light'
    DEFAULT_COLOR_THEME = 'dark-blue'

    WINDOW_WIDTH = 420
    WINDOW_HEIGHT = 670

    WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
    WINDOW_TITLE = ACTIVE_LANGUAGE['window_title']


    def __init__(self):
        """creates window instance with default configs"""

        # Create app window
        self.app = CTk()
        self.app.title(self.WINDOW_TITLE)

        # Place app always in the screen's center
        self.center_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

        # Place widgets in GUI
        self.create_widgets()
    # end

    
    def set_color_scheme(self):
        """ makes default UI colors"""
        set_appearance_mode(self.DEFAULT_BACKGROUND_THEME)
        set_default_color_theme(self.DEFAULT_COLOR_THEME)
        # 123213
    # end


    def center_window(self, width, height):
        """makes window always at the screen's center """
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2
        
        self.app.geometry(f"{width}x{height}+{x}+{y}")
    # end


    def create_widgets(self):
        create_widgets(self.app)


    def run(self):
        """Runs app"""
        self.app.mainloop()


