import os
import argparse
import subprocess

import numpy as np


def main(args):

    print("Uploading model to repository")
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-repository', type=str, help='PLACEHOLDER', default='product-recommendation')

    args = parser.parse_args()
    print(args)

    main(args)


