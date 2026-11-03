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
N = 10_000


#rng with seed
rng = np.random.default_rng(44)


#define shappes , rectangel and cicles#
left_center = (-R / 2, 0.0)
right_center = (R / 2, 0.0)

#def integration
def monte_carlo_integration(rng,N, R ):

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



        
    #return lists
x, y, neither_circle, left_only, right_only, both_circles = (
    monte_carlo_integration(rng, N, R)
)

#count the points in each category
n_neither = np.count_nonzero(neither_circle)
n_left = np.count_nonzero(left_only)
n_right = np.count_nonzero(right_only)
n_both = np.count_nonzero(both_circles)

#logger
logger.info(
    f'Classified {N} points: neither={n_neither}, '
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
overlap_fraction = H / N
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