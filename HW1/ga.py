def get_payoff_for_A(move_a: int, move_b: int) -> int:
    assert move_a in ["c", "d"] and move_b in ["c", "d"]
    if (move_a, move_b) == ("c", "c"):
        return 3
    if (move_a, move_b) == ("c", "d"):
        return 0
    if (move_a, move_b) == ("d", "c"):
        return 5
    if (move_a, move_b) == ("d", "d"):
        return 1


def get_payoff_for_B(move_a: int, move_b: int) -> int:
    assert move_a in ["c", "d"] and move_b in ["c", "d"]
    if (move_a, move_b) == ("c", "c"):
        return 3
    if (move_a, move_b) == ("c", "d"):
        return 5
    if (move_a, move_b) == ("d", "c"):
        return 0
    if (move_a, move_b) == ("d", "d"):
        return 1


def get_TFT_move(current_move: int, opp_move_history: str) -> str:
    if current_move == 0:
        return "c"

    return opp_move_history[current_move - 1]


def compute_average_TFT_payoff(games: int) -> int:
    total_payoff = 0

    def helper(current_move: int, move_history: str, run_payoff: int) -> None:
        nonlocal total_payoff

        if current_move == games:
            total_payoff += run_payoff
            return

        # Recursive call for `cooperate`
        TFT_coop_move = get_TFT_move(current_move, move_history)
        helper(
            current_move + 1,
            move_history + "c",
            run_payoff + get_payoff_for_A(TFT_coop_move, "c"),
        )

        # Recursive call for `defect`
        TFT_defect_move = get_TFT_move(current_move, move_history)
        helper(
            current_move + 1,
            move_history + "d",
            run_payoff + get_payoff_for_A(TFT_coop_move, "d"),
        )

    helper(0, "", 0)

    return total_payoff / (2 ** games)


def compute_average_RANDOM_payoff(games: int) -> int:
    total_payoff = 0

    def helper(current_move: int, move_history: str, run_payoff: int) -> None:
        nonlocal total_payoff

        if current_move == games:
            total_payoff += run_payoff
            return

        # Recursive call for `cooperate`
        TFT_coop_move = get_TFT_move(current_move, move_history)
        helper(
            current_move + 1,
            move_history + "c",
            run_payoff + get_payoff_for_B(TFT_coop_move, "c"),
        )

        # Recursive call for `defect`
        TFT_defect_move = get_TFT_move(current_move, move_history)
        helper(
            current_move + 1,
            move_history + "d",
            run_payoff + get_payoff_for_B(TFT_coop_move, "d"),
        )

    helper(0, "", 0)

    return total_payoff / (2 ** games)


def main():
    print(f"Average TFT Payoff for {10} games: {compute_average_TFT_payoff(10)}")
    print(f"Average RANDOM Payoff for {10} games: {compute_average_RANDOM_payoff(10)}")


if __name__ == "__main__":
    main()
