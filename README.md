# Single Face Extractor (Tak nafar generator)
this script will get a video from a folder 'trimmed' and generates video  clips that there is only one face 
The main file name is: alltogether.py 

this script will get a video from a folder 'trimmed' and genrates video 
clips that there is only one face (from one identity eg. Mohammad Reza Golzar) in it,
it uses:  
1. Open-CV (for manipulating videos and frame extraction),
2. RetinaFace (for face detection on frames),
3. scenedetect (for detecting scene and divide them)

## Installing dependecies
Install dependencies using ``` pip3 install requirment.txt ```

## An Example Scenario
we get an video and load it with cv2, then we extract all of the frames in it, checking
for face existion will happen every fps/2 in video (eg for a 30 fps video we check every
 15 frames). we divide clips here, then we run Scene Detection to make sure that in every
scene there is one identity.
after scence detection we inital dividing phase to divide clips into unique scenes. 

(to demonstrate this lets imagine an example, imagine a scence
that Mr golzar having a Conversation wih Sahar Ghoreyshi, camera is zoomed at Mr.Golzar face
and we have a cut and then we have a zoomed scene on Ms.Ghoreyshi's face. our algorithm should
divide thsis into 2 clips.)


## Performance
a 30 min clip for this script will have a time of 20 minutes or less on a core i7 (4 x 4.0 Ghz) cpu 


## Attention
need to make 'output' and 'scenesplitted' dirs for output videos 
and need to have a 'trimmed' dir for input videos
all of them in script folder!


## TODO: 
- [x] smiling
- [ ] fix creating extensive small sized unused clips
- [ ] add args for calling from terminal
- [ ] extrac frames with FFMPEG instead of open cv
- [ ] enhance speed of algorithm
- [ ] fine tune scene detection
- [ ] over all enhancing
