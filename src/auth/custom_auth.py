# from pytube import request, innertube
from pytubefix import request, innertube
from interface.widgets import WIDGETS
from time import time, sleep
from json import loads
from webbrowser import open
import pyperclip
from os import path


def create_tokenfile_at(folder) -> None:
    """ Creates new token location in given folder"""
    innertube._cache_dir = folder
    innertube._token_file = path.join(innertube._cache_dir, 'tokens.json')
    print("🐍",folder)
    print("🐍)", path.join(innertube._cache_dir, 'tokens.json'))
    
# end


# modified pytube's Google authentication
def custom_fetch_bearer_token(self, _client_id=innertube._client_id, _client_secret=innertube._client_secret, WIDGETS=WIDGETS):
        """Fetch an OAuth token."""
        is_login_confirmed = False
        
        try:
            start_time = int(time() - 30)
            data = {
                'client_id': _client_id,
                'scope': 'https://www.googleapis.com/auth/youtube'
            }
            response = request._execute_request(
                'https://oauth2.googleapis.com/device/code',
                'POST',
                headers={
                    'Content-Type': 'application/json'
                },
                data=data
            )
            response_data = loads(response.read())
            verification_url = response_data['verification_url']
            user_code = response_data['user_code']
            
            show_login_widgets(url=verification_url, code=user_code)
            
            while not is_login_confirmed:
                try:
                    sleep(5)
                        
                    data = {
                        'client_id': _client_id,
                        'client_secret': _client_secret,
                        'device_code': response_data['device_code'],
                        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
                    }
                    
                    response = request._execute_request(
                        'https://oauth2.googleapis.com/token',
                        'POST',
                        headers={
                            'Content-Type': 'application/json'
                        },
                        data=data
                    )
                    response_data = loads(response.read())

                    self.access_token = response_data['access_token']
                    self.refresh_token = response_data['refresh_token']
                    self.expires = start_time + response_data['expires_in']
                    
                    self.cache_tokens()
                    
                    is_login_confirmed = True
                    if is_login_confirmed: hide_login_widgets()
                
                except Exception as error:
                    print('login attemp error: ', error)
                    
        except Exception as error:
            print('custom_auth error: ', error)
# end
            

def show_login_widgets(url: str, code: str) -> None:
    """Displays login widgets"""
    WIDGETS['video_title'].configure(text='Enter the code in your browser:')
    WIDGETS['channel_name'].configure(text=code)
    WIDGETS['progress_bar'].grid_forget()
    WIDGETS['percents'].grid_forget()

    # set commands for hidden buttons    
    WIDGETS['open_link_button'].configure(command=lambda: open_link(url, code))

    # show hidden elements
    WIDGETS['open_link_button'].grid(row=5, column=0)
# end


def hide_login_widgets() -> None:
    """Hide login widgets from UI"""
    WIDGETS['open_link_button'].grid_forget()
    WIDGETS['confirm_login_button'].grid_forget()
    
    WIDGETS['percents'].grid(row=6, column=0)
    WIDGETS['progress_bar'].grid(row=7, column=0, padx=10, pady=10)
# end


def open_link(url: str, code: str) -> None:
    """Open verification link in the browser"""
    open(url)
    copy_to_clipboard(code)
# end


def copy_to_clipboard(code: str) -> None:
    """ Copy the user login code to clipboard"""
    pyperclip.copy(code)
    WIDGETS['open_link_button'].configure(text="Пароль скопирован - вставь его✅")
# end


# create new location for auth token (rewrite pytube's code)
TOKENFILE_FOLDER = path.expanduser("~")
create_tokenfile_at(TOKENFILE_FOLDER)
            
# replace pytube's auth method with a custom one
innertube.InnerTube.fetch_bearer_token = custom_fetch_bearer_token