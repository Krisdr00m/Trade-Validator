from trade_parser.models import Trade

def volume_by_symbol(trades: list[Trade]) -> dict[str, int]:
    symbol_dict = {}
    for trade in trades:
        if symbol_dict[trade.symbol]:
            symbol_dict[trade.symbol] += trade.quantity
        else:
            symbol_dict[trade.symbol] = trade.quantity
    
    return symbol_dict
            