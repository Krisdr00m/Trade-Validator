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
            