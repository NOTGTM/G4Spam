from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files
from src.util.other import other

class soundboardspammer:
    def __init__(self):
        self.module = 'Soundboard Spammer'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.channelid = None
        self.sound_id = None
        self.delay = 0

    def spam(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        while True:
            try:
                other.delay(self.delay)
                if not cl:
                    cl = client(token)

                r = cl.sess.post(
                    f'https://discord.com/api/v9/channels/{self.channelid}/voice-channel-effects',
                    headers=cl.headers,
                    json={
                        'type': 1,
                        'emoji_id': None,
                        'emoji_name': None,
                        'sound_id': self.sound_id,
                        'source_user_id': None
                    }
                )

                if r.status_code == 204:
                    self.logger.succeded(f'{ctoken} Played soundboard')
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
        self.sound_id = self.ui.input('Soundboard Sound ID', str)
        self.delay = self.ui.delayinput()

        threading(
            func=self.spam,
            tokens=files.gettokens(),
            delay=self.delay,
        )