from customtkinter import CTkLabel, CTkEntry, CTkProgressBar, CTkButton, CTkCheckBox, CTkOptionMenu, CTkSegmentedButton

# initialize global UI widgets
WIDGETS: dict[str, type] = {
    'subtitle': CTkLabel,
    'input': CTkEntry,
    'audio_checkbox': CTkCheckBox,
    'download_button': CTkButton,
    'video_title': CTkLabel,
    'channel_name': CTkLabel,
    'preview': CTkLabel,
    'percents': CTkLabel,
    'progress_bar': CTkProgressBar,
    'finish_status': CTkLabel,
    'languages': CTkSegmentedButton,
    'dark_mode_switch': CTkOptionMenu,
    'open_link_button': CTkButton,
    'confirm_login_button': CTkButton,
}
