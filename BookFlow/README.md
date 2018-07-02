# Dependencies
You will need to install Python's OpenCV library:

      pip install opencv-python

This will install OpenCV3 which is what is used in this project.

You will also need to install Python's Numpy library:

    pip  install numpy
    
#Usage
Need to run the script on commandline with the following parameters:
a) location of database which stores information of each image(.csv)
b) location of the images folder which has images stored in database
c) query image which is to be matched


Example:

<img width="682" alt="screen shot 2018-07-03 at 00 23 54" src="https://user-images.githubusercontent.com/40769934/42181472-8c6a11be-7e58-11e8-8216-45c1fbd4b356.png">


  
 This will produce the following output:
 
 
 
<img width="889" alt="screen shot 2018-07-03 at 01 27 41" src="https://user-images.githubusercontent.com/40769934/42183732-9832f0bc-7e60-11e8-9a88-b4b5bfdecd79.png">



As you can see in the above snap the script was able to locate and indentify the book in the noisy image with an accuracy of
82.46%.
