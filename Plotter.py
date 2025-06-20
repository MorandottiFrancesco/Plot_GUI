import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, Listbox, Scrollbar, EXTENDED, Radiobutton, StringVar, Frame, Canvas, VERTICAL, RIGHT, LEFT, BOTH, Y, Entry, END, NW, Checkbutton, BooleanVar, OptionMenu

def plot_csv_data(csv_file):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Extract column names
    columns = df.columns.tolist()

    # Create the Tkinter window
    root = Tk()
    root.title("Select Columns to Plot")
    root.geometry("1200x600")  # Increase window size for more space

    # ===================== Axis Selection =====================
    Label(root, text="Axis Selection", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=5, columnspan=3)

    # Frame for X-axis selection with a scrollbar
    x_frame = Frame(root)
    x_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Canvas widget to allow scrolling
    x_canvas = Canvas(x_frame, width=250)  # Increase width to allow for longer names
    x_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # Scrollbar for the X-axis selection canvas
    x_scrollbar = Scrollbar(x_frame, orient=VERTICAL, command=x_canvas.yview)
    x_scrollbar.pack(side=RIGHT, fill=Y)

    # Another frame inside the canvas to hold the Radiobuttons
    x_inner_frame = Frame(x_canvas)
    x_canvas.create_window((0, 0), window=x_inner_frame, anchor=NW)

    # Variable to store selected X-axis column
    x_var = StringVar()

    # Add labels
    Label(root, text="Select X-axis:").grid(row=2, column=0)
    Label(root, text="Select Y-axis:").grid(row=2, column=1)

    # Create Radiobuttons for selecting the X-axis column inside the inner frame
    for idx, column in enumerate(columns):
        Radiobutton(x_inner_frame, text=column, variable=x_var, value=column, anchor=NW).pack(fill=BOTH)

    # Update the scroll region of the canvas whenever the content changes
    x_inner_frame.update_idletasks()
    x_canvas.config(scrollregion=x_canvas.bbox("all"))
    x_canvas.config(yscrollcommand=x_scrollbar.set)

    # Create listbox for selecting Y-axis columns with scrollbar
    y_scrollbar = Scrollbar(root, orient="vertical")
    listbox_y = Listbox(root, selectmode=EXTENDED, yscrollcommand=y_scrollbar.set, height=15, width=40)  # Increase width

    for column in columns:
        listbox_y.insert(END, column)

    listbox_y.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    y_scrollbar.grid(row=1, column=2, sticky="ns")
    y_scrollbar.config(command=listbox_y.yview)

    # Option to filter Y columns by keyword
    Label(root, text="Y-axis filter:").grid(row=2, column=2)
    y_filter_entry = Entry(root, width=20)
    y_filter_entry.grid(row=3, column=2, padx=10, pady=5)
    
    # Button to apply filter
    def apply_filter():
        filter_text = y_filter_entry.get().lower()
        listbox_y.delete(0, END)
        for column in columns:
            if filter_text in column.lower():
                listbox_y.insert(END, column)
    
    filter_button = Button(root, text="Apply Filter", command=apply_filter)
    filter_button.grid(row=4, column=2, padx=10, pady=5)

    # ===================== Label and Title Options =====================
    Label(root, text="Labels and Title", font=("Arial", 12, "bold")).grid(row=0, column=3, padx=10, pady=5, columnspan=3)

    Label(root, text="X-axis label:").grid(row=1, column=3)
    x_label_entry = Entry(root, width=20)  # Increase width
    x_label_entry.grid(row=2, column=3, padx=10, pady=5)

    Label(root, text="Y-axis label:").grid(row=1, column=4)
    y_label_entry = Entry(root, width=20)  # Increase width
    y_label_entry.grid(row=2, column=4, padx=10, pady=5)

    Label(root, text="Graph title:").grid(row=1, column=5)
    title_entry = Entry(root, width=20)  # Increase width
    title_entry.grid(row=2, column=5, padx=10, pady=5)

    # ===================== Fitting Options =====================
    Label(root, text="Fitting Options", font=("Arial", 12, "bold")).grid(row=5, column=0, padx=10, pady=5, columnspan=3)

    # Dropdown for selecting intercept option
    intercept_options = ["Variable", "Fixed to 0"]
    intercept_var = StringVar(value="Variable")
    Label(root, text="Intercept option:").grid(row=6, column=0)
    intercept_menu = OptionMenu(root, intercept_var, *intercept_options)
    intercept_menu.grid(row=6, column=1)

    # Option to enable/disable fitting
    fit_var = BooleanVar()
    Checkbutton(root, text="Enable Fitting", variable=fit_var).grid(row=7, column=0)

    # Option to plot fit line or not
    plot_fit_var = BooleanVar()
    Checkbutton(root, text="Plot Fit Line", variable=plot_fit_var).grid(row=7, column=1)

    # ===================== Additional Options =====================
    Label(root, text="Additional Options", font=("Arial", 12, "bold")).grid(row=8, column=0, padx=10, pady=5, columnspan=3)

    # Checkboxes for gridlines and fix zero
    grid_var = BooleanVar()
    Checkbutton(root, text="Show Grid", variable=grid_var).grid(row=9, column=0)

    fix_zero_var = BooleanVar()
    Checkbutton(root, text="Fix zero (Add (0,0))", variable=fix_zero_var).grid(row=9, column=1)

    # ===================== Plot Button =====================
    Button(root, text="Plot", command=lambda: plot_selected()).grid(row=10, column=3, padx=10, pady=20, columnspan=2)

    # ===================== Plotting Function =====================
    def plot_selected():
        selected_x = x_var.get()
        selected_y = [listbox_y.get(i) for i in listbox_y.curselection()]
        slopes = []

        if not selected_x or not selected_y:
            print("Please select both X and Y columns.")
            return

        # Get custom labels and title
        x_label = x_label_entry.get() if x_label_entry.get() else selected_x
        y_label = y_label_entry.get() if y_label_entry.get() else ', '.join(selected_y)
        title = title_entry.get() if title_entry.get() else f'{selected_x} vs {" & ".join(selected_y)}'

        # Apply Y-axis filter if provided
        y_filter = y_filter_entry.get().lower()
        if y_filter:
            selected_y = [col for col in columns if y_filter in col.lower()]

        # Initialize slope variable
        m = 0
        b = 0

        # Plot each selected Y against the selected X and perform linear fit
        plt.figure(figsize=(12, 8))
        for y in selected_y:
            x_data = pd.to_numeric(df[selected_x], errors='coerce')
            y_data = pd.to_numeric(df[y], errors='coerce')

            # Apply fix zero if selected
            if fix_zero_var.get():
                x_data = np.insert(x_data, 0, 0)
                y_data = np.insert(y_data, 0, 0)

            # Perform fitting if enabled
            if fit_var.get():
                if intercept_var.get() == "Fixed to 0":
                    m, _ = np.polyfit(x_data, y_data, 1, full=False)
                    b = 0
                else:  # Variable intercept
                    m, b = np.polyfit(x_data, y_data, 1, full=False)

                # Plot the fit line if selected
                if plot_fit_var.get():
                    plt.plot(x_data, m * x_data + b, linestyle='--', label=f'Fit: y={m:.2e}x+{b:.2e}')
            else:
                # Plot data without fitting line
                plt.plot(x_data, y_data, label=y)

            slopes.append(m)

        # Show grid if selected
        if grid_var.get():
            plt.grid(True)

        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.show()

        # Print slope and intercept values and statistics in scientific notation
        print("Fit results (m and b) for each line:")
        for y, m in zip(selected_y, slopes):
            print(f"{y}: m={m:.4e}, b={b:.4e}")  # Display in scientific notation

        print("\nSlope Statistics:")
        print(f"Min slope: {min(slopes):.4e}")
        print(f"Max slope: {max(slopes):.4e}")
        print(f"Average slope: {np.mean(slopes):.4e}")

    root.mainloop()

# Example usage:
plot_csv_data('C:\\Users\\moran\\OneDrive\\Documenti\\Phyton Scripts\\Plot GUI\\LUT_DATA.txt')

