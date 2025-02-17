# 📰 NewsMagzine

## ✨ Overview
**NewsMagzine** is a web application designed to extract and analyze news articles from *Times of India* by URL. It provides users with a convenient platform to understand and analyze news articles, enhancing their reading experience with features like sentiment analysis, summaries, and more.

## 🛠️ Tools & Technologies Used
- **Backend:** Flask
- **Database:** PostgreSQL
- **Text Processing:** NLTK, BeautifulSoup, requests, urllib, tokenize, psycopg2, json
- **Authentication:** Authlib (Google authentication)
- **Frontend:** HTML, CSS, JavaScript
- **Additional:** `abort` function in Flask for error handling

## 🔄 Work Process
1. Users enter a *Times of India* article URL.
2. The article content is extracted using **BeautifulSoup**.
3. The text is cleaned and processed using **NLTK**.
4. **Sentiment analysis**, **summarization**, and **tokenization** are applied.
5. Data is organized and displayed in an analytical format.
6. User data is stored in **PostgreSQL** for a seamless experience.
7. Admins can access user history.

## 👨‍💻 User Benefits
- Easily analyze news articles.
- Get sentiment insights (Positive, Negative, Neutral).
- Receive a **summary** and **estimated reading time**.
- View detailed stats: word count, sentences, stop words, POS tags.
- Secure Google authentication.
- Admins can access user view history.

## 🔍 Features
- **Title Extraction**
- **Genre Identification**
- **Sentiment Analysis**
- **Published Date & Time**
- **Summary Generation**
- **Cleaned Article Text**
- **Word, Sentence, and POS Analysis**
- **Admin View Access to User History**
- **Google Authentication for Users**

## ⚙️ Algorithm
1. The entered URL is fetched using `requests`.
2. **BeautifulSoup** extracts the article content.
3. The text is cleaned and processed.
4. Sentiment, summary, and genre classification are performed.
5. The extracted data is displayed in an **analysis report**.
6. User data is securely stored in **PostgreSQL**.
7. Admins can view user history upon login.

## 🛡️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/MayankRaii/News_Magazine.git
   cd NewsMagzine
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up PostgreSQL database and configure `.env` file.
4. Run the application:
   ```bash
   flask run
   ```

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/6/60/Newspaper_noun_project_227.svg" alt="NewsMagzine Icon" width="120px"/>
</p>

