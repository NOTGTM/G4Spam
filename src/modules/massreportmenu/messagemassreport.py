from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files
from src.util.discordutils import discordutils

class messagemassreport:
    def __init__(self):
        self.module = 'Message Mass Report'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.channelid = None
        self.messageid = None
        self.reason = None
        self.delay = 0

    def report(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.post(
                'https://discord.com/api/v9/report',
                headers=cl.headers,
                json={
                    'version': '1.0',
                    'variant': '3',
                    'language': 'en',
                    'breadcrumbs': [1, 4, self.reason],
                    'elements': {},
                    'name': 'message',
                    'channel_id': self.channelid,
                    'message_id': self.messageid
                }
            )

            if r.status_code == 201:
                self.logger.succeded(f'{ctoken} Reported message')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.report(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.report(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.report(token, cl)
            
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
        message_link = self.ui.input('Message Link to report', str)
        ids = discordutils.extractids(message_link)
        self.channelid = ids['channel']
        self.messageid = ids['message']

        if not self.channelid or not self.messageid:
            self.logger.log('Invalid message link')
            return
        
        reasons = {
            '1': (1, 'Harassment'),
            '2': (2, 'Spam'),
            '3': (3, 'Self-harm'),
            '4': (4, 'NSFW content'),
            '5': (5, 'Hate speech'),
            '6': (6, 'Doxxing'),
            '7': (7, 'Other')
        }
        
        self.ui.createmenu([f'{reasons[k][1]}' for k in reasons.keys()])
        choice = self.ui.input('Report reason', str)
        
        if choice in reasons:
            self.reason = reasons[choice][0]
        else:
            self.reason = 7  # Default to "Other"

        self.delay = self.ui.delayinput()

        threading(
            func=self.report,
            tokens=files.gettokens(),
            delay=self.delay,
        )