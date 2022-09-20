from tkinter import *
from tkinter.filedialog import askopenfilename
import matplotlib
import numpy as np
import pandas as pd


matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

root = Tk()

def update_label(label, new_text, column, row):
    label.grid_forget()
    label["text"] = new_text
    label.grid(column=column, row=row)


class Gui:
    def __init__(self):
        self.frame_main = LabelFrame(root, padx=5, pady=5)
        self.frame_main.grid(row=0, column=1, padx=40)

        self.frame = LabelFrame(self.frame_main, padx=5, pady=5)
        self.frame.grid(row=0, column=2, padx=40)

        self.frame2 = LabelFrame(self.frame_main, padx=5, pady=5)
        self.frame2.grid(row=1, column=2, padx=40)

        self.frame3 = LabelFrame(self.frame_main, padx=5, pady=5)
        self.frame3.grid(row=2, column=2, padx=40)

        self.generate_button = Button(self.frame3, text="Generuj wizualizację", command=self.get_plot)
        self.generate_button.grid(row=0, column=0)


        self.M1_button = Button(self.frame2, text="M1", command=lambda: self.get_sheet_name("M1"))
        self.M2_button = Button(self.frame2, text="M2", command=lambda: self.get_sheet_name("M2"))
        self.M3_button = Button(self.frame2, text="M3", command=lambda: self.get_sheet_name("M3"))
        self.L1_button = Button(self.frame2, text="L1", command=lambda: self.get_sheet_name("L1"))
        self.L2_button = Button(self.frame2, text="L2", command=lambda: self.get_sheet_name("L2"))
        self.H1_button = Button(self.frame2, text="H1", command=lambda: self.get_sheet_name("H1"))
        self.H2_button = Button(self.frame2, text="H2", command=lambda: self.get_sheet_name("H2"))

        self.M1_button.grid(row=0, column=0)
        self.M2_button.grid(row=0, column=1)
        self.M3_button.grid(row=0, column=2)
        self.L1_button.grid(row=1, column=0)
        self.L2_button.grid(row=1, column=1)
        self.H1_button.grid(row=2, column=0)
        self.H2_button.grid(row=2, column=1)

        self.sheet_name_label1 = Label(self.frame2)
        update_label(self.sheet_name_label1, "Wybrana karta:", column=4, row=0)

        self.sheet_name_label = Label(self.frame2)
        self.sheet_name = "Nie wybrano karty"
        update_label(self.sheet_name_label, self.sheet_name, column=4, row=1)

        self.path_label = Label(self.frame)
        self.path = "Nie wybrano pliku"
        update_label(self.path_label, self.path, column=0, row=1)

        self.get_path_button = Button(self.frame, text="Wybierz plik", command=self.get_path)
        self.get_path_button.grid(row=0, column=0)

    def get_path(self):
        self.path = askopenfilename()
        update_label(self.path_label, self.path, 0, 1)

    def get_plot(self):
        path = rf"{self.path}"
        sheet_name = self.sheet_name

        # draw half-sphere
        fig = Figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(projection='3d')
        ax.set_box_aspect(aspect=(1, 1, 0.5))

        u, v = np.mgrid[0:2 * np.pi:25j, 0:np.pi:25j]
        x = np.cos(u) * np.sin(v) * 0.9
        y = np.sin(u) * np.sin(v) * 0.9
        z = abs(np.cos(v)) * 0.9

        # fig.axis('off')

        ax.plot_surface(x, y, z - np.min(z), color=[0, 0, 0], alpha=0.3)

        # points
        u, v = np.mgrid[0:2 * np.pi:25j, 0:np.pi:13j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = abs(np.cos(v))

        points_x = [0]
        points_y = [0]
        points_z = [1]

        def join_vectors(points, vector):
            def add_numbers(points, vector):
                for num in vector[1:7]:
                    points.append(num)

            def join_multiple(points, vector, start, stop):
                for i in range(start, stop):
                    add_numbers(points, vector[i])

            add_numbers(points, vector[9])
            add_numbers(points, vector[15])
            join_multiple(points, vector, 18, 25)
            add_numbers(points, vector[3])

        join_vectors(points_x, x)
        join_vectors(points_y, y)
        join_vectors(points_z, z)

        # excel
        df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")

        values = [df.iloc[10, 12]]
        for r in range(9, 3, -1):
            values.append(df.iloc[r, 2])

        for c in range(11, 2, -1):
            for r in range(9, 3, -1):
                values.append(df.iloc[r, c])

        # r = 3
        # c = 2
        # print(f"Wartosc z {c} kolumny, {r} rzedu: {df.iloc[r, c]}")

        p = ax.scatter(points_x, points_y, points_z, c=values, cmap="RdYlGn_r")
        ax.set_facecolor((0.5, 0.5, 0.5))

        ax.text2D(0.03, 0.95, f"Object: {df.columns[2]}", transform=ax.transAxes, size=13, color="white")

        # index = 10
        # ax.scatter(points_x[index], points_y[index], points_z[index], cmap=plt.cm.magma, s=100)
        fig.colorbar(p)


        figure_canvas = FigureCanvasTkAgg(fig, root)
        figure_canvas.get_tk_widget().grid(column=0, row=0)



    def get_sheet_name(self, sheet_name):
        self.sheet_name = sheet_name
        update_label(self.sheet_name_label, self.sheet_name, 4, 1)


gui = Gui()
root.mainloop()
