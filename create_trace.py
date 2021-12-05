import sys
import subprocess
import pandas as pd
import os


def append_to_trace(args):
    function_name = args[0]
    installation_time = args[1]
    dependency_size = args[2]
    function_execution_time = args[3]
    data = {"function_name": function_name,
            "installation_time": installation_time,
            "dependency_size_in_mb": dependency_size,
            "function_execution_time": function_execution_time}

    df = pd.DataFrame(columns=["function_name", "installation_time", "dependency_size_in_mb", "function_execution_time"])
    if os.path.exists("trace.csv"):
        df = pd.read_csv("trace.csv")

    df = df.append(data, ignore_index=True)
    df.to_csv("trace.csv", index=False)


if __name__ == "__main__":
    args = sys.argv[1:]

    append_to_trace(args)