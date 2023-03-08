from math import sqrt

def d(q, e):
    starte = e[0]
    ende = e[1]
    dist = 0
    # print(starte, ende)

    # vector e
    evect = [ende[0] - starte[0], ende[1] - starte[1]]

    # vector of ende and q
    endq = [q[0] - ende[0], q[1] - ende[1]]

    # vector of starte and q
    startq = [q[0] - starte[0], q[1] - starte[1]]

    # dot products for case analysis
    enddot = evect[0] * endq[0] + evect[1] * endq[1]
    startdot = evect[0] * startq[0] + evect[1] * startq[1]

    # if the point lies past the end point of the segment 
    # distance is point to end point 
    if (enddot > 0) :
        x = q[0] - ende[0]
        y = q[1] - ende[1]
        dist = sqrt(x * x + y * y)
    # if the point lies before the start point of the segment 
    # distance is point to start point 
    elif (startdot < 0) :
        x = q[0] - starte[0]
        y = q[1] - starte[1]
        dist = sqrt(x * x + y * y)
    # if the point lies between the start and end point of the segment
    # distance is perpendicular line from point to segment 
    else:
        denom = sqrt(evect[0] * evect[0] + evect[1] * evect[1])
        num = abs(evect[0] * startq[1] - evect[1] * startq[0])
        dist = num / denom

    return dist