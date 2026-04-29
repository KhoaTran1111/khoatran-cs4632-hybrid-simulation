# CS 4632 – Warehouse Operations Simulation

## Project Overview

This project proposes a custom-built development simulation of warehouse operations within a supply chain and logistics context. The simulation models will replicate order processing, inventory management, and autonomous robot routing within a warehouse environment. Key computational models such as shortest-path routing, task allocation heuristics, and inventory control policies will be implemented to analyze system performance. The simulation will output measurable metrics that include throughput, storage efficiency, robot utilization, and order fulfillment time to analyze operational strategies and resource allocation decisions.

## Project Status

**Current Status (Milestone 5):** Final Report

Key features include:
- Time-stepped discrete simulation engine
- A* pathfinding for robot navigation
- Enhanced Social Force Model for realistic pedestrian movement and evacuation
- Configurable emergency mode with robot retreat to safe zones
- Proactive task dispatcher to improve robot utilization
- Comprehensive metrics collection and batch experimentation
- YAML-based configuration system

---

## Features

- **Hybrid Agent Interaction**: Robots and pedestrians coexist in a shared grid environment
- **Emergency Simulation**: Robots retreat to safe zones; pedestrians evacuate using Social Force
- **Order Fulfillment**: Poisson order generation with proactive task assignment
- **High Configurability**: All parameters (grid size, agent counts, order rate, emergency timing, etc.) are controlled via YAML
- **Detailed Analysis**: Time-series logging, sensitivity analysis, and scenario testing
- **Improved Utilization**: Proactive dispatching significantly reduces robot idle time

---

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
    *   Console output includes:

+ Task completion logs
+ Inventory reorder messages
+ Emergency trigger notification
+ Final performance metrics

## Architecture Overview

The simulation is organized into several key components that directly map to the UML class diagram from the proposal.

- **`core`**: Contains the main simulation orchestrator (`SimulationEngine`) and the shared environment (`EnvironmentGrid`) which navigate and detect neighbor, obstacles. The `SimulationEngine` controls the main loop, time progression, manages mode changes and records metrics.
- **`agents`**: Houses the `Robot` and `Pedestrian` classes. These agents hold their own state (position, velocity, etc.) and have methods to update themselves based on internal logic and the environment.
- **`models`**: This package holds the core algorithmic implementations.
    - `pathfinding.py`: Implements the A* algorithm, used by agents to find paths to goals for robot.
    - `social_force.py`: Implements the calculations for the Ssocial Force Model, used by pedestrians to determine their movement based on interactions with others and obstacles.
- **`managers`**: Contains centralized controllers for specific subsystems.
    - `task_dispatcher.py`: (Planned) Will manage and assign tasks to robots.
    - `inventory_manager.py`: (Planned) Will manage stock levels and reordering.
- **`utils`**: Provides helper modules like `metrics.py`, which is responsible for logging agent states and records robot distance, evacuation time.