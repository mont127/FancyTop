import subprocess
import shutil
import sys
import os
import select


RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
CYAN   = "\033[36m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
REVERSE = "\033[7m"
RESET  = "\033[0m"
REFRESH_INTERVAL = 2


class MainCLI():
    def __init__(self):
        self.processes = []
        self.selected = 0
        self.offset = 0
        self.refresh_time = REFRESH_INTERVAL

    def get_terminal_size(self):
        size = shutil.get_terminal_size()
        return size.columns, size.lines

    def visible_rows(self):
        return max(1, self.get_terminal_size()[1] - 4)

    def get_top_processes(self):
        result = subprocess.run(['ps', '-arcxo', 'pid,command,time'], stdout=subprocess.PIPE)
        self.processes = []
        for line in result.stdout.decode().strip().split('\n')[1:]:
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                continue
            pid, rest = parts
            name, _, time = rest.rpartition(' ')
            if name:
                self.processes.append((name.strip(), pid, time))
        self.selected = min(self.selected, max(0, len(self.processes) - 1))


    def render(self, out):
        sys.stdout.write("\033[H" + "\033[K\n".join(out) + "\033[K\033[J")
        sys.stdout.flush()

    def display_processes(self):
        if not self.processes:
            self.render([f"{BOLD}Top Processes:{RESET}  {DIM}(none){RESET}"])
            return
        cols, lines = self.get_terminal_size()
        rows = self.visible_rows()
        self.offset = max(0, min(self.offset, len(self.processes) - rows))
        if self.selected < self.offset:
            self.offset = self.selected
        elif self.selected >= self.offset + rows:
            self.offset = self.selected - rows + 1
        visible = self.processes[self.offset:self.offset + rows]

        rank_w = max(3, len(str(self.offset + len(visible))))
        pid_w = max(3, max(len(pid) for _, pid, _ in visible))
        time_w = 10
        name_w = max(20, cols - (8 + rank_w + pid_w + time_w))

        out = [
            f"{BOLD}Top Processes ({len(self.processes)}){RESET}",
            f"{BOLD}{YELLOW}  {'#':>{rank_w}}  {'PID':>{pid_w}}  {'PROCESS':<{name_w}}  {'TIME':>{time_w}}{RESET} REFRESH TIME {self.refresh_time} ",
            f"{DIM}  {'-' * rank_w}  {'-' * pid_w}  {'-' * name_w}  {'-' * time_w}{RESET}",
        ]
        for i, (name, pid, time) in enumerate(visible):
            rank = self.offset + i + 1
            if len(name) > name_w:
                name = name[:name_w - 1] + "\u2026"
            if self.offset + i == self.selected:
                out.append(f"{REVERSE}{BOLD}  {rank:>{rank_w}}  {pid:>{pid_w}}  "
                           f"{name:<{name_w}}  {time:>{time_w}}{RESET}")
            else:
                out.append(f"  {DIM}{rank:>{rank_w}}{RESET}  {BLUE}{pid:>{pid_w}}{RESET}  "
                           f"{GREEN}{name:<{name_w}}{RESET}  {CYAN}{time:>{time_w}}{RESET}")
        self.render(out)

    def read_key(self, timeout):
        fd = sys.stdin.fileno()
        ready, _, _ = select.select([fd], [], [], timeout)
        if not ready:
            return None
        return os.read(fd, 3)

    def handle_key(self, key):
        if key in (b'\x1b[A', b'\x1bOA'):
            self.move_up()
        elif key in (b'\x1b[B', b'\x1bOB'):
            self.move_down()
        elif key in (b'\x1b[C', b'\x1bOC'):
            self.move_right()
        elif key in (b'\x1b[D', b'\x1bOD'):
            self.move_left()
        elif key == b' ':
            self.press_space()

    def move_up(self):
        if self.selected > 0:
            self.selected -= 1

    def move_down(self):
        if self.selected < len(self.processes) - 1:
            self.selected += 1

    def move_left(self):
        self.refresh_time = round(max(0.1, self.refresh_time + 0.1), 2)

    def move_right(self):
        self.refresh_time = round(max(0.1, self.refresh_time - 0.1), 2)

    def press_space(self):
        if self.selected < len(self.processes):
            pid = self.processes[self.selected][1]
            try:
                os.kill(int(pid), 9)
                print(f"{RED}Killed process {pid}{RESET}")
            except Exception as e:
                print(f"{RED}Failed to kill process {pid}: {e}{RESET}")

