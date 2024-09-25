import random
import tkinter as tk

# 5 days, 7 periods per day
matrix = [[0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0]]

# Total theory and lab sessions per week
class_schedule = {
    "Math": [3, 1],
    "Python": [1, 1],
    "Material_Science": [2, 1],
    "Design": [1, 1],
    "Actuators_Drives": [3, 0],
    "Mechanisms&Machines": [3, 1],
    "Microcontrollers": [3, 1],
    "LSE": [3, 0],
    "Mahabharata": [1, 0],
    "Library": [1, 0]
}

# Generate lablist by adding "_Lab" to subjects that have labs
lablist = [subject + "_Lab" for subject, counts in class_schedule.items() if counts[1] > 0]
def generate_timetable(matrix, class_schedule, lablist):
# Randomly assign classes to periods while tracking counts
    for j in range(5):  # For each day
        i = 0
        while i < 7:  # For each period in a day
            # Filter out classes with no remaining sessions
            available_classes = [cls for cls, counts in class_schedule.items() if counts[0] > 0 or counts[1] > 0]
            print(available_classes)
            if not available_classes:
                break  # Stop if there are no more classes to schedule

            choice = random.choice(available_classes)  # Choose a random class
            is_lab = False
            # Check if it's a lab
            if class_schedule[choice][1] > 0:
                is_lab = True
            
            if is_lab:
                # Schedule lab sessions (spanning multiple periods)
                if i == 0:  # Labs can only be placed in first, fourth, or sixth periods
                    matrix[j][i] = matrix[j][i + 1] = matrix[j][i + 2] = choice + "_Lab"
                    class_schedule[choice][1] -= 1  # Reduce lab count after scheduling
                    if class_schedule[choice][1] == 0 and class_schedule[choice][0] == 0:
                        del class_schedule[choice]  # Remove class if both counts are zero
                    i += 3
                elif i == 3:
                    if matrix[j][0] not in lablist:
                        matrix[j][i] = matrix[j][i + 1] = choice + "_Lab"
                        class_schedule[choice][1] -= 1
                        if class_schedule[choice][1] == 0 and class_schedule[choice][0] == 0:
                            del class_schedule[choice]
                        i += 2
                elif i == 5:
                    if matrix[j][3] not in lablist:
                        matrix[j][i] = matrix[j][i + 1] = choice + "_Lab"
                        class_schedule[choice][1] -= 1
                        if class_schedule[choice][1] == 0 and class_schedule[choice][0] == 0:
                            del class_schedule[choice]
                        i += 2
                else:
                    continue
            else:
                # Schedule theory class
                matrix[j][i] = choice  # Place theory class
                class_schedule[choice][0] -= 1  # Reduce theory count
                if class_schedule[choice][0] == 0 and class_schedule[choice][1] == 0:
                    del class_schedule[choice]  # Remove class if both counts are zero)
                i += 1
    remaining_classes = [cls for cls, counts in class_schedule.items() if counts[0] > 0 or counts[1] > 0]
    print("The remaining classes are:")
    print(remaining_classes)
    return matrix
MatA=generate_timetable(matrix, class_schedule, lablist)
def create_timetable_gui(matrix):
    # Color dictionary for each class
    color_dict = {
        "Python_Lab": "lightblue",
        "Python": "blue",
        "Material_Science_Lab": "lightgreen",
        "Material_Science": "green",
        "Design_Lab": "lightpink",
        "Design": "pink",
        "Actuators_Drives": "yellow",
        "Mechanisms&Machines_Lab": "lightgray",
        "Mechanisms&Machines": "gray",
        "Microcontrollers_Lab": "lightcoral",
        "Microcontrollers": "coral",
        "LSE": "orange",
        "Mahabharata": "purple",
        "Math": "brown",
        "Math_Lab": "gray",
        "Library": "red"
    }

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Timetable")

    # Days and periods headers
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    periods = ["1", "2", "3", "4", "5", "6", "7"]

    # Create headers for days and periods
    for i, day in enumerate(days):
        label = tk.Label(root, text=day, relief=tk.RAISED)
        label.grid(row=i + 1, column=0, sticky="nsew")

    for i, period in enumerate(periods):
        label = tk.Label(root, text=period, relief=tk.RAISED)
        label.grid(row=0, column=i + 1, sticky="nsew")

    # Keep track of already spanned cells
    spanned_cells = set()

    # Fill in the timetable with the classes and colors
    for i in range(5):  # Days
        j = 0  # Periods
        while j < 7:
            subject = matrix[i][j]

            if subject == 0:
                label = tk.Label(root, text="", relief=tk.RAISED, width=12, height=4)
                label.grid(row=i + 1, column=j + 1, sticky="nsew")
                j += 1  # Move to the next period
            elif (i, j) not in spanned_cells:  # Check if this cell is part of a previously spanned cell
                color = color_dict.get(subject, "white")  # Default to white if not found in color_dict

                # Check if the subject spans multiple periods (i.e., lab)
                if j + 2 < 7 and matrix[i][j] == matrix[i][j + 1] == matrix[i][j + 2]:  # Lab spanning 3 periods
                    label = tk.Label(root, text=subject, bg=color, relief=tk.RAISED, width=36, height=4)
                    label.grid(row=i + 1, column=j + 1, columnspan=3, sticky="nsew")
                    spanned_cells.update([(i, j), (i, j + 1), (i, j + 2)])  # Mark these cells as spanned
                    j += 3  # Move forward by 3 periods
                elif j + 1 < 7 and matrix[i][j] == matrix[i][j + 1]:  # Lab spanning 2 periods
                    label = tk.Label(root, text=subject, bg=color, relief=tk.RAISED, width=24, height=4)
                    label.grid(row=i + 1, column=j + 1, columnspan=2, sticky="nsew")
                    spanned_cells.update([(i, j), (i, j + 1)])  # Mark these cells as spanned
                    j += 2  # Move forward by 2 periods
                else:  # Single period class (theory)
                    label = tk.Label(root, text=subject, bg=color, relief=tk.RAISED, width=12, height=4)
                    label.grid(row=i + 1, column=j + 1, sticky="nsew")
                    j += 1  # Move to the next period

    # Run the application
    root.mainloop()
create_timetable_gui(MatA)
