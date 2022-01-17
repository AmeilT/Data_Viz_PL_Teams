import numpy as np

title_font="HydrophiliaLiquid-Regular"
title_size=20
label_font="HydrophiliaLiquid-Regular"
label_size=14
text_colour="w"
back_colour="#04013b"

def y_equals_x(data,x,y,axes,colour="g--"):
    a = np.linspace(data[x].min(), data[x].max(), 20)
    b = np.linspace(data[y].min(), data[y].max(), 20)
    axes.plot(a, b, colour)