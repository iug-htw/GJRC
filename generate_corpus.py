#! /usr/bin/env python3.7
# -*- coding: utf-8 -*-
# Author: Finn Folkerts, Vanessa Schreck
# Date: 2019 March 21

import pandas as pd
import numpy as np
import re

'''
Generates a csv-file with all sentences, for various different persons. (as specified in surnames.csv)
'''


# GLOBAL VARIABLES
gender_spec_words = {
            'gender': ['male', 'female'],
            'title': ['Herr', 'Frau'],
            'title_dat_acc': ['Herrn', 'Frau'],

            'pers_pron_nom': ['er', 'sie'],
            'pers_pron_dat': ['ihm', 'ihr'],
            'pers_pron_acc': ['ihn', 'sie'],

            'poss_nom_m_n_acc_n': ['sein', 'ihr'],
            'poss_nom_w_pl_acc_w_pl': ['seine', 'ihre'],
            'poss_gen_m_n': ['seines', 'ihres'],
            'poss_gen_w_pl_dat_w': ['seiner', 'ihrer'],
            'poss_dat_m_n': ['seinem', 'ihrem'],
            'poss_dat_pl_acc_m': ['seinen', 'ihren'],

            'contact': ['Ansprechpartner', 'Ansprechpartnerin'],
            'supervisor': ['Vorgesetzter', 'Vorgesetzte'],
            'employee': ['Mitarbeiter', 'Mitarbeiterin'],
            'frequent': ['frequentierter', 'frequentierte'],
            'popular': ['beliebter', 'beliebte'],
            'project_leader': ['Projektleiter', 'Projektleiterin'],
            'problemsolver': ['Problemlöser', 'Problemlöserin'],
            'connoisseur': ['Kenner', 'Kennerin'],
            'manager': ['Manager', 'Managerin'],
            'consistent': ['konsequenter', 'konsequente'],
            'systematic': ['systematischer', 'systematische'],
            'motivated': ['motivierten', 'motivierte'],
            'mobile': ['mobilen', 'mobile'],
            'highperformance': ['leistungsstarken', 'leistungsstarke'],
            'resilient_nom': ['belastbarer', 'belastbare'],
            'resilient_acc': ['belastbaren', 'belastbare'],
            'appreciated': ['geschätzter', 'geschätzte'],
            'goaloriented_acc': ['zielorientierten', 'zielorientierte'],
            'responsible_acc': ['verantwortungsbewussten', 'verantwortungsbewusste'],
            'responsible_nom': ['verantwortungsbewusster', 'verantwortungsbewusste'],
            'dynamic': ['dynamischen', 'dynamische'],
            'tireless': ['unermüdlicher', 'unermüdliche'],
            'polite': ['höflicher', 'höfliche'],
            'respected': ['respektierter', 'respektierte'],  # neu
            'cooperative': ['kooperativer', 'kooperative'],
            'teamoriented': ['teamorientierter', 'teamorientierte'],
            'communicative': ['kommunikationsstarker', 'kommunikationsstarke'],
            'competent': ['kompetenter', 'kompetente'],  # neu
            'collaborative': ['kooperationsfähiger', 'kooperationsfähige'],
            'respective': ['respektierter', 'respektierte'],
            'qualified_nom': ['qualifizierter', 'qualifizierte'],  # neu
            'qualified_acc': ['qualifizierten', 'qualifizierte'],  # neu
            'colleague': ['Kollege', 'Kollegin'],  # neu
            'engaged': ['engagierter', 'engagierte'],  # neu
            'thoughtful_nom': ['umsichtiger', 'umsichtige'],  # neu
            'conscientious_nom': ['gewissenhafter', 'gewissenhafte'],  # neu
            'friendly': ['freundlicher', 'freundliche'],  # neu
            'diligent': ['fleißiger', 'fleißige'],  # neu
            'correct': ['korrekter', 'korrekte'],  # neu
            'sincere': ['aufrichtiger', 'aufrichtige'],  # neu
            'upright': ['integrer', 'integre'],  # neu
            'good': ['guter', 'gute'],  # neu
            'good_acc': ['guten', 'gute'],  # neu
            # 'longstanding': ['langjähriger', 'langjährige'],  # neu
            'longstanding_acc': ['langjährigen', 'langjährige'],  # neu
            'highly_reliable': ['hochzuverlässigen', 'hochzuverlässigen'],  # neu
            'reliable_acc': ['zuverlässigen', 'zuverlässige'],  # neu
            'reliable_nom': ['zuverlässiger', 'zuverlässige'],  # neu
            'dutiful': ['pflichtbewussten', 'pflichtbewusste'],  # neu
            'honest': ['ehrlichen', 'ehrliche'],  # neu
            'valuable_acc': ['wertvollen', 'wertvolle'],  # neu
            'def_art': ['der', 'die'],
            'indef_art': ['ein', 'eine'],
            'indef_art_acc': ['einen', 'eine']}  # neu

gender_spec_words_df = pd.DataFrame(gender_spec_words, index=['m', 'f'])

word_to_grade_num = {'Very Good': 1,
                     'Good': 2,
                     'Satisfactory': 3,
                     'Sufficient': 4,
                     'Insufficient': 5,
                     'Poor': 6
                     }


# AUXILIARY FUNCTION
def capitalize(string, lower_rest=False):
    # capitalize first letter
    return string[:1].upper() + (string[1:].lower() if lower_rest else string[1:])


# MAIN
def main():
    names = pd.read_csv('data/surnames.csv', delimiter=';')
    sentences = pd.read_csv('data/template_sentences.csv', delimiter=';')

    cs_df = pd.DataFrame()

    i = 0
    for sentence_row in sentences.itertuples(index=False):
        sentence = getattr(sentence_row, 'Template')
        placeholders = re.findall('<\w*>', sentence)
        for gender in gender_spec_words_df.itertuples(index=False):
            for name in names.itertuples(index=False):
                new_sentence = sentence
                for placeholder in placeholders:
                    if placeholder[1:5] == 'name':
                        surname = getattr(name, 'Surname')
                        if placeholder[1:-1] == 'name_s':
                            if surname[-1] in ['s', 'z', 'ß', 'x'] or surname[-2:] == 'ce':
                                surname += '\''
                            else:
                                surname += 's'
                        new_sentence = new_sentence.replace(placeholder, surname)
                        cs_df.at[i, 'Person'] = getattr(gender, 'title') + ' ' + getattr(name, 'Surname')
                        cs_df.at[i, 'Origin'] = getattr(name, 'Origin')
                        cs_df.at[i, 'Nobiliary_particle'] = getattr(name, 'Nobiliary_particle')

                    elif placeholder[1:-1] in gender_spec_words.keys():
                        new_sentence = new_sentence.replace(placeholder, getattr(gender, placeholder[1:-1]))
                        if placeholder in ['pers_pron_nom', 'pers_pron_dat', 'pers_pron_acc',
                                           'poss_nom', 'poss_dat', 'poss_gen', 'poss_acc',
                                           'poss_nom_pl', 'poss_gen_pl']:
                            if re.search('Herr|Frau', new_sentence):
                                pass
                            else:
                                cs_df.at[i, 'Person'] = getattr(gender, placeholder)
                    else:
                        print(placeholder)
                        print('Placeholder missing in dictionary!')
                        print(sentence)
                        print(new_sentence)

                cs_df.at[i, 'Sentence'] = capitalize(new_sentence)
                cs_df.at[i, 'Template'] = getattr(sentence_row, 'Template')
                cs_df.at[i, 'Template_ID'] = getattr(sentence_row, 'Template_ID')
                cs_df.at[i, 'Title'] = getattr(sentence_row, 'Title')
                cs_df.at[i, 'Gender'] = getattr(gender, 'gender')
                cs_df.at[i, 'Grade'] = getattr(sentence_row, 'Grade')
                cs_df.at[i, 'Grade Number'] = word_to_grade_num[getattr(sentence_row, 'Grade')]  # convert grade to num
                cs_df.at[i, 'Source(ISBN)'] = getattr(sentence_row, 'Source')
                i += 1

    # remove duplicate sentences
    length = len(cs_df)
    cs_df.drop_duplicates(subset='Sentence', keep='first', inplace=True)
    if length != len(cs_df):
        print('Removed {} duplicates.'.format(length-len(cs_df)))
    # rearrange columns
    cs_df = cs_df[['Sentence', 'Template', 'Template_ID', 'Title', 'Person', 'Gender', 'Origin',
                   'Nobiliary_particle', 'Grade', 'Grade Number', 'Source(ISBN)']]
    cs_df.sort_values(by=['Template_ID', 'Title', 'Gender'])
    # replace empty cells with NaN
    cs_df.replace('', np.nan, inplace=True)

    # save dataframe into csv file
    cs_df.to_csv(path_or_buf='data/GJRCorpus.csv', index=False, sep=';', encoding='utf-8-sig')


if __name__ == '__main__':
    main()
