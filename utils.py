import os

def display_welcome_message():
    print("""
+---------------------------------------------+
|🚀  SUPERCHARGE YOUR AIRTABLE EXPERIENCE!  🚀|
+---------------------------------------------+
|                                             |
| Tired of endless clicking for new bases?    |
| Drowning in menus for simple data uploads?  |
|                                             |
|   _    ___ ____ _____  _    ____  _     _____ 
|  / \  |_ _|  _ \_   _|/ \  | __ )| |   | ____|
| / _ \  | || |_) || | / _ \ |  _ \| |   |  _||  
|/ ___ \ | ||  _ < | |/ ___ \| |_) | |___| |__| 
/_/   \_\___|_| \_\|_/_/   \_\____/|_____|_____|
|                                             |
| • Base creation in a flash!                 |
| • Tailored table setups, no sweat!          |
| • CSV data uploads? Consider it done!       |
|                                             |
| Ditch the manual. => Embrace automation!    |
|                                             |  
| Even more at https://learnwith.cc           |
+---------------------------------------------+
""")

""" Clears the console screen, works for Windows, Mac, and Linux. """
def clear_screen():
    # For Windows
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Mac and Linux
        os.system('clear')