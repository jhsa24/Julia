"""
For control over greyscale images, we need to define colour functions to and from the unit interval.
Domain: 0=diverges immeadiately, 1=converges  Codomain: 0=black, 1=white
Note that functions need to work on arrays
"""
def colour_gs_lin(i):
    return 1-i
def colour_gs_boundary(i):
    output = np.where(i<0.2,1,i)
    return 1 - output
def colour_gs_invert(i):
    return i

"""
For control over colour images we apply a similar strategy, but now we use a function from the interval I to [0,255]^3
As before, the domain: 0=diverges immeadiately, 1=converges
This time, the codomain is of the form (r,g,b), with values in the range 0 to 255 inclusive
Each number r,g,b determines the intensity of red, green and blue
For simplicity, we can define three functions for each of these channels

A template function:

def colour_template(i):
    red = f(i) #eg 255 * i**(1/2)
    green = g(i)
    blue = h(i)
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

graphing f,g,h will help plan colour schemes
"""

def colour_grey(i):
    return np.stack([255*i] * 3 , axis = -1).astype(np.uint8)

def colour_default(i):
    red = 255 * np.sin(3.14 * i)**2
    green = 255 * i**2
    blue = 255 * i
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

def colour_purple_fade(i):
    red = 255 * np.log(i+1)
    green = 255 * np.log(i+1)
    blue = 255 * i**(1/2)
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

def colour_icicle(i):
    red = 300 * np.log(i+1)
    green = 255 * np.log(i+1.1)
    blue = 255 *  np.log(i+1.7)
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

def colour_wiki(i):
    red = 255 * 4 * i**2 * (1-i)
    green = 255 * 4 * (i)**2 * (1-i)
    blue = 255 * (0.38 -0.38 * i**2)
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

def colour_test(i):
    red = 255 * 4 * i**2 * (1-i)
    green = 255 * 4 * (i)**2 * (1-i)
    blue = 255 * (0.38 -0.38 * i**2)
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

def colour_boundary(i):
    red = 255 * np.sin(np.pi * i -0.1)**2
    green = 180 * np.sin(np.pi * i -0.1)**2
    blue = 150 * np.sin(np.pi * i -0.1)**2
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)

def colour_unamed(i):
    red = 220 * i**(1/2)
    green = 180 * i**2
    blue = 255 * (1/5) * (1 - np.log(i + 1))
    stack = [red , green , blue ]
    return np.stack(stack , axis = -1).astype(np.uint8)
