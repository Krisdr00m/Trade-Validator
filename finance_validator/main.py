import sys
from trade_parser.parser import process_csv_file
from trade_parser.validator import check_data, clean_data
from analytics.execution_metrics import volume_by_broker, buy_volume_by_symbol, notional_by_symbol, volume_per_minute
def main ():
    if len(sys.argv) > 1:
        trade_data = process_csv_file("finance_validator/data/" + sys.argv[1])
        invalid_rows = []
        new_stage = check_data(trade_data, invalid_rows)
        final_data = clean_data(new_stage, invalid_rows)
        # symbol_data = volume_by_symbol(final_data)
        # vwap_data = vwap_by_symbol(final_data)
        # net_position = net_position_by_symbol(final_data)
        broker_aggreg = volume_by_broker(final_data)
        print(broker_aggreg)
        # print(
        #     f"{len(final_data)} rows of valid trades \n",
        #     f"{len(invalid_rows)} rows of invalid trades \n",
        #     {
        #     "VALID ROWS": final_data,
        #     "INVALID ROWS": invalid_rows,
        #     })
        
        print(volume_by_broker(final_data))
        print(buy_volume_by_symbol(final_data))
        print(notional_by_symbol(final_data))
        print(volume_per_minute(final_data))
        

if __name__ == "__main__":
    main()