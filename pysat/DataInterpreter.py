import os
import pynmea2
'''This was made quickly to analyze our launch data and does not have any real purpose in the overall program'''
'''This might be helpful to analyze your own data or build this out into an MVC website that shows you the data'''


class DataInterpreter:

    @staticmethod
    def make_csv_from_files(files_dir, csv_file_name):
        csv = open("C:\\Users\\Justin\\Desktop\\Technical_Project\\analyzed.csv", "w")
        files = os.listdir("C:\\Users\\Justin\\Desktop\\Technical_Project\\launch_data")
        files.sort()
        for file in files:
            try:
                print(file)
                file = open(os.path.join("C:\\Users\\Justin\\Desktop\\Technical_Project\\launch_data", file), "r")
                lines = file.readlines()
                for line in lines:
                    parts = line.split("\",\"")
                    final_line = parts[0][1:-2] + ","
                    try:
                        gpgga = pynmea2.parse(parts[1])
                        final_line = final_line + str(gpgga.latitude) + "," + str(gpgga.longitude) + "," + str(
                            gpgga.altitude) + ","

                        gprmc = pynmea2.parse(parts[2])
                        final_line = final_line + str(gprmc.spd_over_grnd) + "," + str(gprmc.timestamp)
                    except:
                        final_line = final_line + "None,None,None,None,None"
                    # final_line = final_line + parts[3][:-2]

                    x = ""
                    csv.write(final_line + "\n")
            except Exception as e:
                print(e)
            finally:
                file.close()
        csv.close()
