import tkinter as tk
from tkinter import messagebox

def choose_bar_size():
    try:
        bar_size_meters = float(bar_size_entry.get())
        bar_size_cm = bar_size_meters * 100  # Convert to centimeters
        output_text.insert(tk.END, f"You have chosen a bar size of {bar_size_cm} centimeters.\n")
        return bar_size_cm
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for the bar size.")
        return None

def add_element():
    dimensions = dimensions_entry.get()
    quantity = quantity_entry.get()

    if dimensions.strip() == '0':
        return

    try:
        dimensions_list = [float(dim) for dim in dimensions.split(',')]
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter comma-separated numbers for dimensions.")
        return

    try:
        quantity = int(quantity)
        if quantity == 0:
            return
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number for quantity.")
        return

    elements.append({'dimensions': dimensions_list, 'quantity': quantity})
    output_text.insert(tk.END, f"Added element: Dimensions {dimensions_list}, Quantity {quantity}\n")

    # Clear the input fields after adding the element
    dimensions_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)

def optimize_cutting():
    bar_size = choose_bar_size()
    if bar_size is None:
        return

    remainders, bar_cuts = optimize_cutting_logic(bar_size, elements)

    output_text.insert(tk.END, "\nSummary:\n")
    output_text.insert(tk.END, f"Bar size: {bar_size} centimeters\n")
    output_text.insert(tk.END, "Elements:\n")
    for element in elements:
        output_text.insert(tk.END, f"  Dimensions: {element['dimensions']}, Quantity: {element['quantity']}\n")
    output_text.insert(tk.END, "Bars used:\n")
    for i, (remaining_length, cuts) in enumerate(zip(remainders, bar_cuts)):
        output_text.insert(tk.END, f"  Bar {i+1}:\n")
        for j, length in enumerate(cuts):
            output_text.insert(tk.END, f"    Cut {j+1}: {length} centimeters\n")
        output_text.insert(tk.END, f"    Total length used: {bar_size - remaining_length} centimeters, Remaining length: {remaining_length} centimeters\n")

def optimize_cutting_logic(bar_size, elements):
    CUT_WIDTH = 0.5  # Width of the cutting machine in centimeters
    element_details = []

    for element in elements:
        for _ in range(element['quantity']):
            dimensions = element['dimensions']
            if len(dimensions) == 2:
                # Duplicate each dimension to represent four sides
                dimensions = [dimensions[0], dimensions[1], dimensions[0], dimensions[1]]
            element_details.extend(dimensions)

    # Sort elements by length in descending order
    element_details.sort(reverse=True)

    remainders = [bar_size]  # Initialize remainders with the first bar
    bar_cuts = [[]]  # Cuts corresponding to each bar

    for length in element_details:
        placed = False
        for i in range(len(remainders)):
            if remainders[i] >= length:
                remainders[i] -= (length + CUT_WIDTH)
                bar_cuts[i].append(length)
                placed = True
                break

        if not placed:
            remainders.append(bar_size - (length + CUT_WIDTH))
            bar_cuts.append([length])

    return remainders, bar_cuts

# GUI Setup
root = tk.Tk()
root.title("Bar Cutting Optimizer")

# Bar size input
bar_size_label = tk.Label(root, text="Enter the bar size (in meters):")
bar_size_label.pack()

bar_size_entry = tk.Entry(root)
bar_size_entry.pack()

# Element input
dimensions_label = tk.Label(root, text="Enter the dimensions of the element (comma-separated):")
dimensions_label.pack()

dimensions_entry = tk.Entry(root)
dimensions_entry.pack()

quantity_label = tk.Label(root, text="Enter the quantity of the element:")
quantity_label.pack()

quantity_entry = tk.Entry(root)
quantity_entry.pack()

add_element_button = tk.Button(root, text="Add Element", command=add_element)
add_element_button.pack()

# Output area
output_text = tk.Text(root, height=20, width=60)
output_text.pack()

# Calculate button
calculate_button = tk.Button(root, text="Optimize Cutting", command=optimize_cutting)
calculate_button.pack()

elements = []

# Run the Tkinter event loop
root.mainloop()
