from FancyTop import MainCLI
import sys
import termios
import tty

def main():
    print("Initializing FancyTop...")
    print("Initialization complete.")
    app = MainCLI()
    fd = sys.stdin.fileno()
    old_term = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    sys.stdout.write("\033[?1049h\033[?25l\033[2J")
    try:
        while True:
            app.clear_processes()
            app.get_top_processes()
            app.display_processes()
            key = app.read_key(0.3)
            if key:
                app.handle_key(key)
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()
    print("Exiting FancyTop...")
main()
