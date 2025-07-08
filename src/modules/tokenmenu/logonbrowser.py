# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui
from src.util.files import files

class logonbrowser:
    def __init__(self):
        self.module = 'Log On Browser'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        
        tokens = files.gettokens()
        if not tokens:
            self.logger.log('No tokens found')
            return

        self.ui.createmenu([f'Token {i+1}: {self.ui.cut(token, 30, "...")}' for i, token in enumerate(tokens)])
        
        try:
            choice = self.ui.input('Select token to log in with', int) - 1
            if 0 <= choice < len(tokens):
                token = tokens[choice]
                
                # Create Discord login URL with token
                login_url = f'https://discord.com/login'
                
                self.logger.log(f'Opening browser for token: {self.ui.cut(token, 30, "...")}')
                self.logger.log('You will need to manually enter the token in browser console:')
                self.logger.log('1. Press F12 to open developer tools')
                self.logger.log('2. Go to Console tab')
                self.logger.log('3. Paste this code:')
                self.logger.log(f'setToken("{token}")')
                self.logger.log('4. Press Enter')
                
                webbrowser.open(login_url)
                
                # Also save token to clipboard if possible
                try:
                    import pyperclip
                    pyperclip.copy(f'setToken("{token}")')
                    self.logger.log('Login code copied to clipboard!')
                except:
                    pass
                    
            else:
                self.logger.log('Invalid selection')
                
        except Exception as e:
            self.logger.error('Failed to process selection', e)