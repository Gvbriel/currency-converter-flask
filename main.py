
from __future__ import print_function
import sys
from datetime import date
from flask import Flask, redirect, url_for, render_template, request
from currency_converter import CurrencyConverter


c = CurrencyConverter(fallback_on_wrong_date=True)

currencyList = c.currencies
baseValue = 0

class currency:
    tocur = "USD"
    fromcur = "USD"


app = Flask(__name__)

def setDateMin(tocurrency, fromcurrency):
    dateone, lastdateIn = c.bounds[tocurrency]
    datetwo, lastdateOut = c.bounds[fromcurrency]
    dateone1 = str(dateone)
    datetwo1 = str(datetwo)

    if dateone1 and datetwo1:
        dateone = dateone1.split("-", -1)
        datetwo = datetwo1.split("-", -1)

        if (dateone[0] == datetwo[0]) and (dateone[1] == datetwo[1]) and (dateone[2] == datetwo[2]):
            return dateone
        else:
            if dateone[0] < datetwo[0]:
                return datetwo
            elif dateone[0] > datetwo[0]:
                return dateone
            else:
                if dateone[1] > datetwo[1]:
                    return datetwo
                elif dateone[1] < datetwo[1]:
                    return dateone
                else:
                    if dateone[2] > datetwo[2]:
                        return datetwo
                    elif dateone[2] < datetwo[2]:
                        return dateone
    else:
        return 0


def setDateMax(tocurrency, fromcurrency):
    dateone, lastdateIn = c.bounds[tocurrency]
    datetwo, lastdateOut = c.bounds[fromcurrency]
    dateone1 = str(lastdateIn)
    datetwo1 = str(lastdateOut)

    if dateone1 and datetwo1:

        dateone = dateone1.split("-", -1)
        datetwo = datetwo1.split("-", -1)

        if (dateone[0] == datetwo[0]) and (dateone[1] == datetwo[1]) and (dateone[2] == datetwo[2]):
            return dateone
        else:
            if dateone[0] > datetwo[0]:
                return datetwo
            elif dateone[0] < datetwo[0]:
                return dateone
            else:
                if dateone[1] > datetwo[1]:
                    return datetwo
                elif dateone[1] < datetwo[1]:
                    return dateone
                else:
                    if dateone[2] > datetwo[2]:
                        return datetwo
                    elif dateone[2] < datetwo[2]:
                        return dateone
    else:
        return 0

def datesplit(date):
    dateD = date.split("-", -1)
    list = [int(n) for n in dateD]
    return list

@app.route('/', methods=["POST","GET"])
def home():

    if request.method == "POST":

        if request.form["submit"] == "selectcurrencies":
            tocurrency = request.form["tocurrencies"]
            fromcurrency = request.form["fromcurrencies"]
            currency.fromcur = fromcurrency
            currency.tocur = tocurrency
            mind = setDateMin(tocurrency, fromcurrency)
            maxd = setDateMax(tocurrency, fromcurrency)
            mind = mind[0] + "-" + mind[1] + "-" + mind[2]
            maxd = maxd[0] + "-" + maxd[1] + "-" + maxd[2]
            print("Min date" + mind, file=sys.stderr)
            print("Max date" + maxd, file=sys.stderr)
            return render_template("index.html", usd=0, currencyList=currencyList, mindate=mind, maxdate=maxd, fromCur=fromcurrency, toCur=tocurrency, priceCurValue=round(c.convert(1, fromcurrency, tocurrency),2),
                                           priceCur=tocurrency)

        elif request.form["submit"] == "convert":
            amount = request.form["amount"]
            dateD = request.form["pricedate"]
            dateD = datesplit(dateD)
            tocurrency = currency.tocur
            fromcurrency = currency.fromcur

            if amount.isdigit():
                print(dateD, file=sys.stderr)
                #print(setDate(tocurrency,fromcurrency), file=sys.stderr),
                converted = c.convert(amount, fromcurrency, tocurrency, date=date(dateD[0], dateD[1], dateD[2]))
                converted = round(converted, 2)
                return render_template("index.html", usd=converted,
                                           currencyList=currencyList, conv=fromcurrency)
            else:
                return render_template("index.html", usd=baseValue, currencyList=currencyList)

            #return render_template("index.html", usd=c.convert(amount, fromcurrency, tocurrency), currencyList=currencyList, priceCurValue=c.convert(1, fromcurrency, tocurrency), priceCur=tocurrency,mindate=setDate(tocurrency, fromcurrency), maxdate="2020-10-12")
    else:
        return render_template("index.html", usd=0, currencyList=currencyList)



if __name__ == "__main__":
    app.run(debug=True)

