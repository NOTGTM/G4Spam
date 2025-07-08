from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files
from src.util.other import other

class vcspamjoinleave:
    def __init__(self):
        self.module = 'VC Spam Join-Leave'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.channelid = None
        self.delay = 0

    def spam(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        while True:
            try:
                other.delay(self.delay)
                if not cl:
                    cl = client(token)

                # Join VC
                r = cl.sess.patch(
                    f'https://discord.com/api/v9/guilds/{self.serverid}/voice-states/@me',
                    headers=cl.headers,
                    json={
                        'channel_id': self.channelid,
                        'self_mute': False,
                        'self_deaf': False
                    }
                )

                if r.status_code == 204:
                    self.logger.succeded(f'{ctoken} Joined VC')
                    
                    # Wait a bit then leave
                    time.sleep(1)
                    
                    # Leave VC
                    r = cl.sess.patch(
                        f'https://discord.com/api/v9/guilds/{self.serverid}/voice-states/@me',
                        headers=cl.headers,
                        json={
                            'channel_id': None
                        }
                    )
                    
                    if r.status_code == 204:
                        self.logger.succeded(f'{ctoken} Left VC')
                    
                    continue

                elif 'retry_after' in r.text:
                    limit = r.json().get('retry_after', 1.5)
                    self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                    time.sleep(float(limit))
                    continue

                elif 'Try again later' in r.text:
                    self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                    time.sleep(5)
                    continue

                elif 'Cloudflare' in r.text:
                    self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                    time.sleep(10)
                    continue
                
                elif 'captcha_key' in r.text:
                    self.logger.hcaptcha(f'{ctoken} Hcaptcha required')
                    break

                elif 'You need to verify' in r.text:
                    self.logger.locked(f'{ctoken} Locked/Flagged')
                    break

                else:
                    error = self.logger.errordatabase(r.text)
                    self.logger.error(f'{ctoken}', error)
                    break

            except Exception as e:
                self.logger.error(f'{ctoken}', e)
                break

    def menu(self):
        self.ui.prep()
        self.serverid = self.ui.input('Server ID', str)
        self.channelid = self.ui.input('Voice Channel ID', str)
        self.delay = self.ui.delayinput()

        threading(
            func=self.spam,
            tokens=files.gettokens(),
            delay=self.delay,
        )