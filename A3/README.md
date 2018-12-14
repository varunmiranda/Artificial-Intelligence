# Image Orientation Detection - Question devised by Prof. David Crandall
# Authors: 
#Code for KNN: Supriya Ayalur Balasubramanian 
#Code for Adaboost: Sumeet Mishra
#Code for Random Forest: Varun Miranda

Question:

To help you get started, we’ve prepared a dataset of images from the Flickr photo sharing website. The images were taken and uploaded by real users from across the world, making this a challenging task on a very realistic dataset.

Since image processing is beyond the scope of this class, we don’t expect you to implement any special techniques related to images in particular. Instead, we’ll simply treat the raw images as numerical feature vectors, on which we can then apply standard machine learning techniques. In particular, we’ll take an n × m × 3 color image (the third dimension is because color images are stored as three separate planes – red, green, and blue), and append all of the rows together to produce a single vector of size 1 × 3mn. We’ve done this work for you already, so that you can treat the images simply as vectors and do not have to worry about them being images at all.

To generate this file, we rescaled each image to a very tiny “micro-thumbnail” of 8 × 8 pixels, resulting in an 8 × 8 × 3 = 192 dimensional feature vector. The text files have one row per image, where each row is formatted like:

photo_id correct_orientation r11 g11 b11 r12 g12 b12 ...

where:
• photo id is a photo ID for the image.
• correct orientation is 0, 90, 180, or 270. Note that some small percentage of these labels may be wrong because of noise; this is just a fact of life when dealing with data from real-world sources.
• r11 refers to the red pixel value at row 1 column 1, r12 refers to red pixel at row 1 column 2, etc., each in the range 0-255.

You can view the original high-resolution image on Flickr.com by taking just the numeric portion of the photo id in the file above (e.g. if the photo id in the file is test/123456.jpg, just use 123456), and then visiting the following URL:

http://www.flickr.com/photo_zoom.gne?id=numeric_photo_id

The training dataset consists of about 10,000 images, while the test set contains about 1,000. For the training set, we’ve rotated each image 4 times to give four times as much training data, so there are about 40,000 lines in the train.txt file (the training images on Flickr and the ZIP file are all oriented correctly already). In test.txt, each image occurs just once (rotated to a random orientation) so there are only about 1,000 lines. If you view these images on Flickr, they’ll be oriented correctly, but those in the ZIP file may not be.

Your goal is to implement and test several different classifiers on this problem: k-nearest neighbors, AdaBoost, and decision forests. For training, your program should be run like this:

./orient.py train train_file.txt model_file.txt [model]

where [model] is one of nearest, adaboost, forest, or best. This program uses the data in train file.txt to produce a trained classifier of the specified type, and save the parameters in model file.txt. You may use any file format you’d like for model file.txt; the important thing is that your test code knows how to interpret it. For testing, your program should be run like this:

./orient.py test test_file.txt model_file.txt [model]

where [model] is again one of nearest, adaboost, forest, best. This program should load in the trained parameters from model file.txt, run each test example through the model, display the classification accuracy (in terms of percentage of correctly-classified images), and output a file called output.txt which indicates the estimated label for each image in the test file. The output file should correspond to one test image per line, with the photo id, a space, and then the estimated label, e.g.:

test/124567.jpg 180
test/8234732.jpg 0