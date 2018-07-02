# Projects
This is a repository of code, and data for my projects.
There are 2 projects listed here:

1) BookFlow
Bookflow is an image-processing based image search engine which was inspired by google images much like google images when searched with an image shows the relevant results we decided to build a similar platform for books.
Upon passing an queried book image BookFlow, extracts features from the passed image and tries to locate the book image as stored in the database upon a match it shows the details of the book stored in the database and the percentage of the match.


2) HOG Reader
HOG Reader is a computer vision and image processing application which is designed to read handwritten numbers.
This project was designed with various applications in mind like reading pincodes, phone numbers etc
HOG Reader works on the priciple of HOG image descriptor which stands for Histogram of Oriented Gradients, which unlike BookFlow which works with edge orientated feature extraction, operates on the gradient magnitude of the image.
But HOG alone is not enough to identify numbers for that we will also need to apply a Linear Support Vector Machine (SVM) to
learn the representation of image digits.

 

