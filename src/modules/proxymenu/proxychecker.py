from src import *
from src.util.logger import logger
from src.util.ui import ui
from src.util.files import files
import concurrent.futures

class proxychecker:
    def __init__(self):
        self.module = 'Proxy Checker'
        self.logger = logger(self.module)
        self.ui = ui(self.module)
        self.working = []
        self.failed = []

    def check_proxy(self, proxy):
        try:
            # Parse proxy format: user:pass@host:port
            if '@' in proxy:
                auth, address = proxy.split('@')
                username, password = auth.split(':')
                host, port = address.split(':')
                proxy_dict = {
                    'http': f'http://{username}:{password}@{host}:{port}',
                    'https': f'http://{username}:{password}@{host}:{port}'
                }
            else:
                # host:port format
                host, port = proxy.split(':')
                proxy_dict = {
                    'http': f'http://{host}:{port}',
                    'https': f'http://{host}:{port}'
                }

            # Test proxy with a simple request
            response = requests.get(
                'https://httpbin.org/ip',
                proxies=proxy_dict,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.succeded(f'Working: {proxy}')
                self.working.append(proxy)
            else:
                self.logger.error(f'Failed: {proxy}')
                self.failed.append(proxy)
                
        except Exception as e:
            self.logger.error(f'Failed: {proxy}')
            self.failed.append(proxy)

    def menu(self):
        self.ui.prep()
        
        proxies = files.getproxies()
        if not proxies:
            self.logger.log('No proxies found in data\\proxies.txt')
            return

        self.logger.log(f'Checking {len(proxies)} proxies...')
        
        # Use ThreadPoolExecutor for concurrent checking
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(self.check_proxy, proxies)

        self.logger.log(f'Results: {len(self.working)} working, {len(self.failed)} failed')
        
        if self.working and self.ui.input('Replace proxies.txt with only working proxies', bool):
            with open('data\\proxies.txt', 'w') as f:
                f.write('\n'.join(self.working))
            self.logger.log('Updated proxies.txt with working proxies')

        # Save detailed results
        timestamp = dt.now().strftime('%Y-%m-%d--%H-%M-%S')
        os.makedirs('data\\proxy_check', exist_ok=True)
        
        with open(f'data\\proxy_check\\working_{timestamp}.txt', 'w') as f:
            f.write('\n'.join(self.working))
        
        with open(f'data\\proxy_check\\failed_{timestamp}.txt', 'w') as f:
            f.write('\n'.join(self.failed))
        
        self.logger.log(f'Detailed results saved to data\\proxy_check\\')