from math import sqrt

def d(q, e):
    starte = e[0]
    ende = e[1]
    dist = 0
    # print(starte, ende)

    # vector e
    ab = [ende[0]-starte[0], ende[1]-starte[1]]

    # vector of ende and q
    bq = [q[0]-ende[0], q[1]-ende[1]]

    # vector of starte and q
    aq = [q[0]-starte[0], q[1]-starte[1]]

    # dot products for case analysis
    enddot = ab[0]*bq[0]+ab[1]*bq[1]
    startdot = ab[0]*aq[0]+ab[1]*aq[1]

    # if the point lies past the end point of the segment 
    # distance is point to end point 
    if (enddot > 0) :
        x = q[0]-ende[0]
        y = q[1]-ende[1]
        dist = sqrt(x*x+y*y)
    # if the point lies before the start point of the segment 
    # distance is point to start point 
    elif (startdot < 0) :
        x = q[0]-starte[0]
        y = q[1]-starte[1]
        dist = sqrt(x*x+y*y)
    # if the point lies between the start and end point of the segment
    # distance is perpendicular line from point to segment 
    else:
        denom = sqrt(ab[0]*ab[0]+ab[1]*ab[1])
        num = abs(ab[0]*aq[1] - ab[1]*aq[0])
        dist = num / denom

    return dist