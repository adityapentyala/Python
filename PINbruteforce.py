#This is a program that attempts to brute force attack a 4-numeric character password protected zip file.

#importing the required modules
from zipfile import ZipFile
import time

#noting time when program starts
starttime = time.time()

#listing the characters to use
numbers = list(map(str, '0123456789'))

#variable that tells us if we've found the password and can be used to tell the program to end
cracked = False

#nested loop - 4 levels for a 4 nember long PIN. Break statements tell the program to exit each successive loop if the password is found
for n1 in numbers:
    if cracked == True:
        break
    for n2 in numbers:
        if cracked == True:
            break
        for n3 in numbers:
            if cracked == True:
                break
            for n4 in numbers:
                pin_guess = n1 + n2 + n3 + n4                             #form a pin
                pin_guess_in_bytes = (bytes(pin_guess, 'utf-8'))          #encode it in bytes; ZipFile.read function takes its password parameter as a bytes object
                with ZipFile('/Users/sureshp/Desktop/samplezip.zip', 'r') as zip:
                    try:                                                  #tries accessing the file with the guessed password
                        data = zip.read('Users/sureshp/Documents/Sample/Untitled.rtf', pwd=pin_guess_in_bytes)
                        cracked = True                                    #changes the variable value to true
                        print(data.decode('utf-8'))
                    except:                                               #handles error in case of wrong password and continues the program
                        continue
                if cracked == True:                                       #prints the password and time taken and then breaks the loop, thereby ending the program
                    print("PASSWORD FOUND:", pin_guess)
                    print("TIME TAKEN:", time.time() - starttime, "seconds")
                    break
