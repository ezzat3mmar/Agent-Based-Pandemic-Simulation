import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.spatial.distance import cdist
import os

def run_pandemic_simulation(params):
     # 1. Simulation Parameters (From UI) -----
    N_AGENTS = int(params['N_AGENTS'])
    DAYS = int(params['DAYS'])
    SPACE_SIZE = int(params['SPACE_SIZE'])
    INFECTION_RADIUS = float(params['INF_RADIUS'])
    BASE_INFECTION_PROB = float(params['INF_PROB'])
    EXPOSED_DURATION = int(params['E_DUR'])
    INFECTED_DURATION = int(params['I_DUR'])
    BASE_DEATH_PROB = float(params['D_PROB'])
    HOSPITAL_CAPACITY = int(params['HOSP_CAP'])
    VACCINATION_RATE = int(params['V_RATE'])
    VaccinatiON_START_DAY = int(params['V_START'])
    LOCKDOWN_START_DAY = int(params['LOCKDOWN_START_DAY'])
    Infection_control_start_day = int(params['CTRL_START'])
    # MUTATION DYNAMICS
    VARIANT_START_DAY = int(params['VARIANT_START'])     
    VARIANT_INF_PROB = float(params['VARIANT_INF_PROB'])        
    VARIANT_I_DUR = int(params['VARIANT_I_DUR'])           
    variant_active = False     

    nom_ofStart_infected = int(params['START_INFECTED'])
    nom_ofVariant_infected = int(params['VARIANT_INFECTED'])

    # States constants
    S, E, I, R, D, V = 0, 1, 2, 3, 4, 5

     # 2. Agent Structure -----
    ages = np.random.randint(5, 80, N_AGENTS) 
    is_chronic = np.random.rand(N_AGENTS) < 0.30
    is_essential = np.random.rand(N_AGENTS) < 0.10

    positions = np.random.rand(N_AGENTS, 2) * SPACE_SIZE
    angles = np.random.rand(N_AGENTS) * 2 * np.pi
    speeds = np.random.uniform(0.5, 1.5, N_AGENTS)
    states = np.zeros(N_AGENTS, dtype=int)
    states[np.random.choice(N_AGENTS, nom_ofStart_infected, replace=False)] = I
    time_in_state = np.zeros(N_AGENTS)

    history = {'S': [], 'E': [], 'I': [], 'R': [], 'D': [], 'V': []}
    healthy_recoveries = []
    chronic_recoveries = []

     # 3. Visualization Setup ....
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(18, 10), facecolor="#1D1D1DFF") 
    fig.canvas.manager.set_window_title('SEIR-V Pandemic')
    
    # make a grid layout for the main map and side graphs
    gs = gridspec.GridSpec(2, 2, figure=fig, width_ratios=[3, 1], height_ratios=[1, 1])

    ax_map = fig.add_subplot(gs[:, 0])      
    ax_stack = fig.add_subplot(gs[0, 1:])   
    ax_recov = fig.add_subplot(gs[1, 1:])   

    # color scheme for states
    colors_dict = {
        S: "#45B7FED1", # Soft Blue
        E: "#FAD12EDD", # Muted Gold
        I: "#FF4D4DDD", # Coral Red
        R: "#3DDE80", # Emerald Green
        D: "#434748DB", # Steel Gray
        V: "#C130DEBE"  # Light Purple
    }

    if not os.path.exists('snapshots'):
        os.makedirs('snapshots')

    # 4. Simulation Loop -----
    for day in range(DAYS):
        if day == VARIANT_START_DAY:
            variant_active = True
            susceptible_mask = (states == S)
            if np.sum(susceptible_mask) > 1:
                new_cases = np.random.choice(np.where(susceptible_mask)[0], nom_ofVariant_infected, replace=False)
                states[new_cases] = I
                time_in_state[new_cases] = 0

        if variant_active:
            current_inf_prob = VARIANT_INF_PROB
            current_i_dur = VARIANT_I_DUR
            current_speed_mult = 0.5 if day >= LOCKDOWN_START_DAY else 1.0 
        else:
            current_inf_prob = BASE_INFECTION_PROB * 0.2 if day >= Infection_control_start_day else BASE_INFECTION_PROB
            current_i_dur = INFECTED_DURATION
            current_speed_mult = 0.7 if day >= LOCKDOWN_START_DAY else 1.0

        # --- Movement Engine ---
        for i in range(N_AGENTS):
            if states[i] == D: continue 
            mult = 1.0 if is_essential[i] else current_speed_mult
            positions[i, 0] += np.cos(angles[i]) * speeds[i] * mult
            positions[i, 1] += np.sin(angles[i]) * speeds[i] * mult
            if positions[i, 0] <= 0 or positions[i, 0] >= SPACE_SIZE: angles[i] = np.pi - angles[i]
            if positions[i, 1] <= 0 or positions[i, 1] >= SPACE_SIZE: angles[i] = -angles[i]
            positions[i] = np.clip(positions[i], 0.1, SPACE_SIZE - 0.1)

        # --- Transmission Engine ---
        current_infected = np.sum(states == I)
        hospital_overload = current_infected > HOSPITAL_CAPACITY
        susceptible_idx = np.where(states == S)[0]
        infected_idx = np.where(states == I)[0]
        recovered_idx = np.where(states == R)[0]
        
        if len(susceptible_idx) > 0 and len(infected_idx) > 0:
            distances = cdist(positions[susceptible_idx], positions[infected_idx])
            for i, s_id in enumerate(susceptible_idx):
                if np.any(distances[i] < INFECTION_RADIUS):
                    if np.random.rand() < current_inf_prob:
                        states[s_id] = E
                        time_in_state[s_id] = 0

        if len(recovered_idx) > 0 and len(infected_idx) > 0:
            distances2 = cdist(positions[recovered_idx], positions[infected_idx])
            for i, r_id in enumerate(recovered_idx):
                if np.any(distances2[i] < INFECTION_RADIUS):
                    if np.random.rand() < current_inf_prob *0.3: 
                        states[r_id] = E
                        time_in_state[r_id] = 0

        # Vaccination logic
        if day >= VaccinatiON_START_DAY:
            s_indices = np.where(states == S)[0]
            s_indices_2 = np.where(states == R)[0]
            
            if len(s_indices) > 0:
                to_vaccinate = np.random.choice(s_indices, min(VACCINATION_RATE, len(s_indices)), replace=False)
                states[to_vaccinate] = V
            if len(s_indices_2) > 0:
                to_vaccinate_2 = np.random.choice(s_indices_2, min(VACCINATION_RATE, len(s_indices_2)), replace=False)
                states[to_vaccinate_2] = V

        # State Transitions
        for i in range(N_AGENTS):
            if states[i] in [E, I]:
                time_in_state[i] += 1
                if states[i] == E and time_in_state[i] >= EXPOSED_DURATION:
                    states[i] = I
                    time_in_state[i] = 0
                elif states[i] == I and time_in_state[i] >= current_i_dur:
                    death_risk = BASE_DEATH_PROB
                    if is_chronic[i]: death_risk *= 3.0
                    if hospital_overload: death_risk *= 2.0
                    states[i] = D if np.random.rand() < death_risk else R
                    time_in_state[i] = 0

        # Data Logging
        current_deaths = np.sum(states == D)
        current_vaccinated = np.sum(states == V)
        current_EXPOSED =np.sum(states == E)
        current_recoverd=np.sum(states == R)
        for code, key in zip([S, E, I, R, D, V], ['S', 'E', 'I', 'R', 'D', 'V']):
            history[key].append(np.sum(states == code))
        healthy_recoveries.append(np.sum((states == R) & (~is_chronic)))
        chronic_recoveries.append(np.sum((states == R) & (is_chronic)))

       # --- Rendering Logic Inside the Loop ---
        ax_map.clear() 
        ax_stack.clear()
        ax_recov.clear()

        # Draw agents with enhanced aesthetics
        ax_map.scatter(positions[:, 0], positions[:, 1], s=ages*2.5, c=[colors_dict[s] for s in states], 
                    edgecolors=['white' if c else 'none' for c in is_chronic], 
                    linewidths=0.6, alpha=0.9)
        
        # Map aesthetics
        ax_map.set_facecolor("#222222")
        ax_map.set_title("STRATEGIC INFECTIOUS DISEASE MAP", color='white', fontsize=14, fontweight='bold', pad=15)
        ax_map.set_xticks([]); ax_map.set_yticks([]) 

        # Stats HUD (Glassmorphism effect)
        stats_text = (
            f" Day: {day} \n"
            f" Infected: {current_infected} \n"
            f" Deaths: {current_deaths} \n"
            f" Exposed: {current_EXPOSED}\n"
            f" Recoverd: {current_recoverd}\n"
            f" Vaccinated: {current_vaccinated} \n"
            f" Hospital: {'OVERLOAD !' if hospital_overload else 'Normal'}"
        )
        ax_map.text(0.05, 0.95, stats_text, transform=ax_map.transAxes, color='white', 
                    fontsize=10, fontweight='bold', verticalalignment='top', family='monospace',
                    bbox=dict(facecolor='#1E1E1E', alpha=0.8, edgecolor=colors_dict[I] if hospital_overload else colors_dict[S], boxstyle='round,pad=0.8'))

        ax_map.set_title("LIVE MAP", color='white', fontsize=12, fontweight='bold', pad=15)
        ax_map.set_facecolor("#1F1F1F")
        ax_map.set_xticks([]); ax_map.set_yticks([])

        # draw new variant emergence
        if variant_active:
            ax_map.text(0.5, -0.09, "NEW VARIANT detected!", transform=ax_map.transAxes, color='#FF6B6B', 
                        fontsize=12, fontweight='bold', verticalalignment='bottom', horizontalalignment='center',
                        bbox=dict(facecolor='#1E1E1E', alpha=0.9, edgecolor='#FF6B6B', boxstyle='round,pad=0.8'))

        # Side Graphs
        days_arr = np.arange(len(history['S']))
        ax_stack.stackplot(days_arr, history['V'], history['D'], history['R'], history['I'], history['E'], history['S'],
                    labels=['Vaccinated', 'Dead', 'Recovered', 'Infected', 'Exposed', 'Susceptible'], 
                    colors=[colors_dict[V], colors_dict[D], colors_dict[R], colors_dict[I], colors_dict[E], colors_dict[S]], 
                    alpha=0.85)
        ax_stack.legend(loc='upper left', fontsize=8, frameon=False)
        ax_stack.set_title("POPULATION DYNAMICS", fontsize=10, color='#AAAAAA')

        ax_recov.plot(days_arr, healthy_recoveries, color='#00D2FF', label='Healthy Recovery', linewidth=1.5)
        ax_recov.plot(days_arr, chronic_recoveries, color='#FF9966', label='Chronic Recovery', linewidth=1.5)
        ax_recov.legend(loc='upper left', fontsize=8, frameon=False)
        ax_recov.set_title("RECOVERY TRENDS", fontsize=10, color='#AAAAAA')



        plt.pause(1)
        
        # Snapshots
        if day in [1, 50, 100, 150,  200, 250, 300, 364]:
            plt.savefig(f"snapshots/pandemic_day_{day}.png", dpi=200, bbox_inches='tight')

    plt.show()

    # 5. Export Final Excel Report -----
    report_df = pd.DataFrame({
        'Day': np.arange(DAYS),
        'Susceptible': history['S'], 'Exposed': history['E'], 'Infected': history['I'],
        'Recovered': history['R'], 'Deaths': history['D'], 'Vaccinated': history['V']
    })
    
    output_file = "Pandemic_Report.xlsx"
    try:
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
          report_df.to_excel(writer, index=False)
    
        if os.path.exists(output_file):
          print(f"Report saved successfully at: {os.path.abspath(output_file)}")
    except Exception as e:
         print(f"Error saving Excel: {e}")
