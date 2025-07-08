from src import *
from src.util.logger import logger
from src.util.ui import ui

class funnystuff:
    def __init__(self):
        self.module = 'Funny Stuff'
        self.logger = logger(self.module)
        self.ui = ui(self.module)

    def menu(self):
        self.ui.prep()
        
        options = {
            'ASCII Art Generator': self.ascii_art,
            'Random Joke': self.random_joke,
            'Discord Status Generator': self.status_generator,
            'Fake Loading Screen': self.fake_loading,
            'Random Quote': self.random_quote
        }
        
        self.ui.createmenu(list(options.keys()) + ['Back'])
        choice = self.ui.input('Option', int) - 1
        keys = list(options.keys())
        
        if choice == len(keys):
            return
        elif choice < len(keys):
            options[keys[choice]]()
        else:
            self.logger.log('Invalid option')

    def ascii_art(self):
        text = self.ui.input('Text to convert to ASCII art', str)
        
        # Simple ASCII art generator
        ascii_chars = {
            'A': ['  █  ', ' █ █ ', '█████', '█   █', '█   █'],
            'B': ['████ ', '█   █', '████ ', '█   █', '████ '],
            'C': [' ████', '█    ', '█    ', '█    ', ' ████'],
            'D': ['████ ', '█   █', '█   █', '█   █', '████ '],
            'E': ['█████', '█    ', '███  ', '█    ', '█████'],
            ' ': ['     ', '     ', '     ', '     ', '     ']
        }
        
        text = text.upper()[:10]  # Limit length
        
        for row in range(5):
            line = ''
            for char in text:
                if char in ascii_chars:
                    line += ascii_chars[char][row] + ' '
                else:
                    line += ascii_chars[' '][row] + ' '
            print(line)
        
        input('Press Enter to continue...')

    def random_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why don't skeletons fight each other? They don't have the guts!",
            "What's orange and sounds like a parrot? A carrot!"
        ]
        
        joke = random.choice(jokes)
        self.logger.log(f'Random Joke: {joke}')
        input('Press Enter to continue...')

    def status_generator(self):
        activities = ['Playing', 'Watching', 'Listening to', 'Competing in']
        things = [
            'with fire', 'Discord', 'the void', 'my feelings', 'hide and seek',
            'Netflix', 'YouTube', 'the news', 'paint dry', 'grass grow',
            'music', 'the rain', 'silence', 'my heartbeat', 'nature sounds',
            'life', 'chess', 'video games', 'sports', 'cooking'
        ]
        
        activity = random.choice(activities)
        thing = random.choice(things)
        status = f'{activity} {thing}'
        
        self.logger.log(f'Random Status: {status}')
        input('Press Enter to continue...')

    def fake_loading(self):
        self.logger.log('Initializing fake loading screen...')
        
        tasks = [
            'Loading Discord API...',
            'Connecting to servers...',
            'Authenticating tokens...',
            'Bypassing rate limits...',
            'Downloading more RAM...',
            'Hacking the mainframe...',
            'Reversing the polarity...',
            'Calibrating flux capacitor...',
            'Initializing quantum processors...',
            'Finalizing setup...'
        ]
        
        for i, task in enumerate(tasks):
            print(f'[{i+1}/10] {task}')
            time.sleep(random.uniform(0.5, 2.0))
            
        self.logger.log('Loading complete! (Just kidding)')
        input('Press Enter to continue...')

    def random_quote(self):
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "It is during our darkest moments that we must focus to see the light. - Aristotle",
            "The only impossible journey is the one you never begin. - Tony Robbins",
            "In the end, we will remember not the words of our enemies, but the silence of our friends. - Martin Luther King Jr.",
            "The way to get started is to quit talking and begin doing. - Walt Disney",
            "Don't let yesterday take up too much of today. - Will Rogers"
        ]
        
        quote = random.choice(quotes)
        self.logger.log(f'Random Quote: {quote}')
        input('Press Enter to continue...')