# You are wizards, Andrew and Sujith!

<img src="https://pbs.twimg.com/media/Cen7qkHWIAAdKsB.jpg" height="400">

In this lab, we want you to practice wizarding an interactive device as discussed in class. We will focus on audio as the main modality for interaction but there is no reason these general techniques can't extend to video, haptics or other interactive mechanisms. In fact, you are welcome to add those to your project if they enhance your design.


## Text to Speech and Speech to Text

In the home directory of your Pi there is a folder called `text2speech` containing some shell scripts.

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav

```

you can run these examples by typing 
`./espeakdeom.sh`. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts

```

You can also play audio files directly with `aplay filename`.

After looking through this folder do the same for the `speech2text` folder. In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

## Serving Pages

In Lab 1 we served a webpage with flask. In this lab you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/$ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to [http://ixe00.local:5000]()


## Demo

In the [demo directory](./demo), you will find an example wizard of oz project you may use as a template. **You do not have to** feel free to get creative. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser. You can control what system says from the controller as well.

## Optional

There is an included [dspeech](./dspeech) demo that uses [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) for speech to text. If you're interested in trying it out we suggest you create a seperarate virutalenv. 



# Lab 3 Part 2

Create a system that runs on the Raspberry Pi that takes in one or more sensors and requires participants to speak to it. Document how the system works and include videos of both the system and the controller.

## Prep for Part 2

1. Sketch ideas for what you'll work on in lab on Wednesday.

## Share your idea sketches with Zoom Room mates and get feedback

Grace Tan: "I really like your idea and thought it was also a nice touch with the LEDs.  I think it would also be cool if the system could "learn" and "remember" people the users have invited in the past- as a future step"

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 


Our storyboard for PyCom:
![Sketch 1](https://github.com/andrewhtsai/Interactive-Lab-Hub/blob/Spring2021/Lab%203/ECE5413_Lab3Storyboard.jpg)
*Document how the system works*

*Include videos or screencaptures of both the system and the controller.*

Here is a video demonstrating our system: https://drive.google.com/file/d/1SUpWerY2CTSv-QRWXjFIHoZzKEhVfbUO/view?usp=sharing
## Test the system
We had two of Sujith's housemates help test out our system and provide some feedback.

### What worked well about the system and what didn't?
Andy Zhu: The arming operation and the speech seemed to work, but the proximity sensor was inconspicuous and it was not obvious how to interact with it. There was also
a lot of latency between speaking into the mic and hearing a response, which made the system feel a little unnatural.

Rishi Singhal: The bright red LED signifying armed/disarmed was cool, and waving the hand as kind of a "doorbell ringing" gesture was a neat interaction. The voice
latency however felt like it could be improved.


### What worked well about the controller and what didn't?
The text to speech worked amazingly well, and was a great way to introduce an "automated" feel to the system experienced by the end user. However, the latency of 
transmitting the mic voice audio was quite high as remarked on by our two testers, and that made the interaction feel more unnatural than it could have been with 
modern technology especially when considering the added time of having to type a response.

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?
If the system were automated, the overall latency would likely be very much reduced since the need for streaming/responding would be removed, and instead replaced
with logic running on the Pi. A database containing names of "good neighbors", as part of Grace's feedback, would be a very good implementation feature, although
the logic for determining whether to disarm for a new arrival would likely require several back-and-forth dialogues and would be rather complicated to program.


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?
A potential sensor to use for this intercom/security system would be a fingerprint sensor, which would easily allow for authentication of people who are
already registered within the system. Also, now in COVID times, a temperature sensor could also be integrated to allow for temperature measurements before anyone
is allowed in.

For this lab, both were very hands-on with the hardware and software, and we used peer programming when writing code for all of the software files that we worked on.
