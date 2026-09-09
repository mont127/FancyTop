import subprocess 
import shutil

class MainCLI():
    def __init__(self):
        self.processes = []
    
    def get_top_processes(self):
        result = subprocess.run(['ps', '-arcxo', 'pid,command,time'], stdout=subprocess.PIPE)
        lines = result.stdout.decode().split('\n')[1:15]
        for line in lines:
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2:
                continue
            pid, rest = parts
            name, _, time = rest.rpartition(' ')
            if name:
                self.processes.append((name.strip(), pid, time))

    def get_terminal_size(self):
        size = shutil.get_terminal_size()
        return size.columns, size.lines

    def display_processes(self):
        if not self.processes:
            print("Top Processes:  (none)")
            return
        cols, lines = self.get_terminal_size()
        rank_w = max(3, len(str(len(self.processes))))
        pid_w = max(3, max(len(pid) for _, pid, _ in self.processes))
        time_w = 10
        name_w = max(20, cols - (8 + rank_w + pid_w + time_w))
        
        print(f"Top Processes ({len(self.processes)})")
        print(f"  {'#':>{rank_w}}  {'PID':>{pid_w}}  {'PROCESS':<{name_w}}  {'TIME':>{time_w}}")
        print(f"  {'-' * rank_w}  {'-' * pid_w}  {'-' * name_w}  {'-' * time_w}")
        for rank, (name, pid, time) in enumerate(self.processes, start=1):
            if len(name) > name_w:
                name = name[:name_w - 1] + "\u2026"
            print(f"  {rank:>{rank_w}}  {pid:>{pid_w}}  {name:<{name_w}}  {time:>{time_w}}")


    def clear_processes(self):
        self.processes = []    

