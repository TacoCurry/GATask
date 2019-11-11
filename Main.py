from inout import InputUtils, OutputUtils
from Solution import Solution


def run():
    # from files
    Solution.memories = InputUtils.get_memories()
    Solution.processor = InputUtils.get_processor()
    Solution.tasks = InputUtils.get_tasks()

    # for GA
    max_generations = int(input("Max Generations: "))
    population = int(input("Population: "))
    Solution.UTIL_LIMIT_RATIO = float(input("Util Limit Ratio(0.0 ~ 1.0): "))

    # 1. Make initial solution set
    Solution.set_random_seed()
    solutions = [Solution.get_random_solution() for i in range(population)]
    solutions.sort()  # Sort solutions by score

    for i in range(max_generations):
        if i != 0 and i % 100 == 0:
            OutputUtils.report_print(i, solutions)

        get_new_solution = False
        for j in range(Solution.TRY_LIMIT):
            # 2. Select two solution
            solution1_index, solution1 = Solution.select_solution_using_roulette_wheel(solutions)
            solution2_index, solution2 = Solution.select_solution_using_roulette_wheel(solutions)
            solutions.insert(solution2_index, solution2)
            solutions.insert(solution1_index, solution1)

            # 3. Crossover
            new_solution = Solution.crossover(solution1, solution2)
            new_solution.mutation()

            # 4. Check Validity
            if new_solution.check_memory() and new_solution.check_utilization():
                get_new_solution = True
                break

        if get_new_solution:
            # Replace worst solution into new solution
            solutions[-1] = new_solution
            solutions.sort()
            continue
        else:
            raise Exception("{}번째 generation 이후, solution 교배 불가".format(i+1))

    # 5. Print result
    for solution in solutions:
        if solution.is_schedule():
            OutputUtils.result_print(solution)
            break


run()
