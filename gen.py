from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import math
import numpy
phases = numpy.arange(-1.0, 1.0, 2/27.3)
for idphase, phase in enumerate(phases):
    print(phase)
    with Image(filename='./images/white_circle.png') as img:
        radius = img.height // 2
        with Drawing() as draw:
            draw.fill_color = Color("rgba(0, 0, 0, 0.7)")
            if phase < 0:
                phase = abs(phase)
                for y in range(radius):
                    x = math.sqrt(radius**2 - y**2)
                    x = round(x)
                    X = radius - x
                    Y = radius - y
                    Y_mirror = radius + y
                    moon_width = 2 * (radius - X)
                    shade = moon_width * phase
                    shade = round(shade)
                    x_shade = X + shade
                    draw.line((X, Y), (x_shade, Y))
                    if Y_mirror != Y:
                        draw.line((X, Y_mirror), (x_shade, Y_mirror))
                draw(img)
                img.save(filename=f'./images/phases/{str(idphase)}.png')

            elif phase > 0:
                phase = abs(phase)
                for y in range(radius):
                    x = math.sqrt(radius**2 - y**2)
                    x = round(x)
                    X = radius + x
                    Y = radius - y
                    Y_mirror = radius + y
                    moon_width = 2 * (radius - X)
                    shade = moon_width * phase
                    shade = round(shade)
                    x_shade = X + shade
                    draw.line((X, Y), (x_shade, Y))
                    if Y_mirror != Y:
                        draw.line((X, Y_mirror), (x_shade, Y_mirror))
                draw(img)
                img.save(filename=f'./images/phases/{str(idphase+1)}.png')
