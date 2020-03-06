from retinaface import RetinaFace
import cv2
from scenedetect.scene_manager import SceneManager
from scenedetect.video_manager import VideoManager
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors.content_detector import ContentDetector
from os import listdir, remove, path
import os
from os.path import isfile, join
import shutil

#defien importatnt parameters
DETECTION_THRESHOLD = 0.6  # you can change this
VIDEO_DIR = 'trimmed/'
VIDEO_OUT_DIR = 'output/'

#retina face initializataion
model = RetinaFace('model-mnet/mnet.25', 0, 0, 'net3')

#get files in the list 
onlyfiles = [f for f in listdir(VIDEO_DIR) if isfile(join(VIDEO_DIR, f))]
the_current_vid = 0
number_of_output_videos=0
while len(onlyfiles) > the_current_vid :  
    VIDEO_PATH = onlyfiles[the_current_vid] 
    cap = cv2.VideoCapture(VIDEO_PATH)

    #get video details 
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # float -> int
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # float -> int 

    frame_number=0
    out = cv2.VideoWriter( 'output/output'+str(number_of_output_videos)+'.avi',
                            cv2.VideoWriter_fourcc('M','J','P','G'), int(fps),
                            (width,height) )
    while cap.isOpened():
        # flag=0
        ret, frame = cap.read()
        frame_number+=1
        if ret == True:
            if frame_number%(fps/2) == 1 : # this is the step that we check the faces in it 
                detections,point = model.detect(frame)
                # dinish_of_short_interval=i
            if len(detections) == 1 :
                if detections[0][4]>DETECTION_THRESHOLD:
                    out.write(frame)
                    # flag=1
            else:#if flag == 1 :
                number_of_output_videos+=1
                out.release()
                out.release()
                out = cv2.VideoWriter( 'output/output'+str(number_of_output_videos)+'.avi',
                            cv2.VideoWriter_fourcc('M','J','P','G'), int(fps),
                            (width,height) )
                # flag=0
                # start_of_short_interval=i
                pass
        else:
            break
    out.release()
    the_current_vid += 1
    cap.release()
print('the number of vids = ' + str(the_current_vid))
######################################### scene detector ###############################################
print("######### phase scene detector #########")
DETECTION_THRESHOLD = 0.7


f=0
onlyfiles=[]
onlyfiles = [f for f in listdir(VIDEO_OUT_DIR) if isfile(join(VIDEO_OUT_DIR, f))]

# this will remove unnecesery files (video files that generated that their size is under 15 Kb)
for i in range(len(onlyfiles)):
    file = VIDEO_OUT_DIR + ''.join(onlyfiles[i:i+1])
    if os.path.getsize(file) < 15 * 1024:
        os.remove(file)

onlyfiles=[]
onlyfiles = [f for f in listdir(VIDEO_OUT_DIR) if isfile(join(VIDEO_OUT_DIR, f))]
the_current_vid = 0
while len(onlyfiles) > the_current_vid:
    address = VIDEO_OUT_DIR + ''.join(onlyfiles[the_current_vid : the_current_vid+1])
    print(address)
    video_manager = VideoManager([address])
    stats_manager = StatsManager()
    scene_manager = SceneManager(stats_manager)
    scene_manager.add_detector(ContentDetector())
    base_timecode = video_manager.get_base_timecode()
    video_manager.start()
    # Perform scene detection on video_manager.
    scene_manager.detect_scenes(video_manager)
    # Obtain list of detected scenes.
    scene_list = scene_manager.get_scene_list(base_timecode)
    # Each scene is a tuple of (start, end) FrameTimecodes.
    print('List of scenes obtained:')
    sc_list = []
    scene_number_in_vid=0
    for i, scene in enumerate(scene_list):
        sc_list.append(scene[0].get_frames())
        sc_list.append(scene[1].get_frames())
        scene_number_in_vid=i+1
        print(
            'Scene %2d: Start Frame %d, End Frame %d' % (
            i+1,
            scene[0].get_frames(), scene[1].get_frames(),))
    sc_list.remove(0)
    ###########################################################
    print("######### phase scene splitting #########")
    print(sc_list)
    splitted_vid=0
    if scene_number_in_vid > 1 : 
        while scene_number_in_vid > splitted_vid:
            # VIDEO_PATH = VIDEO_OUT_DIR + ''.join(onlyfiles[the_current_vid : the_current_vid+1])
            cap = cv2.VideoCapture(address)
            out = cv2.VideoWriter('scenesplitted/scene_splitted_'+str(the_current_vid)+'_'+str(splitted_vid)+'.avi',
                                                cv2.VideoWriter_fourcc('M','J','P','G'), 
                                                fps, ((width),(height)) )
            this_frame=0
            while cap.isOpened():
                retr, framec = cap.read()
                this_frame += 1
                if retr == True:
                    out.write(framec) 
                    if this_frame in sc_list:
                        splitted_vid += 1
                        out.release()
                        out = cv2.VideoWriter(
                            'scenesplitted/scene_splitted_'+str(the_current_vid)+'_'+str(splitted_vid)+'.avi',
                            cv2.VideoWriter_fourcc('M','J','P','G'), 
                            fps,
                            (width,height)
                            )

                else:
                    # print(i)
                    break
            
            cap.release()
            out.release()
            splitted_vid += 1
    else : 
        VIDEO_PATH = VIDEO_OUT_DIR + ''.join(onlyfiles[the_current_vid : the_current_vid+1])
        shutil.copy(VIDEO_PATH , "scenesplitted/")
    the_current_vid += 1
    video_manager.release()

######################### a python list 2 txt file and reverse script ################################
# TODO writing list of scenes into txt files
# with open('listfile.txt', 'w') as filehandle:
#     for listitem in sc_list:
#         filehandle.write('%s\n' % listitem)



# # open file and read the content in a list
# with open('listfile.txt', 'r') as filehandle:
#     for line in filehandle:
#         # remove linebreak which is the last character of the string
#         currentPlace = line[:-1]

#         # add item to the list
#         sc_list.append(currentPlace)


####################################### scene splitting ############################################
# print("######### phase scene splitting #########")
# the_current_vid=0
# while len(onlyfiles) > the_current_vid:
#     VIDEO_PATH = onlyfiles[the_current_vid] 
#     cap = cv2.VideoCapture(VIDEO_PATH)
#     out = cv2.VideoWriter('scenesplitted/scene_splitted_'+str(the_current_vid)+'.avi',
#                                         cv2.VideoWriter_fourcc('M','J','P','G'), 
#                                         fps, ((width),(height)) )
#     i=0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret == True:
#             out.write(frame) 
#             if i in sc_list:
#                 the_current_vid += 1
#                 out.release()
#                 out = cv2.VideoWriter('scenesplitted/scene_splitted_'+str(the_current_vid)+'.avi',
#                                         cv2.VideoWriter_fourcc('M','J','P','G'), 
#                                         fps, ((width),(height)) )
#             i+=1

#         else:
#             # print(i)
#             break
    
#     cap.release()
#     out.release()


############## a splitting video script ########################
# import cv2

# if __name__ == '__main__':
#     vidPath = '/path/foo/video.mp4'
#     shotsPath = '/path/foo/video/%d.avi' # output path (must be avi, otherwize choose other codecs)
#     segRange = [(0,40),(50,100),(200,400)] # a list of starting/ending frame indices pairs

#     cap = cv2.VideoCapture(vidPath)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
#     fourcc = int(cv2.VideoWriter_fourcc('M','J','P','G')) # XVID codecs

#     for idx,(begFidx,endFidx) in enumerate(segRange):
#         writer = cv2.VideoWriter(shotsPath%idx,fourcc,fps,size)
#         cap.set(cv2.CAP_PROP_POS_FRAMES,begFidx)
#         ret = True # has frame returned
#         while(cap.isOpened() and ret and writer.isOpened()):
#             ret, frame = cap.read()
#             frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES) - 1
#             if frame_number < endFidx:
#                 writer.write(frame)
#             else:
#                 break
#         writer.release()
