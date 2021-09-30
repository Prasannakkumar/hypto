from random import randint
from time import time


def start_game(casino_id,dealer_name,start_time,thrown_number,db):
    """
    start the game by dealer_name  
    
    Args:
        casino_name: Name of the casino
        dealer_name: Name of the dealer
        start_time: Start time of the game
        thrown_number: The number obtained by the throwing on to die on roullete
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        json_data = db.child("casino_db").child(casino_id).child("dealers").child(dealer_name).get().val()
        end_time = 0
        data = {
                "casino_id": casino_id,
                "dealer_name": dealer_name,
                "bet_status": True ,
                "thrown_number": thrown_number,
                "start_time": json_data["start_time"] if not start_time else start_time,
                "end_time": end_time,
                "game_id": casino_id + "_" + str(dealer_name) + "_" + str(json_data["start_time"] if not start_time else start_time),
        }

        #print(data, data["game_id"])
        db.child("game_db").child(data["game_id"]).set(data)

        data = {
            "start": True ,
            "thrown_number": thrown_number,
            "start_time": json_data["start_time"] if not start_time else start_time,
            "end_time": end_time,
        }

        db.child("casino_db").child(casino_id).child("dealers").child(dealer_name).set(data)
        return {"status":200, "message":"casino game started"}
    except:
        return {"status":500, "message":"Something went wrong"}
        


def stop_game(casino_id,dealer_name,db):
    """
    Stop the game by dealer_name, update the balance and find the winner  

    Args:
        casino_name: Name of the casino
        dealer_name: Name of the dealer 
        db: Database cursor to execute querries
    
    Returns:
        json data
    """
    try:
        json_data = db.child("game_db").get().val()
        for key_ in json_data:
            key_ = key_.strip()
            if json_data[key_]["casino_id"] == casino_id and json_data[key_]["dealer_name"] == dealer_name:
                if json_data[key_]["bet_status"]:
                    thrown_number = json_data[key_]["thrown_number"]
                    json_data[key_]["bet_status"] = False 
                    json_data[key_]["end_time"] = str(time()).split(".")[0]
                    db.child(key_).set(json_data[key_])
                    json_data_bet = db.child("bet_db").get().val()
                    print(key_,"->>>>>the key")
                    for keyBet in json_data_bet:
                        keyBet = keyBet.replace('"',"")
                        keyBet = keyBet.replace("'",'')
                        print(keyBet,"->>> user keys",json_data_bet[keyBet])
                        #keyBet = keyBet.strip()
                        #print("----------")
                        #key_ = key_.strip()
                        #print("---------->",json_data_bet[keyBet])
                        #print(json_data_bet[keyBet]["game_id"].strip() == key_,json_data_bet[keyBet])
                        if json_data_bet[keyBet]["game_id"] == key_ or json_data_bet[keyBet]["game_id"].strip() == key_.strip():
                            userData = db.child("user_db").child(json_data_bet[keyBet]["user_id"]).get().val()
                            casinoData = db.child("casino_db").child(casino_id).get().val()
                            bet_amount = json_data_bet[keyBet]["bet_amount"]
                            if json_data_bet[keyBet]["bet_number"] == thrown_number:
                                json_data_bet[keyBet]["bet_status"] = 1
                                casinoData["balance"] = str(int(casinoData["balance"]) - bet_amount)
                                userData["balance"] = str(int(userData["balance"]) + bet_amount)
                            else:
                                json_data_bet[keyBet]["bet_status"] = 2
                                casinoData["balance"] = str(int(casinoData["balance"]) + bet_amount)
                                userData["balance"] = str(int(userData["balance"]) - bet_amount)
                            #print(casinoData,userData,bet_amount,"ffff")
                            db.child("casino_db").child(casino_id).set(casinoData)
                            db.child("user_db").child(json_data_bet[keyBet]["user_id"]).set(userData)
                            db.child("bet_db").child(keyBet).set(json_data_bet[keyBet])
                    db.child("game_db").child(key_).set(json_data[key_])
                    break
        return {"status":200, "message":"casino game stopped"}
    except Exception as e:
        print(e,"not")
        return {"status":500, "message":"Something went wrong"}


def convertStrToList(dataStr)->list:
    dataList = []
    if dataStr:
        if dataStr[0] == '[':
            dataStr = dataStr[1:-1]
            dataList = dataStr.split(',')
        else:
            dataList.append(dataStr)
    res = []
    for data in dataList:
        data = data.replace("'","")
        data = data.replace('"','')
        res.append(data)
    #print(res)
    return res