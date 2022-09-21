import requests


def valueItem(itemId):
    r = requests.get("https://ollie.fund/api/history/" + str(itemId))
    r = r.json()
    valuedPrice = 0
    avgPrices = []
    lowestPrice = 0
    avg = 0
    dates = []
    temp = 0
    for date in r['history']:
        dates.append(date)
    lowestNormal = 9999999999
    for date in dates:
        if r['history'][date]['rap'] is not None:
            if r['history'][date]['rap'] < lowestNormal:
                lowestNormal = r['history'][date]['rap']
        if r['history'][date]['avgSalePrice'] is not None:
            if r['history'][date]['avgSalePrice'] < lowestNormal:
                lowestNormal = r['history'][date]['avgSalePrice']
        if r['history'][date]['rap'] is None:
            avgPrices.append(r['history'][date]['avgSalePrice'])
        elif r['history'][date]['avgSalePrice'] is None:
            avgPrices.append(r['history'][date]['rap'])
        elif r['history'][date]['rap'] > r['history'][date]['avgSalePrice']:
            avgPrices.append(r['history'][date]['avgSalePrice'])
        elif r['history'][date]['avgSalePrice'] > r['history'][date]['rap']:
            avgPrices.append(r['history'][date]['rap'])
        else:
            avgPrices.append(r['history'][date]['rap'])

    for price in avgPrices:
        avg += price
        temp+=1
    avg /= len(avgPrices)

    lowestEverPrice = avg
    for price in range(len(avgPrices)):
        if avgPrices[price] < lowestEverPrice and avgPrices[price] > lowestNormal and price < 30:
            lowestEverPrice = avgPrices[price]

    r = requests.get("https://ollie.fund/api/item/" + str(itemId))
    r = r.json()
    lowestPrice = int(r['lowestPrice'])
    rap = int(r['rap'])

    if lowestEverPrice * 2 < lowestPrice:
        toDiv = lowestPrice / lowestEverPrice
        if toDiv > 2:
            toDiv += toDiv-2
        valuedPrice = (rap/toDiv + lowestPrice/toDiv + avg + avg)/4
    elif lowestPrice * 1.15 < rap:
        valuedPrice = (lowestEverPrice + lowestPrice + (avg*0.5))/3
    elif lowestPrice > rap:
        valuedPrice = (lowestPrice+rap+lowestEverPrice)/3
    elif avg > lowestPrice:
        valuedPrice = (lowestPrice + lowestEverPrice)/2
    elif rap < lowestPrice:
        valuedPrice = (rap + rap + lowestPrice)/3
    else:
        valuedPrice = (avg + (2*lowestPrice))/3

    return int(valuedPrice)

print(valueItem(input("Item ID of item to value: ")))
