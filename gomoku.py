"""Simple console-based Gomoku (Five in a Row) game.

Two human players take turns placing stones on a 15x15 board. The
first player to align five stones horizontally, vertically, or
(diagonally) wins the game. Players can enter moves as ``row col``
(1-indexed) or type ``quit`` to exit the game early.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

BOARD_SIZE = 15
EMPTY = "."
PLAYER_STONES = {"black": "X", "white": "O"}


def create_board(size: int = BOARD_SIZE) -> List[List[str]]:
    """Return a ``size`` x ``size`` board filled with ``EMPTY`` markers."""
    return [[EMPTY for _ in range(size)] for _ in range(size)]


@dataclass
class MoveResult:
    winner: Optional[str] = None
    draw: bool = False


class GomokuGame:
    """A minimal text-based Gomoku implementation."""

    def __init__(self, size: int = BOARD_SIZE) -> None:
        self.size = size
        self.board = create_board(size)
        self.current_player = "black"
        self.moves_played = 0

    def switch_player(self) -> None:
        self.current_player = "white" if self.current_player == "black" else "black"

    def place_stone(self, row: int, col: int) -> bool:
        """Place the current player's stone at ``row, col`` if possible."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            print("位置超出棋盘范围，请重新输入。")
            return False
        if self.board[row][col] != EMPTY:
            print("该位置已经有棋子，请重新输入。")
            return False

        stone = PLAYER_STONES[self.current_player]
        self.board[row][col] = stone
        self.moves_played += 1
        return True

    def check_winner(self, row: int, col: int) -> MoveResult:
        stone = PLAYER_STONES[self.current_player]

        def count(direction_row: int, direction_col: int) -> int:
            count_stones = 1
            for direction in (1, -1):
                r, c = row, col
                while True:
                    r += direction_row * direction
                    c += direction_col * direction
                    if 0 <= r < self.size and 0 <= c < self.size and self.board[r][c] == stone:
                        count_stones += 1
                    else:
                        break
            return count_stones

        directions = ((1, 0), (0, 1), (1, 1), (1, -1))
        for dr, dc in directions:
            if count(dr, dc) >= 5:
                return MoveResult(winner=self.current_player)

        if self.moves_played == self.size * self.size:
            return MoveResult(draw=True)

        return MoveResult()

    def print_board(self) -> None:
        header = "   " + " ".join(f"{i:2}" for i in range(1, self.size + 1))
        print(header)
        for idx, row in enumerate(self.board, start=1):
            row_str = " ".join(row)
            print(f"{idx:2} {row_str}")

    def run(self) -> None:
        print("欢迎来到简易五子棋！玩家黑棋 (X) 先手，白棋 (O) 后手。")
        print("输入格式：行 列（均为 1-15 之间的数字），或输入 quit 退出。\n")
        self.print_board()

        while True:
            stone = PLAYER_STONES[self.current_player]
            user_input = input(f"轮到{self.current_player} ({stone})，请输入坐标：").strip().lower()
            if user_input in {"quit", "q", "exit"}:
                print("游戏已退出。")
                break

            try:
                row_str, col_str = user_input.split()
                row = int(row_str) - 1
                col = int(col_str) - 1
            except ValueError:
                print("输入格式不正确，请输入两个数字，例如：8 8。")
                continue

            if not self.place_stone(row, col):
                continue

            result = self.check_winner(row, col)
            self.print_board()

            if result.winner:
                print(f"恭喜！{result.winner} 获胜！")
                break
            if result.draw:
                print("棋盘已满，平局结束！")
                break

            self.switch_player()


def main() -> None:
    game = GomokuGame()
    game.run()


if __name__ == "__main__":
    main()
