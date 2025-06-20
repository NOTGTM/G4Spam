# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui

class nukingmenu:
    def __init__(self):
        self.module = 'Nuking Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'Will be added later as this is the least important menu and the least used',
            'Back'
        ])
        chosen = self.ui.input('Option')

        if chosen == '1':
            self.menu()

        elif chosen == '2':
            return
        
        else:
            self.menu()