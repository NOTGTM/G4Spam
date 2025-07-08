# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.logger import logger
from src.util.ui import ui
from src.modules.vcmenu.vcjoiner import vcjoiner
from src.modules.vcmenu.vcspamjoinleave import vcspamjoinleave
from src.modules.vcmenu.soundboardspammer import soundboardspammer

class vcmenu:
    def __init__(self):
        self.module = 'VC Menu'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        options = {
            'VC Joiner': vcjoiner().menu,
            'VC Spam Join-Leave': vcspamjoinleave().menu,
            'Soundboard Spammer': soundboardspammer().menu,
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