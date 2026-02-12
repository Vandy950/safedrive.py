import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
import os

class SafeDriveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SafeDrive - Vehicle Trip Logger")
        self.root.geometry("600x450")

        # Data storage
        self.trips = []
        self.vehicles = []
        self.drivers = []

        self.data_file = "safedrive_data.json"
        self.load_json()

        ttk.Label(root, text="SafeDrive – Vehicle Trip Logger", font=("Arial", 16, "bold")).pack(pady=10)

        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True)

        # --- Tabs ---
        self.trip_tab = ttk.Frame(notebook)
        self.vehicle_tab = ttk.Frame(notebook)
        self.driver_tab = ttk.Frame(notebook)
        self.output_tab = ttk.Frame(notebook)

        notebook.add(self.trip_tab, text="Trip Manager")
        notebook.add(self.vehicle_tab, text="Vehicle Manager")
        notebook.add(self.driver_tab, text="Driver Manager")
        notebook.add(self.output_tab, text="Reports")

        self.setup_trip_tab()
        self.setup_vehicle_tab()
        self.setup_driver_tab()
        self.setup_output_tab()

    # --- Trip Manager ---
    def setup_trip_tab(self):
        ttk.Label(self.trip_tab, text="Trip ID").grid(row=0, column=0, padx=10, pady=5)
        self.trip_id = ttk.Entry(self.trip_tab)
        self.trip_id.grid(row=0, column=1)

        ttk.Label(self.trip_tab, text="Vehicle").grid(row=1, column=0, padx=10, pady=5)
        self.trip_vehicle = ttk.Entry(self.trip_tab)
        self.trip_vehicle.grid(row=1, column=1)

        ttk.Label(self.trip_tab, text="Driver").grid(row=2, column=0, padx=10, pady=5)
        self.trip_driver = ttk.Entry(self.trip_tab)
        self.trip_driver.grid(row=2, column=1)

        ttk.Label(self.trip_tab, text="Distance (km)").grid(row=3, column=0, padx=10, pady=5)
        self.trip_distance = ttk.Entry(self.trip_tab)
        self.trip_distance.grid(row=3, column=1)

        ttk.Button(self.trip_tab, text="Add Trip", command=self.add_trip).grid(row=4, column=0, columnspan=2, pady=10)

    def add_trip(self):
        data = {
            "TripID": self.trip_id.get(),
            "Vehicle": self.trip_vehicle.get(),
            "Driver": self.trip_driver.get(),
            "Distance": self.trip_distance.get()
        }
        self.trips.append(data)
        self.save_json()
        messagebox.showinfo("Success", "Trip added successfully!")

    # --- Vehicle Manager ---
    def setup_vehicle_tab(self):
        ttk.Label(self.vehicle_tab, text="Vehicle ID").grid(row=0, column=0, padx=10, pady=5)
        self.vehicle_id = ttk.Entry(self.vehicle_tab)
        self.vehicle_id.grid(row=0, column=1)

        ttk.Label(self.vehicle_tab, text="Model").grid(row=1, column=0, padx=10, pady=5)
        self.vehicle_model = ttk.Entry(self.vehicle_tab)
        self.vehicle_model.grid(row=1, column=1)

        ttk.Button(self.vehicle_tab, text="Add Vehicle", command=self.add_vehicle).grid(row=2, column=0, columnspan=2, pady=10)

    def add_vehicle(self):
        data = {"VehicleID": self.vehicle_id.get(), "Model": self.vehicle_model.get()}
        self.vehicles.append(data)
        self.save_json()
        messagebox.showinfo("Success", "Vehicle added successfully!")

    # --- Driver Manager ---
    def setup_driver_tab(self):
        ttk.Label(self.driver_tab, text="Driver ID").grid(row=0, column=0, padx=10, pady=5)
        self.driver_id = ttk.Entry(self.driver_tab)
        self.driver_id.grid(row=0, column=1)

        ttk.Label(self.driver_tab, text="Name").grid(row=1, column=0, padx=10, pady=5)
        self.driver_name = ttk.Entry(self.driver_tab)
        self.driver_name.grid(row=1, column=1)

        ttk.Button(self.driver_tab, text="Add Driver", command=self.add_driver).grid(row=2, column=0, columnspan=2, pady=10)

    def add_driver(self):
        data = {"DriverID": self.driver_id.get(), "Name": self.driver_name.get()}
        self.drivers.append(data)
        self.save_json()
        messagebox.showinfo("Success", "Driver added successfully!")

    # --- Output / Reports ---
    def setup_output_tab(self):
        ttk.Button(self.output_tab, text="Save Data (CSV)", command=self.save_csv).pack(pady=10)
        ttk.Button(self.output_tab, text="Save Data (JSON)", command=self.save_json_dialog).pack(pady=10)
        ttk.Button(self.output_tab, text="Show Summary", command=self.show_summary).pack(pady=10)
        self.summary_box = tk.Text(self.output_tab, height=10, width=60)
        self.summary_box.pack(pady=10)

    def save_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["TripID", "Vehicle", "Driver", "Distance"])
                for trip in self.trips:
                    writer.writerow(trip.values())
            messagebox.showinfo("Saved", "Data saved as CSV!")

    def save_json_dialog(self):
        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file:
            with open(file, 'w') as f:
                json.dump({"Trips": self.trips, "Vehicles": self.vehicles, "Drivers": self.drivers}, f, indent=4)
            messagebox.showinfo("Saved", "Data saved as JSON!")

    def save_json(self):
        with open(self.data_file, 'w') as f:
            json.dump({"Trips": self.trips, "Vehicles": self.vehicles, "Drivers": self.drivers}, f, indent=4)

    def load_json(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.trips = data.get("Trips", [])
                self.vehicles = data.get("Vehicles", [])
                self.drivers = data.get("Drivers", [])

    def show_summary(self):
        total_distance = sum(float(t["Distance"]) for t in self.trips if t["Distance"].replace('.', '', 1).isdigit())
        self.summary_box.delete(1.0, tk.END)
        self.summary_box.insert(tk.END, f"Total Trips: {len(self.trips)}\n")
        self.summary_box.insert(tk.END, f"Total Distance: {total_distance} km\n")
        self.summary_box.insert(tk.END, f"Vehicles Registered: {len(self.vehicles)}\n")
        self.summary_box.insert(tk.END, f"Drivers Registered: {len(self.drivers)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = SafeDriveApp(root)
    root.mainloop()