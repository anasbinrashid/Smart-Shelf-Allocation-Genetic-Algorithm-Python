import random
import pandas as pd


class Product:
    def __init__(self, id, name, weight, category, is_refrigerated=False, is_hazardous=False, is_high_demand=False, is_bulky=False, is_promotional=False, is_expensive=False,
                    comp_group=None):
        self.id = id
        self.name = name
        self.weight = weight
        self.category = category
        self.is_refrigerated = is_refrigerated
        self.is_hazardous = is_hazardous
        self.is_high_demand = is_high_demand
        self.is_bulky = is_bulky
        self.is_promotional = is_promotional
        self.is_expensive = is_expensive
        self.comp_group = comp_group
        print(f"Created Product: {id} - {name} (Weight: {weight}, Category: {category})")


class Shelf:
    def __init__(self, id, name, shelf_type, capacity, accessible=False, secure=False):
        self.id = id
        self.name = name
        self.shelf_type = shelf_type
        self.capacity = capacity
        self.accessible = accessible
        self.secure = secure
        print(f"Created Shelf: {id} - {name} (Type: {shelf_type}, Capacity: {capacity}, Accessible: {accessible}, Secure: {secure})")


shelves = [
    Shelf("S1", "Checkout Display", "checkout", 8, accessible=True, secure=True),
    Shelf("S2", "Lower Shelf", "lower", 25, accessible=False, secure=False),
    Shelf("S4", "Eye-Level Shelf", "eye-level", 15, accessible=True, secure=False),
    Shelf("S5", "General Aisle Shelf", "general", 20, accessible=True, secure=False),
    Shelf("R1", "Refrigerator Zone", "refrigerated", 20, accessible=False, secure=False),
    Shelf("H1", "Hazardous Item Zone", "hazardous", 10, accessible=False, secure=True)
]

print(f"\nTotal shelves created: {len(shelves)}")

products = [
    # id, name, weight, category, is_refrigerated, is_hazardous, is_high_demand, is_bulky, is_promotional, is_expensive, comp_group
    Product("P1", "Milk", 5, "dairy", is_refrigerated=False, is_high_demand=True),
    Product("P2", "Rice Bag", 10, "grains", is_bulky=True),
    Product("P3", "Frozen Nuggets", 5, "frozen", is_refrigerated=True),
    Product("P4", "Cereal", 3, "breakfast", is_high_demand=True),
    Product("P5", "Pasta", 2, "pasta", comp_group="pasta"),
    Product("P6", "Pasta Sauce", 3, "pasta", comp_group="pasta"),
    Product("P7", "Detergent", 4, "cleaning", is_hazardous=True),
    Product("P8", "Glass Cleaner", 5, "cleaning", is_hazardous=True),
    Product("P9", "Macaroni", 2, "pasta", comp_group="pasta")
]

print(f"\nTotal products created: {len(products)}")

def fitness(assignment, products, shelves):
    print(f"\n--- Evaluating Fitness for Assignment ---")
    
    penalty = 0
    shelf_assignments = {shelf.id: [] for shelf in shelves}
    prod_dict = {p.id: p for p in products}
    for pid, sid in assignment.items():
        shelf_assignments[sid].append(pid)
    
    print(f"Current shelf assignments: {shelf_assignments}")

    print("\nEvaluating Constraint 1: Shelf Capacity & Weight Limit")
    for shelf in shelves:
        total_weight = sum(prod_dict[pid].weight for pid in shelf_assignments[shelf.id])
        print(f"  Shelf {shelf.id} - Weight: {total_weight}/{shelf.capacity}")
        if total_weight > shelf.capacity:
            current_penalty = (total_weight - shelf.capacity) * 10
            penalty += current_penalty
            print(f"  Constraint 1 violated for shelf {shelf.id}: Weight {total_weight} > Capacity {shelf.capacity}, adding penalty: {current_penalty}")
        else:
            print(f"  Constraint 1 satisfied for shelf {shelf.id}")

    print("\nEvaluating Constraint 2: High-Demand Product Accessibility")
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_high_demand:
            shelf_obj = next(s for s in shelves if s.id == sid)
            print(f"  High-demand product {p.id} ({p.name}) on shelf {sid} (Accessible: {shelf_obj.accessible})")
            if not shelf_obj.accessible:
                penalty += 20
                print(f"  Constraint 2 violated: High-demand product {p.id} on non-accessible shelf {sid}, adding penalty: 20")
            else:
                print(f"  Constraint 2 satisfied for product {p.id}")

    print("\nEvaluating Constraint 3: Product Category Segmentation")
    category_shelves = {}
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.category not in category_shelves:
            category_shelves[p.category] = set()
        category_shelves[p.category].add(sid)
    
    print(f"  Category distribution: {category_shelves}")
    for cat, shelf_set in category_shelves.items():
        if len(shelf_set) > 1:
            current_penalty = (len(shelf_set) - 1) * 5
            penalty += current_penalty
            print(f"  Constraint 3 violated: Category '{cat}' spread across {len(shelf_set)} shelves, adding penalty: {current_penalty}")
        else:
            print(f"  Constraint 3 satisfied for category '{cat}'")

    print("\nEvaluating Constraint 4: Perishable Goods / Refrigeration")
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_refrigerated:
            shelf_obj = next(s for s in shelves if s.id == sid)
            print(f"  Refrigerated product {p.id} ({p.name}) on shelf {sid} (Type: {shelf_obj.shelf_type})")
            if shelf_obj.shelf_type != "refrigerated":
                penalty += 30
                print(f"  Constraint 4 violated: Refrigerated product {p.id} on non-refrigerated shelf {sid}, adding penalty: 30")
            else:
                print(f"  Constraint 4 satisfied for product {p.id}")

    print("\nEvaluating Constraint 5: Hazardous Items")
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_hazardous:
            shelf_obj = next(s for s in shelves if s.id == sid)
            print(f"  Hazardous product {p.id} ({p.name}) on shelf {sid} (Type: {shelf_obj.shelf_type})")
            if shelf_obj.shelf_type != "hazardous":
                penalty += 30
                print(f"  Constraint 5 violated: Hazardous product {p.id} on non-hazardous shelf {sid}, adding penalty: 30")
            else:
                print(f"  Constraint 5 satisfied for product {p.id}")

    print("\nEvaluating Constraint 6: Product Compatibility")
    comp_groups = {}
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.comp_group is not None:
            if p.comp_group not in comp_groups:
                comp_groups[p.comp_group] = set()
            comp_groups[p.comp_group].add(sid)
    
    print(f"  Compatibility groups: {comp_groups}")
    for group, shelf_set in comp_groups.items():
        if len(shelf_set) > 1:
            current_penalty = (len(shelf_set) - 1) * 10
            penalty += current_penalty
            print(f"  Constraint 6 violated: Compatibility group '{group}' spread across {len(shelf_set)} shelves, adding penalty: {current_penalty}")
        else:
            print(f"  Constraint 6 satisfied for group '{group}'")

    print("\nEvaluating Constraint 7: Restocking Efficiency")
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_bulky:
            shelf_obj = next(s for s in shelves if s.id == sid)
            print(f"  Bulky product {p.id} ({p.name}) on shelf {sid} (Type: {shelf_obj.shelf_type})")
            if shelf_obj.shelf_type != "lower":
                penalty += 15
                print(f"  Constraint 7 violated: Bulky product {p.id} not on lower shelf, adding penalty: 15")
            else:
                print(f"  Constraint 7 satisfied for product {p.id}")

    print("\nEvaluating Constraint 8: Refrigeration Efficiency")
    refrigerated_shelves = [shelf.id for shelf in shelves if shelf.shelf_type == "refrigerated"]
    assigned_refrigerated = set()
    print(f"  Available refrigerated shelves: {refrigerated_shelves}")
    
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_refrigerated and sid in refrigerated_shelves:
            assigned_refrigerated.add(sid)
    
    print(f"  Refrigerated shelves in use: {assigned_refrigerated}")
    if len(assigned_refrigerated) > 1:
        current_penalty = (len(assigned_refrigerated) - 1) * 5
        penalty += current_penalty
        print(f"  Constraint 8 violated: Refrigerated products spread across {len(assigned_refrigerated)} shelves, adding penalty: {current_penalty}")
    else:
        print(f"  Constraint 8 satisfied")

    print("\nEvaluating Constraint 9: Promotional Items Visibility")
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_promotional:
            shelf_obj = next(s for s in shelves if s.id == sid)
            print(f"  Promotional product {p.id} ({p.name}) on shelf {sid} (Accessible: {shelf_obj.accessible})")
            if not shelf_obj.accessible:
                penalty += 20
                print(f"  Constraint 9 violated: Promotional product {p.id} on non-accessible shelf, adding penalty: 20")
            else:
                print(f"  Constraint 9 satisfied for product {p.id}")

    print("\nEvaluating Constraint 10: Theft Prevention")
    for pid, sid in assignment.items():
        p = prod_dict[pid]
        if p.is_expensive:
            shelf_obj = next(s for s in shelves if s.id == sid)
            print(f"  Expensive product {p.id} ({p.name}) on shelf {sid} (Secure: {shelf_obj.secure})")
            if not shelf_obj.secure:
                penalty += 25
                print(f"  Constraint 10 violated: Expensive product {p.id} on non-secure shelf, adding penalty: 25")
            else:
                print(f"  Constraint 10 satisfied for product {p.id}")

    print(f"\nTotal penalty for this assignment: {penalty}")
    return penalty


def generate_initial_population(pop_size, products, shelves):
    print(f"\n--- Generating Initial Population (Size: {pop_size}) ---")
    population = []
    for i in range(pop_size):
        assignment = {}
        for p in products:
            shelf = random.choice(shelves)
            assignment[p.id] = shelf.id
        population.append(assignment)
        print(f"  Generated individual {i+1}/{pop_size}")
    print(f"Initial population generated with {len(population)} individuals")
    return population

def tournament_selection(population, fitnesses, tournament_size=3):
    participants = random.sample(list(zip(population, fitnesses)), tournament_size)
    print(f"\n--- Tournament Selection (Size: {tournament_size}) ---")
    for i, (_, fitness) in enumerate(participants):
        print(f"  Participant {i+1} fitness: {fitness}")
    
    participants.sort(key=lambda x: x[1])
    print(f"  Winner has fitness: {participants[0][1]}")
    return participants[0][0]

def crossover(parent1, parent2, products):
    print("\n--- Performing Crossover ---")
    child = {}
    for p in products:
        if random.random() < 0.5:
            child[p.id] = parent1[p.id]
            print(f"  Product {p.id}: Inherited shelf {parent1[p.id]} from Parent 1")
        else:
            child[p.id] = parent2[p.id]
            print(f"  Product {p.id}: Inherited shelf {parent2[p.id]} from Parent 2")
    return child

def mutate(assignment, products, shelves, mutation_rate=0.1):
    print(f"\n--- Performing Mutation (Rate: {mutation_rate}) ---")
    new_assignment = assignment.copy()
    for p in products:
        if random.random() < mutation_rate:
            old_shelf = new_assignment[p.id]
            shelf = random.choice(shelves)
            new_assignment[p.id] = shelf.id
            print(f"  Mutated product {p.id}: {old_shelf} -> {shelf.id}")
        else:
            print(f"  Product {p.id} unchanged: {new_assignment[p.id]}")
    return new_assignment


def genetic_algorithm(products, shelves, pop_size=50, generations=100, mutation_rate=0.1):
    print(f"\n=== Starting Genetic Algorithm ===")
    print(f"Population Size: {pop_size}")
    print(f"Generations: {generations}")
    print(f"Mutation Rate: {mutation_rate}")
    
    population = generate_initial_population(pop_size, products, shelves)
    best_assignment = None
    best_fitness = float('inf')

    for g in range(generations):
        print(f"\n=== Generation {g+1}/{generations} ===")
        
        print("Evaluating fitness for each individual...")
        fitnesses = []
        for i, assignment in enumerate(population):
            print(f"\nIndividual {i+1}/{pop_size}:")
            fit_val = fitness(assignment, products, shelves)
            fitnesses.append(fit_val)
            
        current_best_idx = fitnesses.index(min(fitnesses))
        print(f"\nBest fitness in generation {g+1}: {fitnesses[current_best_idx]}")
        
        for i, f_val in enumerate(fitnesses):
            if f_val < best_fitness:
                best_fitness = f_val
                best_assignment = population[i]
                print(f"New best solution found! Fitness: {best_fitness}")
        
        print(f"\nCreating new population for generation {g+2}...")
        new_population = []
        while len(new_population) < pop_size:
            print(f"\nCreating individual {len(new_population)+1}/{pop_size}")
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child = crossover(parent1, parent2, products)
            child = mutate(child, products, shelves, mutation_rate)
            new_population.append(child)
        
        population = new_population
        print(f"Generation {g+1} complete: Best Fitness = {best_fitness}")
        if best_fitness == 0:
            print("Perfect solution found! Stopping early.")
            break
    
    print(f"\n=== Genetic Algorithm Complete ===")
    print(f"Best Fitness: {best_fitness}")
    return best_assignment, best_fitness


def store_results_excel(assignment, products, shelves, filename="shelf_allocation.xlsx"):
    print(f"\n--- Storing Results in Excel: {filename} ---")
    # Build shelf to product mapping
    shelf_assignments = {shelf.id: [] for shelf in shelves}
    prod_dict = {p.id: p for p in products}
    for pid, sid in assignment.items():
        shelf_assignments[sid].append(pid)
        print(f"  Product {pid} ({prod_dict[pid].name}) assigned to Shelf {sid}")

    rows = []
    for shelf in shelves:
        print(f"\n  Shelf {shelf.id} ({shelf.name}) contains:")
        for pid in shelf_assignments[shelf.id]:
            p = prod_dict[pid]
            print(f"    - {p.id}: {p.name} (Weight: {p.weight}, Category: {p.category})")
            rows.append({
                "Shelf ID": shelf.id,
                "Shelf Name": shelf.name,
                "Shelf Type": shelf.shelf_type,
                "Shelf Capacity": shelf.capacity,
                "Product ID": p.id,
                "Product Name": p.name,
                "Product Weight": p.weight,
                "Category": p.category
            })
    
    print(f"  Creating DataFrame with {len(rows)} rows")
    df = pd.DataFrame(rows)
    print(f"  Saving to {filename}")
    df.to_excel(filename, index=False)
    print(f"Results stored in {filename}")


def main():
    print("\n=== Starting Shelf Allocation Program ===")
    
    best_assignment, best_fit = genetic_algorithm(products, shelves, pop_size=50, generations=200, mutation_rate=0.1)
    
    print("\n=== Best Assignment Results ===")
    print(f"Best Fitness Score: {best_fit}")
    
    prod_dict = {p.id: p for p in products}
    for pid, sid in best_assignment.items():
        product = prod_dict[pid]
        shelf = next(s for s in shelves if s.id == sid)
        print(f"Product {pid} ({product.name}) -> Shelf {sid} ({shelf.name})")
    
    store_results_excel(best_assignment, products, shelves)
    print("\n=== Program Complete ===")

if __name__ == "__main__":
    main()