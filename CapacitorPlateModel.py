#!/usr/bin/env python3

#
# Generates an electric potential plot for parallel-plate capacitors using
# the relaxation method.
#
# Ethan Kern
# 07June18

import numpy as np
import matplotlib.pyplot as plt

ITER = 1000     # Number of iterations.
SIZE = 120      # Length of side of grid.
THICKNESS = 7   # Thickness (vertical) of capacitor plates.
WIDTH = 80      # Width (horizontal) of capacitor plates.
GAP = 10        # Gap between capacitor plates.
POT = 20.0      # Potential across capacitor.

grid = np.zeros((SIZE,SIZE), 'float')   # Create empty square grid.

                        # Function takes a 2D array, plus the rest of the above
                        # parameters as args, and returns the array with the
			# boundary conditions set.
def set_boundary(grid, SIZE, GAP, WIDTH, THICKNESS, POT):

				       # Find center of top plate face:
	tcr = int(SIZE/2)-int(GAP/2)-1 # Row number (TopCenterRow)
	tcc = int(SIZE/2)	       # Column number (TopCenterColumn)

			# Set top plate, from top to bottom over its thickness,
				        # and left to right over its width.
	grid[tcr-THICKNESS:tcr, tcc-int(WIDTH/2):tcc+int(WIDTH/2)] = POT

					 # Find center of bottom plate face:
	bcr = int(SIZE/2)+int(GAP/2) 	 # Row number (BottomCenterRow)
	bcc = int(SIZE/2)		 # Column number (BottomCenterColumn)

				# Set bottom plate, also from top to bottom
                                # and left to right.
	grid[bcr:bcr+THICKNESS, bcc-int(WIDTH/2):bcc+int(WIDTH/2)] = -POT

	grid[0,:] = 0.0		# Ground outer perimeter of grid.
	grid[-1,:] = 0.0
	grid[:,0] = 0.0
	grid[:,-1] = 0.0

	return grid  # Function returns the input grid with
	              # boundary conditions set.



				# Create initial grid with boundary conditions.
oldgrid = set_boundary(grid, SIZE, GAP, WIDTH, THICKNESS, POT)


for i in range(1, ITER+1):  # Each iteration calculates local averages of every
                            # element in the grid for the relaxation method.

              # Every element in the 2D array is shifted left, right, up, and
              # down using numpy array methods, and the average of these shifts
              # overlaid with each other results in the original grid now having
              # each element equal to the average of its 4 nearest neighbors.
	old = oldgrid
	oldgrid = 0.25*(np.roll(oldgrid, 1, axis=0) \
	               + np.roll(oldgrid, -1, axis=0) \
	               + np.roll(oldgrid, 1, axis=1) \
	               + np.roll(oldgrid, -1, axis=1))

                    # The averaged array is passed to the function to re-set the
                    # boundary conditions.
	newgrid = set_boundary(oldgrid, SIZE, GAP, WIDTH, THICKNESS, POT)

                    # Prints the average change between one iteration of the
                    # relaxation method to the next, ideally becoming
                    # negligibly small with enough iterations.
	print('Iteration %d: %f average difference per element' \
				%(i, np.sum(np.abs(newgrid-old))/(SIZE*SIZE)))


f1, ax1 = plt.subplots()

picture = ax1.imshow(newgrid, interpolation='none', cmap='jet')
ax1.axis('off')
ax1.set_title('Capacitor Potential via Relaxation Method')
f1.colorbar(picture, label='Electric Potential (Volts)')

f1.show()
#plt.show() # Use this instead of f1.show() if running on Windows.

input("\nPress <Enter> to exit...\n")
