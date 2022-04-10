import os


def run_benchmarking():
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
    from AlignFive.benchmarks.multiprocessing_benchmark import benchmarking_main
    benchmarking_main()

def two_player_game():
    from AlignFive.align_five import two_player_game_main
    two_player_game_main()

def single_player_game():
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "True"
    from AlignFive.align_five import single_player_game_main
    single_player_game_main()
