import subprocess 

class MainCLI():
    def __init__(self):
        self.processes = []
    
    def get_top_processes(self):
        result = subprocess.run(['ps', '-arcxo', 'pid,command,time'], stdout=subprocess.PIPE)
        lines = result.stdout.decode().split('\n')[1:12]
        for line in lines:
            parts = line.strip().split(maxsplit=1)
            if len(parts) == 2:
                pid, name = parts
                self.processes.append((name, pid))


    def display_processes(self):
        if not self.processes:
            print("Top Processes:  (none)")
            return

        rank_w = len(str(len(self.processes)))
        pid_w = max(3, max(len(pid) for _, pid in self.processes))
        name_w = 50

        print(f"Top Processes ({len(self.processes)})")
        print(f"  {'#':>{rank_w}}  {'PID':>{pid_w}}  {'PROCESS':<{name_w}}")
        print(f"  {'-' * rank_w}  {'-' * pid_w}  {'-' * name_w}")
        for rank, (name, pid) in enumerate(self.processes, start=1):
            if len(name) > name_w:
                name = name[:name_w - 1] + "\u2026"
            print(f"  {rank:>{rank_w}}  {pid:>{pid_w}}  {name}")


    def clear_processes(self):
        self.processes = []    

