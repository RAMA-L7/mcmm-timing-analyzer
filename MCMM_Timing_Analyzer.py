import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import pandas as pd

from parser import parse_mcmm_report


class TimingAnalyzerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("MCMM Timing Analyzer")
        self.root.geometry("1200x600")

        self.df = None

        # -------------------------
        # Top Controls
        # -------------------------
        frame = tk.Frame(root)
        frame.pack(fill="x")

        tk.Button(frame, text="Load Report", command=self.load_file).pack(side="left")
        tk.Button(frame, text="Show Violations", command=self.show_violations).pack(side="left")
        tk.Button(frame, text="Show Worst Path", command=self.show_worst).pack(side="left")
        tk.Button(frame, text="Export CSV", command=self.export_csv).pack(side="left")

        # Search box
        tk.Label(frame, text="Search Startpoint:").pack(side="left")
        self.search_entry = tk.Entry(frame)
        self.search_entry.pack(side="left")
        tk.Button(frame, text="Search", command=self.search_startpoint).pack(side="left")

        # Scenario filter
        tk.Label(frame, text="Scenario:").pack(side="left")
        self.scenario_combo = ttk.Combobox(frame)
        self.scenario_combo.pack(side="left")
        tk.Button(frame, text="Filter", command=self.filter_scenario).pack(side="left")

        # -------------------------
        # Table
        # -------------------------
        self.tree = ttk.Treeview(root)
        self.tree.pack(expand=True, fill="both")

        self.tree.tag_configure("violation", background="red")

    # -------------------------
    # Load File
    # -------------------------
    def load_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        try:
            self.df = parse_mcmm_report(file_path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if self.df.empty:
            messagebox.showwarning("Warning", "No data found!")
            return

        # Populate scenario dropdown
        scenarios = sorted(self.df["Scenario"].dropna().unique())
        self.scenario_combo["values"] = scenarios

        self.display_table(self.df)

    # -------------------------
    # Display Table
    # -------------------------
    def display_table(self, df):
        self.tree.delete(*self.tree.get_children())

        self.tree["columns"] = list(df.columns)
        self.tree["show"] = "headings"

        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        for _, row in df.iterrows():
            values = list(row)
            tag = "violation" if row.get("Slack", 0) < 0 else ""
            self.tree.insert("", "end", values=values, tags=(tag,))

    # -------------------------
    # Filters
    # -------------------------
    def show_violations(self):
        if self.df is not None:
            df = self.df[self.df["Slack"] < 0]
            self.display_table(df)

    def show_worst(self):
        if self.df is not None:
            worst = self.df.loc[[self.df["Slack"].idxmin()]]
            self.display_table(worst)

    def search_startpoint(self):
        if self.df is not None:
            text = self.search_entry.get()
            df = self.df[self.df["Startpoint"].str.contains(text, na=False)]
            self.display_table(df)

    def filter_scenario(self):
        if self.df is not None:
            scenario = self.scenario_combo.get()
            df = self.df[self.df["Scenario"] == scenario]
            self.display_table(df)

    # -------------------------
    # Export
    # -------------------------
    def export_csv(self):
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv")
            if file_path:
                self.df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "Exported successfully!")


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TimingAnalyzerGUI(root)
    root.mainloop()