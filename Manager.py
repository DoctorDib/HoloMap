import subprocess
import time
import os
import threading
import sys

class SimplePM2:
    def __init__(self):
        self.processes = {}

    def start(self, name, command, cwd=None):
        """Start a new process in a specific directory and keep track of it."""
        print(f'Starting {name}...')
        command_str = ' '.join(command)  # Join the command list into a single string
        print(f'Executing command: {command_str} in {cwd}')  # Log the command
        process = subprocess.Popen(command_str, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, shell=True)
        self.processes[name] = process
        self.monitor_process_output(process, name)

    def monitor_process_output(self, process, name):
        """Monitor the output and error of the process."""
        def output_reader():
            for line in iter(process.stdout.readline, b''):
                print(f'{name}: {line.decode().strip()}')
            process.stdout.close()

        def log_reader():
            for line in iter(process.stderr.readline, b''):
                print(f'{name} log: {line.decode().strip()}')
            process.stderr.close()

        # Start threads to read output and error streams
        threading.Thread(target=output_reader, daemon=True).start()
        threading.Thread(target=log_reader, daemon=True).start()

    def monitor(self):
        """Monitor running processes and restart if necessary."""
        while True:
            for name, process in list(self.processes.items()):
                if process.poll() is not None:  # Check if the process has terminated
                    print(f'{name} has stopped. Restarting...')
                    self.start(name, process.args, cwd=os.path.dirname(process.args[0]))  # Restart the process
            time.sleep(1)  # Poll every second

    def stop(self, name):
        """Stop a specific process."""
        if name in self.processes:
            print(f'Stopping {name}...')
            self.processes[name].terminate()
            self.processes[name].wait()  # Wait for the process to terminate
            del self.processes[name]

    def stop_all(self):
        """Stop all managed processes."""
        for name in list(self.processes.keys()):
            self.stop(name)

if __name__ == '__main__':
    pm2 = SimplePM2()
    
    count = len(sys.argv)
    if (count > 1):
        match(sys.argv[1]):
            case "PC_DEV":
                # FOR LOCAL DEVELOPMENT
                pm2.start('client_app', ['npm', 'run', 'start'], cwd='client')
                pm2.start('debugger_app', ['npm', 'run', 'start'], cwd='debugger')
                pm2.start('app', ['poetry', 'run', 'python', 'app.py'])
            case "HOLOMAP_DEV":
                # FOR HOLOMAP
                pm2.start('client_app1', ['npm', 'run', 'start'], cwd='client')
                pm2.start('client_app2', ['npm', 'run', 'electron:start'], cwd='client')
                pm2.start('debugger_app', ['npm', 'run', 'start'], cwd='debugger')
                pm2.start('app', ['poetry', 'run', 'python', 'app.py'])
            case "PC_DEV_CLIENTS":
                # FOR LOCAL DEVELOPMENT (ONLY CLIENTS)
                pm2.start('client_app1', ['npm', 'run', 'start'], cwd='client')
                pm2.start('debugger_app', ['npm', 'run', 'start'], cwd='debugger')
            case "TEST":
                pm2.start('client_app', ['npm', 'run', 'electron:start'], cwd='client')
            case _:
                # TODO - Add production here
                pass

    try:
        pm2.monitor()
    except KeyboardInterrupt:
        print('Stopping all processes...')
        pm2.stop_all()
