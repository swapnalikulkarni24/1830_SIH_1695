import pandas as pd


file_path = 'DWLR_synthetic_data.csv'
df_original = pd.read_csv(file_path)

rainfall_file_path = 'synthetic_rainfall_dataset_2024.csv'
df_rainfall = pd.read_csv(rainfall_file_path)

MOVING_AVERAGE_WINDOW = 10

def get_moving_average_range(df, column_name, window, rainfall_mm):
    """
    Calculate the moving average and dynamically adjust the standard deviation
    based on the rainfall levels. Returns the lower and upper bounds for water level.
    """
 
    moving_avg = df[column_name].tail(window).mean()
    std_dev = df[column_name].tail(window).std()

    if rainfall_mm == 0:
        adjustment_factor = 1.0  # No rainfall => no adjustment
    elif 0 < rainfall_mm <= 2:
        adjustment_factor = 1.2  # Low rainfall
    elif 2 < rainfall_mm <= 5:
        adjustment_factor = 1.5  # Moderate rainfall
    elif 5 < rainfall_mm <= 10:
        adjustment_factor = 1.8  # Heavy rainfall
    else:
        adjustment_factor = 2.0  # Very heavy rainfall


    lower_bound = moving_avg - (adjustment_factor * std_dev)
    upper_bound = moving_avg + (adjustment_factor * std_dev)

    return lower_bound, upper_bound

def validate_and_add_data(timestamp, water_level, battery):

    date = pd.to_datetime(timestamp).strftime("%Y-%m-%d")
    hour = pd.to_datetime(timestamp).strftime("%H:%M:%S")

    rainfall_mm = df_rainfall.loc[(df_rainfall['date'] == date) & (df_rainfall['hour'] == hour), 'rainfall (MM)'].values[0]

    water_level_lower, water_level_upper = get_moving_average_range(df_original, 'Water Level (m)', MOVING_AVERAGE_WINDOW, rainfall_mm)

    if not (water_level_lower <= water_level <= water_level_upper):
        return f"Error: Water level is an outlier based on the last {MOVING_AVERAGE_WINDOW} readings. \n" \
               f"Expected water level range: {water_level_lower:.2f} to {water_level_upper:.2f}.\nData not added."

    battery_message = ""
    if battery < 20.0:
        battery_message = "Warning: Battery is below 20%. Please replace or charge the battery."

    new_entry = pd.DataFrame([[timestamp, water_level, battery, 'normal']],
                             columns=['Timestamp', 'Water Level (m)', 'Battery (%)', 'Sensor Status'])

    new_entry.to_csv(file_path, mode='a', header=False, index=False)

    if battery_message:
        return f"Success: Data added to the dataset.\n{battery_message}"
    else:
        return "Success: Data added successfully to the dataset."


timestamp = "2024-09-22 12:00" 
water_level = float(input("Enter water level: "))  
battery = float(input("Enter battery percentage: ")) 


message = validate_and_add_data(timestamp, water_level, battery)
print(message)
