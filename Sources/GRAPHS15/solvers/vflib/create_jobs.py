import sys
import os
from shutil import copyfile

if __name__ == "__main__":
    # get all instance names
    with open("/gscratch/dpulatov/GRAPHS2015/instances/instances_gscratch.txt") as file:
        files = file.readlines()

    files = list(map(lambda x: x.split(" "), files))
    files = list(map(lambda x: x[0:3], files))
    files = list(map(lambda x: [x[0], x[1].replace("/gscratch/dpulatov/GRAPHS2015/instances/", ""), x[2].replace("/gscratch/dpulatov/GRAPHS2015/instances/", "")], files))

    base_dir = os.getcwd()
    solver = os.path.basename(base_dir)
    os.makedirs("./job_files")
    os.chdir("./job_files")
    print(os.getcwd())

    paths = {}
    instances = [] 
    for file in files:
        directory = os.path.dirname(file[1])
        if directory not in paths:
            paths[directory] = []
        paths[directory].append([file[0], file[1], file[2]])

    # create directories
    for path in paths:
        if os.path.isdir(path):
            os.chdir(path)
        else:
            os.makedirs(path)
            os.chdir(path)
            # create error and output
            os.makedirs("./error")
            os.makedirs("./output")

        # create job files
        for inst in paths[path]:
            cwd = os.getcwd()
            job_file = "job_" + solver + "_" + inst[0] 
            job_file = job_file.strip()
            job_file = job_file + ".sh"
            copyfile("/gscratch/dpulatov/GRAPHS2015/solvers/template.sh", os.path.join(cwd, job_file))
            with open(job_file, "a") as file:
                file.write('#SBATCH -o /dev/null\n')
                file.write('#SBATCH -e ./error/%s_%s.err\n' % (solver, inst[0]))
                inst_path_pattern = os.path.join("/gscratch/dpulatov/GRAPHS2015/instances", inst[1])
                inst_path_target = os.path.join("/gscratch/dpulatov/GRAPHS2015/instances", inst[2])
                file.write("srun /usr/bin/time -f %%e %s/solve_vf %s %s 100000" % (base_dir, inst_path_pattern, inst_path_target)) 
        os.chdir(os.path.join(base_dir, "job_files"))
