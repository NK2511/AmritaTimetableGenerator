import random
import tkinter as tk

# Timetable matrix (5 days, 7 periods per day)
DAYS = 5
PERIODS_PER_DAY = 7
timetable_matrix = [[0 for _ in range(PERIODS_PER_DAY)] for _ in range(DAYS)]

# Class schedule with total theory and lab sessions per week
class_schedule = {
    "Math_Lab": 1,
    "Python_Lab": 1,
    "Python_Theory": 2,
    "Material_Science_Lab": 1,
    "Material_Science_Theory": 2,
    "Design_Lab": 1,
    "Design_Theory": 2,
    "Actuators_Drives_Theory": 3,
    "Mechanisms&Machines_Lab": 1,
    "Mechanisms&Machines_Theory": 3,
    "Microcontrollers_Lab": 1,
    "Microcontrollers_Theory": 3,
    "LSE": 3,
    "Mahabharata": 1,
    "Math": 3,
    "Library": 1
}

# Define labs
lab_list = ["Python_Lab", "Material_Science_Lab", "Design_Lab", "Mechanisms&Machines_Lab", "Microcontrollers_Lab", "Math_Lab"]

# Color dictionary for each class
color_dict = {
    "Python_Lab": "lightblue",
    "Python_Theory": "blue",
    "Material_Science_Lab": "lightgreen",
    "Material_Science_Theory": "green",
    "Design_Lab": "lightpink",
    "Design_Theory": "pink",
    "Actuators_Drives_Theory": "yellow",
    "Mechanisms&Machines_Lab": "lightgray",
    "Mechanisms&Machines_Theory": "gray",
    "Microcontrollers_Lab": "lightcoral",
    "Microcontrollers_Theory": "coral",
    "LSE": "orange",
    "Mahabharata": "purple",
    "Math": "brown",
    "Math_Lab": "gray"
}

# Constraint for lab periods
LAB_PERIOD_SLOTS = [(0, 3), (3, 2), (5, 2)]

# Function to get available classes
def get_available_classes():
    return [cls for cls, count in class_schedule.items() if count > 0]

# Function to assign labs to appropriate slots
def assign_lab(day, period):
    available_labs = [lab for lab in lab_list if class_schedule[lab] > 0]
    
    # If no labs are available, return 0 (no lab assigned)
    if not available_labs:
        return 0

    for lab, duration in LAB_PERIOD_SLOTS:
        if period == lab and period + duration <= PERIODS_PER_DAY:
            chosen_lab = random.choice(available_labs)
            for p in range(duration):
                timetable_matrix[day][period + p] = chosen_lab
            class_schedule[chosen_lab] -= 1
            return duration
    return 0


# Function to assign theory classes
def assign_theory(day, period):
    available_classes = get_available_classes()
    chosen_class = random.choice(available_classes)
    timetable_matrix[day][period] = chosen_class
    class_schedule[chosen_class] -= 1

# Function to populate the timetable matrix
def populate_timetable():
    for day in range(DAYS):
        period = 0
        while period < PERIODS_PER_DAY:
            if period in [0, 3, 5]:  # Only assign labs in certain slots
                lab_duration = assign_lab(day, period)
                if lab_duration > 0:
                    period += lab_duration
                    continue
            assign_theory(day, period)
            period += 1

# Function to create the timetable in a Tkinter GUI
def create_gui():
    root = tk.Tk()
    root.title("Timetable")
    
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = ["1", "2", "3", "4", "5", "6", "7"]

    # Create headers for days and periods
    for i, day in enumerate(days):
        label = tk.Label(root, text=day, relief=tk.RAISED)
        label.grid(row=i+1, column=0, sticky="nsew")

    for i, period in enumerate(periods):
        label = tk.Label(root, text=period, relief=tk.RAISED)
        label.grid(row=0, column=i+1, sticky="nsew")

    spanned_cells = set()

    # Fill in the timetable matrix
    for day in range(DAYS):
        period = 0
        while period < PERIODS_PER_DAY:
            subject = timetable_matrix[day][period]
            if subject == 0:
                label = tk.Label(root, text="", relief=tk.RAISED, width=12, height=4)
                label.grid(row=day+1, column=period+1, sticky="nsew")
                period += 1
            elif (day, period) not in spanned_cells:
                color = color_dict.get(subject, "white")
                if period+2 < PERIODS_PER_DAY and timetable_matrix[day][period] == timetable_matrix[day][period+1] == timetable_matrix[day][period+2]:
                    label = tk.Label(root, text=subject, bg=color, relief=tk.RAISED, width=36, height=4)
                    label.grid(row=day+1, column=period+1, columnspan=3, sticky="nsew")
                    spanned_cells.update([(day, period), (day, period+1), (day, period+2)])
                    period += 3
                elif period+1 < PERIODS_PER_DAY and timetable_matrix[day][period] == timetable_matrix[day][period+1]:
                    label = tk.Label(root, text=subject, bg=color, relief=tk.RAISED, width=24, height=4)
                    label.grid(row=day+1, column=period+1, columnspan=2, sticky="nsew")
                    spanned_cells.update([(day, period), (day, period+1)])
                    period += 2
                else:
                    label = tk.Label(root, text=subject, bg=color, relief=tk.RAISED, width=12, height=4)
                    label.grid(row=day+1, column=period+1, sticky="nsew")
                    period += 1

    root.mainloop()

# Generate timetable and display it
populate_timetable()
create_gui()
