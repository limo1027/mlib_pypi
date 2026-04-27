# __init__.py

# 数学
from .smath import (pi, e, tau, phi, EPSILON, INF, gcd, lcm, factorial, comb, perm, log, ln, log10, log2, exp, sin, cos, tan, cot, sec, csc, asin, acos, atan, atan2, sinh, cosh, tanh, coth,
                    acosh, asinh, atanh,sqrt, cbrt, root, hypot, floor, ceil, trunc, clamp, lerp, inv_lerp, sign, rad, deg, fract, wrap,is_prime, prime_factors, fibonacci, product,
                    distance, angle_between, normalize_angle)
from .sfrac import Frac
from .sradical import Radical
from .svector import vec2, vec3, vec4, v2, v3, v4, lerp as vlerp
from .smatrix import Matrix, matrix, matrix_from_func
from .squaternion import Quaternion, slerp, nlerp
from .srandom import SimpleRNG, random, randint, choice, shuffle, sample
from .scolor import (
    rgb, rgba, hex_to_rgb, rgb_to_hex, hsv_to_rgb, rgb_to_hsv, lerp as color_lerp, blend, mix, grayscale, invert, adjust_brightness, adjust_saturation, adjust_hue,
    WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, CYAN, GRAY, BROWN, PINK, GOLD, MAGENTA, BACKGROUND,
    LIGHT_BLUE, LIGHT_GRAY, LIGHT_ORANGE, LIGHT_GREEN, LIGHT_BROWN, LIGHT_PINK, LIGHT_PURPLE, LIGHT_CYAN, LIGHT_YELLOW, LIGHT_CORAL,
    DARK_GREEN, DARK_BLUE, DARK_RED, DARK_GOLD, DARK_PURPLE, DARK_BROWN, DARK_CYAN, DARK_ORANGE, DARK_GRAY, DARK_PINK,
    AQUA, LAVENDER, CORAL, TEAL, INDIGO, VIOLET, MAROON, OLIVE, NAVY, LIME, FUCHSIA, SILVER,
    PRIMARY, SECONDARY, SUCCESS, WARNING, ERROR, INFO,
    TRANSPARENT,
)
from .sgeometry import Rect, Circle, Polygon, Line2, raycast_rect, reflect, rect, circle, line
from .sgeometry3d import AABB, Ray, Sphere, Plane
from .scurve import bezier, cubic_bezier, quadratic_bezier, b_spline, nurbs, bezier_path, bezier_length, curve_length
from .seasing import linear, quad_in, quad_out, cubic_in, cubic_out, bounce_out, elastic_in
from .sinterp import lerp, slerp, smoothstep, catmull_rom, hermite, remap
from .scache import LRUCache, TTLCache, memoize, RingBuffer, CacheStats
from .sevent import EventSystem, event
from .sfsm import StateMachine, State, FunctionState, StateTransition
from .spool import ObjectPool, PooledObject, AutoReleasePool, StackAllocator
from .spathfinder import astar, dijkstra, bfs, dfs_maker
from .ssaver import SGTsaver
from .sui import Label, Button, Bar
from .sformat import center, table, ordinal, number_to_english, encode, decode
from .snoise import *
from .scrypt import encrypt, decrypt
from .solver import solve_linear, solve_quadratic, solve_cubic, solve_polynomial
from .sstat import mean, median, mode, variance, stdev, correlation as stat_correlation, summary
from .sformat import *
from .seasing import EASING, tween, Tween
