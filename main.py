from FancyTop import MainCLI
import sys
import time

def main():
    print("Initializing FancyTop...")
    print("Initialization complete.")
    app = MainCLI()
    sys.stdout.write("\033[?1049h\033[?25l\033[2J")
    try:
        while True:
            app.get_top_processes()
            app.display_processes()
            app.clear_processes()
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()
    print("Exiting FancyTop...")
main()
