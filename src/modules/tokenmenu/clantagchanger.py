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

class clantagchanger:
    def __init__(self):
        self.module = 'Clan Tag Changer'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.clan_tag = None

    def change(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.patch(
                'https://discord.com/api/v9/users/@me',
                headers=cl.headers,
                json={
                    'clan': {
                        'identity_guild_id': None,
                        'identity_enabled': True,
                        'tag': self.clan_tag
                    } if self.clan_tag else None
                }
            )

            if r.status_code == 200:
                action = 'Changed clan tag' if self.clan_tag else 'Removed clan tag'
                self.logger.succeded(f'{ctoken} {action}')

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
        
        choice = self.ui.input('Set clan tag or remove it? (set/remove)', str).lower()
        
        if choice in ['remove', 'r']:
            self.clan_tag = None
        else:
            self.clan_tag = self.ui.input('Clan Tag (max 4 characters)', str)[:4]

        self.delay = self.ui.delayinput()

        threading(
            func=self.change,
            tokens=files.gettokens(),
            delay=self.delay,
        )