# Walk As One

## Objective
We wanted to design an interactive device that would help people reach their exercise goals in an innovative way. The problem we identified with current exercise devices and trackers (such as Apple Watches, Fitbits, etc.) are that they could help a person reach their own exercise goals, but often an individual may have difficulty finding the motivation to exercise just from their own device. We present "We Walk As One," a distributed device where a group of users can combine their goals together
as a collective in order to Walk As One.

## Description
A single user's device consists of a Raspberry Pi 4, connected to a MiniPiTFT and an Adafruit MPU-6050. Another important requirement is connection to the Internet, since the devices communicate using MQTT, which we familiarized ourselves with in Lab 6. Every Raspberry Pi belonging to a group of users will run the app.py and member-reader.py 
scripts, and one Pi (or any device that can act as a server) runs server.py. Each of these programs is described further below.

## Design Process
Our design process followed an incremental pattern, where we developed and tested each feature that we wanted in the final design independently, and combined them together at the end. The major components of our design consisted of:\ 
1. Motion/step detection
2. Sending Data Through MQTT
3. Receiving Data With MQTT
4. Displaying Data on the MiniPiTFT
5. Showing Overall Group Progress On Webpage

These design components, along with their corresponding Python code, are explained below:

### app.py
This program uses the MPU-6050 accelerometer to collect acceleration data, and uses a filter on the data in order to detect a "step," in a manner similar to a pedometer. 
We accomplished this step detection 
behavior by first taking one accelerometer reading (in the x, y, and z dimensions) as a "baseline," then subsequently taking 10 samples
and comparing them to the baseline. We take the sum of the differences between each reading and the baseline, and then if that sum exceeds a certain threshold, then we 
register a step. We used this method because we wanted a reliable way to detect a step, and other methods we tried were not as consistent. If a sample was only compared to the previous one, the pedometer would be too sensitive to changes and register too many steps. If we used too long of a sampling window, or added delays that were too long, the system would miss steps. 
Furthermore, we initially only examined data in one dimension (the z dimension), which we thought was effective since our initial testing was only by shaking the accelerometer. 
As we tested the accelerometer more, and also considered how we wanted to attach it to a user, we realized it would be much more effective if we made its behavior agnostic to
the orientation of the accelerometer itself. Thus we decided to expand the readings to account for all three dimensions, and took the square root of the differences squared as the result. This gave us much better step detection, and we were comfortable moving on to the next design step.

### server.py
This program uses MQTT as both a client and a server, taking advantage of the python Threading library to accomplish this. We decided to use MQTT because of its beautiful simplicity, allowing any number of clients to connect, push messages to the same topic, and listen to messages from the same topic in a highly distributed yet easy-to-use manner. In the client thread, the program listens for step updates from members. When it gets an update, it increments a global "stepCount" variable. This is the method we use to allow many users to all send step updates to a 
centralized location, which accumulates them. The reason stepCount is global is in order to allow another server thread (running in "main") to send out MQTT messages corresponding to the current stepCount total. We thought using threading would be a more elegant solution for allowing a client and a server to run concurrently rather than having to execute two Python scripts.
To test the server program, we used the MQTT Explorer program introduced in Lab 6 in order to send messages to the appropriate topic, and check that the server was responding with updated stepCount totals.

### member-reader.py
This program also uses MQTT to read in a total stepCount, and maps it to a progress bar shown on the MiniPiTFT. The result is shown below:


### Putting It All Together
To get all of our programs to work together, we modified app.py to keep track of the number of steps it detects, sending a message after a certain number is reached. It then broadcasts that number through MQTT on the "member" topic to be received by the server. The server behavior remains unchanged from when we tested it. member-reader.py reads the message that the server sends on each update through 
the "goal" topic, and the updates are reflected on the progress bar, which will be displayed on every member's device that is connected.

An additional feature we added after filming our demo video (below), based on feedback from our functional demo that we didn't have time to implement, was to implement within server.py
a webpage host that displays the total stepCount over time, as an additional way to track the activity of a group:

## Video
Here are our demo videos!
1. [Device Explanation](https://drive.google.com/file/d/1Q2UmhhDiq2YnH0HOuFTd2Yv1kTwAkwFC/view?usp=sharing)
2. [Demo Video](https://drive.google.com/file/d/18brt5WscvJwN8dK8VTIqkXXAIoyJSPlT/view?usp=sharing)
3. [Edited Video We Showed in Class](https://drive.google.com/file/d/1TlNYVYbU1G9MFd2cv2dusruymZlbddWb/view?usp=sharing)

## Reflections
Exercise (and software work) can be difficult for many people, but doing anything with a group makes even difficult things potentially more fun. We thought we were able to convey this philosophy successfully with our project, both in the process and with the end result. We also wanted to take advantage of 
a number of the things we learned in this class, such as using MQTT, sensor integration with the Pi, TFT display, and webpage development. In the end, we wish we had a little more time to work on our project since we didn't get to implement the 
webpage aspect in time for the class demonstration, but we thought we were still able to show our project effectively. The most difficult part of this lab
actually ended up being the webpage development, since we are still new to incorporating html and javascript code along with using socketio. However,
the experience was definitely valuable, and we're glad we chose to work on this project.

## Teams

I worked with Sujith Naapa Ramesh as my partner for this project. As far as work distribution is concerned, we used peer programming to develop our Python programs rather than working on different files independently, which helped us catch bugs and also allowed us to stay on the same page throughout the entirety of the project.
