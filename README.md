# learn-numbers

## Introduction
This is the a web application for children to learn numbers mainly using Flask, python, javascript.
It performs well in both Edge or Chrome browser.

* The main page:

![avatar](/picture/main.jpg)
* The reading page:
 
Click the voice button and will hear a number. Then they can write on the canvas on the right.

Click recognize to displace the number using digit recognition based on MNIST dataset.

![avatar](/picture/reading.jpg)

Click submit answer you can know the result like this:

If your answer is right:

![avatar](/picture/right.jpg)

If your answer is wrong:

![avatar](/picture/wrong.jpg)


* The math page:

The process is similar to reading. There will be a simple math problem and you can write your answer to automatically check.

![avatar](/picture/math.jpg)


## Requirement
* Language: python 3.6
* Frame: flask
* Computer vision: sklearn, skimage
* Voice: pyttsx3

## Run
STEP 1
install packages like flask (other needed pakages is the same)
```
pip install flask
```

STEP 2
run the web 
```
python project.py
```

