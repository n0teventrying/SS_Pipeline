import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
except ImportError:
    messagebox.showerror("Missing Module", "Please install tkinterdnd2: pip install tkinterdnd2")
    raise

class InteractivePlotApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        
        # Create the figure and plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        
        self.scatter = self.ax.scatter(self.data['x'], self.data['y'], picker=True, color='blue', s=100)
        self.canvas.mpl_connect('pick_event', self.on_pick)
        
        # Add save button
        self.save_button = tk.Button(root, text="Save to CSV", command=self.save_to_csv)
        self.save_button.pack()

        self.redraw_plot()

    def on_pick(self, event):
        ind = event.ind[0]  # Get index of picked point
        x, y = self.data.loc[ind, ['x', 'y']]
        if messagebox.askyesno("Delete Point", f"Delete point ({x}, {y})?"):
            self.data = self.data.drop(index=ind).reset_index(drop=True)
            self.redraw_plot()
    
    def redraw_plot(self):
        self.ax.clear()
        self.ax.scatter(self.data['x'], self.data['y'], picker=True, color='blue', s=100)
        self.ax.set_title("Click a point to delete it")
        self.canvas.draw()

    def save_to_csv(self):
        filename = simpledialog.askstring("Save CSV", "Enter filename (without extension):")
        if filename:
            self.data.to_csv(f"{filename}.csv", index=False)
            messagebox.showinfo("Success", f"Data saved to {filename}.csv")
        else:
            messagebox.showwarning("Canceled", "Save operation canceled")

def load_csv_from_explorer():
    filepath = filedialog.askopenfilename(
        title="Select a CSV File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
    )
    if filepath:
        return validate_and_load_csv(filepath)
    return None

def validate_and_load_csv(filepath):
    try:
        data = pd.read_csv(filepath)
        if 'x' in data.columns and 'y' in data.columns:
            return data
        else:
            messagebox.showerror("Invalid Data", "CSV must contain 'x' and 'y' columns.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV: {e}")
    return None

def on_drop(event, root):
    filepath = event.data.strip()
    if filepath.endswith('.csv'):
        data = validate_and_load_csv(filepath)
        if data is not None:
            app = InteractivePlotApp(root, data)
    else:
        messagebox.showerror("Invalid File", "Only CSV files are supported.")

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Enable drag-and-drop

    # Set the window title dynamically
    window_title = simpledialog.askstring("Window Title", "Enter window title:")
    if window_title:
        root.title(window_title)
    else:
        root.title("Interactive Plot with Tkinter")

    # Add a button for loading via explorer
    load_button = tk.Button(root, text="Load CSV via Explorer", command=lambda: InteractivePlotApp(root, load_csv_from_explorer()) if load_csv_from_explorer() else None)
    load_button.pack()

    # Enable drag-and-drop
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', lambda e: on_drop(e, root))

    root.mainloop()