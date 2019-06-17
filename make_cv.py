import subprocess
import pygmsh

geometry = pygmsh.built_in.Geometry()

δx = 0.01

coords = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]]
points = [geometry.add_point(coord, δx) for coord in coords]
lines = [geometry.add_line(points[n], points[(n + 1) % len(points)])
         for n in range(len(points))]
geometry.add_physical(lines)
line_loop = geometry.add_line_loop(lines)

r = 0.25
center = geometry.add_point([0.5, 0.5, 0], δx)
coords = [[0.75, 0.5, 0], [0.5, 0.75, 0], [0.25, 0.5, 0], [0.5, 0.25, 0]]
points = [geometry.add_point(coord, δx) for coord in coords]
arcs = [geometry.add_circle_arc(points[n], center, points[(n + 1) % len(points)])
        for n in range(len(points))]
#geometry.add_physical(arcs)

plane_surface = geometry.add_plane_surface(line_loop)
geometry.add_physical(plane_surface)

with open('cv.geo', 'w') as geo_file:
    geo_file.write(geometry.get_code())

subprocess.call(['gmsh', '-2', '-format', 'msh2', 'cv.geo'])
