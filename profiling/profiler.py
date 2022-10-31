#!/usr/bin/python

import argparse
import logging
import os
import subprocess

logging.basicConfig(level=os.environ.get("LOG_LEVEL", logging.INFO))
__logger = logging.getLogger(__name__)


OUTPUT_BASE_PATH = "profiling/output"
OUTPUT_STATS_PATH = f"{OUTPUT_BASE_PATH}/output.pstats"
OUTPUT_GRAPH_PATH = f"{OUTPUT_BASE_PATH}/graph.png"

parser = argparse.ArgumentParser(
    prog="Enigma Machine Profiler",
    description=(
        "It measures the time spent within functions and the number of calls made to them using cProfile profiler."
        "In addition, it generates a visualisation of the profiling output with gprof2dot."
    ),
    epilog='Text at the bottom of help'
)

parser.add_argument('-o', '--output-dir', default=OUTPUT_BASE_PATH, help="Desired output directory")
parser.add_argument('-s', '--stats-filename', default="stats.pstats", help="cProfile stats filename")
parser.add_argument('-g', '--graph-filename', default="graph.png", help="Graph stats filename")
parser.add_argument('-t', '--profiling-target', default="profiling/profiling_target.py")
args = parser.parse_args()

# makes sure the path does not end with a slash
args.output_dir = args.output_dir.rstrip("/")


def install():
    """

    :return:
    """
    __logger.info("installing necessary packages: graphviz, gprof2dot")
    proc = subprocess.run(
        ["pip", "install", "graphviz", "gprof2dot"],
        capture_output=True,
    )
    __check_subprocess_out(proc, "Unable to install required packages.")


def prepare():
    __logger.info(f"making sure {args.output_dir} exists")
    proc = subprocess.run(f"mkdir {args.output_dir}", shell=True, capture_output=True)
    if proc.returncode == 1:
        __logger.info(f"WARNING: {proc.stderr}")


def measure():
    __logger.info(f"running cProfile on {args.profiling_target}")
    print(f"python -m cProfile -o {args.output_dir}/{args.stats_filename} {args.profiling_target}")
    proc = subprocess.run(
        f"python -m cProfile -o {args.output_dir}/{args.stats_filename} {args.profiling_target}",
        shell=True,
        capture_output=True,
    )
    __check_subprocess_out(proc, "Unable to measure file.")
    __logger.info(f"pstats file stored at {args.output_dir}/{args.stats_filename}")


def generate_visualisation():
    __logger.info(f"generating visualisation")
    proc = subprocess.run(
        f"gprof2dot --colour-nodes-by-selftime -f pstats {args.output_dir}/{args.stats_filename} | dot -Tpng -o {args.output_dir}/{args.graph_filename}",
        shell=True,
        capture_output=True,
    )
    print(proc)
    __check_subprocess_out(proc, "Unable to generate visualisation.")
    __logger.info(f"graph file stored at {args.output_dir}/{args.graph_filename}")


def __check_subprocess_out(proc: subprocess.CompletedProcess, message: str):
    if proc.returncode == 1:
        __logger.error(f"ERROR: {message} {str(proc.stdout)}")
        exit(proc.returncode)


if __name__ == '__main__':
    install()
    prepare()
    measure()
    generate_visualisation()

