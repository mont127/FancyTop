import subprocess
import shutil
import sys

RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

class MainCLI():
    def __init__(self):
        self.processes = []

    def get_terminal_size(self):
        size = shutil.get_terminal_size()
        return size.columns, size.lines
    

    
    def get_top_processes(self):
        result = subprocess.run(['ps', '-arcxo', 'pid,command,time'], stdout=subprocess.PIPE)
        cols, size = self.get_terminal_size()
        lines = result.stdout.decode().split('\n')[1:size-3] 
        for line in lines:
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                continue
            pid, rest = parts
            name, _, time = rest.rpartition(' ')
            if name:
                self.processes.append((name.strip(), pid, time))


    def render(self, out):
        sys.stdout.write("\033[H" + "\033[K\n".join(out) + "\033[K\033[J")
        sys.stdout.flush()

    def display_processes(self):
        if not self.processes:
            self.render([f"{BOLD}Top Processes:{RESET}  {DIM}(none){RESET}"])
            return
        cols, lines = self.get_terminal_size()
        rank_w = max(3, len(str(len(self.processes))))
        pid_w = max(3, max(len(pid) for _, pid, _ in self.processes))
        time_w = 10
        name_w = max(20, cols - (8 + rank_w + pid_w + time_w))

        out = [
            f"{BOLD}Top Processes ({len(self.processes)}){RESET}",
            f"{BOLD}{YELLOW}  {'#':>{rank_w}}  {'PID':>{pid_w}}  {'PROCESS':<{name_w}}  {'TIME':>{time_w}}{RESET}",
            f"{DIM}  {'-' * rank_w}  {'-' * pid_w}  {'-' * name_w}  {'-' * time_w}{RESET}",
        ]
        for rank, (name, pid, time) in enumerate(self.processes, start=1):
            if len(name) > name_w:
                name = name[:name_w - 1] + "\u2026"
            out.append(f"  {DIM}{rank:>{rank_w}}{RESET}  {BLUE}{pid:>{pid_w}}{RESET}  "
                       f"{GREEN}{name:<{name_w}}{RESET}  {CYAN}{time:>{time_w}}{RESET}")
        self.render(out)


    def clear_processes(self):
        self.processes = []    

