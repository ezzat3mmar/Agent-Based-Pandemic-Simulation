# Advanced Agent-Based Pandemic Simulation (SEIR-V Model)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Framework: CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-orange.svg)](https://github.com/TomSchimansky/CustomTkinter)

##  Overview
This repository hosts a sophisticated **Agent-Based Modeling (ABM)** platform designed to simulate the dynamics of infectious diseases using an enhanced **SEIR-V** framework. By treating individuals as autonomous agents, the simulation captures complex emergent behaviors that traditional mathematical models often miss.

##  System Architecture
The project follows a modular design to separate the UI logic from the mathematical simulation engine. Below is the architectural flow:

```text
       +-------------------------------------------------+
       |              User Interface (GUI)               |
       |      (CustomTkinter Dashboard & Control)        |
       +------------------------+------------------------+
                                |
                                v
       +-------------------------------------------------+
       |               Simulation Engine                 |
       |      (Time-Step Loops & Spatial Mapping)        |
       +---------+--------------+--------------+---------+
                 |              |              |
                 v              v              v
       +--------------+  +--------------+  +--------------+
       | Agent Logic  |  | Environment  |  |  Data Logger |
       | (SEIR-V ABM) |  | (Collisions) |  | (CSV/Excel)  |
       +--------------+  +--------------+  +--------------+
                 |              |              |
                 +--------------+--------------+
                                |
                                v
       +-------------------------------------------------+
       |             Analytics & Visualization           |
       |       (Live Matplotlib Plots & Statistics)      |
       +-------------------------------------------------+
```
Unlike traditional compartmental models that use ordinary differential equations to represent population averages, this simulation treats every individual as an autonomous **"Agent"** with unique spatial coordinates, velocity, and health states. This allows for the emergence of complex patterns such as localized outbreaks, the impact of "superspreaders," and the effectiveness of vaccination campaigns in a stochastic environment.

##  Key Features

### 1. Advanced Epidemiological Engine
* **SEIR-V Multi-State Dynamics:** Tracks transitions between Susceptible, Exposed (latent period), Infectious (symptomatic/asymptomatic), Recovered (acquired immunity), Deceased, and Vaccinated states.
* **Viral Mutation Logic:** Simulation of genetic drift where the virus can evolve higher transmission or mortality rates over time.
* **Hospital Pressure System:** Real-time monitoring of healthcare capacity. If infections exceed the `Hospital Capacity` threshold, mortality rates increase dynamically to simulate system collapse.

### 2. Interactive Graphical User Interface (GUI)
* **Dynamic Control Panel:** Built with `CustomTkinter`, offering a modern, dark-themed dashboard.
* **17+ Real-time Variables:** Adjust population density, social distancing efficacy, mask-wearing compliance, and vaccination roll-out speed on the fly.
* **Live Visualizer:** A high-performance canvas that renders agent movement and interactions in real-time.

### 3. Data Analytics & Visualization
* **Real-time Plotting:** Integrated `Matplotlib` charts showing the epidemic curve (Infections vs. Time) as the simulation progresses.
* **Comprehensive Exporting:** One-click export of all simulation metrics to **Excel (.xlsx)** for academic post-processing and statistical analysis.
* **Statistical Summaries:** Automated calculation of $R_0$ (Basic Reproduction Number) and Case Fatality Rate (CFR).

##  Technical Architecture

### Core Components:
* **`main_ui.py`**: The entry point. Manages the lifecycle of the GUI and binds user inputs to the simulation parameters.
* **`mainSim.py`**: The "Brain" of the project. It handles the spatial partitioning, collision detection (for infection spread), and state transition probabilities using `NumPy`.

### Mathematical Foundation:
The simulation approximates the following transition logic for each agent:
* **Infection Probability:** $P(inf) = f(\text{Distance}, \text{Contagiousness}, \text{Protective Gear})$
* **Vaccine Efficacy:** Reduces $P(inf)$ by a user-defined factor $\epsilon$.
* **Mortality:** $P(death) = \mu_{base} + \mu_{excess}(\text{if Hospital Load} > 200\%)$

##  Configurable Parameters
| Category | Parameters |
| :--- | :--- |
| **Demographics** | Population Size, Initial Infected, Initial Vaccinated |
| **Virus Profile** | Infection Radius, Transmission Rate, Incubation Period, Recovery Time |
| **Healthcare** | Hospital Bed Capacity, Base Mortality Rate, Mutation Probability |
| **Interventions** | Social Distancing (Movement Speed), Mask Efficacy, Vaccination Speed |

##  Documentation
Detailed technical documentation and project reports can be found in the `Docs` folder:

*    [Project documentation (PDF)](./Docs/pandemic_simulation_docs.pdf)
*    [project presentation (PDF)](./Docs/Pandemic_Simulation_Presentation.pdf)

#  Installation & System Requirements

To ensure the **Agent-Based Pandemic Simulation** runs smoothly with all its features (GUI, Real-time plotting, and Excel exporting), please follow the requirements below.

## 🐍 Python Version
*   **Minimum:** Python 3.8
*   **Recommended:** Python 3.10 or higher

---

##  Required Libraries (Dependencies)

The simulation relies on the following libraries. You can install them individually or using the bulk command provided in the next section.

| Library | Purpose in this Project |
| :--- | :--- |
| **CustomTkinter** | Used to build the modern, dark-themed User Interface (GUI). |
| **NumPy** | Handles high-speed mathematical calculations and agent coordinate vectors. |
| **Matplotlib** | Responsible for rendering the live epidemic curves and charts. |
| **Pandas** | Manages the simulation data and structures it for logging. |
| **Openpyxl** | The engine required to export simulation results into `.xlsx` (Excel) files. |
| **SciPy** | Used for statistical functions and calculating transition probabilities. |
| **Pillow (PIL)** | Required for image processing and icon rendering within the UI. |

---

##  Quick Installation (Terminal/Command Prompt)

Copy and paste the following command to install all dependencies at once:

```bash
pip install customtkinter numpy matplotlib pandas openpyxl scipy Pillow

```
**Clone the repository:**
   ```bash
   git clone https://github.com/ezzat3mmar/Agent-Based-Pandemic-Simulation.git
cd Agent-Based-Pandemic-Simulation
