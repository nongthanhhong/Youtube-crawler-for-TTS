# Youtube crawler for TTS
 Extract subtitles and its audio give a list YT video id


# crawl_data_from_youtube.py:
- extract captions and speech from video
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

 **split_train**: *train data ratio*

 # evaluate_data.py
 - Given a word dictionary about a topic, check diversity of collected data base on this dict.

**--dict_path** *path to dict.txt file*

**--data_path** *path to total_dataset.csv file*
