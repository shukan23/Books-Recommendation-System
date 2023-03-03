from server.models import User, Books, Clicks, Search
from flask_wtf import FlaskForm
from flask import flash,render_template, redirect, session, jsonify, request, url_for
from server import app, bcrypt
from server import db
from datetime import datetime
from sqlalchemy import desc
from server.forms import LoginForm,RegistrationForm 
from flask_login import login_user, logout_user, current_user ,login_required
from ast import literal_eval
import pandas as pd
import numpy as np
import csv
from bs4 import BeautifulSoup
import requests
import re
from random import randint
import spacy
import enchant
import pickle
nlp = spacy.load("en_core_web_sm")

header ={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"} 
# amazon = 'https://www.amazon.in'
amazon_sk = 'https://www.amazon.in/s?k='

titles = []
keywords = {}
books = pd.read_csv('./instance/books_v2.csv',sep=";")
grammar = ['PROPN', 'NOUN', 'VERB', 'NUM', 'SYM']

new_books = books[['ISBN','Book-Title']]
f=open("./instance/similarity.pkl","rb")
vector = pickle.load(f)

def get_amazon_ad(item):
    cata = ['t-shirt', 'cups', 'hoodie', 'pillow', 'mobile cover']
    item = item + " " + cata[randint(0,len(cata)-1)]
    html_data = requests.get(amazon_sk + item, headers=header).text
    soup = BeautifulSoup(html_data, 'lxml')
    items = soup.find_all('div', {'data-component-type': 's-search-result'})
    name = items[0].h2.text.strip()
    img = items[0].find_all('img')[0]['src']
    price = items[0].find_all('span',{'class': 'a-price'})[0].find_all('span')[0].text
    return {'Name':name, 'Image':img, 'Price':price}

def recommend(movie):
    index = new_books[new_books['Book-Title'] == movie].index[0]
    distances = sorted(list(enumerate(vector[index])),reverse=True,key = lambda x: x[1])
    result = []
    for i in distances[1:6]:
        result.append(new_books.iloc[i[0], 0])
        # print(new_books.iloc[i[0], 0])
    return result

def create_search_dict():
    for index, row in books.iterrows():
      title = row['Book-Title']
      titles.append([title, row['ISBN']])
      title = re.sub("[,.:;&#?()'-]", "", title)
      doc = nlp(title)
      for token in doc:
        if(token.pos_ in grammar):
          if(token.text in keywords):
            keywords[token.text].add(index);
          else:
            keywords[token.text] = {index};
        
def search111(s):
    doc = nlp(s)
    ans = set()
    for word in doc:
        if(word.pos_ in grammar):
            for key in keywords:
                if(enchant.utils.levenshtein(key,word.text)<3):
                    ans = ans.union(keywords[key])
    results = []
    for boook in ans:
        results.append(titles[boook][1])
    return results

create_search_dict()

@app.route('/')
def start_application():
    return render_template('first.html')

@app.route('/signup', methods=['POST','GET'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit() :
        result = (
        db.session.query(User)
        .filter(User.email == form.email.data)
        .one_or_none()
        )
        # print("result: ",result)
        if result is not None:
            # print("Account Exists")
            flash("Email Already Registred")
            return redirect(url_for('sign_up'),form = form)
        else:
            return render_template('details.html', email = form.email.data , password = form.password.data)
    elif request.method == 'GET':
        return render_template('signup.html',form = form)
    return render_template('signup.html',form = form)
    
@app.route('/details', methods=['POST','GET'])
def take_details():
    if request.method == 'POST' :
        x = datetime.strptime(request.form.get("dob") , '%Y-%m-%d')
        print(x.year)
        print(x.month)
        print(x.day)
        hased_pw = bcrypt.generate_password_hash(request.form.get('passw')).decode('utf-8')
        me = User(email= request.form.get("email"),firstName = request.form.get("fname"),lastName = request.form.get("lname"),password = hased_pw, addressLine = request.form.get("adline1"),city = request.form.get("city"),zip = request.form.get("zip"),state = request.form.get("state"),country = request.form.get("country"),dob = x)
        print(me)
        db.session.add(me)
        db.session.commit()
        return redirect(url_for('login_one'))
    if request.method == 'GET':
        # print("request for signup")
        return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login_one():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # print('Email:',form.email.data)
        # print('Password:',form.password.data)
        result = User.query.filter_by(email=form.email.data).first()
        result = User.query.filter_by(email=form.email.data).first()
        # result = User.query.filter_by().all()
        # print(type(result[0]),"Swaminarayan")
        # y = jsonify()
        if result is None :
            flash("You are not registred.")
            return redirect(url_for('login_one'))
        else:
            comp = bcrypt.check_password_hash(result.password,form.password.data)
            if comp :
                login_user(result, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))      
            else:
                flash("Password Does Not Match",'danger')
                return redirect(url_for('login_one'))
    return render_template('login.html', email="" , form = form)

@app.route('/home')
@login_required 
def home():
    
    click = Clicks.query.filter_by(uid=current_user.uid).order_by(desc(Clicks.time1)).limit(5).all()
    clicked_books = []
    for i in click:
        x = Books.query.filter_by(isbn=i.isbn).first()
        if x not in clicked_books:
            clicked_books.append(x)

    book_rec = []
    d = []
    d1 = []
    if click:
        d = recommend(clicked_books[0].title)
    
    # if len(click) == 2:
    #     d1 = recommend(clicked_books[1].title)
    #     x = Books.query.filter_by(isbn = d1[0]).first()
    #     book_rec.append(x)
    
    for k in d:
        x = Books.query.filter_by(isbn=k).first()
        book_rec.append(x)
    
    

    sea = Search.query.filter_by(uid=current_user.uid).order_by(desc(Search.time1)).limit(4).all()
    ads = []
    # total = 3 
    # remain = 3 - len(sea)
    # for i in range(remain):
    #     ads.append(get_amazon_ad(""))
    for i in sea:
        ads.append(get_amazon_ad(i.searchtxt))

    print(ads)
    result = Books.query.filter_by().limit(50).all()
    # page = request.args.get('page',1,type=int)
    # result = Books.query.paginate(page=page,per_page=5)

    return render_template('home.html', recommended=book_rec ,history=clicked_books,books=result,ads=ads)

@app.route('/search',methods=['POST'])
def search_books():

    text = request.form['text']
    searched = Search(uid=current_user.uid,searchtxt = text)
    db.session.add(searched)
    db.session.commit()

    print("this is searched",text)
    ans = search111(text)
    result_final = []
    for i in ans:
        x = Books.query.filter_by(isbn=i).first()
        result_final.append(x)
    # print(ans)
    return render_template('home.html',books = result_final)

@app.route('/book/<isbn1>')
@login_required 
def openbook(isbn1):

    clicked = Clicks(uid=current_user.uid,isbn = isbn1)
    db.session.add(clicked)
    db.session.commit()
    
    # print("i have printed",isbn1)
    result = Books.query.filter_by(isbn=isbn1).first()
    books2 = recommend(result.title)
    book_rec = []
    for k in books2:
        x = Books.query.filter_by(isbn=k).first()
        book_rec.append(x)
    
    revi1 = literal_eval(result.reviews)
    return render_template('book.html',i=result,books=book_rec,review = revi1)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('start_application'))








