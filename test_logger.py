from logger import Logger
import time

def method_test1(t):
    i = 0
    j = 42
    for cnt in range(i, j+1):
        t.log(cnt)
    t.log("\n---------------END OF FILE METHOD_TEST1-----------------------------------")

def method_test2(t):
    i = 1
    j = 24
    for cnt in range(i, j+1):
        t.log(cnt)
    t.log("\n---------------END OF FILE METHOD_TEST2-----------------------------------")

def test_characters(t):
    t.log("hello, 1, $%^#@#$, 100.9, 23.3456738")  

if __name__ == "__main__":
    
    #These inputs should all write to file1.txt
    t = Logger()
    t.log("file1")
    t.log("file1")
    t.log("file1")

    #These inputs should all write to file2.txt
    time.sleep(5)
    t.log("file2")
    t.log("file2")

    #These inputs should all write to file3.txt
    time.sleep(5)
    t.log("file3")

    #These inputs should all write to file4.txt
    time.sleep(5)
    t.log("file4")
    t.log("file4")
    t.log("file4")
    t.log("file4")

    #These inputs should all write to file5.txt
    time.sleep(5)
    t.log("file5")
    t.log("file5")
    t.log("file5")
    t.log("file5")
    t.log("file5")
    t.log("file5")
    t.log("file5")
    t.log("file5")

    #These inputs should all write to file6.txt
    time.sleep(6)
    t.log("file6")
    #These inputs should also write to file6.txt
    time.sleep(1)
    t.log("forLoop")
    i = 0
    j = 2
    for cnt in range(i , j+1):
        t.log(cnt)

    #These inputs should all write to file7.txt
    time.sleep(3)
    t.log("file7")
    t.log("file7")
    #These inputs should also write to file7.txt
    time.sleep(1)
    method_test1(t)
    method_test2(t)

    #These inputs should all write to file8.txt
    time.sleep(5)
    method_test2(t)

    #These inputs should all write to file9.txt
    time.sleep(5)
    test_characters(t)
    


    
    


    



    
    

    
        
