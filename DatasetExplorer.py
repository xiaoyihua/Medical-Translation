import pandas as pd
import numpy as np
from pathlib import Path
from io import StringIO
from lxml import etree
import xml.etree.ElementTree as ET
import os
import re
import nltk
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize

def format_xml(path):
    txt = Path(path).read_text()
    xml_data = StringIO(txt)

    df = pd.read_xml(xml_data, 
                    xpath="//dc:title", 
                    namespaces={"dc": "http://purl.org/dc/elements/1.1/", "dcterms":"http://purl.org/dc/terms/", 
                                                            "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
                    parser="lxml")
    df = df.convert_dtypes(convert_string=True)

    txt = Path(path).read_text()
    xml_data = StringIO(txt)

    df2 = pd.read_xml(xml_data, 
                    xpath="//dc:description", 
                    namespaces={"dc": "http://purl.org/dc/elements/1.1/", "dcterms":"http://purl.org/dc/terms/", 
                                                            "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
                    parser="lxml")
    
    df2 = df2.convert_dtypes(convert_string=True)
    df = df.merge(df2, on='lang', how='left')

    df.set_index('lang', inplace=True)
    data = {'title_en': [df['title']['en']], 'title_es': [df['title']['es']], 'description_en': [df['description']['en']], 'description_es': [df['description']['es']]}
    df = pd.DataFrame.from_dict(data)

    df['Source'] = 'MedlinePlus'
    df['File'] = f'{path}'

    return df

def create_dataframes(dir):
    directory = dir

    dataframes = []
    counter = 0

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            try:
                df = format_xml(f)
                dataframes.append(df)
            except (UnicodeDecodeError, ValueError, KeyError):
                print(f)
                counter += 1

    print(counter)

    final = pd.concat(dataframes, ignore_index=True)

    return final

def count_words(df):
    df['NumWordsEn'] = df.apply(lambda x: len((str(x['description_en'])).split()), axis=1)
    df['NumWordsEs'] = df.apply(lambda x: len((str(x['description_es'])).split()), axis=1)

    return df

def count_sentences(df):
    df['NumSentencesEn'] = df.apply(lambda x: len(sent_tokenize(x['description_en'], language='english')), axis=1)
    df['NumSentencesEs'] = df.apply(lambda x: len(sent_tokenize(x['description_es'], language='spanish')), axis=1)

    return df

def graph_wordcount_en(df, source):
    df['NumWordsEn'].hist()

    # add labels and title
    plt.xlabel('Num')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Words En {source}')
    plt.show()

def graph_wordcount_es(df, source):
    df['NumWordsEs'].hist()

    # add labels and title
    plt.xlabel('Num')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Words Es {source}')
    plt.show()

def graph_sentcount_en(df, source):
    df['NumSentencesEn'].hist()

    # add labels and title
    plt.xlabel('Num')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Sentences En {source}')
    plt.show()

def graph_sentcount_es(df, source):
    df['NumSentencesEs'].hist()

    # add labels and title
    plt.xlabel('Num')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of Sentences Es{source}')
    plt.show()

def main():
    dir = 'Pubmed'
    df = create_dataframes('Pubmed')

    df = count_words(df)
    df = count_sentences(df)

    graph_wordcount_en(df, dir)
    graph_wordcount_es(df, dir)

if __name__ == "__main__":
    main()