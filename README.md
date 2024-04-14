# Youtube crawler for TTS
 Extract transcripts and its audio give a list YT video id

**Notes**:
- must install ffprobe and ffmpeg

# crawl_data_from_youtube.py:
- Extract transcript and speech from video and give as below:
```
root
    |_ Information of the dataset is in the total_dataset.csv file, we have 5 columns
    |       |__1: id 
    |       |__2: corresponding transcript
    |       |__3: duration of transcript
    |       |__4: path to speech file
    |       |__5: emotion
    |
    |
    |_ speech
            |_ id_1.wav
            |_ id_2.wav
```
 **--config** *path to crawl_config.json*

# crawl_config.json 

 **root_path**: *folder to save all data*

 **url_file**: *file list video id line by line*

 **lang** *prefer language of transcripts* check [YouTubeTranscriptApi](https://pypi.org/project/youtube-transcript-api/)

 **split_train**: *train data ratio*

 # evaluate_data.py
 - Given a word dictionary about a topic, check diversity of collected data base on this dict.

**--dict_path** *path to dict.txt file*

**--data_path** *path to total_dataset.csv file*
