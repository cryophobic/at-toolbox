import os

def display_welcome_message():
    """
    Displays a welcome message on the console.

    This function prints a formatted welcome message, enhancing the user experience at the start of the application.
    """
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

def clear_screen():
    """
    Clears the console screen.

    This function provides a way to clear the console screen to maintain a clean user interface. It's system independent, working on both Windows and Unix systems.
    """
    # For Windows
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Mac and Linux
        os.system('clear')