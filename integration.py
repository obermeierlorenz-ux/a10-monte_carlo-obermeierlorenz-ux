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
        #or both cicles
        neither_circle = 0
        left_only = 0
        right_only = 0
        both_circles = 0
        #for loop for random numberes
        for j in range(1, N+1):

            #generate points inside the rechtangel
            x = rng.uniform(-3*R /2, 3*R /2, N)
            y = rng.uniform(R, R, N)

            #overlap condiotion and estimate aread+
            inside_left = ((x - left_center[0])**2 
                           + (y - left_center[1])**2
                           <=R**2)

            inside_right = ((x - right_center[0])**2 
                                       + (y - right_center[1])**2
                                       <=R**2)

            #append the lists if the overlap conditiosn are true 
            if inside_left & ~inside_right:
                left_only +=1

            if inside_right & ~inside_left:
                right_only  += 1

            if inside_left & inside_right:
                 both_circles +=1

            if ~inside_right  & ~inside_left:
                 neither_circle +=1

        



        
    #return lists

#calculate overlap with points in the searched rgion


