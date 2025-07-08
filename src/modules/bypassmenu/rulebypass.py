from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class rulebypass:
    def __init__(self):
        self.module = 'Rule Bypass'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.delay = 0

    def accept(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.post(
                f'https://discord.com/api/v9/guilds/{self.serverid}/requests/@me',
                headers=cl.headers,
                json={
                    'version': '2024-05-16',
                    'form_fields': [
                        {
                            'field_type': 'TERMS',
                            'label': 'Rules',
                            'description': 'Accept server rules',
                            'required': True,
                            'values': ['on']
                        }
                    ]
                }
            )

            if r.status_code == 201:
                self.logger.succeded(f'{ctoken} Accepted rules')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.accept(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.accept(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.accept(token, cl)
            
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
            func=self.accept,
            tokens=files.gettokens(),
            delay=self.delay,
        )