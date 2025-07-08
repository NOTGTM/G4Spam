from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.files import files

class invitescraper:
    def __init__(self):
        self.module = 'Invite Scraper'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.scraped_invites = set()

    def scrape(self):
        tokens = files.gettokens()
        if not tokens:
            self.logger.log('No tokens found')
            return

        for token in tokens:
            try:
                cl = client(token)
                ctoken = self.ui.cut(token, 20, '...')

                # Get guild invites
                r = cl.sess.get(
                    f'https://discord.com/api/v9/guilds/{self.serverid}/invites',
                    headers=cl.headers
                )

                if r.status_code == 200:
                    invites = r.json()
                    for invite in invites:
                        invite_code = invite.get('code')
                        if invite_code:
                            invite_url = f'https://discord.gg/{invite_code}'
                            self.scraped_invites.add(invite_url)
                    
                    self.logger.succeded(f'{ctoken} Scraped {len(invites)} invites')
                    break  # Success, no need to try other tokens

                elif 'retry_after' in r.text:
                    limit = r.json().get('retry_after', 1.5)
                    self.logger.ratelimited(f'{ctoken} Rate limited', limit)
                    time.sleep(float(limit))

                elif 'Try again later' in r.text:
                    self.logger.ratelimited(f'{ctoken} Rate limited', 5)
                    time.sleep(5)

                elif 'Cloudflare' in r.text:
                    self.logger.cloudflared(f'{ctoken} Cloudflare rate limited', 10)
                    time.sleep(10)
                
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
        
        self.scrape()
        
        if self.scraped_invites:
            timestamp = dt.now().strftime('%Y-%m-%d--%H-%M-%S')
            os.makedirs('data\\scraped', exist_ok=True)
            
            filename = f'data\\scraped\\invites_{self.serverid}_{timestamp}.txt'
            with open(filename, 'w') as f:
                f.write('\n'.join(self.scraped_invites))
            
            self.logger.log(f'Scraped {len(self.scraped_invites)} unique invites')
            self.logger.log(f'Saved to {filename}')
        else:
            self.logger.log('No invites scraped')