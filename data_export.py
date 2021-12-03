import pandas as pd
import sys
import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse
import bz2

from benchmark.datasets import DATASETS
from benchmark.plotting.utils  import compute_metrics_all_runs
from benchmark.results import load_all_results, get_unique_algorithms

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--output',
        help='Path to the output csv file',
        required=True)
    parser.add_argument(
        '--recompute',
        action='store_true',
        help='Path to the output csv file')
    parser.add_argument(
        '--private-query',
        help='Use the private queries and ground truth',
        action='store_true')
    args = parser.parse_args()

    datasets = DATASETS.keys()
    dfs = []

    is_first = True
    for dataset_name in datasets:
        print("Looking at dataset", dataset_name)
        dataset = DATASETS[dataset_name]()
        results = load_all_results(dataset_name)
        results = compute_metrics_all_runs(dataset, results, args.recompute)
        cleaned = []
        for result in results:
            if 'k-nn' in result:
                result['recall/ap'] = result['k-nn']
                del result['k-nn']
            if 'ap' in result:
                result['recall/ap'] = result['ap']
                del result['ap']
            cleaned.append(result)
        dfs.append(pd.DataFrame(cleaned))
    if len(dfs) > 0:
        data = pd.concat(dfs)
        data.to_csv(args.output, index=False)

