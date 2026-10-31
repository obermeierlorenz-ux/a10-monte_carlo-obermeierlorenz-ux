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

#defining the needle drop function
def needle_drops(l, d, N):



        #creat empty lists
        P_values =[]
        P_head_values = []
        pi_head_values = []
        #number of crossing a line
        H = []

        #Probability of crossing a line
        P = 2*l / (np.pi * d)
        print(P)

        #for loop with random nummber generator to calculate P, P_head and pi
        for j in range(N):
            
            rng = np.random.default_rng(44)
            #random distace from the needls center to the nearest line
            x = rng.uniform(0.0, d/2)

            #random angle between the needle and the lines
            phi = rng.uniform(0.0, np.pi/2)

            #if loop for crossing
            if x <= (l/2)*np.sin(phi):
                          
                #add the results to the lists
                  H += 1
                  P_head_values += sum(H)/j
                  if  sum(H)>0:
                    pi_head_values += (2*l*j)/(d*sum(H))


        return P_head_values, pi_head_values, H

P_head_values, pi_head_values, H = needle_drops(l, d, N)

print('P:', P_head_values)
print('estimate pi', pi_head_values[-1])
print(np.pi)
print('number of crossing:', sum(H))







