from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class vcjoiner:
    def __init__(self):
        self.module = 'VC Joiner'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.channelid = None
        self.delay = 0

    def join(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.patch(
                'https://discord.com/api/v9/guilds/{}/voice-states/@me'.format(self.serverid),
                headers=cl.headers,
                json={
                    'channel_id': self.channelid,
                    'self_mute': False,
                    'self_deaf': False
                }
            )

            if r.status_code == 204:
                self.logger.succeded(f'{ctoken} Joined VC')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.join(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.join(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.join(token, cl)
            
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
        self.serverid = self.ui.input('Server ID', str)
        self.channelid = self.ui.input('Voice Channel ID', str)
        self.delay = self.ui.delayinput()

        threading(
            func=self.join,
            tokens=files.gettokens(),
            delay=self.delay,
        )