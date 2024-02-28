import csv
from datetime import datetime


class ClimateData:
    def __init__(self, local_date, speed_max_gust, total_precipitation, min_temperature, max_temperature, mean_temperature):
        self.local_date = local_date
        self.speed_max_gust = speed_max_gust
        self.total_precipitation = total_precipitation
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature

def load_data(filename):
    datalist = []

    with open(filename) as numbers:
        numberdata = csv.reader(numbers, delimiter=',')
        next(numberdata)
        for row in numberdata:
            try:
                local_date = (row[0])
                speed_max_gust = float(row[1])
                total_precipitation = float(row[2])
                min_temperature = float(row[3])
                max_temperature = float(row[4])
                mean_temperature = float(row[5])
                climate = ClimateData(local_date, speed_max_gust,total_precipitation,min_temperature,max_temperature,mean_temperature)
                datalist.append(climate)
            except ValueError:
                continue

    return datalist

def find_total_precipitation(datalist):
    monthly_precipitation = []
    
    return 

def find_speed_max_gust(datalist):

    return

def find_temperature_fluctuation(datalist):

    return


newlist = load_data('climate-daily.csv')
sumTemp = 0
for row in newlist:
    sumTemp += row.total_precipitation
    
print(sumTemp)
    #print(row.local_date, row.speed_max_gust, row.total_precipitation, row.min_temperature, row.max_temperature, row.mean_temperature)

