# Single Face Extractor (a.k.a. Tak Nafar Generator)

<p align="center">
<img src="https://amintaheri23.github.io/img/portfolio/single_face.png">
</p>

This script will get a video from the directory 'trimmed' and generates video clips where there is only one face in it.
The main file name is: alltogether.py 

This script will get a video from a folder 'trimmed' and generates video 
clips where there is only one face (from one identity eg. Mohammad Reza Golzar) in it,
it uses: 

1. Open-CV (for manipulating videos and frame extraction),
2. RetinaFace (for face detection in frames),
3. scene detection (for detecting scenes and dividing them)

## Installing dependecies
Install dependencies using ``` pip3 install requirment.txt ```

## Making it work
Please manually make these directories
- trimmed
- scenesplitted
- output

## An Example Scenario
We get a video and load it with cv2, then we extract all of the frames in it, checking
for face exsistion will happen for every fps/2 in the video (eg for a 30 fps video we check every 15 frames). we divide clips here, then we run Scene Detection to make sure that in every
scene there is one identity.
After science detection we initial dividing phase to divide clips into unique scenes. 

(to demonstrate this let's imagine an example, imagine a scence
That Mr. Golzar was having a conversation with Sahar Ghoreyshi, the camera zoomed in on Mr. Golzar's face.
We have a cut and then we have a zoomed scene on Ms.Ghoreyshi's face. our algorithm should
divide this into 2 clips.)

## Performance
The 30 min clip for this script will have a time of 20 minutes or less on a core i7 (4 x 4.0 ghz) cpu 

## Attention
need to manually make 'output' and 'scenesplitted' dirs for output videos 
and need to have a 'trimmed' directory to input videos
all of them are in the script folder!

## Thanks and appreciations
Thanks to [Shenasa-ai.ir](http://Shenasa-ai.ir) and Alireza Akhavanpour and Bahar Baradaran for their sincere contributions.

## TODO: 
- [ ] add directories by script (not manual)
- [ ] fix creating extensive small sized unused clips
- [ ] add args for calling from terminal
- [ ] extract frames with FFMPEG instead of open cv
- [ ] enhance speed of algorithm
- [ ] fine tune scene detection
- [ ] over all enhancing
