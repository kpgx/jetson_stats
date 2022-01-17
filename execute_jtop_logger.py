import subprocess
import time

command = ["python3", "jtop_logger.py"]

while 1:
    time.sleep(1)
    print("(re)starting jtop_logger)")
    subprocess.run(command)
