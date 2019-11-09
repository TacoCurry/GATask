from Task import Tasks, Task
import sys
from Processor import Processor
from Memory import Memories


class InputUtils:
    @staticmethod
    def get_memories(file="input_memory.txt"):
        memories = Memories()
        try:
            with open(file, "r", encoding='UTF8') as f:
                # get num of mem types
                n_memories = int(f.readline())

                # get memories
                for i in range(n_memories):
                    mem_info = input().split()
                    memories.insert_memory(mem_info[0], int(mem_info[1]), float(mem_info[2]), float(mem_info[3]))

            return memories
        except FileNotFoundError:
            print("%s이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("%s의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)

    @staticmethod
    def get_processor(file="input_processor.txt"):
        processor = Processor()
        try:
            with open(file, "r", encoding='UTF8') as f:
                # get n_cores
                n_core = int(f.readline())
                processor.n_core = n_core

                # get voltage/frequency mode
                n_mode = int(f.readline())
                for i in range(n_mode):
                    mode_info = list(map(int, input().split()))
                    processor.insert_mode(mode_info[0], mode_info[1], mode_info[2])

            return processor
        except FileNotFoundError:
            print("%s이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("%s의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)

    @staticmethod
    def get_tasks(file="input_task.txt"):
        tasks = Tasks()
        try:
            with open(file, "r", encoding='UTF8') as f:
                # get tasks
                n_tasks = int(f.readline())
                for i in range(n_tasks):
                    task_info = list(map(int, input().split()))
                    tasks.insert_task(Task(task_info[0], task_info[1], task_info[2], task_info[3]))
            return tasks
        except FileNotFoundError:
            print("%s이 존재하는지 확인하세요".format(file))
            sys.exit(0)
        except IndexError:
            print("%s의 형식이 올바른지 확인하세요".format(file))
            sys.exit(0)


