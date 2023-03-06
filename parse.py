import csv

# file input example: './geolife-cars.csv'
def getPoints(file, x):
    points = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['id_'] == x):
                points.append([row["x"], row["y"]])
    return points





