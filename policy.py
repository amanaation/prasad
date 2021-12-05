import multiprocessing
import time
import subprocess
import pandas as pd
import os
import shutil
import importlib
from create_trace import append_to_trace


class Policy:
    def __init__(self):
        self.running_functions = []
        self.keep_alive = []
        self.memory_occupied = 0

    def trigger(self, file_name):
        function_name = file_name.split(".")[0]
        if function_name not in self.running_functions:
            self.running_functions.append(function_name)
            self.keep_alive.append(function_name)
            dependency_installation_time = self.install_dependency(function_name)
            dependency_size = self.get_memory_occupied(function_name)
            self.memory_occupied += dependency_size

            function_start_time = time.time()
            importlib.import_module(f"python_files.{function_name}", package=None)
            print("Triggered : ", function_name)
            function_end_time = time.time()
            function_execution_time = function_end_time - function_start_time

            self.running_functions.remove(function_name)

            print("function name : ", function_name)
            print("function execution name : ", function_execution_time)
            print("dependency size : ", dependency_size)
            print("dependency installation time : ", dependency_installation_time)
            append_to_trace([function_name, dependency_installation_time, dependency_size, function_execution_time])

        else:
            print(f"Function {function_name} is already running!!!")
        print("Functions : ", self.running_functions, self.keep_alive)

    def evict(self, function_name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        env_path = dir_path + f"/{function_name}_env/"
        if os.path.exists(env_path):
            shutil.rmtree(env_path)
        self.memory_occupied -= self.get_memory_occupied(function_name, env_path)
        self.keep_alive.remove(function_name)

    def get_memory_occupied(self, function_name, env_path=None):
        if not env_path:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            env_path = dir_path + f"/{function_name}_env/"
        dependency_size = subprocess.check_output(['du', '-sh', env_path]).split()[0].decode('utf-8')
        unit = dependency_size[-1]
        dependency_size = float(dependency_size[:-1])
        return dependency_size

    def monitor(self):
        while self.running_functions:
            print("Running Functions : ", self.running_functions)
            time.sleep(10)

    def policy(self):
        pass

    def install_dependency(self, function_name):
        s = time.time()
        subprocess.call(['sh', f'sh_files/{function_name}.sh'])
        print("Completed Installing dependency")
        return time.time() - s


if __name__ == "__main__":
    #"""
    policy = Policy()
    processes = []
    for i in range(1, 4):
        print(f" Starting Function : function {i}", )
        process = multiprocessing.Process(target=policy.trigger, args=(f"func{i}.sh",))
        process.start()
        process.join()
    p3 = multiprocessing.Process(target=policy.monitor)

    # both processes finished
    print("Done!")
    #"""



