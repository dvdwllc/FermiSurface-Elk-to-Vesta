"""
Script for converting Fermi surfaces from the 
Elk LAPW electronic structure code to a format 
that can be read by VESTA.

##########################
Author: David C. Wallace
May 15, 2015
##########################

IMPORTANT: You must add three lines to the top
of the exported data file:
    First line: Name of compound
    Second line: a, b, c, alpha, beta, gamma
    Third line: number of slices along each axis
        (This can be found in the first line of FERMISURF.OUT)
Example Header:
    
CeNiAsO
0.24529 0.24529 0.12343 90.0 90.0 90.0
20 20 20

Save with the extension '.ted' and open using Vesta.
"""

import numpy as np

#import mayavi
###Mayavi is nice for plotting the raw energies, if you like.
###Download Mayavi through the Enthought Canopy package manager

#Import and clean data
data = []
with open('FERMISURF.OUT') as infile:
    for line in infile:
        data.append(line)

for i in range(len(data)):
    data[i] = data[i].split(' ')

header = []
for i in range(len(data[0])):
    if data[0][i] != '':
            header.append(data[0][i].strip('\n'))

clean_data = []
for i in range(1,len(data)):
    clean_data.append([])
    for j in range(len(data[i])):
        if data[i][j] != '':
            clean_data[i-1].append(float(data[i][j].strip('\n')))

clean_data = np.array(clean_data)
clean_data = clean_data.transpose()

gridx, gridy, gridz = np.array(header[:3], dtype=int)
x = clean_data[0]
y = clean_data[1]
z = clean_data[2]
b1 = clean_data[3]

#plot data using mayavi
#src = mayavi.mlab.pipeline.scalar_scatter(x,y,z, b5)
#pts = mayavi.mlab.pipeline.glyph(src, scale_mode='none', scale_factor=.1)


#Rearrange the list of energies so that Vesta can read it in the correct order
energies = [] 
for i in range(gridx):
    #print('i = %i' %i)
    for j in range(gridy):
        #print('j = %i' % j)
        for k in range(gridz):
            #print('k = %i' % k)
            energies.append(b1[i+j*gridy+k*gridx*gridy])


#Write the energies to a file. You must edit this file! See Header...
with open('FermiSurf_Vesta.txt', 'w') as outfile:
    for i in energies:
        outfile.write('%.17f\n' % i)
        
