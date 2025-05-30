# Smart Shelf Allocation System using Genetic Algorithm

## Overview

The Smart Shelf Allocation System is an intelligent retail optimization tool that uses genetic algorithms to solve the complex problem of product placement in stores. The system automatically assigns products to shelves while considering multiple constraints including capacity limits, accessibility requirements, safety regulations, and customer convenience factors.

## Features

### Core Functionality
- **Genetic Algorithm Optimization**: Uses evolutionary computation to find optimal product-shelf assignments
- **Multi-Constraint Handling**: Manages 10+ different placement constraints simultaneously
- **Excel Export**: Generates detailed allocation reports in Excel format
- **Real-time Fitness Evaluation**: Provides transparent penalty scoring system
- **Scalable Architecture**: Easily extensible for additional products and shelves

### Constraint Management
1. **Shelf Capacity & Weight Limits**: Prevents overloading shelves
2. **High-Demand Product Accessibility**: Ensures popular items are easily reachable
3. **Product Category Segmentation**: Groups similar products together
4. **Refrigeration Requirements**: Places perishable goods in appropriate zones
5. **Hazardous Item Safety**: Isolates dangerous products to secure areas
6. **Product Compatibility**: Keeps complementary items on same shelves
7. **Restocking Efficiency**: Places bulky items on lower shelves
8. **Refrigeration Efficiency**: Minimizes number of active cooling zones
9. **Promotional Item Visibility**: Ensures marketing items are prominently displayed
10. **Theft Prevention**: Secures expensive items in monitored areas

## Getting Started

### Prerequisites
```bash
# Required Python packages
pip install pandas
pip install openpyxl
```

## System Architecture

### Core Classes

#### `Product`
Represents items to be placed on shelves with attributes:
- Basic properties: ID, name, weight, category
- Special flags: refrigerated, hazardous, high-demand, bulky, promotional, expensive
- Compatibility grouping for related products

#### `Shelf`
Represents storage locations with properties:
- Capacity and accessibility constraints
- Type specifications (checkout, refrigerated, hazardous, etc.)
- Security features

### Algorithm Components

#### Genetic Algorithm Flow
1. **Population Initialization**: Generate random product-shelf assignments
2. **Fitness Evaluation**: Calculate penalty scores based on constraint violations
3. **Selection**: Tournament selection for parent candidates
4. **Crossover**: Combine parent solutions to create offspring
5. **Mutation**: Introduce random changes to maintain diversity
6. **Evolution**: Repeat process across generations

#### Fitness Function
The system uses a penalty-based fitness function where lower scores indicate better solutions:
- Capacity violations: 10 points per excess weight unit
- Safety violations: 30 points per hazardous/refrigeration mismatch
- Accessibility issues: 20 points per high-demand/promotional item misplacement
- Efficiency penalties: 5-25 points for organizational violations

## Sample Data

### Products (9 items)
- **P1**: Milk (dairy, high-demand)
- **P2**: Rice Bag (grains, bulky)
- **P3**: Frozen Nuggets (frozen, refrigerated)
- **P4**: Cereal (breakfast, high-demand)
- **P5-P6-P9**: Pasta products (compatibility group)
- **P7-P8**: Cleaning products (hazardous)

### Shelves (6 locations)
- **S1**: Checkout Display (secure, accessible)
- **S2**: Lower Shelf (high capacity)
- **S4**: Eye-Level Shelf (accessible)
- **S5**: General Aisle Shelf (accessible)
- **R1**: Refrigerator Zone (specialized)
- **H1**: Hazardous Item Zone (secure, specialized)

## Configuration

### Algorithm Parameters
```python
# Genetic Algorithm Settings
pop_size = 50          # Population size
generations = 200      # Number of evolution cycles
mutation_rate = 0.1    # Probability of random changes
tournament_size = 3    # Selection competition size
```

### Penalty Weights
```python
# Constraint violation penalties
CAPACITY_PENALTY = 10      # Per unit overweight
SAFETY_PENALTY = 30        # Safety violations
ACCESSIBILITY_PENALTY = 20 # Accessibility issues
EFFICIENCY_PENALTY = 5-25  # Organization problems
```

## Output and Results

### Console Output
The system provides detailed logging including:
- Product and shelf creation confirmation
- Generation-by-generation fitness progress
- Constraint violation analysis
- Best solution tracking

### Excel Report
Generates `shelf_allocation.xlsx` containing:
- Complete product-shelf assignments
- Shelf utilization details
- Product categorization summary

### Sample Output
```
=== Best Assignment Results ===
Best Fitness Score: 0
Product P1 (Milk) -> Shelf S4 (Eye-Level Shelf)
Product P2 (Rice Bag) -> Shelf S2 (Lower Shelf)
Product P3 (Frozen Nuggets) -> Shelf R1 (Refrigerator Zone)
...
```

## Customization

### Adding New Products
```python
products.append(
    Product("P10", "New Item", weight=3, category="new_category",
            is_high_demand=True, is_expensive=True)
)
```

### Adding New Shelves
```python
shelves.append(
    Shelf("S6", "New Shelf", "general", capacity=30, 
          accessible=True, secure=False)
)
```

### Modifying Constraints
Edit the `fitness()` function to adjust penalty values or add new constraints.

## Testing

Run with different parameters to test system robustness:
```python
# Quick test
genetic_algorithm(products, shelves, pop_size=10, generations=50)

# Intensive optimization
genetic_algorithm(products, shelves, pop_size=100, generations=500)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Enhancement
- Multi-objective optimization (cost, accessibility, efficiency)
- Machine learning integration for demand prediction
- 3D visualization of shelf layouts
- Real-time inventory integration
- Mobile app for store managers

## Acknowledgments

- Genetic Algorithm methodology based on evolutionary computation principles
- Retail optimization strategies from supply chain management research
- Constraint satisfaction techniques from operations research
