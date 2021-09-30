from random import randint
import casinoUtil
from time import time

def register_user(user_name,casino_id,balance,db):
    """
    Register new user with user name and balance into db

    Args:
        user_name: Name of the user
        casino_id: Id of casino to start betting
        balance: The balnce to get into a bet
        db: Database cursor to execute querries

    Returns:
        json data
    """
    try:
        user_id = user_name + "_" + str(randint(1,1000))

        data = {
            "user_name" : user_name,
            "casino_id": casino_id,
            "balance": balance,
        }
        print(data)
        db.child("user_db").child(user_id).set(data)
        
        # bettable dealers
        # casinoUtil.list_casino(db)
        return {"Status":200, "message":"User registration Successfull"}
    except:
        return {"status":500, "message":"Something went wrong"}

def bet_game(casino_id,bet_amount,user_id,game_id,bet_number,db):
    """
    Register new user with user name and balance into db

    Args:
        user_id: id of the user 
        casino_id: Id of casino to start betting
        bet_amount: the amount of bet being placed
        game_id: Id of the bettable game
        bet_number: Bet number on the Roullete 
        db: Database cursor to execute querries

    Returns:
        json data
    """
    try:
        casino_data = db.child("casino_db").child(casino_id).get().val()
        casino_bal = int(casino_data["balance"])

        amount = int(db.child("user_db").child(user_id).get().val()["balance"])
        if bet_amount<=0 or amount<bet_amount:
            return {"Status":400,"message":"Please enter bet amount within your balance"}

        if bet_amount*2 > casino_bal:
            return {"Status":400,"message":"Please choose another dealer"}

        data = {
            "user_id" : user_id,
            "casino_id": casino_id,
            "game_id": game_id,
            "bet_number": bet_number,
            "bet_amount": bet_amount,
            "bet_time": str(time()).split(".")[0],
            "bet_status": 0
        }

        key_ = data["game_id"] + "-" + data["user_id"]
        
        db.child("bet_db").child(key_).set(data)
        return {"Status":200, "message":"Bet has been placed"}
    except Exception as e:
        print("error",e)
        return {"status":500, "message":"Something went wrong"}

def get_user_casino(user_id,db):
    """
    Return casino id of user

    Args:
        user_id: Id of the user
        db: Database cursor to execute querries
    
    Returns:
        int: casino id

    """
    try:
        return db.child("user_db").child(user_id).get().val()["casino_id"]
    except:
        return -1


def enter_casino(user_id,casino_id,db):
    """
    Update the casino id for the user

    Args:
        user_id : Id of the user
        casino_id: Id of casino user wants to enter
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        db.child("user_db").child(user_id).update({"casino_id":casino_id})
        return {"Status": 200, "message": "User details updated successfully"}
    except:
        return {"status":500, "message":"Something went wrong"}

def cash_out(user_id,db):
    """
    Withdraw amount from the user account

    Args:
        user_id : Id of the user
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        amount = db.child("user_db").child(user_id).get().val()["balance"]
        db.child("user_db").child(user_id).update({"balance":0})
        return {"Status":200, "message":"The amount cashed out :: {}".format(amount)}
    except:
        return {"status":500, "message":"Something went wrong"}

def recharge_user(user_id,balance,db):
    """
    Update casino's balance data into db

    Args:
        casino_name: Name of the casino
        balance: Balance to start casino
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        if not user_id:
                user_id = "default"

        user_bal = db.child("user_db").child(user_id).get().val()["balance"]
        user_bal = str(int(user_bal)+int(balance))
    
        db.child("user_db").child(user_id).update({"balance":user_bal})
        return {"status":200, "message":"user balance updated"}
    except:
        return {"status":500, "message":"Something went wrong"}