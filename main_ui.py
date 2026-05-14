import customtkinter as ctk
from mainSim import run_pandemic_simulation

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Pandemic Simulation setup")
        self.geometry("500x750")

        self.label = ctk.CTkLabel(self, text="Simulation Settings", font=("Roboto", 24, "bold"))
        self.label.pack(pady=20)

        self.form_frame = ctk.CTkScrollableFrame(self, width=450, height=500) # Slightly adjusted height for status label
        self.form_frame.pack(pady=10, padx=10)

        self.inputs = {} 
        fields = [
            ("N_AGENTS", "Number of Agents", "500"),
            ("DAYS", "Total Days", "365"),
            ("SPACE_SIZE", "Map Size", "150"),
            ("INF_RADIUS", "Infection Radius", "2.0"),
            ("INF_PROB", "Infection Probability", "0.5"),
            ("E_DUR", "Exposed Duration", "5"),
            ("I_DUR", "Infected Duration", "20"),
            ("D_PROB", "Death Probability", "0.10"),
            ("HOSP_CAP", "Hospital Capacity", "200"),
            ("START_INFECTED", "Initial Infected", "10"),
            ("VARIANT_START", "Variant Emergence Day", "150"),
            ("VARIANT_INF_PROB", "Variant Infection Probability", "0.8"),
            ("VARIANT_I_DUR", "Variant Infected Duration", "35"),
            ("VARIANT_INFECTED", "Variant Infected Count", "10"),
            ("LOCKDOWN_START_DAY", "Lockdown Start Day", "100"),
            ("V_RATE", "Vaccination Rate", "5"),
            ("V_START", "Vaccination Start Day", "250"),
            ("CTRL_START", "Control Start Day", "300"),
        ]

        for key, label, default in fields:
            row = ctk.CTkFrame(self.form_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            lbl = ctk.CTkLabel(row, text=label, width=200, anchor="w")
            lbl.pack(side="left", padx=10)
            
            entry = ctk.CTkEntry(row, width=150)
            entry.insert(0, default)
            entry.pack(side="right", padx=10)
            self.inputs[key] = entry

        # Error label for "invalid format" feedback
        self.status_label = ctk.CTkLabel(self, text="", text_color="#fa5252", font=("Roboto", 14))
        self.status_label.pack(pady=(5, 0))

        # button to start the simulation
        self.run_btn = ctk.CTkButton(self, text="Start Simulation", 
                                     command=self.start_sim,
                                     font=("Roboto", 16, "bold"),
                                     height=50,
                                     fg_color="#2a7bd0", 
                                     hover_color="#013570")
        self.run_btn.pack(pady=15)

    def start_sim(self):
        # Reset status label
        self.status_label.configure(text="")
        
        final_params = {}
        try:
            for k, v in self.inputs.items():
                val = v.get()
                # Basic validation: check if it can be a float
                float(val) 
                final_params[k] = val
            
            # If all validations pass, run the simulation
            run_pandemic_simulation(final_params)
            
        except ValueError:
            # Display invalid format if any float conversion fails
            self.status_label.configure(text="invalid format")

if __name__ == "__main__":
    app = App()
    app.mainloop()