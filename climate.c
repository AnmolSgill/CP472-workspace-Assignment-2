#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include <ctype.h>


typedef struct {
    char date[20];
    float maxGust;
    float totalPrecipitation;
    float minTemperature;
    float maxTemperature;
    float meanTemperature;
} ClimateRecord;

typedef struct {
    char month[8];
    float totalPrecipitation;
} MonthlyPrecipitation;


// Function to parse a line from the CSV file
ClimateRecord* load_climate_data(char* line) {
    ClimateRecord* record = malloc(sizeof(ClimateRecord));
    if (record == NULL) {
        fprintf(stderr, "Failed to allocate memory for record.\n");
        return NULL;
    }

    char* token = strtok(line, ",");
    if (token == NULL || token[0] == '\0') {
        free(record);
        return NULL;
    }
    strcpy(record->date, token);

    token = strtok(NULL, ",");
    if (token == NULL || token[0] == '\0') {
        free(record);
        return NULL;
    }
    record->maxGust = atof(token);

    token = strtok(NULL, ",");
    if (token == NULL || token[0] == '\0') {
        free(record);
        return NULL;
    }
    record->totalPrecipitation = atof(token);

    token = strtok(NULL, ",");
    if (token == NULL || token[0] == '\0') {
        free(record);
        return NULL;
    }
    record->minTemperature = atof(token);

    token = strtok(NULL, ",");
    if (token == NULL || token[0] == '\0') {
        free(record);
        return NULL;
    }
    record->maxTemperature = atof(token);

    token = strtok(NULL, ",");
    if (token == NULL || token[0] == '\0') {
        free(record);
        return NULL;
    }
    record->meanTemperature = atof(token);

    return record;
}

// Function to analyze the data
void analyzeData(ClimateRecord* records[], int record_count) {
    char* maxGustDate = NULL;
    int maxGust = 0;
    char* maxTempFluctuationDate = NULL;
    float maxTempFluctuation = 0;

    int monthlyPrecipitationSize = 100;
    MonthlyPrecipitation* monthlyPrecipitations = malloc(monthlyPrecipitationSize * sizeof(MonthlyPrecipitation));
    int monthlyPrecipitationCount = 0;


    for (int i = 0; i < record_count; i++) {
        ClimateRecord* record = records[i];
        if (record == NULL) {
            continue;
        }

        char month[8];
        strncpy(month, record->date, 7);
        month[7] = '\0';

        int found = 0;
        for (int j = 0; j < monthlyPrecipitationCount; j++) {
            if (strcmp(monthlyPrecipitations[j].month, month) == 0) {
                monthlyPrecipitations[j].totalPrecipitation += record->totalPrecipitation;
                found = 1;
                break;
            }
        }
        
        if (!found) {
            if (monthlyPrecipitationCount == monthlyPrecipitationSize) {
                monthlyPrecipitationSize *= 2;
                monthlyPrecipitations = realloc(monthlyPrecipitations, monthlyPrecipitationSize * sizeof(MonthlyPrecipitation));
            }
            strcpy(monthlyPrecipitations[monthlyPrecipitationCount].month, month);
            monthlyPrecipitations[monthlyPrecipitationCount].totalPrecipitation = record->totalPrecipitation;
            monthlyPrecipitationCount++;
        }

        if (record->maxGust > maxGust) {
            maxGust = record->maxGust;
            maxGustDate = record->date;
        }

        float tempFluctuation = record->maxTemperature - record->minTemperature;
        if (tempFluctuation > maxTempFluctuation) {
            maxTempFluctuation = tempFluctuation;
            maxTempFluctuationDate = record->date;
        }
    }

    char maxPrecipitationMonth[8] = "";
    float maxPrecipitation = 0;
    for (int i = 0; i < monthlyPrecipitationCount; i++) {
        if (monthlyPrecipitations[i].totalPrecipitation > maxPrecipitation) {
            maxPrecipitation = monthlyPrecipitations[i].totalPrecipitation;
            strcpy(maxPrecipitationMonth, monthlyPrecipitations[i].month);
        }
    }

    printf("\nClimate Data Analysis of Kitchener-Waterloo from 2010 to 2024\n");
    printf("The month with the most precipitation (mm): %s with %.2fmm\n", maxPrecipitationMonth, maxPrecipitation);
    printf("The date with the highest gust speed (km/h): %s with %dkm/h\n", maxGustDate, maxGust);
    printf("The date with the highest temperature fluctation (°C): %s with %.2f°C\n", maxTempFluctuationDate, maxTempFluctuation);
}


// Function to print the records between two dates
void date_range_report(ClimateRecord** records, int record_count, char* start_date, char* end_date) {
    for (int i = 0; i < record_count; i++) {
        ClimateRecord* record = records[i];
        if (record == NULL) {
            continue;
        }
        if (strcmp(record->date, start_date) >= 0 && strcmp(record->date, end_date) <= 0) {
            printf("\nDate: %s\n", record->date);
            printf("Max Gust: %.2fkm/h\n", record->maxGust);
            printf("Total Precipitation: %.2fmm\n", record->totalPrecipitation);
            printf("Min Temperature: %.2f°C\n", record->minTemperature);
            printf("Max Temperature: %.2f°C\n", record->maxTemperature);
            printf("Avg Temperature: %.2f°C\n\n", (record->minTemperature + record->maxTemperature) / 2);
        }
    }
}

// Function to generate user reports
void userGeneratedReport(ClimateRecord** records, int record_count) {
    int choice;
    char start_date[20];
    char end_date[20];
    do {
        printf("\nChoose one of the following options:\n");
        printf("1) Average monthly weather data\n");
        printf("2) Weather records between two dates\n");
        printf("3) Exit\n");
        printf("Enter your option number: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:{
                clock_t start_time = clock();
                //avg_monthly_data(records, record_count);
                clock_t end_time = clock();
                double duration = ((double) (end_time - start_time)) / CLOCKS_PER_SEC;
                printf("The average by month report took %f seconds to run\n", duration);
                break;
            }
            case 2:
                printf("Enter the start date (YYYY-MM-DD): ");
                scanf("%s", start_date);
                printf("Enter the end date (YYYY-MM-DD): ");
                scanf("%s", end_date);
                date_range_report(records, record_count, start_date, end_date);
                break;
            case 3:
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 3);
}

// main function to run climate data program
int main() {
    int record_count = 0;
    int record_capacity = 200;

    // Allocate initial memory
    ClimateRecord** records = malloc(record_capacity * sizeof(ClimateRecord*));

    FILE* file = fopen("climate-daily.csv", "r");
    char line[256];

    while (fgets(line, sizeof(line), file)) {
        // Resize the array when additional memory needed
        if (record_count == record_capacity) {
            record_capacity *= 2;
            records = realloc(records, record_capacity * sizeof(ClimateRecord*));
        }

        ClimateRecord* record = load_climate_data(line);
        if (record == NULL) {
            continue;
        }
        records[record_count++] = record;
    }

    fclose(file);

    analyzeData(records, record_count);
    userGeneratedReport(records, record_count);

    for (int i = 0; i < record_count; i++) {
        free(records[i]);
    }

    return 0;
}