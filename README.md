# CS 4632 – Warehouse Operations Simulation

## Project Overview

his project proposes a custom-built development simulation of warehouse operations within a supply chain and logistics context. The simulation models will replicate order processing, inventory management, and autonomous robot routing within a warehouse environment. Key computational models such as shortest-path routing, task allocation heuristics, and inventory control policies will be implemented to analyze system performance. The simulation will output measurable metrics that include throughput, storage efficiency, robot utilization, and order fulfillment time to analyze operational strategies and resource allocation decisions.

## Project Goals

The main goals of this project are to:

* Simulate how orders are processed in a warehouse
* Model robot movement and task assignment
* Track inventory levels and basic restocking behavior
* Collect performance metrics to analyze warehouse efficiency
* Emergency mode when need it

## Core Features

* In normal mode, robots and pedestrians use warehouse space
* In emergency mode, pedetrians seek for exit, robots is slowing down 
* Discrete-time, agent-based simulation
* Autonomous warehouse robots
* Shortest-path routing for robot navigation
* Basic inventory control using reorder points
* Metric collection for throughput and order fulfillment time

## Metrics Collected

The simulation tracks the following metrics:

* Order throughput
* Average order fulfillment time
* Robot utilization
* Inventory usage and stock levels

## Technologies Used

* Programming Language: Python
* Modeling Style: Agent-based, discrete-time simulation

## Repository Structure

```
/Docs        LaTeX source and project documentation
/src         Simulation source code
/assets     Optional visualization or configuration files
```

## Course Information

CS 4632 – Modeling and Simulation
Milestone 1: Project Foundation

## Author

Khoa Tran
