import numpy as np
import pandas as pd
import random
import json
import re
import textdistance as td

def match(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    total = (j+c)/2
    return total*100

def calculate_scores(resumes, job_description, index):
    scores = []
    for x in range(resumes.shape[0]):
        score = match(resumes['TF_Based'][x], job_description['TF_Based'][index])
        scores.append(score)
    return scores


def generate_random_start(index):
    resumes = pd.read_csv('Resume_Data.csv')
    jobs = pd.read_csv('Job_Data.csv')
    print("Number of resumes in database: " + str(resumes.shape[0]) + "\nNumber of JDs in database: " + str(jobs.shape[0]))
    """Generate `new_words` words of output from a trained model and format into HTML."""
    index = index
    resumes['Scores'] = calculate_scores(resumes, jobs, index)

    ranked_resumes = resumes.sort_values(by=['Scores'], ascending=False).reset_index(drop=True)

    ranked_resumes['Rank'] = pd.DataFrame([i for i in range(1, len(ranked_resumes['Scores'])+1)])
    list =[]
    for i in range(10):
        list.append(ranked_resumes.Name[i])

    # HTML formatting
    original_sequence = ranked_resumes.Name[0]
    gen_list = ranked_resumes.Name[1]
    a = ranked_resumes.Name[2]
    seed_html = ''
    seed_html = addContent(seed_html, header('Top Resume 1', color='darkblue'))
    seed_html = addContent(seed_html,
                           box(remove_spaces(' '.join(original_sequence))))

    gen_html = ''
    gen_html = addContent(gen_html, header('Top Resume 2', color='darkred'))
    gen_html = addContent(gen_html, box(remove_spaces(' '.join(gen_list))))

    a_html = ''
    a_html = addContent(a_html, header('Top Resume 3', color='darkgreen'))
    a_html = addContent(a_html, box(remove_spaces(' '.join(a))))

    return f'<div>{seed_html}</div><div>{gen_html}</div><div>{a_html}</div>'


def header(text, color='black', gen_text=None):
    """Create an HTML header"""

    if gen_text:
        raw_html = f'<h1 style="margin-top:16px;color: {color};font-size:54px"><center>' + str(
            text) + '<span style="color: red">' + str(gen_text) + '</center></h1>'
    else:
        raw_html = f'<h1 style="margin-top:12px;color: {color};font-size:54px"><center>' + str(
            text) + '</center></h1>'
    return raw_html


def box(text, gen_text=None):
    """Create an HTML box of text"""

    if gen_text:
        raw_html = '<div style="padding:8px;font-size:28px;margin-top:28px;margin-bottom:14px;">' + str(
            text) + '<span style="color: red">' + str(gen_text) + '</div>'

    else:
        raw_html = '<div style="border-bottom:1px inset black;border-top:1px inset black;padding:8px;font-size: 28px;">' + str(
            text) + '</div>'
    return raw_html


def addContent(old_html, raw_html):
    """Add html content together"""

    old_html += raw_html
    return old_html


def format_sequence(s):
    """Add spaces around punctuation and remove references to images/citations."""

    # Add spaces around punctuation
    s = re.sub(r'(?<=[^\s0-9])(?=[.,;?])', r' ', s)

    # Remove references to figures
    s = re.sub(r'\((\d+)\)', r'', s)

    # Remove double spaces
    s = re.sub(r'\s\s', ' ', s)
    return s


def remove_spaces(s):
    """Remove spaces around punctuation"""

    s = re.sub(r'\s+([.,;?])', r'\1', s)

    return s
