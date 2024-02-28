import csv
import time
from datetime import datetime 
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
    
# Aux function validate date
def validate_date(date_str):
    try:
        date_object = datetime.strptime(date_str, "%YY-MM-DD")
        return date_object >= datetime(2010, 4, 18) and date_object <= datetime(2024, 2, 8)
    except ValueError:
        return False

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
    print(f"The month with the most precipitation (mm): {max_monthly_precipitation} with {max_precipitation:.2f}mm")
    print(f"The date with the highest gust speed (km/h): {convert_date(max_gust_date, 'day')} with {max_gust}km/h ")
    print(f"The date with the highest temperature fluctation (°C): {convert_date(max_temp_fluctuation_date, 'day')} with {max_temp_fluctuation:.2f}°C\n")

    return

#User report - multiple options for user to select from. This will be "main program" and will call functions to generate specific reports
def user_report(data: list[ClimateData]):
    while True:
        print("Choose one of the following options:")
        print("1) Average monthly weather data")
        print("2) Weather records between two dates")
        print("3) Exit")
        command = input("Enter your option number: ")

        if command == '1':
            start_time = time.time()
            avg_monthly_data(data)
            end_time = time.time()
            print(f"The average by month report took {end_time - start_time} seconds to run")
        elif command == '2':
            start_date = input("Enter a start date (YYYY-MM-DD): ")
            while not validate_date(start_date):
                print("Invalid date! Please enter a date between 2010-04-18 and 2024-02-08 in the format YYYY-MM-DD.")
                start_date = input("Enter a start date (YYYY-MM-DD): ")
            end_date = input("Enter a end date (YYYY-MM-DD): ")
            while not validate_date(end_date):
                print("Invalid date! Please enter a date between 2010-04-18 and 2024-02-08 in the format YYYY-MM-DD.")
                end_date = input("Enter a end date (YYYY-MM-DD): ")
            
            date_range_report(data, start_date, end_date)
        elif command == '3':
            break
        else:
            print("Invalid option number. Please try again")

    return
            
            

def avg_monthly_data(data: list[ClimateData]):

    return

def date_range_report(data: list[ClimateData], start_date, end_date):

    return



        
if __name__ == "__main__":
    data = load_climatedata("climate-daily.csv")
    data_analysis(data)

