class AggregateData:
    def __init__(self):
        self.close = []
        self.high = []
        self.low = []
        self.numTransactions = []
        self.open = []
        self.timestamp = []
        self.volume = []
        self.volWeightedAvg = []

    def appendDataPoint(self, dataPoint: dict):
        self.close.append(dataPoint["c"])
        self.high.append(dataPoint["h"])
        self.low.append(dataPoint["l"])
        self.numTransactions.append(dataPoint["n"])
        self.open.append(dataPoint["o"])
        self.timestamp.append(dataPoint["t"])
        self.volume.append(dataPoint["v"])
        self.volWeightedAvg.append(dataPoint["vw"])

    def convertToDict(self):
        return {
            "Close": self.close,
            "High": self.high,
            "Low": self.low,
            "num_transactions": self.numTransactions,
            "Open": self.open,
            "timestamp": self.timestamp,
            "Volume": self.volume,
            "volume_weighted_avg_price": self.volWeightedAvg
        }
