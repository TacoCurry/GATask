import random


class Solution:
    processor = None
    memories = None
    tasks = None
    TRY_LIMIT = 10000
    UTIL_LIMIT_RATIO = None
    PENALTY_RATIO = 0.3

    def __init__(self):
        self.genes_processor = []
        self.genes_memory = []
        self.utilization = None
        self.power = None
        self.score = None

    def __lt__(self, other):
        # Sort by score
        return self.score - other.score

    def is_valid(self):
        # util, power, score 계산한 후, util 이 UTIL_LIMIT_RATIO 이하일 때만 true 반환하는 메서드
        util_sum = 0
        power_sum = 0

        for i in range(Solution.tasks.n_task):
            task = Solution.tasks.get_task(i)
            processor_mode = Solution.processor.get_mode(self.genes_processor[i])
            memory = Solution.memories.get_memory(self.genes_memory[i])

            wcet_scaled_processor = 1 / processor_mode.wcet_scale
            wcet_scaled_memory = 1 / memory.wcet_scale
            det = task.wcet * max(wcet_scaled_memory, wcet_scaled_processor)

            if det > task.period:
                return False  # deadline ncc

            # Calc util
            util_sum += det / task.period

            # Calc active power for processor
            processor_power_unit = (processor_mode.power_active * wcet_scaled_processor +
                                    processor_mode.power_idle * wcet_scaled_memory) / \
                                   (wcet_scaled_memory + wcet_scaled_processor)
            power_sum += processor_power_unit * det / task.period

            # Calc power for memory
            power_sum += task.mem_req * (task.mem_active_ratio * memory.power_active +
                                         (1 - task.mem_active_ratio) * memory.power_idle) * det / task.period \
                         + task.mem_req * memory.power_idle * (1 - det / task.period)

        n_core = Solution.processor.n_core
        if util_sum > n_core * (1 + Solution.UTIL_LIMIT_RATIO):
            return False

        # Calc idle power for processor
        if util_sum < n_core:
            power_sum += Solution.processor.modes[-1].power_idle * (Solution.processor.n_core - util_sum)

        self.utilization = util_sum
        self.power = power_sum
        self.score = power_sum
        if util_sum >= Solution.processor.n_core:
            # Apply penalty for score
            self.score += power_sum * (util_sum - n_core) * Solution.PENALTY_RATIO
        return True

    @staticmethod
    def set_random_seed():
        random.seed()  # Set seed using current time

    @staticmethod
    def get_random_solution():
        solution = Solution()

        for i in range(Solution.TRY_LIMIT):
            # Make random genes
            for j in range(Solution.tasks.n_task):
                solution.genes_processor.append(random.randint(0, Solution.processor.n_mode - 1))
                solution.genes_memory.append(random.randint(0, Solution.memories.n_mem_types - 1))

            if solution.is_valid():
                return solution

        # 생성을 반복해도 UTIL_LIMIT_RATIO 이하의 solution 을 만들지 못할 경우
        raise Exception("random solution 생성 불가")

    @staticmethod
    def select_solution(sum_fitness, fitness_list, solutions):
        point = random.random() * sum_fitness
        temp = 0
        for i in range(len(fitness_list)):
            temp += fitness_list[i]
            if point < temp:
                break
        return solutions[i]

    @staticmethod
    def select_solution_using_roulette_wheel(solutions):
        # 1. fitness 구하기
        # fi = (Cw - Ci) + ( Cw - Cb ) / (k - 1) 식을 이용
        K = 4

        worst_score = solutions[-1].score
        best_score = solutions[0].score
        constant = (worst_score - best_score) / (K - 1)

        fitness_list = []
        sum_fitness = 0
        for solution in solutions:
            fitness = worst_score - solution.score + constant
            sum_fitness += fitness
            fitness_list.append(fitness)

        # 2. 선택하기
        return Solution.select_solution(sum_fitness, fitness_list, solutions)

    @staticmethod
    def select_solution_using_ranking_selection(solutions):
        # Calculate fitness using Ranking Selection
        MAX = 100
        MIN = 0

        diff = MIN - MAX
        n = len(solutions)
        fitness_list = []
        sum_fitness = 0
        for i in range(1, len(solutions) + 1):
            fitness = MAX + (i - 1) * diff / (n - 1)
            sum_fitness += fitness
            fitness_list.append(fitness)

        # Select
        return Solution.select_solution(sum_fitness, fitness_list, solutions)

    @staticmethod
    def crossover(solution1, solution2):
        n_task = Solution.tasks.n_task

        crossover_point_processor = random.randint(0, n_task)
        crossover_point_memory = random.randint(0, n_task)

        new_solution = Solution()
        new_solution.genes_processor = solution1.genes_processor[:crossover_point_processor] + \
                                       solution2.genes_processor[crossover_point_processor:]
        new_solution.genes_memory = solution1.genes_memory[:crossover_point_memory] + \
                                    solution2.genes_memory[crossover_point_memory:]
        return new_solution

    def mutation(self):
        MUTATION_PROB = 0.001  # 0.1% 확률로 exchange mutation 발생

        if random.random() > MUTATION_PROB:
            return  # 돌연변이 발생 안함.

        n_task = Solution.tasks.n_task

        # processor
        point1 = random.randint(0, n_task - 1)
        point2 = random.randint(0, n_task - 1)
        temp = self.genes_processor[point1]
        self.genes_processor[point1] = self.genes_processor[point2]
        self.genes_processor[point2] = temp

        # memory
        point1 = random.randint(0, n_task - 1)
        point2 = random.randint(0, n_task - 1)
        temp = self.genes_memory[point1]
        self.genes_memory[point1] = self.genes_memory[point2]
        self.genes_memory[point2] = temp

    def is_schedule(self):
        if self.utilization <= Solution.processor.n_core:
            return True
        return False

