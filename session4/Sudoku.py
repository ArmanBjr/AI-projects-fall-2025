#4021262459
#4021262131

import pygad
import numpy as np
import random

# Define Sudoku puzzles (0 represents empty cells)
SUDOKU_EXAMPLES = {
    "easy": [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 0, 0, 0, 9],  # 3 missing values
    ],
    "medium": [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 0, 0, 0, 0],
        [2, 8, 7, 4, 1, 0, 0, 0, 0],
        [3, 4, 5, 2, 8, 0, 0, 0, 0],  # 10 missing values
    ],
    "scattered_8": [
        [5, 3, 0, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 0, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 0, 7],
        [8, 5, 9, 7, 6, 0, 4, 2, 3],
        [4, 2, 6, 0, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 0, 5, 6],
        [9, 6, 1, 5, 0, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 0, 5],
        [3, 4, 5, 2, 8, 0, 1, 7, 9],  # 8 empty cells (easy with scattered pattern)
    ],
    "scattered_27": [
        [5, 0, 4, 0, 7, 0, 9, 0, 2],
        [0, 7, 0, 1, 0, 5, 0, 4, 0],
        [1, 0, 8, 0, 4, 0, 5, 0, 7],
        [0, 5, 0, 7, 0, 1, 0, 2, 0],
        [4, 0, 6, 0, 5, 0, 7, 0, 1],
        [0, 1, 0, 9, 0, 4, 0, 5, 0],
        [9, 0, 1, 0, 3, 0, 2, 0, 4],
        [0, 8, 0, 4, 0, 9, 0, 3, 0],
        [3, 0, 5, 0, 8, 0, 1, 0, 9],  # 27 empty cells (medium difficulty with alternating pattern)
    ],
    "hard": [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 8, 0, 0, 7, 0, 0, 9, 0],
        [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0],
        [0, 0, 4, 6, 0, 2, 9, 0, 0],
        [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4],
        [0, 4, 0, 0, 5, 0, 0, 3, 6],
        [7, 0, 3, 0, 1, 8, 0, 0, 0],  # 47 empty cells
    ],
    "expert": [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],  # 51 empty cells (challenging)
    ]
}


class SudokuSolver:
    def __init__(self, puzzle):
        self.original_puzzle = np.array(puzzle)
        self.fixed_positions = self.original_puzzle != 0
        self.empty_positions = []  # List of (row, col) tuples for empty cells
        self.box_empty_positions = {}  # Dictionary mapping box_id to list of empty positions

        # Get all empty cell positions organized by box
        for box_id in range(9):
            self.box_empty_positions[box_id] = []

        for row_idx in range(9):
            for col_idx in range(9):
                if not self.fixed_positions[row_idx, col_idx]:
                    self.empty_positions.append((row_idx, col_idx))
                    box_id = (row_idx // 3) * 3 + (col_idx // 3)
                    self.box_empty_positions[box_id].append((row_idx, col_idx))

        print(f"Number of empty cells: {len(self.empty_positions)}")
        print(f"Empty cells per box: {[len(self.box_empty_positions[i]) for i in range(9)]}")

    def get_box_id(self, row, col):
        """Get box ID (0-8) for a given cell"""
        return (row // 3) * 3 + (col // 3)

    def create_initial_solution(self):
        num_genes = len(self.empty_positions)
        genes = [0] * num_genes
        posToIdx = {}
        for idx, pos in enumerate(self.empty_positions):
            posToIdx[pos] = idx
        on = self.original_puzzle.copy()
        for box_id in range(0, 9):
            r0 = (box_id // 3) * 3
            c0 = (box_id % 3) * 3
            fixed = []
            for r in range(r0, r0 + 3):
                for c in range(c0, c0 + 3):
                    if self.fixed_positions[r, c]:
                        fixed.append(int(self.original_puzzle[r, c]))
            khali = self.box_empty_positions[box_id]  
            missing = []
            for d in range(1, 10):
                if d not in set(fixed):
                    missing.append(d)
            random.shuffle(missing)
            i = 0
            for (r, c) in khali:
                if i < len(missing):
                    chosen = int(missing[i])
                else:
                    chosen = random.randint(1, 9)
                genIdx = posToIdx[(r, c)]
                genes[genIdx] = chosen
                on[r, c] = chosen
                i += 1
        return np.array(genes, dtype=int)


    def initial_population(self, sol_per_pop):
        all_solutions = []
        for i in range(sol_per_pop):
            one = self.create_initial_solution()
            all_solutions.append(one)
        all_solutions = np.array(all_solutions)

        return all_solutions

    def custom_crossover(self, parents, offspring_size, ga_instance):
        num_babies, num_genes = offspring_size
        all_solutions = np.empty((num_babies, num_genes), dtype=int)
        pos_to_idx = {pos: i for i, pos in enumerate(self.empty_positions)}

        box_gene_indices = []
        for box_id in range(9):
            indices_here = []
            for (r, c) in self.box_empty_positions[box_id]:
                indices_here.append(pos_to_idx[(r, c)])
            indices_here.sort()  
            box_gene_indices.append(indices_here)

        parent_count = parents.shape[0]
        baby_idx = 0

        while baby_idx < num_babies:
            p1_idx = (baby_idx * 2) % parent_count
            p2_idx = (baby_idx * 2 + 1) % parent_count
            mom = parents[p1_idx, :].copy()
            dad = parents[p2_idx, :].copy()
            kid = np.empty(num_genes, dtype=int)
            for box_id in range(9):
                gene_ids = box_gene_indices[box_id]
                parentPick = mom if random.random() < 0.5 else dad
                for g in gene_ids:
                    kid[g] = int(parentPick[g])

            all_solutions[baby_idx] = kid
            baby_idx += 1

        return all_solutions




    def custom_mutation(self, offspring, ga_instance):
        # baraye inke ye dict as (row, col) be gene index dashte bashim, ertebat bein gen va box
        pos_to_idx = {pos: i for i, pos in enumerate(self.empty_positions)}

        box_gene_indices = []
        for box_id in range(9):
            ids_here = []
            for (r, c) in self.box_empty_positions[box_id]:
                ids_here.append(pos_to_idx[(r, c)])
            ids_here.sort() 
            box_gene_indices.append(ids_here)

        for kid_i in range(offspring.shape[0]):
            baby = offspring[kid_i]
            which_box = random.randint(0, 8)
            genes_in_box = box_gene_indices[which_box]
            if len(genes_in_box) < 2:
                continue
            g1 = random.choice(genes_in_box)
            g2 = g1
            while g2 == g1:
                g2 = random.choice(genes_in_box)
            val1 = int(baby[g1])
            val2 = int(baby[g2])
            baby[g1], baby[g2] = val2, val1
            offspring[kid_i] = baby
        return offspring


    def decode_solution(self, solution):
        """Convert GA solution (genes) to Sudoku grid"""
        grid = self.original_puzzle.copy()

        # Fill empty positions with gene values
        for idx, (row, col) in enumerate(self.empty_positions):
            grid[row, col] = int(solution[idx])

        return grid

    def fitness_function(self, ga_instance, solution, solution_idx):
        grid_here = self.decode_solution(solution)
        cnt = 0
        for i in range(0, 9):
            for k in range(0, 9):
                for m in range(k + 1, 9):
                    if grid_here[i][k] == grid_here[i][m] and grid_here[i][k] != 0:
                        cnt += 1

        for j in range(0, 9):
            for k in range(0, 9):
                for m in range(k + 1, 9):
                    if grid_here[k][j] == grid_here[m][j] and grid_here[k][j] != 0:
                        cnt += 1

        for box_id in range(0, 9):
            r0 = (box_id // 3) * 3   
            c0 = (box_id % 3)  * 3   
            tekrari = []
            for row in range(r0, r0 + 3):
                for col in range(c0, c0 + 3):
                    tekrari.append(grid_here[row][col])

            unique_vals = set(v for v in tekrari if v != 0)
            cnt += 9 - len(unique_vals)

        return -cnt
    
                

    def solve(self, num_generations, num_parents_mating, sol_per_pop):
        """Solve Sudoku using Genetic Algorithm"""
        num_genes = len(self.empty_positions)

        print(f"Number of genes: {num_genes}")
        print(f"Population size: {sol_per_pop}")
        print(f"Number of generations: {num_generations}")
        print(f"Starting genetic algorithm...")

        
        # Calculate mutation_num_genes based on puzzle difficulty
        # For easy (3 genes): mutate 1 gene
        # For medium (10 genes): mutate 2-3 genes
        # For hard (20 genes): mutate 4-5 genes

        ga = pygad.GA(
        initial_population=self.initial_population(sol_per_pop), 
        num_generations=num_generations,
        num_parents_mating=num_parents_mating,
        sol_per_pop=sol_per_pop,
        num_genes=num_genes,
        gene_type=int,
        gene_space=list(range(1, 10)),
        fitness_func=self.fitness_function,
        parent_selection_type="tournament",
        K_tournament=3,
        keep_parents=3,
        crossover_type=self.custom_crossover,
        mutation_type=self.custom_mutation,
        on_generation=self.on_generation, 
        stop_criteria=["reach_0"] #har seri tool mikeshid in ro ezafe kardim!
        )
        ga.run()
        best_solution, best_fitness, best_index = ga.best_solution()
        solved = self.decode_solution(best_solution)

        return solved, best_fitness

    def on_generation(self, ga_instance):
        """Callback function to monitor progress"""
        if ga_instance.generations_completed % 100 == 0:
            solution, fitness, _ = ga_instance.best_solution()
            print(
                f"Generation {ga_instance.generations_completed}: Best Fitness = {fitness})"
            )
        


def print_sudoku(grid, title="Sudoku Grid"):
    """Pretty print Sudoku grid"""
    print(f"\n{title}")
    print("=" * 37)
    for i, row in enumerate(grid):
        if i % 3 == 0 and i != 0:
            print("-" * 37)
        row_str = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_str += " | "
            row_str += f" {num if num != 0 else '.'} "
        print(row_str)
    print("=" * 37)


def analyze_solution(grid, solver):
    """Analyze the solution quality"""
    complete_rows = 0
    complete_cols = 0
    complete_boxes = 0

    # Check rows
    for row in range(9):
        row_values = grid[row, :]
        if len(set(row_values)) == 9 and set(row_values) == set(range(1, 10)):
            complete_rows += 1

    # Check columns
    for col in range(9):
        col_values = grid[:, col]
        if len(set(col_values)) == 9 and set(col_values) == set(range(1, 10)):
            complete_cols += 1

    # Check boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = grid[box_row : box_row + 3, box_col : box_col + 3].flatten()
            if len(set(box)) == 9 and set(box) == set(range(1, 10)):
                complete_boxes += 1

    print(f"\n📊 Solution Analysis:")
    print(f"  Complete Rows: {complete_rows}/9")
    print(f"  Complete Columns: {complete_cols}/9")
    print(f"  Complete Boxes: {complete_boxes}/9")
    print(f"  Total: {complete_rows + complete_cols + complete_boxes}/27")
    print(f"  Valid Solution: {complete_rows == 9 and complete_cols == 9 and complete_boxes == 9}")


# Example usage
if __name__ == "__main__":
    selected_puzzle = "expert"
    print("🧩 Sudoku Solver using Genetic Algorithm (PyGAD)")
    print("=" * 60)

    # Solve Puzzle
    print("\n" + "=" * 60)
    print(f"📋 PUZZLE ({SUDOKU_EXAMPLES[selected_puzzle].count(0)} empty cells)")
    print("=" * 60)
    print_sudoku(SUDOKU_EXAMPLES[selected_puzzle], "Original Puzzle")

    solver = SudokuSolver(SUDOKU_EXAMPLES[selected_puzzle])
    solution, fitness = solver.solve(
        3000, 100, 500)

    print_sudoku(solution, "Solved Puzzle")
    print(f"\n✨ Fitness Score: {fitness}")
    analyze_solution(solution, solver)

