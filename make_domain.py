import subprocess
from numpy import sin, cos, pi as π
import pygmsh

geometry = pygmsh.built_in.Geometry()

δx = 0.25

a, b = 3/2, 1.
N = 256
points = [geometry.add_point([a*cos(2*π*n/N), b*sin(2*π*n/N), 0], δx)
          for n in range(N)]
lines = [geometry.add_line(points[n], points[(n + 1) % N]) for n in range(N)]

geometry.add_physical(lines[:N//4])
geometry.add_physical(lines[N // 4 : N // 2])
geometry.add_physical(lines[N // 2 : 3 * N // 4])
geometry.add_physical(lines[3 * N // 4:])
outer_line_loop = geometry.add_line_loop(lines)

N = 72
a, b = 1/4, 1/4
x, y = -1/2, 1/4
points = [geometry.add_point([a*cos(2*π*n/N) + x, b * sin(2*π*n/N) + y, 0], δx)
          for n in range(N)]
lines = [geometry.add_line(points[n], points[(n + 1) % N]) for n in range(N)]
geometry.add_physical(lines)
inner_line_loop1 = geometry.add_line_loop(lines)

N = 96
a, b = 3/8, 3/8
x, y = 1/2, -1/4
points = [geometry.add_point([a*cos(2*π*n/N) + x, b * sin(2*π*n/N) + y, 0], δx)
          for n in range(N)]
lines = [geometry.add_line(points[n], points[(n + 1) % N]) for n in range(N)]
geometry.add_physical(lines)
inner_line_loop2 = geometry.add_line_loop(lines)

plane_surface = geometry.add_plane_surface(
    outer_line_loop, holes=[inner_line_loop1, inner_line_loop2])
geometry.add_physical(plane_surface)

with open('domain.geo', 'w') as geo_file:
    geo_file.write(geometry.get_code())

subprocess.call(['gmsh', '-2', '-format', 'msh2', 'domain.geo'])
