from abaqus import *
from explicitsim import dynamic_explicit
import sys


a = sys.argv[-3]
b = sys.argv[-2]
c = sys.argv[-1]

dynamic_explicit(a,b,c)