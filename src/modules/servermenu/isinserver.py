from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.threading import threading
from src.util.files import files

class isinserver:
    def __init__(self):
        self.module = 'Is In Server'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.in_server = []
        self.not_in_server = []

    def check(self, token, cl: client=None):
        ctoken = self.ui.cut(token, 20, '...')
        try:
            if not cl:
                cl = client(token)

            r = cl.sess.get(
                f'https://discord.com/api/v9/guilds/{self.serverid}',
                headers=cl.headers
            )

            if r.status_code == 200:
                self.logger.succeded(f'{ctoken} Is in server')
                self.in_server.append(token)

            elif r.status_code == 403:
                self.logger.error(f'{ctoken} Not in server')
                self.not_in_server.append(token)

            elif 'retry_after' in r.text:
                limit = r.json().get('retry_after', 1.5)
                self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                time.sleep(float(limit))
                self.check(token, cl)

            elif 'Try again later' in r.text:
                self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                time.sleep(5)
                self.check(token, cl)

            elif 'Cloudflare' in r.text:
                self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                time.sleep(10)
                self.check(token, cl)
            
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
            func=self.check,
            tokens=files.gettokens(),
            delay=self.delay,
        )

        self.logger.log(f'Results: {len(self.in_server)} in server, {len(self.not_in_server)} not in server')
        
        if self.ui.input('Save results to files', bool):
            timestamp = dt.now().strftime('%Y-%m-%d--%H-%M-%S')
            os.makedirs('data\\server_check', exist_ok=True)
            
            with open(f'data\\server_check\\in_server_{timestamp}.txt', 'w') as f:
                f.write('\n'.join(self.in_server))
            
            with open(f'data\\server_check\\not_in_server_{timestamp}.txt', 'w') as f:
                f.write('\n'.join(self.not_in_server))
            
            self.logger.log('Results saved to data\\server_check\\')