import get_data
import tp_helper
from option import Option

# test = get_data.calculateDataBars("AAPL", 1, "hour", "2024-11-04", "2024-11-08")

# test = tp_helper.findAllRelatedTickers("AAPL")
# print(test)

testOption = Option("O:SPY251219C00650000")

print(testOption.basicInfo)
print(testOption.extendedInfo)