from enum import Enum, auto
from dataclasses import dataclass

class Progress(Enum):
    FAILED = 1
    SUCCESS = 1
    PROCESSING = auto()


class Test:
    current_progress: Progress

    def __init__(self, progress):
        self.current_progress = Progress
        print(self.current_progress == Progress.SUCCESS)



def main():
    t = Test(Progress.FAILED)
    print(t)


if __name__ == '__main__':
    main()
