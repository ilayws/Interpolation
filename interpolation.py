from numpy import power, arange
from random import randint
import matplotlib.pyplot as plt


# --------------------------------------------------------------------------------------------------------
# Misc.
def appended(list, item):
    list.append(item)
    return list

# --------------------------------------------------------------------------------------------------------
#  Interpolation (Doesn't go through original points)
#  Uses Bezier curves as interpolation for any number of points

def linear_interpolate(a, b, t):
    tval = t*t * (3 - 2*t)
    val = tval*(b-a) + a
    return val

def interpolate_point(xdat, ydat, t):
    if not len(xdat) == len(ydat):
        return
    data = [(xdat[i], ydat[i]) for i in range(len(xdat))]
    while len(data) > 1:
        new_data = []
        for i in range(len(data)-1):
            x_val = linear_interpolate(data[i][0], data[i+1][0], t)
            y_val = linear_interpolate(data[i][1], data[i+1][1], t)
            new_data.append( (x_val,y_val) )
        data = new_data
    return data[0]

# Bezier
def interpolate_graph(xdat, ydat):
    new_xdat = []
    new_ydat = []
    xs = arange(0, 1, 0.01)
    for x in xs:
        point = interpolate_point(xdat, ydat, x)
        if point[0] > max(xdat):
            break
        new_xdat.append(point[0])
        new_ydat.append(point[1])
    return (new_xdat, new_ydat)

# --------------------------------------------------------------------------------------------------------
# n interpolation (goes through original points for n<11)

def row_echilon(m):
    for row in range(len(m)):
        for x in range(len(m[row])):
            if row == x:
                factor = 1 / m[x][x]
                m[row] = [m[row][i]*factor for i in range(len(m[row]))]
            if row > x:
                factor = m[row][x]/m[x][x]
                m[row] = [m[row][i]-factor*m[x][i] for i in range(len(m[row]))]
    return m

def echilon2values(e, precision=2):
    values = [0]*len(e)
    for i in range(1, len(values)+1):
        values[-i] = round(e[-i][-1] - sum([e[-i][-n-1]*values[-n] for n in range(1, i)]), precision)
    return values

# # TODO : devide interpolation into groups of <type> {i:2->8} and average
# def temp(xData, yData, type=4, points=100):
#     if len(xData) != len(yData):
#         return "Error: List lengths not matching"
#     step = ( max(xData)-min(xData) ) / points
#     new_x = [x for x in arange(min(xData), max(xData)-step, step)]
#     new_y = []
#     for s in range(0, len(xData), type-1):
#         cur_x = xData[s:s+type]
#         cur_y = yData[s:s+type]
#         matrix = [appended([power(cur_x[i], p) for p in range(len(cur_x))],cur_y[i]) for i in range(len(cur_x))]
#         echilon = row_echilon(matrix)
#         polyform = echilon2values(matrix, precision=4)
#         polyfunc = lambda x : sum([polyform[i]*power(x,i) for i in range(len(polyform))])
#         for x in arange(cur_x[0],cur_x[-1]-step,step):
#             new_y.append(polyfunc(x))
#     return {'x':new_x, 'y':new_y, 0:new_x, 1:new_y, 'func':polyform}

def interpolate(xData, yData, points=100):
    if len(xData) != len(yData):
        return "Error: List lengths not matching"
    step = ( max(xData)-min(xData) ) / points
    new_x = [x for x in arange(min(xData), max(xData), step)]
    new_y = []
    matrix = [appended([power(xData[i], p) for p in range(len(xData))],yData[i]) for i in range(len(xData))]
    echilon = row_echilon(matrix)
    polyform = echilon2values(matrix, precision=4)
    polyfunc = lambda x : sum([polyform[i]*power(x,i) for i in range(len(polyform))])
    for x in new_x:
        new_y.append(polyfunc(x))
    return (new_x, new_y, polyform)

x = [i for i in range(8)]
y = [randint(-20,20) for i in x]
xy = interpolate(x,y)

plt.plot(x,y, ".b")
plt.plot(xy[0], xy[1], "-k")
plt.show()
