import argparse
import os
import pathlib
import time
from collections import defaultdict
from typing import List, Dict

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from AlignFive.game.align_five import AlignFive
from AlignFive.players.smart_player import SmartPlayer
from AlignFive.utils import Color


def add_slots(original_array: np.ndarray, number_of_slots_to_add: int) -> np.ndarray:
    modified_array = original_array.copy()

    modified_array = modified_array.flatten()
    modified_array[:number_of_slots_to_add] = 0
    return modified_array.reshape((19, 19))

def plot_results(data_per_slot: Dict[int, Dict[str, List[float]]]):
    data_per_worker = {number_of_workers: defaultdict(list) for number_of_workers in list(data_per_slot.values())[0]["number_of_workers"]}

    for number_of_workers in list(data_per_slot.values())[0]["number_of_workers"]:
        for number_of_slots, data in data_per_slot.items():
            data_per_worker[number_of_workers]["number_of_empty_slots"].append(number_of_slots)

            worker_idx = data["number_of_workers"].index(number_of_workers)
            elapsed_time = data["elapsed_times"][worker_idx]
            data_per_worker[number_of_workers]["elapsed_times"].append(elapsed_time)

    for number_of_workers_in_simulation, data in data_per_worker.items():
        if number_of_workers_in_simulation > 1:
            worker_string = "workers"
        else:
            worker_string = "worker"

        plt.plot(data["number_of_empty_slots"], data["elapsed_times"],
                 label=f"{number_of_workers_in_simulation} {worker_string}")

    running_file = pathlib.Path(os.getcwd())

    plot_folder = running_file / "Plots" / "v2"

    plot_folder.mkdir(parents=True, exist_ok=True)

    total_number_of_slots_in_simulations = max(list(data_per_worker.values())[0]["number_of_empty_slots"])
    plot_file = plot_folder / f"simulation_time_against_free_slots_{total_number_of_slots_in_simulations}.pdf"

    plt.title("Time taken to complete simulations against number of slots available")
    plt.xlabel("Number of slots available")
    plt.ylabel("Time taken to simulate")
    plt.legend()
    plt.savefig(plot_file.as_posix())
    plt.close()


def benchmark_multiprocessing(starting_array: np.ndarray, number_of_extra_empty_slots: int, number_of_workers_to_benchmark: List[int]):
    # time computation for boards of increasing sizes
    data_per_slot = {}

    for number_of_slots in tqdm(range(1, number_of_extra_empty_slots + 1)):
        data_dict = {"number_of_workers": [], "elapsed_times": []}

        benchmarking_array = add_slots(starting_array, number_of_slots)

        for number_of_workers in number_of_workers_to_benchmark:

            average_time = 0
            for i in range(10):
                align_five = AlignFive.from_existing_board(
                    current_game_state_board=benchmarking_array,
                    with_bots=True,
                    player_list=[SmartPlayer(2, Color(255, 255, 255), n_workers=number_of_workers)],
                )

                tic = time.time()
                align_five.player_list[0].make_move(align_five.game_board)
                tac = time.time()

                elapsed_time = tac - tic
                average_time += elapsed_time

            data_dict["number_of_workers"].append(number_of_workers)
            data_dict["elapsed_times"].append(average_time/10)

        data_per_slot[number_of_slots] = data_dict

    plot_results(data_per_slot)

def benchmarking_main():
    parser = argparse.ArgumentParser(
        description="Benchmark your computer for against our code to figure out "
                    "the number of workers to give to our SmartPlayer."
    )
    parser.add_argument("-w", "--number-of-workers-to-try", metavar='W', type=int, nargs='+',
                        help='A number of worker to try', required=True)

    parser.add_argument("-s", "--maximum-number-of-empty-slots-try", metavar='S', type=int,
                        help='The maximum number of empty slots to try in our benchmarking', required=True)

    # parser.add_argument("-s", "--number-of-empty-slots-to-try", metavar='S', type=int, nargs='+',
    #                     help='The number of empty slots to try in our benchmarking')

    args = parser.parse_args()

    np.set_printoptions(4, suppress=True)
    test_array = np.array([
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2],
        [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
        [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 2, 1, 2, 1],
    ])

    worker_cases_benchmark = args.number_of_workers_to_try
    array_size = args.maximum_number_of_empty_slots_try
    benchmark_multiprocessing(test_array, array_size, worker_cases_benchmark)
