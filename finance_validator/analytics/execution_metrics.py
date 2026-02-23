from trade_parser.models import Trade

def volume_by_symbol(trades: list[Trade]) -> dict[str, int]:
    symbol_dict = dict()
    for trade in trades:
        try:
            if(symbol_dict[trade.symbol]):
                symbol_dict[trade.symbol] += trade.quantity
        except(KeyError):
            symbol_dict[trade.symbol] = trade.quantity
            
    
    return symbol_dict

def vwap_by_symbol(trades: list[Trade]) -> dict[str, float]:
    
    price_quantity_factor_dict = dict()
    volume_dict = volume_by_symbol(trades)
    vwap_by_symbol = dict()
    
    for trade in trades:
        try:
            if(price_quantity_factor_dict[trade.symbol]):
                price_quantity_factor_dict[trade.symbol] += trade.quantity * trade.price
        except(KeyError):
            price_quantity_factor_dict[trade.symbol] = trade.quantity * trade.price
    
    for key, value in price_quantity_factor_dict.items():
        vwap_by_symbol[key] = value/volume_dict[key]
    
    return vwap_by_symbol