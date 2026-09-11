from FancyTop import MainCLI
import sys
import termios
import time
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
        app.get_top_processes()
        next_refresh = time.monotonic() + app.refresh_time
        while True:
            app.display_processes()
            key = app.read_key(max(0, next_refresh - time.monotonic()))
            if key:
                app.handle_key(key)
            if time.monotonic() >= next_refresh:
                app.get_top_processes()
                next_refresh = time.monotonic() + app.refresh_time
    except KeyboardInterrupt:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_term)
        sys.stdout.write("\033[?25h\033[?1049l")
        sys.stdout.flush()
    print("Exiting FancyTop...")

if __name__ == "__main__":
    main()
