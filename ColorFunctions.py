from  numpy import linspace
from  numpy import sqrt, cos, arctan2
from  numpy import fabs
from  numpy import tanh
from  numpy import pi
from numpy.linalg import norm
import matplotlib.colors 
import colorsys
from random import random


colorcycles = {
    'std' : ['1f77b4', 'ff7f0e', '2ca02c', 'd62728', '9467bd', '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf']
}

def randomcolor():
    return triple2hex(
        ( random(), random(), random() )
    )

def triple2hex( triple ):
    val255 = [ 255 * x for x in triple ]
    return '#%02x%02x%02x' % tuple( val255 )

def heaviside( x ):
    if 1.0 * x == 0.0:
        return 0.5
    return 0.0 if x < 0.0 else 1.0

def make_colormap( func , nCol ):
    cdict = { 'red' : [], 'green' : [], 'blue' : [] }
    for x in linspace( 0, 1, nCol ):
        (r , g, b ) = func( x )
        cdict[ 'red' ].append( [ x, r, r ] )
        cdict[ 'green' ].append( [x, g, g ] )
        cdict[ 'blue' ].append( [ x, b, b ] )
    return matplotlib.colors.LinearSegmentedColormap(
        func.__name__+'_CustomMap',
        cdict
    )

##########################################
### different color scales
##########################################

def  peppermintWhite(x):
    rgbTup = (
        sqrt( x ) * ( 1.0 - cos( pi * ( x - 0.5 ) )**16 )
        + cos( pi * ( x - 0.5) )**16, 
        sqrt( 1 - x ) * ( 1 - cos( pi * ( x - 0.5 ) )**16 )
        + cos( pi * ( x - 0.5 ) )**16, 
        0.4 * ( ( 1 - x )**0.3 + x**0.3 )
        * (1 - cos( pi * (x - 0.5 ) )**8 )
        + cos( pi*( x - 0.5 ) )**8
    )
    return rgbTup

def RBColor( y ):
    if y < 0.5:
        rgbTup = ( ( 2.0 *y )**( 2.0 / 3.0 ), 0 , 1.0 )
    else:
        rgbTup = ( 1.0, 0 ,( 2.0- 2.0 * y )**( 2.0 / 3.0 ) )
    return rgbTup 

def RBWhiteColor( y ):
    if y < 0.5:
        rgbTup =(
            ( 2.0 * y )**( 2.0 / 3.0 ),
            ( 2.0 * y )**( 2.0 / 3.0 ),
            1
        )
    else:
        rgbTup=(
            1.0,
            ( 2.0 - 2.0 * y )**( 2.0 / 3.0 ),
            ( 2.0 - 2.0 * y )**( 2.0 / 3.0 )
        )
    return rgbTup

def RBBlackColor( y ):
    if y < 0.5:
        rgbTup = (
            0,
            0,
            sqrt( 1.0 - 2.0 * y )
        )
    else:
        rgbTup = (
            sqrt( 2.0 * ( y - 0.5 ) ),
            0,
            0
        )
    return rgbTup

def STMColor( y ):
    if y < 2.0 / 3.0:
        r = 3.0 / 2.0 * y
        b = 0
    else:
        r = 1.0
        b = 3 * ( y - 2.0 / 3.0 )
    if y < 0.5:
        g = 2.0 / 3.0 * y
    else:
        g = 4.0 / 3.0 * ( y - 0.25 )
    rgbTup = ( r, g, b )
    return rgbTup

def RedScale( y ):
    rgbTup = (
        tanh( 2 * y ) / tanh( 2.0 ),
        y**2,
        y**3
    )
    return rgbTup

def iRedScale( y ):
    return RedScale( 1 - y )

def BlueScale( y ):
    rgbTup = (
        y**3,
        y**2,
        ( tanh( 1.5 * y ) / tanh( 1.5 ) )**0.7
    )
    return rgbTup

def iBlueScale( y ):
    return BlueScale( 1 - y )


def GreenScale( y ):
    rgbTup = (
        y,
        (tanh( 1.5 * y ) / tanh( 1.5 ) )**0.6,
        y**2
    )
    return rgbTup

def Sunset( x ):
    rgbTup = (
        0.5 * ( 1.0 + tanh( 4.0 * ( x - 0.41 ) ) ),
        0.5 * ( 1.0 + tanh( 7.0 * ( x - 0.62 ) ) ),
        ( 
            0.3 * ( 1.0 + tanh( 7.0 * ( x - 0.1 ) ) ) *
            0.5 * ( 1.0 + tanh( 5 * ( ( -x ) + 0.55 ) ) ) +
            0.99 * x**3
        )
    )
    return rgbTup

def iSunset( x ):
    return Sunset( 1 - x )

def Rainbow( x ):
    rgbTup = colorsys.hsv_to_rgb(
        0.7 * (
            0.465184 -
            0.413909 * cos( pi * (1.0 - x ) ) +
            0.009379 * cos( 2.0 * pi * ( 1 - x ) ) +
            0.000145 * cos( 3.0 * pi * ( 1 - x ) ) +
            0.005635 * cos( 4.0 * pi * ( 1 - x ) ) -
            0.047067 * cos( 5.0 * pi * ( 1 - x ) ) +
            0.003350 * cos( 6.0 * pi * ( 1 - x ) ) -
            0.000217 * cos( 7.0 * pi * ( 1 - x ) ) +
            0.002699 * cos( 8.0 * pi * ( 1 - x ) )
        ),
        1,
        1
    )
    return rgbTup


def BW50_CM( x, s=0 ): #jumps at position x from graylevel s to 1-s 
    cdict = {
        'red': (
            ( 0, 0, s),
            ( x, s, 1 - s ),
            (1, 1 - s, 1 )
        ), 
        'green': (
            ( 0, 0, s ),
            ( x, s, 1 - s ),
            ( 1, 1 - s, 1 )
        ), 
        'blue': (
            ( 0, 0, s ),
            ( x, s, 1 - s ),
            ( 1, 1 - s, 1 )
        )
    }
    return matplotlib.colors.LinearSegmentedColormap(
        'cmBW50_CustomMap',
        cdict
    )


def cColor43D( vector, defaultZeroColorTupel=( 0, 0, 0.8 ) ):
    myNorm = norm( vector )
    if myNorm < 10e-6:
        return( defaultZeroColorTupel )
    if ( vector[0]**2 < 10e-12 ) and ( vector[1]**2 < 10e-12 ):
        phi = 0.0
    else:
        phi = arctan2( vector[1], vector[0] )
        if vector[1] < 0:
            phi += ( 2 * pi )#up to here is my classical Srg definition.
    phi /= ( 2 * pi )
    phi = phi - int( phi )#should be in the range [0,1], but just in case
    theta = vector[2] / myNorm;
    hueColors = (
        0.10 * ( 1.0 + tanh( 15 * ( -0.96 + fabs( phi ) ) ) ) +
        0.19 * ( 1.0 + tanh( 9 * ( -0.745 + fabs( phi ) ) ) ) +
        0.14 * ( 1.0 + tanh( 12 * ( -0.5  + fabs( phi ) ) ) ) +
        0.19 * tanh( 5.2 * fabs( phi ) ),
        1 - heaviside( theta ) * theta,
        1 + heaviside( -theta ) * theta
    )
    rgbColors = colorsys.hsv_to_rgb( *hueColors )
    return( rgbColors )

