#installation_start_time=$(date +%s)

python3 -m venv func2_env
source func2_env/bin/activate
pip3 install pandas --no-cache
#installation_end_time=$(date +%s)
#
#function_start_time=$(date +%s)
#python3 func1.py
#function_end_time=$(date +%s)
#
#installation_time=$(expr $installation_end_time - $installation_start_time)
#function_execution_time=$(expr $function_end_time - $function_start_time)
#
#python3 create_trace.py func1 $installation_time func1_env/lib/ $function_execution_time


