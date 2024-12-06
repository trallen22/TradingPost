import get_data
import tp_helper

# test = get_data.calculateDataBars("AAPL", 1, "hour", "2024-11-04", "2024-11-08")

test = tp_helper.findAllRelatedTickers("AAPL")
print(test)