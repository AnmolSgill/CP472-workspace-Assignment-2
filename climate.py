import csv
import time
from collections import defaultdict

#climate data class to hold record in class instance
class ClimateData:
    def __init__(self, local_date, speed_max_gust, total_precipitation, min_temperature, max_temperature, mean_temperature):
        self.local_date = local_date
        self.speed_max_gust = speed_max_gust
        self.total_precipitation = total_precipitation
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.mean_temperature = mean_temperature

#function to process CSV input file
def load_climatedata(filename):
    datalist = []

    with open(filename) as numbers:
        numberdata = csv.reader(numbers, delimiter=',')
        next(numberdata)
        for row in numberdata:
            try:
                local_date = (row[0])
                speed_max_gust = int(row[1])
                total_precipitation = float(row[2])
                min_temperature = float(row[3])
                max_temperature = float(row[4])
                mean_temperature = float(row[5])
                climate = ClimateData(local_date, speed_max_gust,total_precipitation,min_temperature,max_temperature,mean_temperature)
                datalist.append(climate)
            except ValueError:
                continue

    return datalist

#convert date to readable format: YYYY-MM-DD to Month Day Year or Month Year as per the assignment guidelines (February 2010, March 2010 or February dd YYYY etc)
def convert_date(date, format):
    months = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}
    if format == "day":
        return (f"{months[date.split('-')[1]]} {date.split('-')[2].split(' ')[0]} {date.split('-')[0]}")
    elif format == "month":
        return (f"{months[date.split('-')[1]]} {date.split('-')[0]}")

# Analyze data - q2. Must include Highest total_precipitation (month and year). Day with highest max gust speed - print full date. Day with largest temperature fluctation
def data_analysis(data: list[ClimateData]):

    max_gust_date = None
    max_gust = 0
    max_precipitation = 0
    percipitation_per_month = defaultdict(float)
    max_temp_fluctuation = 0
    max_temp_fluctuation_date = None

    for item in data:
        month_key = convert_date(item.local_date,"month")
        percipitation_per_month[month_key] += item.total_precipitation 

        if item.max_temperature - item.min_temperature > max_temp_fluctuation:
            max_temp_fluctuation = item.max_temperature - item.min_temperature
            max_temp_fluctuation_date = item.local_date
        
        if item.speed_max_gust > max_gust:
            max_gust = item.speed_max_gust
            max_gust_date = item.local_date
    
    max_monthly_precipitation, max_precipitation = max(percipitation_per_month.items(), key=lambda value: value[1])
    print("\nClimate Data Analysis of Kitchener-Waterloo from 2010 to 2024")
    print(f"The month with the most precipitation (mm): {max_monthly_precipitation}")




    return

newlist = load_climatedata('climate-daily.csv')
sumTemp = 0
for row in newlist:
    sumTemp += row.total_precipitation
    
print(sumTemp)
    #print(row.local_date, row.speed_max_gust, row.total_precipitation, row.min_temperature, row.max_temperature, row.mean_temperature)

