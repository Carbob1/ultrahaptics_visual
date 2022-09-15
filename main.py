import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

PATH = r"C:\Users\Admin\Desktop\DOK\Kąty.xlsx"
SHEET_NAME = "M1"

# draw half-sphere
fig = plt.figure(figsize=[10, 8])
ax = fig.add_subplot(projection='3d')
ax.set_box_aspect(aspect=(1, 1, 0.5))

u, v = np.mgrid[0:2 * np.pi:25j, 0:np.pi:25j]
x = np.cos(u) * np.sin(v) * 0.9
y = np.sin(u) * np.sin(v) * 0.9
z = abs(np.cos(v)) * 0.9

plt.axis('off')

ax.plot_surface(x, y, z-np.min(z), color=[0, 0, 0], alpha=0.3)


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
df = pd.read_excel(PATH, sheet_name=SHEET_NAME)

values = [df.iloc[10, 12]]
for r in range(9, 3, -1):
    values.append(df.iloc[r, 2])

for c in range(11, 2, -1):
    for r in range(9, 3, -1):
        values.append(df.iloc[r, c])

# r = 3
# c = 2
# print(f"Wartosc z {c} kolumny, {r} rzedu: {df.iloc[r, c]}")

p = ax.scatter(points_x, points_y, points_z, c=values, cmap=plt.cm.RdYlGn_r)
ax.set_facecolor((0.5, 0.5, 0.5))

ax.text2D(0.03, 0.95, f"Object: {df.columns[2]}", transform=ax.transAxes, size=13, color="white")
print(df.columns[2])

# index = 10
# ax.scatter(points_x[index], points_y[index], points_z[index], cmap=plt.cm.magma, s=100)
fig.colorbar(p)

plt.show()


