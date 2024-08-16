from tkinter import END, X
from customtkinter import CTkImage
# from pytube import YouTube, Channel, exceptions as pytube_exceptions
from pytubefix import YouTube, Channel, exceptions as pytube_exceptions
from threading import Thread
from PIL import Image
from io import BytesIO
from requests import get, exceptions as requests_exceptions
from os import path
from json import JSONDecodeError

# app modules
from static.languages import get_active_language
import auth.custom_auth
from interface.widgets import WIDGETS


# widget settings
HOME_DIRECTORY = path.expanduser("~")
DOWNLOADS_FOLDER = path.join(HOME_DIRECTORY, "Desktop")
DEFAULT_PADDINGS = {"padx": 10, "pady": 10}
LINK_SIZE = [350, 40]
PREVIEW_SIZE = (300, 200)
DEFAULT_PADDINGS = {"padx": 10, "pady": 10}


# "Download" button click handler
def create_downloading_thread() -> None:
    """create new thread for video downloading"""
    try:
        # check active language for translation
        active_language = get_active_language()
       
        # get youtube data from a pasted url
        WIDGETS["finish_status"].grid_forget()
        WIDGETS["download_button"].configure(state="disabled")

        # check what user's type / paste in input field
        video_url = WIDGETS["input"].get()
        checkURLEmptiness(video_url)


        # Update labels
        set_widget_text(WIDGETS["video_title"], active_language["video_title_on_start"])
        set_widget_text(
            WIDGETS["channel_name"], active_language["channel_name_on_start"]
        )

        # inititialize status elements: percents and progress bar
        show_progress_widgets()


        WIDGETS["percents"].grid(row=6, column=0, columnspan=2)
        WIDGETS["progress_bar"].grid(row=7, column=0, columnspan=2, padx=10, pady=10)
        WIDGETS["progress_bar"].set(0)
        set_widget_text(WIDGETS["finish_status"], "")
        set_widget_text(WIDGETS["percents"], "0%")

        # create separate thread for downloading to unfreeze GUI
        download_thread = Thread(
            target=downloading_thread, args=(video_url,)
        )
        download_thread.start()

    # when input is empty
    except ValueError as error:
        displayError(active_language["empty_finish_status"])
        hide_progress_widgets()

    # when first login attempt is failed
    except requests_exceptions.HTTPError as error:
        print("cant authorize, try one more time ", error)

    except Exception as error:
        print("В начале загрузки произошла ошибка: ", error)
        hide_progress_widgets()


# create new thread fon unfreezing app when downloading
def downloading_thread(video_url: str) -> None:
    """Separate thread where video is downloaded"""
    try:
        # get active language for correct text displaying
        active_language = get_active_language()
        
        # get youtube data from given url
        data_from_youtube = YouTube(
            url=video_url, use_oauth=True, allow_oauth_cache=True
        )

        show_progress_widgets()

        # set video preview
        preview_url = data_from_youtube.thumbnail_url
        preview_image = get_video_preview(preview_url)

        set_video_preview(preview_image)

        # Get total size for further progress calculation
        total_size = data_from_youtube.streams.get_highest_resolution().filesize
        

        # make a callback for proper progress calculation
        data_from_youtube.register_on_progress_callback(
            lambda _, __, remaining: download_callback(total_size, remaining)
        )

        # get video data
        video = data_from_youtube.streams.get_highest_resolution()

        # get only audio when needed
        is_only_audio_selected = WIDGETS['audio_checkbox'].get()
        if is_only_audio_selected:
            video = data_from_youtube.streams.filter(only_audio=True).first()
        
        channel_name = get_channel_name(data_from_youtube.channel_url)


        # Update neccessary labels
        set_widget_text(WIDGETS["video_title"], video.title)
        set_widget_text(WIDGETS["channel_name"], channel_name)
        set_widget_text(WIDGETS["finish_status"], active_language["success_message"])

        # Download video or audio
        video.download(output_path=DOWNLOADS_FOLDER, skip_existing=False)
        print("видео успешно скачано!")

    except JSONDecodeError as json_error:
        print(f"JSON decoding error: {json_error}")

    except pytube_exceptions.RegexMatchError as error:
        print('RegexMatchError error: ', error) 

        active_language = get_active_language()
        hide_progress_widgets()
        displayError(active_language["invalid_link_status"])

    except Exception as error:
        # get active language for correct text displaying
        active_language = get_active_language()
        hide_progress_widgets()
        set_widget_text(
            WIDGETS["finish_status"], active_language["restricted_finish_status"]
        )
        print("restricted_finish_status", error)

    # finally, place the finish status label into UI
    finally:
        WIDGETS["finish_status"].grid(row=9, column=0, columnspan=2, padx=10, pady=10)
        WIDGETS["download_button"].configure(state="normal")


# end


# on progress callback
def download_callback(total_size: str, bytes_remaining: int) -> None:
    # instantiate_youtube_class()
    """Calculate percents of downloaded video"""
    percent = round((total_size - bytes_remaining) / total_size, 2)

    # update progress bar and percents
    WIDGETS["progress_bar"].set(percent)
    WIDGETS["percents"].configure(text=f"{percent*100:.2f}%")
    


# end


# get channel name from urlk
def get_channel_name(channel_url: str) -> None:
    """get channel name from channel url"""
    channel = Channel(channel_url)
    return channel.channel_name


# end


# update text
def set_widget_text(widget: dict[str, type], new_text: str) -> None:
    """update widget's text"""
    widget.configure(text=new_text)


# end


# check pasted url for being not empty
def checkURLEmptiness(url: str) -> None:
    if len(url) == 0:
        raise ValueError("input is empty")


# end


# check pasted url for being not empty
def displayError(message: str) -> None:
    WIDGETS["input"].delete(0, END)
    WIDGETS["input"].insert(0, message)
    WIDGETS["download_button"].configure(state="normal")


# end


# hide elements when error occurs
def hide_progress_widgets():
    WIDGETS["video_title"].grid_forget()
    WIDGETS["channel_name"].grid_forget()
    WIDGETS["preview"].grid_forget()
    WIDGETS["percents"].grid_forget()
    WIDGETS["progress_bar"].grid_forget()
    WIDGETS["finish_status"].grid_forget()


# end


# show elements when no errors found
def show_progress_widgets():
    WIDGETS["video_title"].grid(row=4, column=0, **DEFAULT_PADDINGS, columnspan=2)
    WIDGETS["channel_name"].grid(row=5, column=0, **DEFAULT_PADDINGS, columnspan=2)
    WIDGETS["preview"].grid(row=6, column=0, **DEFAULT_PADDINGS, columnspan=2)
    WIDGETS["percents"].grid(row=7, column=0)
    WIDGETS["progress_bar"].grid(row=8, column=0, **DEFAULT_PADDINGS, columnspan=2)


# get video preview image
def get_video_preview(url):
    """Get video preview image by given link"""
    response = get(url)
    img = Image.open(BytesIO(response.content))
    return img


# set preview image in the interface
def set_video_preview(image):
    """Set video preview image in the interface"""
    imgCtk = CTkImage(image, size=PREVIEW_SIZE)
    WIDGETS["preview"].configure(image=imgCtk)
