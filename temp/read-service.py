import os
import glob
import time
from flask import Flask, jsonify

# Flask App
app = Flask(__name__)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    try:
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return {"celsius": "{:.2f}".format(temp_c), "fahrenheit": "{:.2f}".format(temp_f)}
    except Exception as e:
        return {"error": str(e)}

@app.route('/temperature', methods=['GET'])
def get_temperature():
    return jsonify(read_temp())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

