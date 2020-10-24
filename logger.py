import os
import sys
import os.path
import time
from datetime import datetime

class Logger:

    def __init__(self):
        self._start_time = None
        self._end_time = 5
        self._current_file = check_file(self)

        '''Create a file that can be used as a reference chart for input ----> file#'''
        if(os.path.isfile):
            write_log = open("ref_chart.txt", "a+")
            write_log.write("|DateTime\t\t\t\t\t |Input \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t |File Name\n")
            write_log.write("_" * 400+ "\n")
        else:
            write_log = open("ref_chart.txt", "a+")
            write_log.write("|DateTime\t\t\t\t\t |Input \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t |File Name\n")
            write_log.write("_" * 400+ "\n")

    global check_file
    def check_file(self):
        '''Check to see if the current file path exists, if it doesn't create a file. 
        If the file path exists, create a new file incremented by 1'''
        
        try:
            os.makedirs('Done_Files')
        except OSError as e:
            None

        i = 1
        while os.path.exists("Done_files/file%s.txt" % i):
            i += 1
        self._current_file = open("Done_Files/file%s.txt" % i, "a+")
        return self._current_file
       
    
    def log(self, input):
        '''Writes input to the current_file and returns the current file number put done files in "FileDone" directory '''
        input = str(input)

        def write_to_current_file():
            self._start_time = time.perf_counter()
            if(self._start_time < self._end_time):
                dateTimeObj = datetime.now()
                timeStamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                self._current_file.write(str(timeStamp) + ":\t")
                self._current_file.write(input + "\n")

            else:
                dateTimeObj = datetime.now()
                timeStamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                self._start_time = None
                self._current_file = check_file(self)
                self._current_file.write(str(dateTimeObj) + ":\t\t\t")
                self._current_file.write(input + "\n")
                self._end_time = self._end_time + 5
                
        '''Write the input to the respected file'''
        write_to_current_file()
        file_name = self._current_file.name
        
        '''Append input data to ref_chart.txt'''
        if(os.path.isfile):
            dateTimeObj = datetime.now()
            timeStamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
            write_log = open("ref_chart.txt", "a+")
            write_log.write(str(timeStamp) + ":\t\t\t")
            write_log.write(input + "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ")
            write_log.write("\t"+file_name + "\n")
            write_log.write("_" * 400+ "\n")
        else:
            dateTimeObj = datetime.now()
            timeStamp = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S)")
            write_log = open("ref_chart.txt", "a+")
            write_log.write(str(timeStamp) + ":\t\t\t")
            write_log.write(input +"\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ")
            write_log.write("\t"+file_name + "\n")
            write_log.write("_" * 400+ "\n")





        

        
        

        

        

           
        
        

            
            
            
        

        

    


        

        



        
        


       
    




        
    

        
        


   
    


    




   
