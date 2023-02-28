# 3D-Map-Generator
A system for converting a 2D physical map into an interactive 3D digital elevation model.  
This is the code accompanying the work published in the [DJ Strike 2021 Conference Proceedings](https://drive.google.com/file/d/1B51kWHIXxzPnldikBu8TaY4XW-epn7bi/preview) with ISBN: 978-93-5437-776-1

Abstract:  
3D modelling techniques for interacting with 3D objects that have up till now been constrained to only 2D representations, have become attractive with recent advances in computer vision. The scope of the presented work is the design and performance of a system to effectively visualize a 2D physical map by transforming it into an interactive 3D model.
The 3D digital elevation model is generated such that the height of a particular point is proportional to its whiteness on a special grayscale 2D map called a height map. The paramount task is to derive a suitable 2D height map from the physical map based on its colour conventions which are different for terrains of different heights.
This system extracts the individual terrains using the centroid-based K-Means Algorithm to cluster map colours, adaptive thresholding, edge detection, terrain contour mask creation, contour inscribing, discrete time Fourier transform and several other techniques. It is implemented through the OpenCV Python library. Suitable textures, materials and custom shades are applied to the 3D model.
