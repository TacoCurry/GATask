from input import InputUtils
from Solution import Solution


def run():
    # from files
    Solution.memories = InputUtils.get_memories()
    Solution.processor = InputUtils.get_processor()
    Solution.tasks = InputUtils.get_tasks()

    # for GA
    max_generations = int(input("Max Generations: "))
    population = int(input("Population: "))
    Solution.UTIL_LIMIT_RATIO = float(input("Util Limitation: "))

    # 1. Make initial solution set
    Solution.set_random_seed()
    solutions = [Solution.get_random_solution() for i in range(population)]
    solutions.sort()  # Sort solutions by score

    for i in range(max_generations):
        is_valid = False
        for j in range(Solution.TRY_LIMIT):
            # 2. Select two solution
            solution1 = Solution.select_solution_using_roulette_wheel(solutions)
            solution2 = Solution.select_solution_using_roulette_wheel(solutions)

            # 3. Crossover
            new_solution = Solution.crossover(solution1, solution2)
            new_solution.mutation()

            # 4. Check Validity
            if new_solution.is_valid():
                is_valid = True
                break
            else:
                # If not valid, retry
                solutions.append(solution1)
                solutions.append(solution2)
                solutions.sort()

        if is_valid:
            continue
        else:
            raise Exception("solution 교배 불가")


run()

