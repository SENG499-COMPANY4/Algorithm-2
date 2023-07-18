import sys
import os

# Get the name of the directory where the file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Get the parent directory name where the current directory is present.
parent = os.path.dirname(current)
 
# Add the parent directory to the sys.path.
sys.path.append(parent)
 
# Import the module in the parent directory.
from app import app