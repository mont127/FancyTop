from FancyTop import MainCLI
import subprocess
import time

def main():
    print("Initializing FancyTop...")
    print("Initialization complete.")
    app = MainCLI()
    while True:
        try:
            subprocess.run(['clear'])  
            app.get_top_processes()
            app.display_processes()
            app.clear_processes()
            time.sleep(2)  
        except KeyboardInterrupt:
            print("Exiting FancyTop...")
            break
main()