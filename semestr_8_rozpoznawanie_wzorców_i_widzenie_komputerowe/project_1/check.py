# -*- coding: utf-8 -*-

import os
import subprocess
import time

import numpy as np


def run(popenargs):
    with subprocess.Popen(popenargs, stdout=subprocess.PIPE) as process:
        try:
            output, unused_err = process.communicate()
        except subprocess.TimeoutExpired:
            process.kill()
            output, unused_err = process.communicate()
        except:
            process.kill()
            process.wait()
            raise
        retcode = process.poll()
        return output.decode("utf-8").splitlines()


def checkDir(commanddir, path, N):
    with open(os.path.join(path, 'correct.txt'), 'rt') as f:
        correct = f.read().splitlines()

    cmd = ['./run.sh', path, str(N)]
    cwd = os.getcwd()
    os.chdir(commanddir)
    start = time.time()
    output = run(cmd)
    stop = time.time()
    os.chdir(cwd)

    size = 6
    result = np.zeros(size, dtype=int)

    if len(output) != len(correct):
        return result, stop - start;

    for line, c in zip(output, correct):
        line = line.split()
        try:
            idx = line.index(c)
        except:
            idx = N - 1
        if idx < size - 1:
            result[idx] += 1
        result[-1] += 1.0 / (1.0 + idx)

    return result, stop - start;

def percent(fraction):
    return "{:5.1f}%".format(100 * fraction)

def format_array(array):
    return '[' + ' '.join("{:3d}".format(val) for val in array) + ']'

if __name__ == "__main__":
    programdir_path = os.path.abspath('.')
    data_path = os.path.abspath('data')

    program_path = os.path.join(programdir_path, 'run.sh')
    os.chmod(program_path, os.stat(program_path).st_mode | 0o100)  # stat.S_IEXEC)

    dirs = [('set0', 6),
            ('set1', 20),
            ('set2', 20),
            ('set3', 20),
            ('set4', 20),
            ('set5', 200),
            ('set6', 200),
            ('set7', 20),
            ('set8', 100)]

    total = []
    times = []
    for d in dirs:
        res, t = checkDir(programdir_path, os.path.join(data_path, d[0]), d[1])
        total.append(res)
        times.append(t)
        print(d[0], '=', format_array(res[:-1]), 'score =', percent(res[-1] / d[1]), "[%dsec]" % t)

    print('-' * 50)
    total_count = sum(count for _, count in dirs)
    summary = np.array(total).sum(axis=0)
    print('total ', format_array(summary[:-1]), 'score =', percent(summary[-1] / total_count), "[%dsec]" % sum(times))
