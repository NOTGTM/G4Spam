# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class avatarchanger:
    def __init__(self):
        self.module = 'Avatar Changer'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.avatar_data = None

    def change(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.patch(
                'https://discord.com/api/v9/users/@me',
                headers=cl.headers,
                json={
                    'avatar': self.avatar_data
                }
            )

            if r.status_code == 200:
                self.logger.succeded(f'{ctoken} Changed avatar')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.change(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.change(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.change(token, cl)
            
            elif 'captcha_key' in r.text:
                self.logger.hcaptcha(f'{ctoken} Hcaptcha required')

            elif 'You need to verify' in r.text:
                self.logger.locked(f'{ctoken} Locked/Flagged')

            else:
                error = self.logger.errordatabase(r.text)
                self.logger.error(f'{ctoken}', error)

        except Exception as e:
            self.logger.error(f'{ctoken}', e)

    def menu(self):
        self.ui.prep()
        
        choice = self.ui.input('Remove avatar or upload new one? (remove/upload)', str).lower()
        
        if choice in ['remove', 'r']:
            self.avatar_data = None
        else:
            avatar_path = files.choosefile()
            if not os.path.exists(avatar_path):
                self.logger.log('File does not exist')
                return
            
            try:
                with open(avatar_path, 'rb') as f:
                    avatar_bytes = f.read()
                
                # Convert to base64 data URI
                import mimetypes
                mime_type = mimetypes.guess_type(avatar_path)[0]
                if not mime_type or not mime_type.startswith('image/'):
                    self.logger.log('File must be an image')
                    return
                
                avatar_b64 = base64.b64encode(avatar_bytes).decode('utf-8')
                self.avatar_data = f'data:{mime_type};base64,{avatar_b64}'
                
            except Exception as e:
                self.logger.error('Failed to read avatar file', e)
                return

        self.delay = self.ui.delayinput()

        threading(
            func=self.change,
            tokens=files.gettokens(),
            delay=self.delay,
        )