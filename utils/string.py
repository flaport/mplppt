#############
## Imports ##
#############

import string
import random


###############
## Functions ##
###############

def random_name(N=10):
  ''' String of N random characters '''
  return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(N))

def get_content(filename):
  ''' Get content of text file as string '''
  with open(filename, 'r') as file:
    content = file.read()
  return content