RUSSIAN = {
    # GUI window title
    'window_title': 'Видео-скачивалка с Ютуба',
    
    # GUI elements
    'subtitle': 'Вставь ссылку на видео сюда 👇',
    'download_button': 'Скачать',
    'audio_checkbox': 'Только аудио',

    # switches text
    'themes': ['Светлая тема', 'Тёмная тема'],
    'languages': ['Русский', 'English'],

    # downloading elements
    'video_title_on_start': 'Начинаю загрузку...',
    'channel_name_on_start': 'Получаю название канала...',

    # error / success statuses
    'empty_finish_status': 'Кажется, ты забыл вставить ссылку =(',
    'invalid_link_status': 'Прости, но с твоей ссылкой что-то не так =(',
    'restricted_finish_status': 'Не могу скачать видео из-за ограничений Ютуба, прости 😢',
    'success_message': 'Видео скачалось на рабочий стол!',

    # signin buttons
    'open_link_button': 'Залогиниться с Google',
    'confirm_login_button': 'Логин подтверждаю',
}

ENGLISH = {
    # GUI window title
    'window_title': 'Free YouTube video downloader',
    
    # GUI elements
    'subtitle': 'Paste the video link here 👇',
    'download_button': 'Download',
    'audio_checkbox': 'Only audio',
    

    # switches text
    'themes': ['Light theme', 'Dark theme'],
    'languages': ['English', 'Русский'],

    # downloading elements
    'video_title_on_start': 'Starting download...',
    'channel_name_on_start': 'Fetching channel name...',

    # error / success statuses
    'empty_finish_status': 'Oops, it seems you forgot to paste the link =(',
    'invalid_link_status': 'There is some sort of error in your link, sorry  =(',
    'restricted_finish_status': 'Cannot download the video due to YouTube restrictions, sorry 😢',
    'success_message': 'Video downloaded to the desktop!',

    # signin buttons
    'open_link_button': 'Sign in with Google',
    'confirm_login_button': 'Confirm the sign in',
}

ACTIVE_LANGUAGE = ENGLISH

ALL_THEME_VALUES = [
    RUSSIAN['themes'],
    ENGLISH['themes'],
]


def update_active_languge(new_language) -> dict:
    global ACTIVE_LANGUAGE
    ACTIVE_LANGUAGE = new_language


def get_active_language() -> dict:
    return ACTIVE_LANGUAGE
