# Optical Character Recognition

Question:

Write a program called ocr.py that is called like this:
./ocr.py train-image-file.png train-text.txt test-image-file.png
The program should load in the train-image-file, which contains images of letters to use for training (we’ve supplied one for you). It should also load in the train-text file which is simply some text document that is representative of the language (English, in this case) that will be recognized. Then, it should use the classifier it has learned to detect the text in test-image-file.png and output the recognized text on the last line of its output. The training file used consists of the part of speech as well so it would be better to skip these while training the model.

[djcran@raichu djc-sol]$ ./ocr.py train-image-file.png train-text.txt test-image-file.png
Simple: 1t 1s so orcerec.
Viterbi: It is so ordered.
Final answer:
It is so ordered.

