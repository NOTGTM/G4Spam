from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class onboarding:
    def __init__(self):
        self.module = 'Onboarding'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.delay = 0

    def complete(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            # Get onboarding info first
            r = cl.sess.get(
                f'https://discord.com/api/v9/guilds/{self.serverid}/onboarding',
                headers=cl.headers
            )

            if r.status_code != 200:
                self.logger.error(f'{ctoken} Failed to get onboarding info')
                return

            onboarding_data = r.json()
            
            # Complete onboarding
            r = cl.sess.put(
                f'https://discord.com/api/v9/guilds/{self.serverid}/onboarding-responses',
                headers=cl.headers,
                json={
                    'onboarding_responses': [],
                    'onboarding_responses_seen': True
                }
            )

            if r.status_code == 200:
                self.logger.succeded(f'{ctoken} Completed onboarding')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.complete(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.complete(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.complete(token, cl)
            
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
        self.delay = self.ui.delayinput()

        threading(
            func=self.complete,
            tokens=files.gettokens(),
            delay=self.delay,
        )