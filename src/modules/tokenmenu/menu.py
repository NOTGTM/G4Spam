# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui

from src.modules.tokenmenu.checker import checker
from src.modules.tokenmenu.formatter import formatter
from src.modules.tokenmenu.biochanger import biochanger
from src.modules.tokenmenu.avatarchanger import avatarchanger
from src.modules.tokenmenu.clantagchanger import clantagchanger
from src.modules.tokenmenu.logonbrowser import logonbrowser

class tokenmenu:
    def __init__(self):
        self.module = 'Token Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        options = {
            'Checker (FREE)': checker().menu,
            'Bio Changer': biochanger().menu,
            'Avatar Changer': avatarchanger().menu,
            'Clan Tag Changer': clantagchanger().menu,
            'Log On Browser': logonbrowser().menu,
            'Formatter (FREE)': formatter().menu
        }
        
        while True:
            self.ui.optionmenu(options)
            choice = self.ui.input('Option', int) - 1
            keys = list(options.keys())
            
            if choice == len(keys):
                return
            
            elif choice < len(keys):
                options[keys[choice]]()
                break
            
            else:
                self.logger.log('Invalid option')
                input('')