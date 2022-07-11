import os
from os.path import join
from pathlib import Path
from re import findall

import pandas
BENCHMARKS_PATH = join(os.path.dirname(__file__), '..', 'pddl_files')
RESULTS_CSV = join(os.path.dirname(__file__), '..', 'tmp_results.csv')

def get_log_files_from_path(path: str):
    log_files_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.log'):
                path_to_log_file = os.path.join(root, file)
                # print(path_to_log_file)
                log_files_list.append(path_to_log_file)
    return log_files_list

def read_results(log_files_list):
    df = pandas.DataFrame()
    for i, log_file_path in enumerate(log_files_list):
        df.loc[i, 'log_file_path'] = log_file_path
        with open(log_file_path) as f:
            output = [line.rstrip() for line in f]
        results = []
        for l in output:
            l = l.split('|')[-1].strip()
            results.extend(findall("[^ ]+::[^ ]+", l))
        for res in results:
            k, v = res.split('::')
            df.loc[i, k] = v
    return df


if __name__ == '__main__':
    log_files_list = get_log_files_from_path(BENCHMARKS_PATH)
    df = read_results(log_files_list)
    df.to_csv(RESULTS_CSV, index=False)