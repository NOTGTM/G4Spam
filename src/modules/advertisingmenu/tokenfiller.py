from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class tokenfiller:
    def __init__(self):
        self.module = 'Token Filler'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.delay = 0

    def fill(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            # Get user info first
            r = cl.sess.get(
                'https://discord.com/api/v9/users/@me',
                headers=cl.headers
            )

            if r.status_code != 200:
                self.logger.error(f'{ctoken} Failed to get user info')
                return

            user_data = r.json()
            
            # Update presence to show as online and active
            r = cl.sess.patch(
                'https://discord.com/api/v9/users/@me/settings',
                headers=cl.headers,
                json={
                    'status': 'online',
                    'custom_status': {
                        'text': 'Active user 🎮',
                        'emoji_id': None,
                        'emoji_name': '🎮'
                    }
                }
            )

            if r.status_code == 200:
                self.logger.succeded(f'{ctoken} Updated presence')
            
            # Join some popular public servers to make account look more legitimate
            popular_invites = ['discord-developers', 'discord-testers', 'discord-api']
            
            for invite in popular_invites:
                try:
                    r = cl.sess.post(
                        f'https://discord.com/api/v9/invites/{invite}',
                        headers=cl.headers,
                        json={'session_id': cl.wssessid}
                    )
                    if r.status_code == 200:
                        self.logger.succeded(f'{ctoken} Joined {invite}')
                    time.sleep(2)
                except:
                    pass

        except Exception as e:
            self.logger.error(f'{ctoken}', e)

    def menu(self):
        self.ui.prep()
        self.logger.log('This will make tokens look more legitimate by:')
        self.logger.log('- Setting online status')
        self.logger.log('- Adding custom status')
        self.logger.log('- Joining popular Discord servers')
        
        if not self.ui.input('Continue', bool):
            return

        self.delay = self.ui.delayinput()

        threading(
            func=self.fill,
            tokens=files.gettokens(),
            delay=self.delay,
        )