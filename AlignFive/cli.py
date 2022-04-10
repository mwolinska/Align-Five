import os


def run_benchmarking():
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
    from AlignFive.benchmarks.multiprocessing_benchmark import benchmarking_main
    benchmarking_main()

def play_game():
    from AlignFive.align_five import play_align_five_main
    play_align_five_main()