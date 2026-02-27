# CS 4632 – Warehouse Operations Simulation

## Project Overview

This project proposes a custom-built development simulation of warehouse operations within a supply chain and logistics context. The simulation models will replicate order processing, inventory management, and autonomous robot routing within a warehouse environment. Key computational models such as shortest-path routing, task allocation heuristics, and inventory control policies will be implemented to analyze system performance. The simulation will output measurable metrics that include throughput, storage efficiency, robot utilization, and order fulfillment time to analyze operational strategies and resource allocation decisions.

## Project Status

**Current Status (Milestone 2):** Core simulation framework and foundational models are implemented.

- **What's Implemented:**

   * Core Simulation Framework
+ Discrete-time simulation engine
+ Global clock and step-based updates
+ Emergency mode switching
+ Metric collection system

    * Warehouse Logistics Components
+ Robot agent class with task queue
+ A* pathfinding algorithm for robot navigation
+ Task generation and assignment
+ Nearest-robot task dispatch heuristic
+ InventoryManager with (Q, r) continuous review policy
+ Stochastic order generation

    * Crowd Dynamics Components
+ Pedestrian agent class
+ Simplified Social Force Model
+ Exit-directed evacuation behavior
+ Neighbor-based collision avoidance
+ Emergency-triggered evacuation mode

    *  Interaction Features
+ Shared grid-based warehouse environment
+ Robots halt during emergency
+ Pedestrians evacuate using force-based navigation
+ Evacuation completion detection

- **What's Still to Come:**

+ Advanced task assignment heuristics (load balancing comparison)
+ Battery management system for robots
+ Robot safe-zone routing during emergencies
+ Dynamic congestion analysis
+ CSV export of performance metrics
+ Visualization/animation module
+ Comparative performance experiments

- **Changes from Original Proposal:**
    - The simulation engine was changed from a pure event-based system to a time-stepped system for easier synchronization between agent types and simpler implementation of the Social Force Model.

## Installation Instructions

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/KhoaTran1111/khoatran-cs4632-hybrid-simulation.git
    cd khoatran-cs4632-hybrid-simulation
    ```

2.  **Set up a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv env
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

- **Troubleshooting:**
    If you encounter issues with `numpy`, ensure you have a Python compiler installed and try `pip install numpy`.

## Usage

1.  **Configure the Simulation:**
    Edit the `config/simulation_config.yaml` file to set parameters like grid size, number of robots, number of pedestrians, and simulation duration.

2.  **Run the Simulation:**
    Navigate to the root directory of the project and execute the main script:
    ```bash
    python src/main.py
    ```

3.  **Expected Output/Behavior:**
    - The console will print the simulation step, mode (Normal/Emergency), and basic metrics like the number of active robots and their positions.
    - Upon completion, a summary report will be printed to the console, and raw data files (e.g., `position_log.csv`) may be generated in the project root for further analysis with tools like Excel or Python scripts.

## Architecture Overview

The simulation is organized into several key components that directly map to the UML class diagram from the proposal.

- **`core`**: Contains the main simulation orchestrator (`SimulationEngine`) and the shared environment (`EnvironmentGrid`). The `SimulationEngine` controls the main loop, time progression, and mode changes.
- **`agents`**: Houses the `Robot` and `Pedestrian` classes. These agents hold their own state (position, velocity, etc.) and have methods to update themselves based on internal logic and the environment.
- **`models`**: This package holds the core algorithmic implementations.
    - `pathfinding.py`: Implements the A* algorithm, used by agents to find paths to goals.
    - `social_force.py`: Implements the calculations for the Social Force Model, used by pedestrians to determine their movement based on interactions with others and obstacles.
- **`managers`**: Contains centralized controllers for specific subsystems.
    - `task_dispatcher.py`: (Planned) Will manage and assign tasks to robots.
    - `inventory_manager.py`: (Planned) Will manage stock levels and reordering.
- **`utils`**: Provides helper modules like `data_collector.py`, which is responsible for logging agent states and simulation events for later analysis.

**Architectural Changes:**
The primary change is the consolidation of the "Crowd Controller" logic directly into the `Pedestrian` agent's behavior and the `SimulationEngine`'s emergency mode trigger. This simplifies the initial implementation while keeping the core interaction logic intact.