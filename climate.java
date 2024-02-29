import java.util.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.nio.file.*;
import java.io.*;

class ClimateRecord{
    LocalDate date;
    float speed_max_gust;
    float total_precipitation;
    float min_temperature;
    float max_temperature;
    float mean_temperature;

    public ClimateRecord(LocalDate date, float speed_max_gust, float total_precipitation, float min_temperature, float max_temperature, float mean_temperature){
        this.date = date;
        this.speed_max_gust = speed_max_gust;
        this.total_precipitation = total_precipitation;
        this.min_temperature = min_temperature;
        this.max_temperature = max_temperature;
        this.mean_temperature = mean_temperature;
    }

}

public class climate {
    public static void main(String[] args){

        ArrayList<ClimateRecord> records = new ArrayList<>();

        load_climatedata(records);
        data_analysis(records);

        while (true){
            // main function to handle user input and call functions
            System.out.println("Choose one of the following options:");
            System.out.println("1) Average monthly weather data");
            System.out.println("2) Daily weather records between two dates");
            System.out.println("3) Exit");
            System.out.println("Enter your option number: ");
            Scanner scanner = new Scanner(System.in);
            String command = scanner.nextLine().trim(); // Clear input buffer

            if (command.equals("1")){
                long start_time = System.nanoTime();
                avg_monthly_data(records);
                long end_time = System.nanoTime();
                long time_nano = end_time - start_time;
                double time_seconds = (double)time_nano / 1_000_000_000.0;
                System.out.println("The average by month report took " + time_seconds + " seconds");
            } else if (command.equals("2")){
                System.out.println("Enter a start date (YYYY-MM-DD): ");
                String start_date = scanner.nextLine();
                System.out.println("Enter a end date (YYYY-MM-DD): ");
                String end_date = scanner.nextLine();
                scanner.close();
                date_range_report(records, LocalDate.parse(start_date), LocalDate.parse(end_date));
                // Will validate dates in date range report function. Had issues implementing a validate_date function that worked in java the same way I did that worked in Python
            }else if (command.equals("3")){
                break;
            }else{
                System.out.println("Invalid option number. Please try again");
            }
        }
    }

    // process input csv file
    public static void load_climatedata(ArrayList<ClimateRecord> records){
        Path filePath = Paths.get("climate-daily.csv");

        try (BufferedReader buf = Files.newBufferedReader(filePath)){
            String line = buf.readLine();
            while((line = buf.readLine())!= null){
                String[] values = line.split(",");
                if(values.length < 6){
                    continue;
                }
                DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd H:mm");
                LocalDate date = LocalDate.parse(values[0],formatter);
                try{
                    float speed_max_gust = Float.parseFloat(values[1]);
                    float total_precipitation = Float.parseFloat(values[2]);
                    float min_temperature = Float.parseFloat(values[3]);
                    float max_temperature = Float.parseFloat(values[4]);
                    float mean_temperature = Float.parseFloat(values[5]);
                    ClimateRecord record = new ClimateRecord(date, speed_max_gust, total_precipitation, min_temperature, max_temperature, mean_temperature);
                    records.add(record);
                }catch (NumberFormatException nfe){
                    continue;
                }
            }
        }catch (IOException ioe) {
            ioe.printStackTrace();
        }
    }


    // General data analysis and insights generated before asing user which report they would like
    public static void data_analysis(ArrayList<ClimateRecord> records){
        Map<String, Float> precipitation_per_month = new HashMap<>();
        // store montly precipitation records 
        float max_gust = 0;
        float max_temperature_diff = 0;
        LocalDate max_fluctuation_date = null;
        LocalDate max_gust_day = null;

        for (ClimateRecord entry : records){
            String month_string = entry.date.format(DateTimeFormatter.ofPattern("MM-yyyy"));
            precipitation_per_month.put(month_string, precipitation_per_month.getOrDefault(month_string,0f) + entry.total_precipitation);

            float temperature_diff = entry.max_temperature - entry.min_temperature;
            if (temperature_diff > max_temperature_diff){
                max_fluctuation_date = entry.date;
                max_temperature_diff = temperature_diff;
            }

            if(entry.speed_max_gust > max_gust){
                max_gust_day = entry.date;
                max_gust = entry.speed_max_gust;

            }
        }

        // Find highest precipitation month
        Map.Entry<String, Float> max_record = null;
        for (Map.Entry<String, Float> entry: precipitation_per_month.entrySet()){
            if(max_record == null || entry.getValue().compareTo(max_record.getValue()) > 0){
                max_record = entry;
            }
        }

        System.out.println("\nClimate Data Analysis of Kitchener-Waterloo from 2010 to 2024\n");
        System.out.println("The month with the most precipitation (mm): " + max_record.getKey() + " with " + String.format("%.2f", max_record.getValue()) + " mm");
        System.out.println("The date with the highest gust speed (km/h): " + max_gust_day + " with " + max_gust + "km/h");
        System.out.println("The date with the highest temperature fluctation (°C): " + max_fluctuation_date + " with " + String.format("%.2f", max_temperature_diff) + "°C\n");
    }

    // averages for each month in the data file
    public static void avg_monthly_data(ArrayList<ClimateRecord> records){
        Map<String, ClimateRecord> month_averages = new HashMap<>();
        for (ClimateRecord entry : records){
            String month = entry.date.getMonth().toString() + " " + entry.date.getYear();
            ClimateRecord month_avg = month_averages.getOrDefault(month, new ClimateRecord(entry.date, 0, 0, Float.MAX_VALUE, Float.MIN_VALUE, 0));
            if(month_avg.speed_max_gust < entry.speed_max_gust){
                month_avg.speed_max_gust = entry.speed_max_gust;
            }
            month_avg.total_precipitation += entry.total_precipitation;
            month_avg.min_temperature = Math.min(month_avg.min_temperature, entry.min_temperature);
            month_avg.max_temperature = Math.max(month_avg.max_temperature, entry.max_temperature);
            month_avg.mean_temperature += entry.mean_temperature;
            month_averages.put(month, month_avg);
        }

        for (Map.Entry<String, ClimateRecord> entry : month_averages.entrySet()){
            ClimateRecord record = entry.getValue();
            System.out.println("Month: " + entry.getKey());
            System.out.println("Average max gust speed (km/h): " + record.speed_max_gust);
            System.out.println("Total precipitation (mm): " + String.format("%.2f", record.total_precipitation));
            System.out.println("Min temperature (°C): " + record.min_temperature);
            System.out.println("Max temperature (°C): " + record.max_temperature);
            System.out.println("Mean temperature (°C): " + String.format("%.2f", record.mean_temperature / 30));
            System.out.println("");
        }

    }

    // Generate user report for weather record between input start and end date 
    public static void date_range_report(ArrayList<ClimateRecord> records, LocalDate start_date, LocalDate end_date){
        for (ClimateRecord entry : records){
            if(entry.date.isAfter(start_date) && entry.date.isBefore(end_date)){
                System.out.println("\nDate: " + entry.date);
                System.out.println("Max gust speed (km/h): " + entry.speed_max_gust);
                System.out.println("Total precipitation (mm): " + entry.total_precipitation);
                System.out.println("Min temperature (°C): " + entry.min_temperature);
                System.out.println("Max temperature (°C): " + entry.max_temperature);
                System.out.println("Mean temperature (°C): " + entry.mean_temperature + "\n");
            }
        }
    }
}