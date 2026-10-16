with open("/sys/class/thermal/thermal_zone0/temp") as f:
    temp = float(f.read()) / 1000
    print(f"{temp}")

    file = open('cpu_temp.txt', 'a+')
    file.write('{:.1f}\n'.format(temp))
    file.close
