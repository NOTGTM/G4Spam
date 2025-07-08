from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class booster:
    def __init__(self):
        self.module = 'Booster'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.delay = 0

    def boost(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            # First check if user has nitro
            r = cl.sess.get(
                'https://discord.com/api/v9/users/@me',
                headers=cl.headers
            )

            if r.status_code != 200:
                self.logger.error(f'{ctoken} Failed to get user info')
                return

            user_data = r.json()
            premium_type = user_data.get('premium_type', 0)
            
            if premium_type == 0:
                self.logger.error(f'{ctoken} No Nitro subscription')
                return

            # Get available boosts
            r = cl.sess.get(
                'https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots',
                headers=cl.headers
            )

            if r.status_code != 200:
                self.logger.error(f'{ctoken} Failed to get boost slots')
                return

            slots = r.json()
            available_slots = [slot for slot in slots if not slot.get('premium_guild_subscription')]
            
            if not available_slots:
                self.logger.error(f'{ctoken} No available boost slots')
                return

            # Use first available slot to boost
            slot_id = available_slots[0]['id']
            
            r = cl.sess.put(
                f'https://discord.com/api/v9/guilds/{self.serverid}/premium/subscriptions',
                headers=cl.headers,
                json={
                    'user_premium_guild_subscription_slot_ids': [slot_id]
                }
            )

            if r.status_code == 201:
                self.logger.succeded(f'{ctoken} Boosted server')

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.boost(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.boost(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.boost(token, cl)
            
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
        self.serverid = self.ui.input('Server ID to boost', str)
        self.delay = self.ui.delayinput()

        self.logger.log('Note: Tokens must have Nitro subscription to boost')

        threading(
            func=self.boost,
            tokens=files.gettokens(),
            delay=self.delay,
        )