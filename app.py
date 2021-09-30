import os
from flask import Flask, json, render_template, request, jsonify, send_file, redirect, url_for
from random import randint
import pyrebase
from time import time
import casinoUtil
import dealerUtil
import userUtil

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyA_rPzl1D8YouEsSJ1AjQwElFqH_mxOAFI",
  "authDomain": "realtime-4a7de.firebaseapp.com",
  "databaseURL": "https://realtime-4a7de.firebaseio.com",
  "projectId": "realtime-4a7de",
  "storageBucket": "realtime-4a7de.appspot.com",
  "messagingSenderId": "624733681109",
  "appId": "1:624733681109:web:e26d8881c0194973d6b95c",
  "measurementId": "G-01BBL7B415",
  "serviceAccount": "credentials/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/')
def render_html():
	return render_template('index.html')

@app.route('/register_casino')
def register_casino():
	return render_template('index.html')

@app.route('/register_casino_api', methods = ['GET', 'POST'])
def register_casino_api():
    if request.method == 'POST':
        
        casino_name = request.form['casino_name']
        casino_name = str(casino_name) if casino_name else ""

        balance = request.form['balance']
        balance = str(balance) if balance else ""

        casinoUtil.register_casino(casino_name,balance,db)
        return redirect(url_for('add_dealer_casino'))

@app.route('/recharge_casino', methods = ['GET', 'POST'])
def recharge_casino():
    casino_id = list(db.child("casino_db").get().val().keys())
    return render_template('recharge_casino.html', casino_id = casino_id,)

@app.route('/recharge_casino_api', methods = ['GET', 'POST'])
def recharge_casino_api():
    if request.method == 'POST':
        casino_id = request.form['casino_id']
        casino_id = str(casino_id) if casino_id else ""

        balance = request.form['balance']
        balance = str(balance) if balance else 0

        return casinoUtil.recharge_casino(casino_id,balance,db) 
    
    return jsonify(result = "wrong request method")

@app.route('/add_dealer_casino', methods = ['GET', 'POST'])
def add_dealer_casino():
    data = list(db.child("casino_db").get().val().keys())
    return render_template('add_dealer_casino.html', data = data)

@app.route('/add_dealer_casino_api', methods = ['GET', 'POST'])
def add_dealer_casino_api():
    if request.method == 'POST':
        casino_id = request.form['casino_id']
        casino_id = str(casino_id) if casino_id else ""

        dealers_name = request.form['dealers_name']
        dealers_name = str(dealers_name) if dealers_name else "default_0"

        return casinoUtil.add_dealer_casino(casino_id,dealers_name,db) 
    
    return jsonify(result = "wrong request method")

@app.route('/dealer_update', methods = ['GET', 'POST'])
def dealer_update():
    casino_name = list(db.child("casino_db").get().val().keys())
    return render_template('dealer.html', casino_name = casino_name)

@app.route('/dealer_update_two', methods = ['GET', 'POST'])
def dealer_update_two():
    if request.method == 'POST':
        casino_name = str(request.form['casino_name'])
        dealers_list = list(db.child("casino_db").child(casino_name).child('dealers').get().val().keys())
        return render_template('dealer_update_two.html', casino_name = casino_name, dealers_list = dealers_list)

@app.route('/dealer_update_api', methods = ['GET', 'POST'])
def dealer_update_api():
    if request.method == 'POST':
        casino_id = str(request.form['casino_name'])
        dealer_name = request.form['dealer_name']
        start_stop = int(request.form['start_stop']) # accept only 0 (end) or 1 (start)
        
        json_data = db.child("casino_db").child(casino_id).child("dealers").get().val()

        if dealer_name in json_data.keys():
            start_time = None
        
            if start_stop:
                start_time = str(time()).split(".")[0]
                thrown_number = randint(1, 36)
            else:
                print(casino_id,dealer_name)
                dealerUtil.stop_game(casino_id,dealer_name,db)
                return redirect(url_for('dealer_update'))
                
            json_data = db.child("casino_db").child(casino_id).child("dealers").child(dealer_name).get().val()

            dealerUtil.start_game(casino_id,dealer_name,start_time,thrown_number,db)
            return redirect(url_for('dealer_update'))

        return jsonify(result = "provide legit dealer names")

@app.route('/user_register', methods = ['GET', 'POST'])
def user_register():
    return render_template('user_register.html')

@app.route('/user_register_api', methods = ['GET', 'POST'])
def user_api():
    if request.method == 'POST':
        user_name = request.form['user_name']
        user_name = str(user_name) if user_name else ""

        casino_id = ""

        balance = request.form['balance']
        balance = int(balance) if balance else 0

        return userUtil.register_user(user_name,casino_id,balance,db)
        
    return jsonify(result = "wrong request method")

@app.route('/list_games_ui', methods=['GET','POST'])
@app.route('/list_games_ui/<casino_name>/<user_id>', methods=['GET','POST'])
def list_games_ui(casino_name = None, user_id = None):
    if not casino_name:
        casino_name = list(db.child("casino_db").get().val().keys())
        user_id = None
    else:
        casino_name = [casino_name]
    return render_template('list_games.html', casino_name = casino_name, user_id = user_id)


@app.route('/list_games', methods=['GET','POST'])
def list_games():
    if request.method == 'POST':
        casino_id = request.form['casino_id']
        casino_id = str(casino_id) if casino_id else ""

        user_id = request.form['user_id']
        user_id = str(user_id) if user_id else ""

        list_of_game_ids = casinoUtil.get_list_of_Games(casino_id,db)["result"]
        return redirect(url_for('user_bet_game_ui', user_id = user_id, list_of_game_ids = list(list_of_game_ids)))

    return jsonify(result = "wrong request method")
        
@app.route('/user_bet_game_ui', methods = ['GET', 'POST'])
@app.route('/user_bet_game_ui/<user_id>/<list_of_game_ids>', methods=['GET','POST'])
def user_bet_game_ui(user_id = None, list_of_game_ids = None):
    # prints string
    # print(user_id, list_of_game_ids,type(list_of_game_ids),"the statement /n/n/n")
    list_of_game_ids =  dealerUtil.convertStrToList(list_of_game_ids)
    return render_template('user_bet_game_ui.html', user_id = user_id, list_of_game_ids = list(list_of_game_ids))


@app.route('/user_bet_game', methods = ['GET', 'POST'])
def user_bet_game():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_id = str(user_id) if user_id else ""

        casino_id = userUtil.get_user_casino(user_id,db)

        game_id = request.form['game_id']
        game_id = str(game_id) if game_id else ""
        
        bet_number = request.form['bet_number']
        bet_number = int(bet_number) if bet_number else 1

        bet_amount = request.form['bet_amount']
        bet_amount = int(bet_amount) if bet_amount else 0

        return userUtil.bet_game(casino_id,bet_amount,user_id,game_id,bet_number,db)

    return jsonify(result = "wrong request method")


@app.route('/user_enter_casino_ui', methods=['GET','POST'])
def user_enter_casino_ui():
    user_id = list(db.child("user_db").get().val().keys())
    casino_id = list(db.child("casino_db").get().val().keys())
    return render_template('user_enter_casino_ui.html', user_id = user_id, casino_id = casino_id)

@app.route('/user_enter_casino', methods=['GET','POST'])
def user_enter_casino():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_id = str(user_id) if user_id else ""

        casino_id = request.form['casino_id']
        casino_id = str(casino_id) if casino_id else ""

        userUtil.enter_casino(user_id,casino_id,db)
        list_of_game_ids = casinoUtil.get_list_of_Games(casino_id,db)["result"]
        return redirect(url_for('user_bet_game_ui', casino_name = casino_id, user_id = user_id,list_of_game_ids = list(list_of_game_ids)))

    return jsonify(result = "wrong request method")

@app.route('/user_cashout_ui', methods = ['GET', 'POST'])
def user_cashuout_ui():
    user_id = list(db.child("user_db").get().val().keys())
    return render_template('user_cashout.html', user_id = user_id,)

@app.route('/user_cash_out', methods=['GET','POST'])
def user_cash_out():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_id = str(user_id) if user_id else ""

        return userUtil.cash_out(user_id,db)

    return jsonify(result = "wrong request method")

@app.route('/recharge_user_ui', methods = ['GET', 'POST'])
def recharge_user_ui():
    user_id = list(db.child("user_db").get().val().keys())
    return render_template('recharge_user.html', user_id = user_id,)

@app.route('/user_recharge', methods=['GET','POST'])
def user_recharge():
    if request.method == 'POST':
        user_id = request.form['user_id']
        user_id = str(user_id) if user_id else ""

        balance = request.form['balance']
        balance = str(balance) if balance else 0
        
        return userUtil.recharge_user(user_id,balance,db)

    return jsonify(result = "wrong request method")

if __name__ == '__main__':
	app.run(debug = True)