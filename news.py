from flask import Flask, render_template, request, redirect, url_for,jsonify,abort
import nltk
# from urllib import requests

from bs4 import BeautifulSoup
# from urllib import requests
from nltk import word_tokenize
from nltk import sent_tokenize
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from heapq import nlargest
import psycopg2
import json
import requests
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("vader_lexicon")
nltk.download("universal_tagset")
nltk.download('averaged_perceptron_tagger')


app = Flask(__name__,static_folder='static')


def calculate_reading_time(text, words_per_minute=200):
    words = re.findall(r'\w+', text)
    word_count = len(words)
    reading_time_minutes = float(word_count / words_per_minute)
    return reading_time_minutes
    




def summarize_text(text, num_sentences):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    # Tokenize the text into words
    words = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = (nltk.corpus.stopwords.words("english"))
    filtered_words = [word for word in words if word not in stop_words]

    # Calculate word frequencies
    word_freq = {}
    for word in filtered_words:
        if word not in word_freq:
            word_freq[word] = 1
        else:
            word_freq[word] += 1

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        for word in word_tokenize(sentence.lower()):
            if word in word_freq:
                if len(sentence.split(' ')) < 30:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_freq[word]
                    else:
                        sentence_scores[sentence] += word_freq[word]

    # Select top sentences based on scores
    summarized_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
    summary = ' '.join(summarized_sentences)
    
    return summary

keywords = {
    'politics1': ['politics', 'government', 'election', 'congress', 'president', 'policy', 'law', 'vote', 'democracy', 
                 'senate', 'parliament', 'legislation', 'campaign', 'political party', 'diplomacy', 'public policy', 
                 'political science', 'constituency', 'political ideology', 'civil rights'],

    'finance1': ['finance', 'economy', 'stock', 'market', 'investment', 'bank', 'money', 'financial', 'budget', 
                'tax', 'business', 'capital', 'credit', 'interest', 'loan', 'insurance', 'retirement', 'asset', 
                'debt', 'wealth'],

    'sports1': ['sports', 'football', 'basketball', 'soccer', 'athlete', 'game', 'match', 'tournament', 'championship', 
               'team', 'player', 'coach', 'score', 'goal', 'victory', 'league', 'training', 'fitness', 'competition', 
               'athletics'],

    'education1': ['education', 'school', 'university', 'student', 'teacher', 'classroom', 'learning', 'degree', 
                  'curriculum', 'exam', 'lecture', 'research', 'library', 'academics', 'college', 'study', 'test', 
                  'homework', 'academic', 'knowledge'],

    'entertainment1': ['entertainment', 'movie', 'music', 'celebrity', 'actor', 'show', 'performance', 'film', 'album', 
                      'art', 'theater', 'concert', 'director', 'award', 'artist', 'dance', 'television', 'pop culture', 
                      'celebrity gossip', 'comedy'],

    'business1': ['business', 'industry', 'entrepreneur', 'startup', 'management', 'strategy', 'marketplace', 'commerce', 
                 'corporation', 'trade', 'profit', 'revenue', 'productivity', 'innovation', 'e-commerce', 'supply chain', 
                 'investment', 'corporate', 'financial', 'entrepreneurship'],

    'technology1': ['technology', 'innovation', 'digital', 'internet', 'computer', 'software', 'hardware', 'IT', 
                   'artificial intelligence', 'data', 'cybersecurity', 'cloud computing', 'robotics', 'automation', 
                   'gadget', 'smartphone', 'social media', 'website', 'programming', 'tech'],

    'religion1': ['religion', 'faith', 'belief', 'god', 'church', 'spirituality', 'worship', 'prayer', 'sacred', 
                 'theology', 'religious', 'bible', 'doctrine', 'ritual', 'clergy', 'holy', 'spiritual', 'divine', 
                 'mosque', 'temple'],

    'astrology1': ['astrology', 'horoscope', 'zodiac', 'sign', 'astronomy', 'planet', 'constellation', 'cosmos', 
                  'forecast', 'prediction', 'star', 'birth chart', 'alignment', 'celestial', 'tarot', 'ninth house', 
                  'lunar', 'sun sign', 'moon sign', 'mercury retrograde'],

    'health1': ['health', 'wellness', 'medicine', 'fitness', 'nutrition', 'exercise', 'diet', 'well-being', 'lifestyle', 
               'mental health', 'medical', 'healthy', 'physical', 'therapy', 'doctor', 'hospital', 'disease', 'wellness', 
               'prevention', 'healthcare'],

    'social_media1': ['social media', 'social network', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube', 
                     'snapchat', 'tiktok', 'platform', 'online community', 'viral', 'influencer', 'hashtag', 'post', 
                     'share', 'like', 'comment', 'follower', 'engagement']
}
def fun_genre(text):
    politics2 =  len([word for word in keywords['politics1'] if word in text])
    finance2 =  len([word for word in keywords['finance1'] if word in text])
    sports2 =  len([word for word in keywords['sports1'] if word in text])
    education2 =  len([word for word in keywords['education1'] if word in text])
    entertainment2 =  len([word for word in keywords['entertainment1'] if word in text])
    business2 =  len([word for word in keywords['business1'] if word in text])
    technology2 =  len([word for word in keywords['technology1'] if word in text])
    religion2 =  len([word for word in keywords['religion1'] if word in text])
    astrology2 =  len([word for word in keywords['astrology1'] if word in text])
    health2 =  len([word for word in keywords['health1'] if word in text])
    social_media2 =  len([word for word in keywords['social_media1'] if word in text])

    max_num = max(politics2,finance2,sports2,education2,entertainment2,business2,technology2,religion2,astrology2,health2,social_media2)
    dict_genre = {'politics': politics2,'finance':finance2, 'sports':sports2,'education':education2,'entertainment':entertainment2,'business':business2,'technology':technology2,'religion':religion2,'astrology':astrology2,'health':health2,'social_media':social_media2 }

    for key,value in dict_genre.items():
        if value == max_num:
            return key
    
def sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)
    # Initialize variable to store cumulative compound sentiment score
    total_compound = 0
    # Iterate through each sentence and calculate compound sentiment score
    for sentence in sentences:
        # Calculate sentiment scores for the sentence
        scores = sid.polarity_scores(sentence)
        total_compound += scores['compound']

    # Calculate the mean compound sentiment score
    num_sentences = len(sentences)
    mean_compound = total_compound / num_sentences

    return mean_compound


conn = psycopg2.connect(host = "dpg-cnmq90qcn0vc738fh5v0-a", database = "news_magazine", user = "news_magazine_user", password = "kcbYdr8UYXTE8jIdK9cw0Sh1KEiR56BS")
cur = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS NEWS (
    url VARCHAR(255),
    text TEXT,
    estimated_time FLOAT,
    title VARCHAR(255),
    genre VARCHAR(50),
    compound DOUBLE PRECISION,
    publisher VARCHAR(100),
    count_word INTEGER,
    count_sent INTEGER,
    count_stp_word INTEGER,
    upos JSONB
)
"""

cur.execute(create_table_query)
conn.commit()


@app.route("/",methods = ('POST','GET'))
def portal():
    url = ""
    text = ""
    
    neg = 0
    pos = 0
    neu = 0
    compound=0
    words_per_minute=200
    dict1 = {}
    estimated_time = 0
    count_word = 0
    count_sent = 0
    count_stp_word = 0
    count_noun = 0 
    count_pron = 0 
    count_verb = 0 
    count_adj = 0 
    count_adv = 0 
    count_conj = 0
    word_list = []
    publisher = ""
    title = ""
    summary = ""
    estimated_summ_time = 0
    genre = ""
    if request.method == 'POST':
        url=request.form["enter_url"] 
        # try:   
        #     if "timesofindia" in url:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find(class_="xf8Pm byline")
    
        
        title = soup.title.get_text()
        main_text= soup.find(class_="_s30J clearfix")
        div_tag = BeautifulSoup(str(main_text))
        for span_tag in div_tag.find_all('span'):
            span_tag.extract()
            
        # text = main_text.get_text()
        text = div_tag.get_text()
        
        summary = summarize_text(text, 6)
        new_text = re.sub(r'[^\w\s]','',text)
        stop_words = (nltk.corpus.stopwords.words("english"))
        lst_text = word_tokenize(new_text)
        lst_words = [word for word in lst_text if word not in stop_words]
        clean_text = ' '.join(lst_words)
        
        compound = sentiment(clean_text) 
        ###



        # html = request.urlopen(url).read().decode('utf8')

        # soup = BeautifulSoup(html, 'html.parser')
        
        a = results.find('span')
        publisher = a.get_text()
        
        
            
        time_1 =  calculate_reading_time(text)
        time_2 =  calculate_reading_time(summary)
        estimated_time = f"{time_1:.2f}"
        estimated_summ_time = f"{time_2:.2f}"

        genre = fun_genre(clean_text)

        word_list = word_tokenize(text)


        pun_list = [".",",","?"]

        for i in word_list:
            if i not in pun_list:
                count_word+=1

        sent_list = sent_tokenize(text)
        count_sent = len(sent_list)

        stp_word = (nltk.corpus.stopwords.words("english"))
        
        for i in word_list:
            if i in stp_word:
                count_stp_word +=1
        # pos_lst1 = ["NOUN","PRON","VERB"]
        pos_lst2 = nltk.pos_tag(word_list,tagset="universal")
        for i in pos_lst2:
            if i[1] == "NOUN":
                count_noun += 1
            elif i[1] == "PRON": 
                count_pron += 1
            elif i[1] == "VERB":
                count_verb += 1 
            elif i[1] == "ADJ":
                count_adj += 1
            elif i[1] == "ADV":
                count_adv +=1
            elif i[1] == "CONJ":
                count_conj += 1

        dict1["NOUN"] = count_noun
        dict1["PRON"] = count_pron
        dict1["VERB"] = count_verb
        dict1["ADV"] = count_adj
        dict1["ADJ"] = count_adv
        dict1["CONJ"] = count_conj


        


        cur.execute("insert into NEWS(url,text,estimated_time,title,genre,compound,publisher,count_word,count_sent,count_stp_word,upos) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(url,  text,estimated_time,title,genre, compound,publisher,count_word, count_sent,count_stp_word, json.dumps(dict1)))
        conn.commit()
        
        #     else:
        #         return abort(406)
        # except:
        #     return abort(406)
    # msg_neg = neg,msg_pos=pos,msg_neu=neu,
    return render_template("index.html",msg_time = estimated_time, msg_title = title, msg_url = url, msg_genre = genre, msg_summary = summary,msg_summ_time = estimated_summ_time, msg_text = text,msg_count_word = count_word,msg_count_sent = count_sent, msg_count_stp_word = count_stp_word,msg_dict1 = dict1,msg_compound=compound,msg_results= publisher)

@app.route("/Password", methods = ('POST','GET'))
def paswrd_input():
    if request.method == 'POST':
        return render_template('password.html')
    
    
@app.route('/user_history',methods=('POST','GET'))
def user_details():
    conn = psycopg2.connect(host = "dpg-cnmq90qcn0vc738fh5v0-a", database = "news_magazine", user = "news_magazine_user", password = "kcbYdr8UYXTE8jIdK9cw0Sh1KEiR56BS")
    cur = conn.cursor()
    
    cur.execute("select * from NEWS")
    data = cur.fetchall()
    return render_template("detail_table.html",data_html = data)
if __name__ == "__main__":
    app.run(debug=True)
