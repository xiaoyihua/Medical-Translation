"""
Program that parses and formats files from MeSpEn dataset into CSV files for further exploration.

Main Functions:
- format_xml (string --> dataframe):
    - Takes in string of os path, reads file of type xml
    - Uses xml schema to extract matched english and spanish titles and descriptions for one file

- create_dataframes (string --> dataframe):
    - Takes in string of relative path to directory folder
    - Loops format_xml and combines dataframes into one

- count_sentences (df --> df):
    - creates new column in df based on sentences found using punkt's sentence tokenizer
    - punkt's sentence tokenizer is built on an unsupervised learning model (unspecified)
    - punkt's tokenizer needs to have its language set as an option

- count_words (df --> df):
    - creates new columns in df based on words in paragraph using python's split

Initial Author: Daniel Wang
Additional Authors: 
Last Refactored: Daniel Wang
Last Tested: 
"""

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

__author__ = '{author}'
__copyright__ = 'Copyright {year}, {project_name}'
__credits__ = ['{credit_list}']
__license__ = '{license}'
__version__ = '{mayor}.{minor}.{rel}'
__maintainer__ = '{maintainer}'
__email__ = '{contact_email}'
__status__ = '{dev_status}'

def format_xml(path, source):
    # Given string path, read one xml file
    # Source to create source column - Equivalent to dir
    txt = Path(path).read_text()
    xml_data = StringIO(txt)

    # Take advantage of xml schemas to extract the fields we want - located in xpath
    # Each df produced by this method returns en title and es title as separate rows
    df = pd.read_xml(xml_data, 
                    xpath="//dc:title", 
                    namespaces={"dc": "http://purl.org/dc/elements/1.1/", "dcterms":"http://purl.org/dc/terms/", 
                                                            "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
                    parser="lxml")
    df = df.convert_dtypes(convert_string=True)

    # Must reopen file and rextract to get the other fields
    txt = Path(path).read_text()
    xml_data = StringIO(txt)

    df2 = pd.read_xml(xml_data, 
                    xpath="//dc:description", 
                    namespaces={"dc": "http://purl.org/dc/elements/1.1/", "dcterms":"http://purl.org/dc/terms/", 
                                                            "xsi": "http://www.w3.org/2001/XMLSchema-instance"},
                    parser="lxml")
    
    # Dataframe formatting to make sure they are the same types for joining
    df2 = df2.convert_dtypes(convert_string=True)
    df = df.merge(df2, on='lang', how='left')

    # Dataframe operations to reshape the data into single rows
    df.set_index('lang', inplace=True)
    data = {'title_en': [df['title']['en']], 'title_es': [df['title']['es']], 'description_en': [df['description']['en']], 'description_es': [df['description']['es']]}
    df = pd.DataFrame.from_dict(data)

    df['Source'] = f'{source}'
    df['File'] = f'{path}'

    return df

def create_dataframes(dir):
    directory = dir
    dataframes = []
    counter = 0

    # Main loop that iterates through each file in the directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        # if it is a file, format using above function and store dataframe in a list
        if os.path.isfile(f):
            try:
                df = format_xml(f, dir)
                dataframes.append(df)
            except (UnicodeDecodeError, ValueError, KeyError):
                print(f)
                counter += 1

    print(counter)

    # connect all dataframes in list together - faster than joining dataframes at every step
    final = pd.concat(dataframes, ignore_index=True)

    return final

def count_words(df):
    # Counting words using split - slightly inflated by punctuation but good enough
    df['NumWordsEn'] = df.apply(lambda x: len((str(x['description_en'])).split()), axis=1)
    df['NumWordsEs'] = df.apply(lambda x: len((str(x['description_es'])).split()), axis=1)

    return df

def count_sentences(df):
    # Counting sentences using nltk setn_tokenize, which uses punkt
    df['NumSentencesEn'] = df.apply(lambda x: len(sent_tokenize(x['description_en'], language='english')) if isinstance(x['decription_en'], str) else 0, axis=1)
    df['NumSentencesEs'] = df.apply(lambda x: len(sent_tokenize(x['description_es'], language='spanish')) if isinstance(x['decription_es'], str) else 0, axis=1)

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