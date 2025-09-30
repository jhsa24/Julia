"""
This file includes all code to generate fractal images of Mandelbrot and Julia sets
There are two families of functions, for Mandelbrot sets and another for Julia
In each family, there are three levels:
    1. a pure black and white image; use the suffix _BW to use
    2. a greyscale image, with midtones; use _GS to use
    3. full colour image, use suffic _COL to use

Note that 2&3 need a colour function as input, from the colour.py file
this function takes an escape value [0,1] as input, and decides what colour
it should be mapped to. In theory, with the right colour function both 3 could
mimick the behaviour of 2 which could mimick 1.
"""
import numpy as np
import os
from PIL import Image
from constants import HEIGHT, WIDTH, OUTPUT_DIR
from colour import *

# M.1
#This produces a pure black and white image, with no midtones at all
def Mandelbrot_BW(complex_min , complex_max , max_iter , name = "Mandelbrot_BW"):
    """
    complex_min is the complex number at the bottom left of the image,
    likewise max for the top right
    name is how the file will be called, no need for a file extension
    """
    #Make real and imaginary axes
    real_axis = np.linspace(complex_min.real , complex_max.real , WIDTH)
    imaginary_axis = np.linspace(complex_min.imag , complex_max.imag , HEIGHT) * 1j
    #Combine into a single matrix of complex numbers
    matrix = real_axis[np.newaxis , : ] + imaginary_axis[ : , np.newaxis]
    #Initialise output with ONEs in case elements diverge immeadiately
    is_divergent = np.ones((matrix.shape), dtype = bool)
    #COPY the coordinate matrix to z, which we can change without disturbing the matrix
    z = np.copy(matrix)
    #The iterative bit
    for _ in range(max_iter):
        small = np.less(z.real * z.real + z.imag * z.imag , 4)
        z[small] = z[small]**2 + matrix[small]
    is_divergent[small] = 0
    #Make black and white image with Pillow
    image = Image.fromarray(is_divergent.astype(np.uint8) * 255)

    filepath = os.path.join(OUTPUT_DIR, name + ".png")
    image.save(filepath)

# M.2
#this produces a greyscale image, and the levels of grey can be adjusted with the colour funtions found in colour.py
def Mandelbrot_GS(complex_min , complex_max , width , height , max_iter , colour_function = colour_gs_lin , name = "Mandelbrot_GS"):
    """
    complex_min is the complex number at the bottom left of the image,
    likewise max for the top right

    colour_function is a map to and from the unit interval, mapping escape
    numbers to colour values, 1=black , 0=white
    The function can be used for fine tuning, the default is set to a linear
    gradient, and is quite pleasant in most cases

    name is how the file will be called, no need for a file extension
    Make real and imaginary axes """
    real_axis = np.linspace(complex_min.real , complex_max.real , width)
    imaginary_axis = np.linspace(complex_min.imag , complex_max.imag , height) * 1j
    #Combine into a single matrix of complex numbers
    matrix = real_axis[np.newaxis , : ] + imaginary_axis[ : , np.newaxis]
    #Initialise output with ZEROs in case elements diverge immeadiately and so diverge time is zero
    escape_speed = np.zeros((matrix.shape))
    #COPY the coordinate matrix to z, which we can change without disturbing the matrix
    z = np.copy(matrix)
    #The iterative bit
    for i in range(max_iter):
        #Find all points that haven't diverged yet
        not_diverged = np.less(abs(z) , 2)
        #Increase their value a little
        escape_speed[not_diverged] = (i+1)/max_iter
        #Iterate again (only over non-divergent values)
        z[not_diverged] = z[not_diverged]**2 + matrix[not_diverged]
    #Make greyscale image with Pillow
    image = Image.fromarray(np.uint8(255 * colour_function(escape_speed) ) , "L")
    image.save(name + ".png")

# M.3
#produces a full colour image of a mandelbrot set
def Mandelbrot_Col(complex_min , complex_max , width , height , max_iter, escape_radius=2 , colour_function = colour_default , name = "Mandelbrot_Col"):
    """
    set z_0 = 0 for Mandelbrot set

    complex_min is the complex number at the bottom left of the image, likewise max for the top right

    max_iter and escape_radius determine how many iterations, and how far do we need to go to reach divergence
    these may have a minor effect on the colour smoothing in the final image

    colour_function is a map from the unit interval, to I^3, essentially mapping (fractional) escape
    values to intensities of red, green and blue, with 255 being max intensity, 0 empty


    name is how the file will be called, no need for a file extension
    """

    #Make real and imaginary axes:
    real_axis = np.linspace(complex_min.real , complex_max.real , width)
    imaginary_axis = np.linspace(complex_max.imag , complex_min.imag , height) * 1j
    #Combine into a single matrix of complex numbers
    matrix = real_axis[np.newaxis , : ] + imaginary_axis[ : , np.newaxis]
    #Initialise output and log(|Z) with ZEROs; first in case of immeadiate divergence, second to decide valid points for fractional escape values
    escape_speed = np.zeros((matrix.shape))
    log_abs_z = np.copy(escape_speed)
    #COPY the coordinate matrix to z, which we can change without disturbing the matrix:
    z = np.copy(matrix)

    #The iterative bit
    for i in range(max_iter):
        #Find non-diverged points, move them on one iteration, and give them a naieve escape value:
        not_diverged = np.less(abs(z) , escape_radius)
        z[not_diverged] = z[not_diverged]**2 + matrix[not_diverged]
        escape_speed[not_diverged] = (i+1) / max_iter

        #Calculate which elements can be fractionally scaled safely (ie without large negative values):
        log_abs_z[not_diverged] = np.log(abs(z[not_diverged]))
        fractional_points = np.greater(log_abs_z , 0)

        #Adjust escape speed if fractional values are suitable:
        if i!=max_iter-1:
            escape_speed[fractional_points] = (i + 1 - np.log2( log_abs_z[fractional_points] / np.log(escape_radius))) / max_iter
            #reset log(|Z) so newly diverged points don't have their escape speed overwritten:
            log_abs_z[fractional_points] = 0

    #Generate and save image:
    image = Image.fromarray(colour_function(escape_speed) , 'RGB')
    image.save(name + ".png")



# J.1
#Julia raw black and white only
def Julia_BW(z_0,complex_min , complex_max , width , height , max_iter , name = "Julia_BW"):
    #complex_min is the complex number at the bottom left of the image,
    # likewise max for the top right
    #name is how the file will be called, no need for a file extension
    #Make real and imaginary axes
    real_axis = np.linspace(complex_min.real , complex_max.real , width)
    imaginary_axis = np.linspace(complex_min.imag , complex_max.imag , height) * 1j
    #Combine into a single matrix of complex numbers
    matrix = real_axis[np.newaxis , : ] + imaginary_axis[ : , np.newaxis]
    #Initialise output with ONEs in case elements diverge immeadiately
    is_divergent = np.ones((matrix.shape), dtype = np.int8)
    #Make a matrix to track the iteration z_(n+1) we initialise the matrix with z_0
    z = np.full(matrix.shape,z_0,dtype=np.csingle)
    #The iterative bit
    for _ in range(max_iter):
        not_divergent = np.less(z.real * z.real + z.imag * z.imag , 4)
        z[not_divergent] = z[not_divergent]**2 + matrix[not_divergent]
    is_divergent[not_divergent] = 0
    #Make black and white image with Pillow
    image = Image.fromarray(np.bool(is_divergent))
    image.save(name + ".png")


# J.2
# Julia greyscale, use colour function from colour.py
def Julia_GS(z_0 , complex_min , complex_max , width , height , max_iter , colour_function = colour_gs_lin , name = "Julia_GS"):
    """
    set z_0 = 0 for Mandelbrot set

    complex_min is the complex number at the bottom left of the image,
    likewise max for the top right

    colour_function is a map to and from the unit interval, mapping escape
    numbers to colour values, 1=black , 0=white
    The function can be used for fine tuning, the default is set to a linear
    gradient, and is quite pleasant in most cases

    name is how the file will be called, no need for a file extension
    Make real and imaginary axes """

    real_axis = np.linspace(complex_min.real , complex_max.real , width)
    imaginary_axis = np.linspace(complex_min.imag , complex_max.imag , height) * 1j

    #Combine into a single matrix of complex numbers
    matrix = real_axis[np.newaxis , : ] + imaginary_axis[ : , np.newaxis]
    #Initialise output with ZEROs in case elements diverge immeadiately and so diverge time is zero
    escape_speed = np.zeros((matrix.shape))
    #define an array to track the iteration, initialising it with our chosen start value, z_0
    z = np.full(matrix.shape,z_0,dtype=np.csingle)
    #The iterative bit
    for i in range(max_iter):
        #Find all points that haven't diverged yet
        not_diverged = np.less(abs(z) , 2)
        #Increase their speed value a little
        escape_speed[not_diverged] = (i+1)/max_iter
        #Iterate again (only over non-divergent values)
        z[not_diverged] = z[not_diverged]**2 + matrix[not_diverged]
    #Make greyscale image with Pillow
    image = Image.fromarray(np.uint8(255 * colour_function(escape_speed) ) , "L")
    image.save(name + ".png")


# J.3
# Full Julia colour image
def Julia_Col(z_0 , complex_min , complex_max , width , height , max_iter, escape_radius=2 , colour_function = colour_default , name = "Julia_Col"):
    """
    complex_min is the complex number at the bottom left of the image, likewise max for the top right

    max_iter and escape_radius determine how many iterations, and how far do we need to go to reach divergence
    these may have a minor effect on the colour smoothing in the final image

    colour_function is a map from the unit interval, to I^3, essentially mapping (fractional) escape
    values to intensities of red, green and blue, with 255 being max intensity, 0 empty


    name is how the boundaryfile will be called, no need for a file extension
    """

    #Make real and imaginary axes:
    real_axis = np.linspacboundarye(complex_min.real , complex_max.real , width)
    imaginary_axis = np.linspace(complex_min.imag , complex_max.imag , height) * 1j
    #Combine into a single matrix of complex numbers
    matrix = real_axis[np.newaxis , : ] + imaginary_axis[ : , np.newaxis]
    #Initialise output and log(|Z) with ZEROs; first in case of immeadiate divergence, second to decide valid points for fractional escape values
    escape_speed = np.zeros((matrix.shape))
    log_abs_z = np.copy(escape_speed)
    #define an array to track the iteration, initialising it with our chosen start value, z_0
    z = np.full(matrix.shape,z_0,dtype=np.csingle)

    #The iterative bit
    for i in range(max_iter):
        #Find non-diverged points, move them on one iteration, and give them a naieve escape value:
        not_diverged = np.less(abs(z) , escape_radius)
        z[not_diverged] = z[not_diverged]**2 + matrix[not_diverged]
        escape_speed[not_diverged] = (i+1) / max_iter

        #Calculate which elements can be fractionally scaled safely (ie without large negative values):
        log_abs_z[not_diverged] = np.log(abs(z[not_diverged]))
        fractional_points = np.greater(log_abs_z , 0)

        #Adjust escape speed if fractional values are suitable:
        if i!=max_iter-1:
            escape_speed[fractional_points] = (i + 1 - np.log2( log_abs_z[fractional_points] / np.log(escape_radius))) / max_iter
            #reset log(|Z) so newly diverged points don't have their escape speed overwritten:
            log_abs_z[fractional_points] = 0

    #Generate and save image:
    image = Image.fromarray(colour_function(escape_speed) , 'RGB')
    image.save(name + ".png")
