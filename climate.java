import java.util.*;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.nio.file.*;
import java.io.*;

class ClimateRecord{
    LocalDate date;
    int speed_max_gust;
    float total_precipitation;
    float min_temperature;
    float max_temperature;
    float mean_temperature;

    public ClimateRecord(LocalDate date, int speed_max_gust, float total_precipitation, float min_temperature, float max_temperature, float mean_temperature){
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
                    System.out.println("Skip record. Missing data entry: "+line);
                    continue;
                }
            }

            

        }catch (IOException ioe) {
            ioe.printStackTrace();
        }


        
    }

    // General data analysis and insights generated before asing user which report they would like
    public static void data_analysis(ArrayList<ClimateRecord> records){

    }

}
