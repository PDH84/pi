#!/usr/bin/python3
import adafruit_dht
import board
import gspread
import json
import os
import pathlib
import subprocess
import time
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

class Temp_Sensor():
    repo_path = pathlib.Path(__file__).parent.resolve()
    heater_on = f"{repo_path}/heater_on.expect"
    heater_off = f"{repo_path}/heater_off.expect"
    command_turn_on = f"{repo_path}/power_on.bash"
    command_turn_off = f"{repo_path}/power_off.bash"
    command_check_relay = f"{repo_path}/check_power.bash"
    command_check_battery= f"{repo_path}/delta2_battery_check.py"
    google_auth_file = f"{repo_path}/shedcontroller-718509a14bc9.json"
    check_date = f"{repo_path}/check_date.bash"
    temp_f = None
    is_relay_on = None
    control_mode = "HEAT"

    def run_script(self, file):
        try:
            result = subprocess.run(file, capture_output=True, text=True)
            std_out = result.stdout
            return std_out
        except Exception as err:
            print("Unable to run {}".format(file))
            print(err)

    def get_battery_level(self):
        try:
            std_out = self.run_script(self.command_check_battery)
            percent = int(std_out.split(":")[1])
            return percent
        except Exception as err:
            print("Unable to run battery check script")
            print(err)

    def str_to_bool(self, val):
        if val is None:
            return False
        return val.lower() == "true"

    def get_relay_status(self):
        is_on = None
        try:
            std_out = self.run_script(self.command_check_relay)
            out_dict = json.loads(std_out)
            is_on = self.str_to_bool(str(out_dict["ison"]))
        except Exception as e:
            print(f"Error: {e}")
        self.is_relay_on = is_on
        if self.is_relay_on:
            print("Relay ON")
        elif self.is_relay_on is None:
            print("Relay not responsive")
            self.is_relay_on = False
        else:
            print("Relay OFF")

    def change_power_state(self, file):
        std_out = self.run_script(file)

    def get_tempf(self):
        dht_device = adafruit_dht.DHT22(board.D2)
        try:
            temp_c = dht_device.temperature
            self.temp_f = temp_c * (9/5) + 32
            humidity = dht_device.humidity
            dht_device.exit()
            print("Temp = {}".format(self.temp_f))
            print("Humidity = {}".format(humidity))
        except:
            print("Can't read temp sensor")

    def check_status(self):
        #checks if it is still the same day and runs the summarize script
        self.run_script(self.check_date)
        current_datetime = datetime.now()
        timestamp = current_datetime.strftime("%H:%M")
        hour_time = int(current_datetime.strftime("%H"))
        print(timestamp)
        self.get_tempf()
        if self.control_mode == "COOL":
            max_temp = 80
            min_temp = 70
        if self.control_mode == "HEAT":
            max_temp = 45
            min_temp = 40

        charge_percent = self.get_battery_level()
        action = "OFF"
        print(f"Battery Level: {charge_percent}")

        if self.control_mode == "COOL":
            if hour_time > 8 and hour_time < 18:
                if charge_percent > 80 and self.temp_f > min_temp:
                    print("Daytime")
                    action = "ON"
            if hour_time > 1 and hour_time < 7:
                if charge_percent > 60 and self.temp_f > min_temp:
                    print("Nighttime")
                    action = "ON"

        if self.control_mode == "HEAT":
            if charge_percent > 85 and self.temp_f < max_temp:
                action = "ON"
            if charge_percent > 40 and self.temp_f < min_temp:
                action = "ON"

        if self.control_mode == "COOL":
            if action == "ON":
                print("Turning on relay")
                self.change_power_state(self.command_turn_on)
            else:
                print("Turning off Relay")
                self.change_power_state(self.command_turn_off)

        if self.control_mode == "HEAT":
            if action == "ON":
                print("Turning on Heater")
                self.run_script(self.heater_on)
                self.is_relay_on = True
            else:
                print("Turning off Heater")
                self.run_script(self.heater_off)
            

        self.get_relay_status()

        print("Writing Local Log")
        output_file = '/home/jread/shed_controller/data.csv'
        if not os.path.exists(output_file):
            with open(output_file, 'a') as file:
                file.write("timestamp, charge_percent, self.temp_f, action, self.is_relay_on\n")
        with open(output_file, 'a') as file:
            file.write("{},{},{:.1f},{},{}\n".format(timestamp, charge_percent, self.temp_f, action, self.is_relay_on))

        #Log to google drive
        # Define the scope and load credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.google_auth_file, scope)
        client = gspread.authorize(creds)
    
        print("Authenticating Remote Log")
        
        retries = 3
        delay = 10
        for attempt in range(retries):
            try:
                # Open your Google Sheet (by name) and worksheet (usually Sheet1)
                sheet = client.open("shed_temp_log").sheet1
                print("Writing Remote Log")
                # Append data to the next available row
                sheet.append_row([timestamp, charge_percent, self.temp_f, action, self.is_relay_on])
                return
            except Exception as e:
                print(f"Connection error, attempt {attempt + 1} failed")
                print(f"Trying again in {delay} seconds")
                time.sleep(delay)
                if attempt == retries:
                    print("Cannot access remote network")
                    exit(1)

        exit(0)

if __name__ == "__main__":
    temp_sensor = Temp_Sensor()
    temp_sensor.check_status()
