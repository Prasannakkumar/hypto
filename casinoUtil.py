from random import randint

def register_casino(casino_name,balance,db):
    """
    Inserts casino's data into db

    Args:
        casino_name: Name of the casino
        balance: Balance to start casino
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        if not casino_name:
            casino_name = "default"

        data = {
            "casino_name": casino_name,
            "balance": balance,
        }

        id_ = randint(1,1000)
        id_ = casino_name + "_" + str(id_)
        db.child("casino_db").child(id_).set(data)
        return {"status":200, "message":"Created casino successfully", "casino_id":id_}
    except:
        return {"status":500, "message":"Something went wrong"}
    

def recharge_casino(casino_id,balance,db):
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
        if not casino_id:
                casino_id = "default"

        casino_bal = db.child("casino_db").child(casino_id).get().val()["balance"]
        casino_bal = str(int(casino_bal)+int(balance))
    
        db.child("casino_db").child(casino_id).update({"balance":casino_bal})
        return {"status":200, "message":"casino balance updated"}
    except:
        return {"status":500, "message":"Something went wrong"}

def add_dealer_casino(casino_id,dealer_name,db):
    """
    add new dealer into casino 

    Args:
        casino_name: Name of the casino
        dealer_name: Name of the dealer to be added
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        if not casino_id:
            casino_id = "default_0"

        #dealers = db.child("casino_db").child(casino_id).get().val()["dealers"]
        #dealers = int(int(dealers)+int(dealers_name))

        data = {"start": False, "thrown_number": 0, "start_time": 0, "end_time": 0}

        db.child("casino_db").child(casino_id).child("dealers").child(dealer_name).set(data)
        return {"status":200,"message":"casino dealeres updated"} 
    except:
        return {"status":500,"message":"Something went wrong"}
    
def get_list_of_Games(casino_id,db):
    """
    Get the list of bettable game's from casino_id

    Args:
        casino_id: Id of casino to get the games
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        res_data = {}
        json_data = db.child("game_db").get().val()
        res_data["result"] = [str(each_dict["game_id"]) for each_dict in json_data.values() if each_dict["casino_id"] == casino_id and each_dict["bet_status"]]
        res_data["Status"] = 200
        return res_data
    except:
        return {"status":500,"message":"Something went wrong"}


def list_casino(db):
    """
    List the casinos from casino db

    Args:
        db: Database cursor to execute querries
    
    Returns:
        json data

    """
    try:
        res = []
        casinos_data = db.child("casino_db").get().val()
        for casino in casinos_data:
            res.append(casinos_data[casino]["casino_name"]+'('+str(casino)+')')
        return {"status" : 200 ,"result":res}
    except Exception as e:
        print(e)
        return {"status" : 500 ,"result":[]}