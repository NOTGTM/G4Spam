# This code is the property of R3CI.
# Unauthorized copying, distribution, or use is prohibited.
# Licensed under the GNU General Public License v3.0 (GPL-3.0).
# For more details, visit https://github.com/R3CI/G4Spam

from src import *
from src.util.ui import ui

class sources:
    def menu():
        module = 'Sources'
        sui = ui(module)
        sui.prep()
        sui.createmenu([
            'G4Spam PAID',
            'Lime SOURCE',
            'Private raiders',
            'Proxies',
            'Tokens',
            'Solvers',
            'Back'
        ])
        chosen = sui.input('Option', str)

        if chosen == '1': 
            webbrowser.open('https://r3ci.sell.app')

        elif chosen == '2':
            webbrowser.open('https://r3ci.sell.app')

        elif chosen == '3':
            webbrowser.open('https://r3ci.sell.app')

        elif chosen == '4':
            sui.createmenu([
                'IPRoyal',
                'Mars proxies',
                'Tokenu proxies',
                'Back'
            ])
            chosen = sui.input('Option', str)

            if chosen == '1':   webbrowser.open('https://iproyal.com/?r=429481')
            elif chosen == '2': webbrowser.open('https://marsproxies.com/r/97040')
            elif chosen == '3': webbrowser.open('https://proxy.tokenu.to/pricing?ref=r3ci')
            else:               sources.menu()

        elif chosen == '5':
            sui.createmenu([
                'My shop (UHQ + AGE GARAUNTEED)',
                'Tokenu',
                'Back'
            ])
            chosen = sui.input('Option', str)

            if chosen == '1':   webbrowser.open('https://r3ci.sell.app')
            elif chosen == '2': webbrowser.open('https://www.tokenu.net?ref=r3ci')
            else:               sources.menu()

        elif chosen == '6':
            sui.createmenu([
                'Soon'
            ])

        elif chosen == '7':
            return

        else:
            sources.menu()