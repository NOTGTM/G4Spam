from src import *
from src.util.logger import logger
from src.util.client import client
from src.util.ui import ui
from src.util.files import files

class usernamescraper:
    def __init__(self):
        self.module = 'Username Scraper'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.serverid = None
        self.scraped_usernames = set()

    def scrape(self):
        tokens = files.gettokens()
        if not tokens:
            self.logger.log('No tokens found')
            return

        for token in tokens:
            try:
                cl = client(token)
                ctoken = self.ui.cut(token, 20, '...')

                # Get guild members
                r = cl.sess.get(
                    f'https://discord.com/api/v9/guilds/{self.serverid}/members?limit=1000',
                    headers=cl.headers
                )

                if r.status_code == 200:
                    members = r.json()
                    for member in members:
                        user = member['user']
                        username = user.get('username', 'Unknown')
                        display_name = user.get('global_name', username)
                        self.scraped_usernames.add(f'{username}#{user.get("discriminator", "0000")} ({display_name})')
                    
                    self.logger.succeded(f'{ctoken} Scraped {len(members)} usernames')
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
        
        if self.scraped_usernames:
            timestamp = dt.now().strftime('%Y-%m-%d--%H-%M-%S')
            os.makedirs('data\\scraped', exist_ok=True)
            
            filename = f'data\\scraped\\usernames_{self.serverid}_{timestamp}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.scraped_usernames))
            
            self.logger.log(f'Scraped {len(self.scraped_usernames)} unique usernames')
            self.logger.log(f'Saved to {filename}')
        else:
            self.logger.log('No usernames scraped')