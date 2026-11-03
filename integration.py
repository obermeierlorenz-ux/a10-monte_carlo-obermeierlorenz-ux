import numpy as np
import matplotlib.pyplot as plt

import argparse 
import logging

VERBOSE = 5
logging.addLevelName(VERBOSE, 'VERBOSE')

parser = argparse.ArgumentParser()

#different arguments possible at the beginning of my program
parser.add_argument('--log-level',
                    choices = ['INFO', 'DEBUG', 'VERBOSE'],
                    default = 'INFO')

#reads the arg of the terminal
args = parser.parse_args()

#translation of the text in the terminal to the nummer 5, 10 , 20
level_values = {'INFO': logging.INFO, 
                'DEBUG': logging.DEBUG,
                'VERBOSE': VERBOSE}

#determines which message is displayed
logging.basicConfig(level = level_values[args.log_level],
                    format = '%(levelname)s: %(message)s')

#erstellt den logger der im restlichen Code benutzt wird
logger = logging.getLogger(__name__)

#outputs for the possible loggers
logger.info('Program started')

#  boundry conditions
R = 1.0
N_circles = 10_000
N_spheres = 100_000


#rng with seed
rng = np.random.default_rng(44)


#define shappes , rectangel and cicles#
left_center = (-R / 2, 0.0)
right_center = (R / 2, 0.0)

#def integration
def monte_carlo_circle(rng,N, R ):

    #empty lists for neither circel, left cicle, right cicle
    #or both cicles -> bot nessecary because i now do it with arrays

    #for loop for random numberes
    logger.debug(f'monte_carlo_integration called with N={N}, R={R}')
    #generate points inside the rechtangel ->array

    x = rng.uniform(-3*R /2, 3*R /2, N)
    y = rng.uniform(-R, R, N)

    #overlap condiotion and estimate aread+
    inside_left = ((x - left_center[0])**2 
                    + (y - left_center[1])**2
                    <=R**2)

    inside_right = ((x - right_center[0])**2 
                                + (y - right_center[1])**2
                                <=R**2)

    #append the lists if the overlap conditiosn are true 
    # Four mutually exclusive point categories

    neither_circle = ~inside_left & ~inside_right
    left_only = inside_left & ~inside_right
    right_only = ~inside_left & inside_right
    both_circles = inside_left & inside_right

    logger.log(VERBOSE,
    f'First point: x={x[0]:.4f}, y={y[0]:.4f}, '
    f'in left={inside_left[0]}, in right={inside_right[0]}'
    )


    return x, y, neither_circle, left_only, right_only, both_circles



def monte_carlo_spheres(rng, N, R):

    logger.debug(f'monte_carlo_spheres called with N={N}, R={R}')

    # Centers of all three spheres
    center_1 = (-R / 2, 0.0, 0.0)
    center_2 = (R / 2, 0.0, 0.0)
    center_3 = (0.0, R / 2, 0.0)

    # #generate points inside the shapes in 3d ->array
    x = rng.uniform(-R / 2, R / 2, N)
    y = rng.uniform(-R, R, N)
    z = rng.uniform(-R, R, N)

    # Membership in sphere 1
    inside_1 = (
        (x - center_1[0])**2
        + (y - center_1[1])**2
        + (z - center_1[2])**2
        <= R**2
    )

    # Membership in sphere 2
    inside_2 = (
        (x - center_2[0])**2
        + (y - center_2[1])**2
        + (z - center_2[2])**2
        <= R**2
    )

    # Membership in sphere 3
    inside_3 = (
        (x - center_3[0])**2
        + (y - center_3[1])**2
        + (z - center_3[2])**2
        <= R**2
    )

    # Intersection of the first two spheres
    inside_two_spheres = inside_1 & inside_2

    # Intersection of all three spheres
    inside_three_spheres = inside_1 & inside_2 & inside_3

    # Bounding-box volume
    V_box = 4 * R**3

    # Two-sphere estimate
    H_2 = np.count_nonzero(inside_two_spheres)
    p_hat_2 = H_2 / N
    V_hat_2 = V_box * p_hat_2

    # Three-sphere estimate
    H_3 = np.count_nonzero(inside_three_spheres)
    p_hat_3 = H_3 / N
    V_hat_3 = V_box * p_hat_3

    # Running estimate of the two-sphere volume
    j_values = np.arange(1, N + 1)
    H_2_running = np.cumsum(inside_two_spheres)
    V_2_running = V_box * H_2_running / j_values

    logger.log(
        VERBOSE,
        f'First point: x={x[0]:.4f}, y={y[0]:.4f}, z={z[0]:.4f}, '
        f'in two spheres={inside_two_spheres[0]}, '
        f'in three spheres={inside_three_spheres[0]}'
    )

    logger.info(
        f'Sphere simulation finished: '
        f'H_2={H_2}, H_3={H_3}, '
        f'V_hat_2={V_hat_2:.6f}, V_hat_3={V_hat_3:.6f}'
    )

    return (
        H_2, p_hat_2, V_hat_2, V_2_running,
        H_3, p_hat_3, V_hat_3,
        inside_two_spheres, inside_three_spheres
    )


        
    #return lists
x, y, neither_circle, left_only, right_only, both_circles = (
    monte_carlo_circle(rng, N_circles, R)
)

#count the points in each category
n_neither = np.count_nonzero(neither_circle)
n_left = np.count_nonzero(left_only)
n_right = np.count_nonzero(right_only)
n_both = np.count_nonzero(both_circles)

#logger
logger.info(
    f'Classified {N_circles} points: neither={n_neither}, '
    f'left only={n_left}, right only={n_right}, '
    f'both={n_both}'
)

print('Neither circle:', n_neither)
print('Left circle only:', n_left)
print('Right circle only:', n_right)
print('Both circles:', n_both)
print('Total:', n_neither + n_left + n_right + n_both)

# Area of the bounding rectangle

A_B = 6 * R**2

# H is the number of points in both circles
H = n_both


# Monte carlo overlap fraction and area estimate
overlap_fraction = H / N_circles
A_hat = A_B * overlap_fraction

# Exact reference overlap area
A_reference = (
    (2 * np.pi / 3) - (np.sqrt(3) / 2)
) * R**2

relative_error = (A_hat - A_reference) / A_reference

print()
print(f'Bounding rectangle area A_B: {A_B:.6f}')
print(f'Overlap count H: {H}')
print(f'Overlap fraction H / N: {overlap_fraction:.6f}')
print(f'Estimated overlap area A_hat: {A_hat:.6f}')
print(f'Reference overlap area: {A_reference:.6f}')
print(f'Relative error: {relative_error:.6%}')

logger.info(
    f'Overlap estimate: H={H}, fraction={overlap_fraction:.6f}, '
    f'A_hat={A_hat:.6f}, relative error={relative_error:.4%}'
)

print('Difference between left-only and right-only:', abs(n_left - n_right))

#plot
# Circle boundaries for the plot
theta = np.linspace(0, 2 * np.pi, 300)

left_circle_x = left_center[0] + R * np.cos(theta)
left_circle_y = left_center[1] + R * np.sin(theta)

right_circle_x = right_center[0] + R * np.cos(theta)
right_circle_y = right_center[1] + R * np.sin(theta)

# Scatter plot
fig, ax = plt.subplots()

ax.scatter(
    x[neither_circle], y[neither_circle],
    s=4, alpha=0.25,
    label='Neither circle'
)

ax.scatter(
    x[left_only], y[left_only],
    s=4, alpha=0.25,
    label='Left circle only'
)

ax.scatter(
    x[right_only], y[right_only],
    s=4, alpha=0.25,
    label='Right circle only'
)

ax.scatter(
    x[both_circles], y[both_circles],
    s=4, alpha=0.35,
    label='Both circles'
)

# Circle boundaries
ax.plot(left_circle_x, left_circle_y, color='black')
ax.plot(right_circle_x, right_circle_y, color='black')

# Circle centers
ax.plot(
    left_center[0], left_center[1],
    marker='x', color='black',
    markersize=8, linestyle='none',
    label='Circle centers'
)

ax.plot(
    right_center[0], right_center[1],
    marker='x', color='black',
    markersize=8, linestyle='none'
)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Monte Carlo Sampling of Two Overlapping Circles')
ax.set_aspect('equal', adjustable='box')
ax.grid()
ax.legend(markerscale=2)

plt.tight_layout()
plt.show()

#spereical
(H_2,p_hat_2,V_hat_2,V_2_running,H_3,
 p_hat_3,V_hat_3,inside_two_spheres,inside_three_spheres
 ) = monte_carlo_spheres(rng, N_spheres, R)


# Exact reference for the two-sphere volume
V_2_reference = (5 * np.pi / 12) * R**3

relative_error_2 = (
    (V_hat_2 - V_2_reference) / V_2_reference
)

print()
print('Two offset spheres')
print(f'H_2 = {H_2}')
print(f'p_hat_2 = {p_hat_2:.6f}')
print(f'V_hat_2 / R^3 = {V_hat_2 / R**3:.6f}')
print(f'Reference V_2 / R^3 = {V_2_reference / R**3:.6f}')
print(f'Relative error for V_2 = {relative_error_2:.6%}')

print()
print('Three offset spheres')
print(f'H_3 = {H_3}')
print(f'p_hat_3 = {p_hat_3:.6f}')
print(f'V_hat_3 / R^3 = {V_hat_3 / R**3:.6f}')

#checks
V_box = 4 * R**3

# Every three-sphere hit must also be a two-sphere hit
subset_check = np.all(
    ~inside_three_spheres | inside_two_spheres
)

# Expected order of the estimated volumes
volume_order_check = (
    0 < V_hat_3 <= V_hat_2 < V_box
)

print()
print('Every three-sphere hit is a two-sphere hit:', subset_check)
print('Volume order 0 < V_3 <= V_2 < V_box:', volume_order_check)

center_1 = np.array([-R / 2, 0.0, 0.0])
center_2 = np.array([R / 2, 0.0, 0.0])
center_3 = np.array([0.0, R / 2, 0.0])

# Inside all three spheres
point_inside_all = np.array([0.0, 0.0, 0.0])

# Inside spheres 1 and 2, but outside sphere 3
point_inside_two_not_three = np.array([0.0, -0.75, 0.0])

# Outside all three spheres
point_outside_all = np.array([0.0, 2.0, 0.0])

def point_in_sphere(point, center):
    return np.sum((point - center)**2) <= R**2

print()
print('Origin is inside all three spheres:',
      point_in_sphere(point_inside_all, center_1)
      and point_in_sphere(point_inside_all, center_2)
      and point_in_sphere(point_inside_all, center_3))

print('Test point is inside spheres 1 and 2, but outside sphere 3:',
      point_in_sphere(point_inside_two_not_three, center_1)
      and point_in_sphere(point_inside_two_not_three, center_2)
      and not point_in_sphere(point_inside_two_not_three, center_3))

print('Outside point is outside all three spheres:',
      not point_in_sphere(point_outside_all, center_1)
      and not point_in_sphere(point_outside_all, center_2)
      and not point_in_sphere(point_outside_all, center_3))

#plot
j_values = np.arange(1, N_spheres + 1)

fig, ax = plt.subplots()
ax.semilogx(
    j_values,
    V_2_running / R**3,
    label=r'Running estimate $\hat{V}_2 / R^3$'
)

ax.axhline(
    V_2_reference / R**3,
    color='black',
    linestyle='--',
    label=r'Reference value $5\pi/12$'
)

ax.set_xlabel('Number of samples j')
ax.set_ylabel(r'Volume $\hat{V}_2 / R^3$')
ax.set_title('Monte Carlo Estimate of Shared Sphere Volume')
ax.grid()
ax.legend()

plt.tight_layout()
plt.show()