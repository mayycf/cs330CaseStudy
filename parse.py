import csv

def getPoints(x):
    points = []
    with open('./geolife-cars.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['id_'] == x):
                points.append([row["x"], row["y"]])
    return points





