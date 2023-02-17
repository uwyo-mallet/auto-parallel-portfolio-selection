import os
from pathlib import Path
import glob
import subprocess
import time

if __name__ == "__main__":
    os.chdir("job_files")
    solver_dir = os.getcwd()

    # get path to all job files
    directories = []
    for path in Path('.').rglob('*.sh'):
        directories.append(os.path.dirname(path))

    # get unique directories
    directories = set(directories)
    directories = list(directories)

    for job_dir in directories:
        os.chdir(job_dir)
        jobs = glob.glob('*.sh')
        #os.chdir(solver_dir)
        i = 0
        for job in jobs:
            i = i + 1
            subprocess.call(['sbatch', job])
            if i % 50 == 0:
                time.sleep(1)
        time.sleep(1)
        os.chdir(solver_dir)


