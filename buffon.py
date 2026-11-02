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
logger.debug('This massage appears for DEBUG and VERBOSE.')
logger.log(VERBOSE, 'This message appears only for VERBOSE.'
           )

#implimenting all conditions

l = 1
d = 1
N = 100_000
rng = np.random.default_rng(44)

#defining the needle drop function
def needle_drops(l, d, N, rng):

        #creat empty lists
        
        P_head_values = []
        pi_head_values = []
        #number of crossing a line
        H = 0

        logger.debug(f'needle_drops called with l={l}, d={d}, N={N}')

        #Probability of crossing a line
        P = 2*l / (np.pi * d)
        print(P)
        
        #for loop with random nummber generator to calculate P, P_head and pi
        for j in range(1, N+1):
            
            
            #random distace from the needls center to the nearest line
            x = rng.uniform(0.0, d/2)

            #random angle between the needle and the lines
            phi = rng.uniform(0.0, np.pi/2)

            #cross condition
            crosses = x <=(l/2)*np.sin(phi)
            #if loop for crossing
            if crosses:
          
              #add the results to the lists
                H += 1

            P_head_values.append( H/j )
            if  H>0:
              
              pi_head_values.append( (2*l*j)/(d*H))
            else: 
              pi_head_values.append(np.nan)

                      # Detailed output only for the first few trials
            if j <= 10:
                logger.log(
                    VERBOSE,
                    f'Trial {j}: x={x:.4f}, phi={phi:.4f}, '
                    f'crosses={crosses}, H={H}'
                )

        logger.info(f'Finished {N} drops with {H} crossings.')

        return P_head_values, pi_head_values, H

P_head_values, pi_head_values, H = needle_drops(l, d, N, rng)

P_head_values = np.array(P_head_values)
pi_head_values = np.array(pi_head_values)

P_hat = P_head_values[-1]
pi_hat = pi_head_values[-1]

relative_error = (pi_hat - np.pi) / np.pi


#print_values
print()
print(f'l = {l}')
print(f'd = {d}')
print(f'N = {N}')
print(f'H = {H}')
print(f'Predicted crossing probability P = {2 * l / (np.pi * d):.6f}')
print(f'Measured crossing probability P_hat = {P_hat:.6f}')
print(f'Estimated pi = {pi_hat:.6f}')
print(f'Reference pi = {np.pi:.6f}')
print(f'Relative error = {relative_error:.6%}')

#plots

j_values = np.arange(1, N + 1)

# True only where the pi estimate is defined
valid_pi = ~np.isnan(pi_head_values)

fig, ax = plt.subplots()

ax.semilogx(
    j_values[valid_pi],
    pi_head_values[valid_pi],
    label=r'Running estimate $\hat{\pi}(j)$'
)

ax.axhline(
    np.pi,
    color='black',
    linestyle='--',
    label=r'Reference value $\pi$'
)

ax.set_xlabel('Number of drops j')
ax.set_ylabel(r'Estimated value $\hat{\pi}$')
ax.set_title("Buffon's Needle: Running Estimate of Pi")
ax.grid()
ax.legend()
plt.tight_layout()
plt.show()

#indipendent experiments


# Independent experiments
M = 30

# Select 500 trial values across the full range
selected_indices = np.unique(
    np.logspace(0, np.log10(N), 500, dtype=int)
) - 1

j_values = np.arange(1, N + 1)
j_selected = j_values[selected_indices]

fig2, ax2 = plt.subplots()

print()
print('M = 30')
print(f'Reference pi = {np.pi:.6f}')

for i in range(1, M + 1):

    # Each experiment gets fresh random draws
    rng2 = np.random.default_rng(i)

    P_head_values_M, pi_head_values_M, H = needle_drops(
        l, d, N, rng2
    )

    pi_head_values_M = np.array(pi_head_values_M)

    # Keep only selected values for this plot
    pi_selected = pi_head_values_M[selected_indices]

    # Do not plot undefined estimates before the first crossing
    valid_pi = ~np.isnan(pi_selected)

    ax2.semilogx(
        j_selected[valid_pi],
        pi_selected[valid_pi],
        color='tab:blue',
        alpha=0.20,
        linewidth=0.7
    )

    # Optional: print the final result of each experiment
    pi_hat_M = pi_head_values_M[-1]
    relative_error_M = (pi_hat_M - np.pi) / np.pi

    print(
        f'Experiment {i:2d}: '
        f'pi_hat = {pi_hat_M:.6f}, '
        f'relative error = {relative_error_M:.4%}'
    )

# Reference line at pi
ax2.axhline(
    np.pi,
    color='black',
    linestyle='--',
    linewidth=2,
    label=r'Reference value $\pi$'
)

ax2.set_xlabel('Number of drops j')
ax2.set_ylabel(r'Estimated value $\hat{\pi}(j)$')
ax2.set_title(r"Buffon's Needle: 30 Independent Estimates of $\pi$")
ax2.grid()
ax2.legend()

plt.tight_layout()
plt.show()

    





