from typing import TypedDict
from typing_extensions import Unpack


class HelloArgs(TypedDict):
    who: str
    n: int


def hello(who: str, n: int = 1) -> None:
    for _ in range(n):
        print(n, "Hello", who)

def print_hello(**kwargs: Unpack[HelloArgs]) -> None:
    hello(**kwargs)
