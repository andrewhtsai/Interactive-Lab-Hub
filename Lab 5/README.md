# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

In Lab 5 part 1, we focus on detecting and sense-making.

In Lab 5 part 2, we'll incorporate interactive responses.


## Prep

1.  Pull the new Github Repo.
2.  Read about [OpenCV](https://opencv.org/about/).
3.  Read Belloti, et al's [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf)

### For the lab, you will need:

1. Raspberry Pi
1. Raspberry Pi Camera (2.1)
1. Microphone (if you want speech or sound input)
1. Webcam (if you want to be able to locate the camera more flexibly than the Pi Camera)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.


## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

Befor you get started connect the RaspberryPi Camera V2. [The Pi hut has a great explanation on how to do that](https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera).  

#### OpenCV
A more traditional to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python.

Additionally, we also included 4 standard OpenCV examples. These examples include contour(blob) detection, face detection with the ``Haarcascade``, flow detection(a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (I.e. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example.

```shell
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
#### Filtering, FFTs, and Time Series data. (beta, optional)
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the set up from the [Lab 3 demo](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Spring2021/Lab%203/demo) and the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

Include links to your code here, and put the code for these in your repo--they will come in handy later.

#### Teachable Machines (beta, optional)
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple.  However, its simplicity is very useful for experimenting with the capabilities of this technology.

You can train a Model on your browser, experiment with its performance, and then port it to the Raspberry Pi to do even its task on the device.

Here is Adafruit's directions on using Raspberry Pi and the Pi camera with Teachable Machines:

1. [Setup](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/raspberry-pi-setup)
2. Install Tensorflow: Like [this](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4/tensorflow-lite-2-setup), but use this [pre-built binary](https://github.com/bitsy-ai/tensorflow-arm-bin/) [the file](https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl) for Tensorflow, it will speed things up a lot.
3. [Collect data and train models using the PiCam](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/training)
4. [Export and run trained models on the Pi](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/transferring-to-the-pi)

Alternative less steps option is [here](https://github.com/FAR-Lab/TensorflowonThePi).

#### PyTorch  
As a note, the global Python install contains also a PyTorch installation. That can be experimented with as well if you are so inclined.

### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interactions outputs and inputs.
**Describe and detail the interaction, as well as your experimentation.**

We first experimented with all four of the given OpenCV examples, and we decided that we really liked the flow detection. We thought it could potentially be useful for autonomous tracking of data points, and then we put an experimental lab setting spin on it. 
We envisioned the interaction being a scientist running an experiment on some distinct samples, potentially tracking their movement over a period of time. Other features would include detection of interference of any sort, like if someone else moves the samples and thus ruins the experiment. 
We experimented using drawings on a piece of paper and by moving the camera around, though we finally settled on drawing shapes on a tablet which gave the flexibility of moving the shapes around while keeping lighting conditions stable and allowing for finer control. 
We also thought it would be a good idea to implement an additional feature which would be beneficial for experiments: color detection. By analyzing and identifying distinct colors, the system can give much more information to someone running the experiment with regards to the sample behaviors. Thus a colored bounding box corresponding to the color
of the samples is drawn on top of each sample.

We also implemented a notification system, where if something drastic happens to the samples, such as a sample moving out of the detection area or interference causing samples
to no longer be detected, the program would stop and the experimenter would be sent a notification email. We originally wanted the program to continue running in case it would
recover from the error, but we came to the realization that we did not want to end up potentially sending large amounts of spam emails.


### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note your observations**:
For example:
1. When does it do what it is supposed to do?
    
The system does what it is supposed to do when the tablet is placed in front of the camera and the samples are clearly displayed on the screen.

2. When does it fail?

The system fails when the tablet is placed irregularly causing extreme differences in lighting from one end of the screen to the other. In addition, it also fails when 
the environmental lighting changes drastically, or when there is too much movement in the camera frames capturing the sample behavior.

3. When it fails, why does it fail?

Another Set of Eyes is quite sensitive to lighting, due to limits in the robustness of the openCV scripts. By testing with the masking thresholds for color detection, we were
able to increase the accuracy of the bounding boxes for the differently colored samples. However, we were not able to improve the accuracy of the flow detection algorithm, which
would often assign multiple flow points to the same sample object due to its usage of corner detection rather than assigning a single point to a given contour.

4. Based on the behavior you have seen, what other scenarios could cause problems?

Other scenarios that could cause problems would be if the experiment was carried out in an unstable environment with random movements that would shake the camera or the samples,
which would introduce artifical movements and thus reducing the accuracy shown by the resultant flows. Another potential failure case would be if the samples were all different colors, which would confuse the system and cause it to sometimes detect false results if a color happened to be on the detection border for a given color.

**Think about someone using the system. Describe how you think this will work.**
1. Are they aware of the uncertainties in the system?
 
Some of the uncertainties are the physical size of the experiment, the lighting in the environment, and the colors present in the experiment. A user also
may not be aware of the detection limitations of the experiment, and if a sub-optimal set of samples is used, they may end up getting notified improperly.

2. How bad would they be impacted by a miss classification?

If the device predicts a change in the experiment when there has not been one, then the user is notified to check on the experiment when they don’t need to. If the device misses a change, then the user will miss important pieces of data from the experiment, which is much more problematic.

3. How could change your interactive system to address this?

The system could be much more sensitive to changes in the experiment because it is much better to have unnecessary notifications than missed notifications. It could also
likely benefit from another camera running the same program so that the two can cross-reference each other for more accuracy.

4. Are there optimizations you can try to do on your sense-making algorithm?

We could potentially incorporate detecting changes in the color of the experiment. Since many experiments show color changes over time, our computer vision algorithm could incorporate this input to determine when the experiment might be finished.

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**Include a short video demonstrating the answers to these questions.**

Our video answering these questions can be found [here](https://drive.google.com/file/d/1eiPhdQPKhIHkjXhv0XilJd30r4qmnkoX/view?usp=sharing)

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.

**Include a short video demonstrating the finished result.**

A short storyboard detailing the final interaction (video below):
![sketch](https://github.com/andrewhtsai/Interactive-Lab-Hub/blob/Spring2021/Lab%205/ECE%205413-11.jpg)

Our video showing a demonstration of the final product is [here](https://drive.google.com/file/d/1cW7JX8A9F8dvAUnqGkXe3j36oqWrXYD-/view?usp=sharing)


**Work Distribution**
Andrew and Sujith worked together on this lab with a brainstorming session to decide how we would use OpenCV, and then after deciding on the project, using peer programming to develop the code and coming up with answers to the characterization questions together.
