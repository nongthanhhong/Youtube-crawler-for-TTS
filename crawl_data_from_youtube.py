

'''
extract captions and speech from video, and save it to two folder

data
    |_ Information of the dataset is in the .csv file, we have 5 columns
    |       |__1: id.csv 
    |       |__2: corresponding transcript
    |       |__3: duration of transcript
    |       |__4: path to speech file
    |       |__5: emotion
    |
    |
    |_ speech
            |_ id_1.wav
            |_ id_2.wav

'''

from youtube_transcript_api import YouTubeTranscriptApi
from operator import itemgetter
from pydub import AudioSegment
from yt_dlp import YoutubeDL
from tqdm import tqdm
import pandas as pd
# import soundfile as sf
import hashlib
import argparse
# import librosa
import logging
import json
import time
import csv
import os


def get_from_file(path):
    '''
    Get list youtube url from file
    '''
    with open(path) as f:
        lines = [str(line.rstrip()) for line in f]
    # for l in lines:
    #     print(l)
    return lines

def download_audio(hsp, list_url):

    '''
    Download audio of all videos in list 
    Save name is path to file 
    '''
    print("Downloading....")
    for url in  tqdm(list_url, ncols=100):
        path_save = os.path.join(hsp.root_path, 'audio', url) 
        if os.path.exists(path_save + '.wav') or os.path.exists(path_save + '.mp3'):
            continue
        # URL of the YouTube video you want to download
        video_url = "https://youtu.be/" + url
        print(video_url)
        # Create a dictionary with the options you want to pass to youtube-dl
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                # 'preferredquality': '192',
            }],
            'noplaylist': True,  # Download only the video specified, not the entire playlist
            'quiet': True,  # Don't print download progress to stdout
            'outtmpl': path_save
        }

        # Create a YoutubeDL object with the options dictionary
        with YoutubeDL(ydl_opts) as ydl:
            # Provide the video URL as an argument to the download method
            ydl.download([video_url])
    print("Download complete")

def trim_speech(root_path, audio_file, id, sub_1, sub_2, sub_3):

    '''
    Split audio to piece with transcript, respectively

    return path of this trim of transcript 
    '''


    # Set the start time in milliseconds
    start_time = sub_1['start']*1000 - 50
    duration = sub_2['start'] - sub_1['start']
    if sub_1['duration'] > duration:
        end_time = sub_2['start']*1000
        
    else: end_time = start_time + sub_1['duration']*1000
    d = end_time - start_time

    # Trim the audio file
    trimmed_audio1  = audio_file[start_time:end_time]
    text = sub_1['text']
    
    # Set the duration in milliseconds
    # duration = duration*1000
    if '[' and ']' not in sub_2['text']:
        start_time = sub_2['start']*1000

        duration = sub_3['start'] - sub_2['start']
        if sub_2['duration'] > duration:
            end_time = sub_3['start']*1000 + 50
        else: end_time = start_time + sub_2['duration']*1000
        d += end_time - start_time

        # Trim the audio file
        trimmed_audio1 += audio_file[start_time:end_time]

        text += " " + sub_2['text']

    # save file
    trimmed_audio1.export(os.path.join(root_path, "speech", id+".wav"),
                            format="wav")
    # print(id+".wav is created and saved")

    #Text, Duration, Path
    return text, d, os.path.join(root_path, "speech", id+".wav")

def crawl_transcript(hsp):

    '''
    Cover all to crawl a dataset, write a csv file with: 

    1 - ID of a trim audio
    2 - Its transcript
    3 - Time start
    4 - Duration
    5 - Path to trimmed audio
    6 - Emotion (None for all, will upgrade later)
    '''
    dataset = {"ID":[], "Text":[],"Duration":[], "Path":[], "Emotion":[]}
    list_url = get_from_file(os.path.join(hsp.url_file))

    records = YouTubeTranscriptApi.get_transcripts(list_url, languages=[hsp.lang])[0]
    # print(records)
    
    # Get all files in the directory
    file_list = os.listdir(os.path.join(hsp.root_path, "speech"))
    count_id = len(file_list)
    download_audio(hsp, list_url)
    for record in range(len(list_url)):

        print(f'Separate audio {record+1}/{len(list_url)} - file: {list_url[record]}')

        list_subtitles = sorted(records[list_url[record]], key=itemgetter('start'))

        # Load the audio file
        if os.path.exists(os.path.join(hsp.root_path, "audio", list_url[record] + '.mp3')):
           audio_file = AudioSegment.from_file(os.path.join(hsp.root_path, "audio", list_url[record]+ ".mp3"), format="mp3")
        else:
           audio_file = AudioSegment.from_file(os.path.join(hsp.root_path, "audio", list_url[record]+ ".wav"), format="wav")

        for idx in tqdm(range(len(list_subtitles)-2), ncols=100):
        
            id = generate_id(str(count_id+1))

            sub_1 = list_subtitles[idx]
            sub_2 = list_subtitles[idx+1]
            sub_3 = list_subtitles[idx+2]

            if '[' and ']' in sub_1['text']:
                continue

            dataset['ID'].append(id)
            
            Text, Duration, Path = trim_speech(hsp.root_path, audio_file, id, sub_1, sub_2, sub_3)


            dataset['Text'].append(Text)
            dataset['Duration'].append(Duration)
            dataset['Path'].append(Path)
            dataset['Emotion'].append(None)
            count_id +=1
            # if count_id == 100: break
    
    return dataset

def generate_id(string):

    '''
    Create id for each record
    '''
    # Convert the string to bytes
    string_bytes = string.encode('utf-8')
    
    # Generate the hash object
    hash_object = hashlib.md5(string_bytes)
    
    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()
    
    # Return the first 8 characters of the hexadecimal representation
    return hex_dig[:8]

def save_to_csv(root_path, my_dict):

    '''
    Save dict to csv file
    '''
    filename = os.path.join(root_path,'total_dataset.csv')
    if os.path.exists(filename):
        append_write = 'a+' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    with open(filename, mode = append_write, encoding='utf-8', newline='') as csv_file:
        # Create a writer object
        writer = csv.writer(csv_file)

        if append_write == 'w':
            # Write the header row
            writer.writerow(my_dict.keys())

        # Write the data rows
        for row in zip(*my_dict.values()):
            writer.writerow(row)
    print("File saved!")

def save_to_train_val(hsp, dataset):

    root_path = hsp.root_path
    data = []
    for text, id in zip(dataset['Text'], dataset['ID']):
       data.append(os.path.join(root_path + "/speech/", id +".wav") + '|' + text)

    train_data = data[:int(len(data)*hsp.split_train)]
    test_data = data[len(train_data):]

    if os.path.exists(os.path.join(root_path, "list_train.txt")):
        append_write = 'a+' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    # Open a file in write mode
    with open(os.path.join(root_path, "list_train.txt"), append_write, encoding='utf-8') as file:
        
        for i in train_data:
         file.write(i+ "\n")

    with open(os.path.join(root_path, "list_val.txt"), append_write, encoding='utf-8') as file:
        
        for i in test_data:
         file.write(i+ "\n")

    print("Train-val saved!")


def get_hparams():
  parser = argparse.ArgumentParser()
  
  parser.add_argument('-c', '--config', type=str, default="crawl_config.json",
                      help='JSON file for configuration')
  
  
  args = parser.parse_args()
  
  config_path = args.config

  
    
  with open(config_path, "r") as f:
      data = f.read()
  config = json.loads(data)
  
  hparams = HParams(**config)
  if not os.path.exists(hparams.root_path+"\\speech"):
    os.makedirs(hparams.root_path+"\\speech")
  if not os.path.exists(hparams.root_path+"\\audio"):
    os.makedirs(hparams.root_path+"\\audio")
  return hparams

class HParams():
  def __init__(self, **kwargs):
    for k, v in kwargs.items():
      if type(v) == dict:
        v = HParams(**v)
      self[k] = v
    
  def keys(self):
    return self.__dict__.keys()

  def items(self):
    return self.__dict__.items()

  def values(self):
    return self.__dict__.values()

  def __len__(self):
    return len(self.__dict__)

  def __getitem__(self, key):
    return getattr(self, key)

  def __setitem__(self, key, value):
    return setattr(self, key, value)

  def __contains__(self, key):
    return key in self.__dict__

  def __repr__(self):
    return self.__dict__.__repr__()

if __name__ == "__main__":


    hsp = get_hparams()

    # print(hsp)

    dataset = crawl_transcript(hsp)

    save_to_csv(hsp.root_path, dataset)
    save_to_train_val(hsp, dataset)

