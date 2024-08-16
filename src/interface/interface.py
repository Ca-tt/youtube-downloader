from customtkinter import (
    set_appearance_mode,
    CTk,
    CTkLabel,
    CTkEntry,
    CTkProgressBar,
    CTkButton,
    CTkCheckBox,
    StringVar,
    CTkFont,
    CTkOptionMenu,
)
from random import randrange

# app modules
from downloader import create_downloading_thread, set_widget_text
from static.languages import (
    ACTIVE_LANGUAGE,
    RUSSIAN,
    ENGLISH,
    ALL_THEME_VALUES,
    update_active_languge,
    get_active_language,
)
from interface.widgets import WIDGETS
# from auth.custom_auth import open_link

# UI elements configuration
# sizes
DEFAULT_PADDING = 10
DEFAULT_PADDINGS = {"padx": DEFAULT_PADDING, "pady": DEFAULT_PADDING}
LINK_SIZE = [350, 40]

# texts
SUBTITLE_TEXT = ACTIVE_LANGUAGE["subtitle"]
BUTTON_TEXT = ACTIVE_LANGUAGE["download_button"]
AUDIO_CHECKBOX_TEXT = ACTIVE_LANGUAGE["audio_checkbox"]
THEME_VALUES = ACTIVE_LANGUAGE["themes"]
LANGUAGE_VALUES = ACTIVE_LANGUAGE["languages"]

# sign in buttons
CONFIRM_LOGIN_TEXT = ACTIVE_LANGUAGE["confirm_login_button"]
OPEN_LINK_TEXT = ACTIVE_LANGUAGE["open_link_button"]


# create and place interface elements inside app
def create_widgets(app: CTk) -> None:
    """Creates interface of UI elements and place them
    in the GUI's windows"""

    # top label text
    WIDGETS["subtitle"] = CTkLabel(
        app, text=SUBTITLE_TEXT, font=CTkFont(family="Segoe UI", size=20)
    )

    # input (for pasting url)
    test_video_url = StringVar(value="https://www.youtube.com/watch?v=hq5fofOLI6w")
    WIDGETS["input"] = CTkEntry(
        app,
        width=LINK_SIZE[0],
        height=LINK_SIZE[1],
        placeholder_text=generate_random_placeholder(),
        textvariable=test_video_url,
    )

    # button (for downloading)
    WIDGETS["download_button"] = CTkButton(
        app,
        text=BUTTON_TEXT,
        command=create_downloading_thread,
    )
    WIDGETS["audio_checkbox"] = CTkCheckBox(app, text=AUDIO_CHECKBOX_TEXT)

    # video name
    # channel name
    # preveiw image
    WIDGETS["video_title"] = CTkLabel(app, text="", font=CTkFont(size=22))
    WIDGETS["channel_name"] = CTkLabel(app, text="", font=CTkFont(size=22))
    WIDGETS["preview"] = CTkLabel(app, text="")

    # percents 
    # progress bar
    # status label (when video downloaded)
    WIDGETS["percents"] = CTkLabel(
        app, text="0%", font=CTkFont(family="Segoe UI", size=16)
    )
    WIDGETS["progress_bar"] = CTkProgressBar(
        app, progress_color="red", width=300, height=6, corner_radius=5
    )
    WIDGETS["progress_bar"].set(0)
    WIDGETS["finish_status"] = CTkLabel(app, text="", font=CTkFont(size=14))

    # languages
    # change theme button
    current_language = StringVar(value=LANGUAGE_VALUES[0])
    isDarkTheme = StringVar(value=THEME_VALUES[0])
    WIDGETS["languages"] = CTkOptionMenu(
        app,
        values=LANGUAGE_VALUES,
        variable=current_language,
        command=lambda current_language: set_active_language(current_language, WIDGETS),
    )
    WIDGETS["dark_mode_switch"] = CTkOptionMenu(
        app, values=THEME_VALUES, variable=isDarkTheme, command=toggle_dark_theme
    )

    # login buttons
    WIDGETS["confirm_login_button"] = CTkButton(
        app, text=CONFIRM_LOGIN_TEXT, font=CTkFont(size=22)
    )
    WIDGETS["open_link_button"] = CTkButton(
        app, text=OPEN_LINK_TEXT, font=CTkFont(size=22)
    )

    # make some rows and columns in layout full width
    # place elements in UI
    configure_grid(app)
    place_widgets()


# end


def place_widgets() -> None:
    """Place widgets in UI"""

    # visible (top) elements
    WIDGETS["subtitle"].grid(row=0, column=0, **DEFAULT_PADDINGS, columnspan=2)
    WIDGETS["input"].grid(row=1, column=0, **DEFAULT_PADDINGS, columnspan=2)
    
    # button
    WIDGETS["download_button"].grid(row=2, column=0, padx=(0), pady=0, columnspan=2)
    WIDGETS["audio_checkbox"].grid(row=2, column=1, padx=(0), pady=0)

    # hidden (download) elements
    WIDGETS["video_title"].grid(row=4, column=0, **DEFAULT_PADDINGS, columnspan=2)
    WIDGETS["channel_name"].grid(row=5, column=0, columnspan=2)
    WIDGETS["preview"].grid(row=6, column=0, columnspan=2)

    # settings (at the side)
    WIDGETS["dark_mode_switch"].grid(row=10, column=0, sticky="ws", **DEFAULT_PADDINGS)
    WIDGETS["languages"].grid(row=10, column=1, sticky="es", **DEFAULT_PADDINGS)
# end


def configure_grid(app) -> None:
    """ " make some rows and columns in layout full width"""
    app.columnconfigure((0), weight=1)
    app.rowconfigure((10), weight=1)
# end


# create random input placeholder
def generate_random_placeholder() -> str:
    INPUT_PLACEHOLDERS = [
        "https://www.youtube.com/",
        "https://www.youtube.com/watch",
        "https://www.youtube.com/watch?v=q-_ezD9Swz4",
        "https://www.youtube.com/watch?v=sdf412",
    ]

    # pick one of placeholders
    random_placeholder = INPUT_PLACEHOLDERS[randrange(0, len(INPUT_PLACEHOLDERS))]
    return random_placeholder
# end


# change interface theme
def toggle_dark_theme(isDarkTheme: StringVar) -> None:
    """Change interface theme"""
    # get current language values for correct comparison
    active_language = get_active_language()
    THEME_VALUES = active_language["themes"]

    set_appearance_mode("dark" if isDarkTheme == THEME_VALUES[1] else "light")


def set_active_language(switch_language: StringVar, WIDGETS) -> None:
    """choose active language"""
    new_interface_language = ENGLISH if switch_language == "English" else RUSSIAN
    update_active_languge(new_interface_language)

    change_widgets_language(WIDGETS)


def change_widgets_language(WIDGETS) -> None:
    """toggle widgets language"""
    active_language = get_active_language()

    # save previous theme value
    previous_dark_mode_value = WIDGETS["dark_mode_switch"].get()
    index = 0
    for array in ALL_THEME_VALUES:
        for value in array:
            if previous_dark_mode_value == value:
                index = array.index(value)

    # set label text
    set_widget_text(WIDGETS["subtitle"], active_language["subtitle"])
    set_widget_text(WIDGETS["download_button"], active_language["download_button"])
    set_widget_text(WIDGETS["audio_checkbox"], active_language["audio_checkbox"])

    # set dropdowns text
    WIDGETS["dark_mode_switch"].configure(
        values=active_language["themes"],
    )
    WIDGETS["dark_mode_switch"].set(active_language["themes"][index])

    # change language widget text
    WIDGETS["languages"].configure(values=active_language["languages"])
    WIDGETS["languages"].set(active_language["languages"][0])
