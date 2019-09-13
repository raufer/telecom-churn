import os
import argparse
import subprocess

import numpy as np


def main(args):

    print("Calculating hash for data...")
    import random
    hash = random.getrandbits(128)
    print("hash value: %032x" % hash)
    print("Uploading data to repository")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepared-data-location', type=str, help='PLACEHOLDER', default='s3://manticore-data/churn/prepared/')
    parser.add_argument('--data-repository', type=str, help='PLACEHOLDER', default='product-recommendation')

    args = parser.parse_args()
    print(args)

    main(args)


