from hkb_diamondsquare import DiamondSquare
import matplotlib.pyplot as plt
import seaborn
import cv2

def show_terrain_2D(terrain_array):

    seaborn.set()
    ax = seaborn.heatmap(terrain_array , cmap = "gray")

map = DiamondSquare.diamond_square(shape=(846,846), min_height=0, max_height=255, roughness=0.7)
cv2.imwrite('diamondsquare.png',map)
show_terrain_2D(map)
plt.show()