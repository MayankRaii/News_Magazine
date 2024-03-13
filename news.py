from flask import Flask, render_template, request, redirect, url_for, abort
from bs4 import BeautifulSoup
import nltk
from nltk import word_tokenize, sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from heapq import nlargest
import psycopg2
import json
import requests

# Download necessary NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("vader_lexicon")

app = Flask(__name__, static_folder='static')

# Define the database connection parameters
DB_HOST = "dpg-cnmq90qcn0vc738fh5v0-a"
DB_NAME = "news_magazine"
DB_USER = "news_magazine_user"
DB_PASSWORD = "kcbYdr8UYXTE8jIdK9cw0Sh1KEiR56BS"

# Define keywords for different genres
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
    stop_words = nltk.corpus.stopwords.words("english")
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


def fun_genre(text):
    genres = {}
    for genre, words in keywords.items():
        count = sum(1 for word in words if word in text)
        genres[genre] = count

    return max(genres, key=genres.get)


def sentiment(text):
    sid = SentimentIntensityAnalyzer()
    sentences = nltk.sent_tokenize(text)
    total_compound = sum(sid.polarity_scores(sentence)['compound'] for sentence in sentences)
    mean_compound = total_compound / len(sentences)

    if mean_compound > 0.5:
        return "Positive"
    elif -0.5 < mean_compound < 0.5:
        return "Negative"
    else:
        return "Neutral"


@app.route("/", methods=('POST', 'GET'))
def portal():
    if request.method == 'POST':
        url = request.form["enter_url"]

        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(class_="xf8Pm byline")
            title = soup.title.get_text()

            main_text = soup.find(class_="_s30J clearfix")
            div_tag = BeautifulSoup(str(main_text))
            for span_tag in div_tag.find_all('span'):
                span_tag.extract()
            text = div_tag.get_text()

            summary = summarize_text(text, 6)
            new_text = re.sub(r'[^\w\s]', '', text)
            lst_text = word_tokenize(new_text)
            lst_words = [word for word in lst_text if word not in nltk.corpus.stopwords.words("english")]
            clean_text = ' '.join(lst_words)
            compound = sentiment(clean_text)

            a = results.find('span')
            publisher = a.get_text()

            estimated_time = calculate_reading_time(text)
            estimated_summ_time = calculate_reading_time(summary)

            genre = fun_genre(clean_text)

            word_list = word_tokenize(text)
            count_word = len([word for word in word_list if word not in [".", ",", "?"]])
            count_sent = len(sent_tokenize(text))
            count_stp_word = len([word for word in word_list if word in nltk.corpus.stopwords.words("english")])

            pos_tags = nltk.pos_tag(word_list, tagset="universal")
            pos_counts = {"NOUN": 0, "PRON": 0, "VERB": 0, "ADJ": 0, "ADV": 0, "CONJ": 0}
            for word, pos in pos_tags:
                if pos in pos_counts:
                    pos_counts[pos] += 1

            with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO NEWS(url,text,estimated_time,title,genre,compound,publisher,count_word,"
                                "count_sent,count_stp_word,upos) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (url, text, estimated_time, title, genre, compound, publisher, count_word,
                                 count_sent, count_stp_word, json.dumps(pos_counts)))
                    conn.commit()

        except Exception as e:
            print(e)
            return abort(406)

    return render_template("index.html", msg_time=estimated_time, msg_title=title, msg_url=url, msg_genre=genre,
                           msg_summary=summary, msg_summ_time=estimated_summ_time, msg_text=text,
                           msg_count_word=count_word, msg_count_sent=count_sent, msg_count_stp_word=count_stp_word,
                           msg_dict1=pos_counts, msg_compound=compound, msg_results=publisher)


@app.route("/Password", methods=('POST', 'GET'))
def paswrd_input():
    if request.method == 'POST':
        return render_template('password.html')


@app.route('/user_history', methods=('POST', 'GET'))
def user_details():
    with psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM NEWS")
            data = cur.fetchall()
    return render_template("detail_table.html", data_html=data)


if __name__ == "__main__":
    app.run(debug=True)
