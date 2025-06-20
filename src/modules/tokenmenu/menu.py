# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui

from src.modules.tokenmenu.checker import checker
from src.modules.tokenmenu.formatter import formatter

class tokenmenu:
    def __init__(self):
        self.module = 'Token Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        self.ui.createmenu([
            'Checker',
            'Formatter',
            'Back'
        ])
        chosen = self.ui.input('Option')

        if chosen == '1':
            checker().menu()

        elif chosen == '2':
            formatter().menu()

        elif chosen == '3':
            return
        
        else:
            self.menu()