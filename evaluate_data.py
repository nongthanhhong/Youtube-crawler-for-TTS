import json
import os
import argparse
from tqdm import tqdm
from os.path import join, exists

def load_dictionary(dictionary_path):
    words = []
    for line in tqdm(open(dictionary_path, encoding='utf-8'), ncols=100):
            content = line.strip()
            words.append(json.loads(content)["text"])
    return words

def load_dataset(dataset_path):
    words = []
    if ".txt" in dataset_path:
        for line in tqdm(open(dataset_path, encoding='utf-8'), ncols=100):
                text = line.strip().split(" ")[1:]
                for t in text:
                    words.append(t)
    
    if ".csv" in dataset_path:
        for line in tqdm(open(dataset_path, encoding='utf-8'), ncols=100):
                text = line.strip().split(",")[1].split(' ')
                
                for t in text:
                    words.append(t)
    
    # if ".csv" in dataset_path:
    #     for line in tqdm(open(dataset_path, encoding='utf-8'), ncols=100):
    #             text = line.strip().split("|")[1].split(' ')
                
    #             for t in text:
    #                 words.append(t)

    return words[1:]

def count_unique_words(dictionary_path, dataset_path):
    

    word_dict, word_data = load_dictionary(dictionary_path), load_dataset(dataset_path)
    # print(len(word_dict))
    # return
    # Tạo một tập hợp để lưu trữ các từ duy nhất
    unique_words = set()
    print("Evaluating...")
    # Lặp qua tất cả các từ trong danh sách các từ
    for word in tqdm(word_data, ncols=100):
        # Kiểm tra xem từ hiện tại có nằm trong từ điển không
        if word in word_dict:
            # Nếu có, thêm từ đó vào tập hợp các từ duy nhất
            unique_words.add(word)
    print("done!")
    # Trả về số lượng các từ duy nhất
    return len(unique_words), len(word_dict)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dict_path', type=str, default="words.txt",
                    help='File dictionary')
    parser.add_argument('-t', '--data_path', type=str, default="total_dataset.csv",
                    help='File dataset')

    args = parser.parse_args()

    a,b = count_unique_words(args.dict_path, args.data_path)
    print(f'Dataset contains {a}/{b} words of dictionary.')