from models import Trade
from datetime import datetime
import re

def check_data(trade_data: list[str], invalid_rows):
    if len(trade_data) > 0:
        next_step_data = []
        for row in trade_data:
            try:
                new_trade = Trade(
                    trade_id= row[0], 
                    symbol= row[1],
                    price= float(row[2]),
                    quantity=int(row[3]),
                    timestamp= datetime.fromisoformat(row[4]),
                    exchange=row[5],
                    side=row[6],
                    broker_id=row[7]
                    )

                next_step_data.append(new_trade)
            except ValueError as e:
                invalid_rows.append(row)
                
                if e.args[0].rfind("float") > 0:
                    print("float issue")
                elif e.args[0].rfind("int") > 0:
                    print("int issue")
                elif e.args[0].rfind("isoformat") > 0:
                    print("time issue")
    return (next_step_data)

def clean_data(trade_data_objects, invalid_rows):
    trade_id_set = set()
    set_size: int
    for index, data in enumerate(trade_data_objects):
        set_size = len(trade_id_set)
        
        #trade id check
        if data.trade_id is not "":
            format = re.search(r"^T\d+", data.trade_id)
            if format and any(char.isdigit() for char in data.trade_id ):
                trade_id_set.add(data.trade_id)
                if(set_size == len(trade_id_set)):
                    trade_data_objects.pop(index)
        else:
            trade_data_objects.pop(index)
            invalid_rows.append(data)

        #price check
        if((data.price <= 0) or (data.quantity <= 0)):
            trade_data_objects.pop(index)
            invalid_rows.append(data)
            
        
        #side check
        if(data.side not in ("BUY", "SELL")):
            trade_data_objects.pop(index)
            invalid_rows.append(data)
            
        
        #exchange check
        if(data.exchange not in ("NASDAQ","NYSE") or not all(char.isupper() for char in data.exchange)):
            trade_data_objects.pop(index)
            invalid_rows.append(data)
            
        
        #symbol check
        if(data.symbol is "") or (data.symbol is " "):
            trade_data_objects.pop(index)
            invalid_rows.append(data)
                
        if not all(char.isupper() for char in data.symbol):
            trade_data_objects.pop(index)
            invalid_rows.append(data)
            
        #broke id check:
        if(data.broker_id is "") or not re.search(r"^BRK\d+", data.broker_id):
                trade_data_objects.pop(index)
                invalid_rows.append(data)
        
    return trade_data_objects