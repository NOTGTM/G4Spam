from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.apibypassing import apibypassing
from src.util.discordutils import discordutils
from src.util.threading import threading
from src.util.files import files
from src.util.other import other
apibypassing = apibypassing()

class multichannelspammer:
    def __init__(self):
        self.module = 'Multi-Channel Spammer'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

        self.messages = []
        self.channels = []
        self.dostring = False
        self.stringlen = 0
        self.doemoji = False
        self.emojilen = 0
        self.delay = 0

    def spam(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        while True:
            try:
                other.delay(self.delay)
                if not cl:
                    cl = client(token)

                # Pick random channel and message
                channelid = random.choice(self.channels)
                message = random.choice(self.messages)
                
                if self.dostring:
                    message = f'{message} | {other.getstring(self.stringlen)}'

                if self.doemoji:
                    message = f'{message} | {other.getemoji(self.emojilen)}'

                r = cl.sess.post(
                    f'https://discord.com/api/v9/channels/{channelid}/messages',
                    headers=cl.headers,
                    json={
                        'mobile_network_type': 'unknown',
                        'content': message,
                        'nonce': discordutils.getsnowflake(),
                        'flags': 0
                    }
                )

                if r.status_code == 200:
                    self.logger.succeded(f'{ctoken} Sent message to {channelid}')
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

                elif 'You need to verify' in r.text:
                    self.logger.locked(f'{ctoken} Locked/Flagged')

                else:
                    error = self.logger.errordatabase(r.text)
                    self.logger.error(f'{ctoken}', error)
                    break

            except Exception as e:
                self.logger.error(f'{ctoken}', e)
                break

    def menu(self):
        self.ui.prep()
        
        # Get multiple channels
        self.logger.log('Enter channel links (one per line, empty line to finish):')
        while True:
            channel_input = input('Channel link: ').strip()
            if not channel_input:
                break
            try:
                ids = discordutils.extractids(channel_input)
                if ids['channel']:
                    self.channels.append(ids['channel'])
                    self.logger.log(f'Added channel: {ids["channel"]}')
                else:
                    self.logger.log('Invalid channel link')
            except:
                self.logger.log('Invalid channel link')

        if not self.channels:
            self.logger.log('No valid channels provided')
            return

        self.dostring = self.ui.input('String', bool)
        if self.dostring:
            self.stringlen = self.ui.input('String length', int)

        self.doemoji = self.ui.input('Emoji', bool)
        if self.doemoji:
            self.emojilen = self.ui.input('Amount of emojis', int)

        if self.ui.input('Use messages from a file', bool):
            path = files.choosefile()
            if not os.path.exists(path):
                self.logger.log('File does not exist')
                self.messages = [self.ui.input('Message', str)]
            else:
                with open(path, 'r', encoding='utf-8') as f:
                    self.messages = f.read().splitlines()
        else:
            self.messages = [self.ui.input('Message', str)]

        self.delay = self.ui.delayinput()

        threading(
            func=self.spam,
            tokens=files.gettokens(),
            delay=self.delay,
        )