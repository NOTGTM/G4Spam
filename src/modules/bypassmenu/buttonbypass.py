from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.apibypassing import apibypassing
from src.util.discordutils import discordutils
from src.util.threading import threading
from src.util.files import files
apibypassing = apibypassing()

class buttonbypass:
    def __init__(self):
        self.module = 'Button Bypass'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        
        self.channelid = None
        self.messageid = None
        self.custom_id = None
        self.delay = 0

    def click(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.post(
                'https://discord.com/api/v9/interactions',
                headers=cl.headers,
                json={
                    'type': 3,
                    'nonce': discordutils.getsnowflake(),
                    'guild_id': None,
                    'channel_id': self.channelid,
                    'message_id': self.messageid,
                    'application_id': None,
                    'session_id': cl.wssessid,
                    'data': {
                        'component_type': 2,
                        'custom_id': self.custom_id
                    }
                }
            )

            if r.status_code == 204:
                self.logger.succeded(f'{ctoken} Clicked button')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.click(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.click(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.click(token, cl)
            
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
        message_link = self.ui.input('Message Link with button', str)
        ids = discordutils.extractids(message_link)
        self.channelid = ids['channel']
        self.messageid = ids['message']
        
        self.custom_id = self.ui.input('Button Custom ID (inspect element to find)', str)
        self.delay = self.ui.delayinput()

        threading(
            func=self.click,
            tokens=files.gettokens(),
            delay=self.delay,
        )