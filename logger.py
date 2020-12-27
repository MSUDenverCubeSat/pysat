import os
import sys
import os.path
from os import path
import time
from time import perf_counter

class Logger:

    
    def __init__(self, text = "Elapsed time: {:0.4f} seconds"):
        self._start_time = None
        self._end_time = 5
        self._current_file = check_file(self)

    global check_file
    def check_file(self):
        '''Check to see if the current file path exists, if it doesn't create a file. 
        If the file path exists, create a new file incremented by 1'''
    
        i = 1
        while os.path.exists("file%s.txt" % i):
            i += 1
        self._current_file = open("file%s.txt" % i, "a+")
        return self._current_file
    
    def log(self, input):
        '''Writes input to the current_file and returns the current file number'''
        def write_to_current_file():
            self._start_time = time.perf_counter()
            if(self._start_time < self._end_time):
                self._current_file.write(input+ "\n")
            else:
                self._start_time = None
                self._current_file = check_file(self)
                self._current_file.write(input + "\n")
                self._end_time = self._end_time + 5
            
        write_to_current_file()
        current_file = self._end_time / 5
        print("Input Written to File number", current_file)
        

        
        

        

        

           
        
        

            
            
            
        

        

    


        

        



        
        


       
    




        
    

        
        


   
    


    




   
