#! python3

import bs4
import datetime
import os
import requests
import re
import csv
import sys

class EarningsDates():

    def __init__(self):
        self.dateList = []
        self.ticker = ''
        self.failures = []

    '''Get user input for what they want to do with the program'''
    def whatToDo(self):
        print('''This program takes stock tickers and finds their historical earning report dates
It will then place them in a folder called \'EarningsDates\'
Please note: you may have to enter the stock\'s CIK\n''')
        while True: 
            choice = input('''What would you like to do?
Press \'A\' to get the earnings report dates for the S&P 500
Press \'I\' to look up an individual stock ticker
Press \'Q\' to quit: ''')
            if choice.lower() == 'a':
                self.getSP500()
                break
            elif choice.lower() == 'i':
                ticker = str(input('\nPlease enter the ticker symbol of a stock you\'d like to look up: ')).upper()
                print()
                self.getEarnings(ticker)
                self.reset()
                break
            elif choice.lower() == 'q':
                print('\nSo long, space cowboy!\n')
                sys.exit()
            else:
                print('\nInvalid choice, please enter \'A\', \'I\' or \'Q\'.\n')

    '''Call to get S&P 500 list, datelist for each company, and add to folder'''
    def getSP500(self):
        tickerList = self.SP500List()
        for i in range(len(tickerList)):
            self.getEarnings(tickerList[i])
        self.reset()

    '''Get datelist and add to CSV folder'''
    def getEarnings(self, ticker):
        self.ticker = ticker
        self.dateList = self.getDateList(self.ticker)
        self.addCSV(self.ticker, self.dateList)

    def reset(self):
        if self.failures != []:
            self.printFailures()
            self.failures = []
        self.dateList = []
        self.ticker = ''
        print()

    '''Build list of S&P 500 companies by scraping list from wikipedia'''
    def SP500List(self):
        print('\nGetting list of S&P 500 companies\n')
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        table = soup.find('table', {'class':'wikitable sortable'})
        tickerList = []
        for i in table.findAll('tr')[1:]:
            ticker = i.findAll('td')[0].text
            tickerList.append(ticker)
        return tickerList

    '''Create CSV file for ticker and datelist and add to folder'''
    def addCSV(self, ticker, dateList):
        if dateList == None:
            print('No available data to create CSV file for '+ticker)
        else:
            if not os.path.exists('EarningsDates'):
                os.makedirs('EarningsDates')
            name = ticker+'_EarningsDates.csv'
            if not os.path.exists('EarningsDates/'+name):
                print('Creating CSV file for '+ticker)
                outFile = open('EarningsDates/'+name, 'w', newline='')
                outWrite = csv.writer(outFile)
                for i in range(len(dateList)):
                    outWrite.writerow(dateList[i])
                outFile.close()
            else:
                print('Already have CSV file for '+ticker)

    '''Go to SEC site for quarterly earnings report and scrape for dates'''
    def getDateList(self, ticker):
        print('Searching for earnings report dates for '+ticker)
        url = 'https://www.sec.gov/cgi-bin/browse-edgar?type=10-&dateb=&owner=include&count=100&action=getcompany&CIK=%s' % ticker
        headerInfo={'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url,headers=headerInfo)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        noMatch = soup.select('p > center > h1')
        trElems = soup.select('tr')
        '''Regex to get earnings report dates no earlier than 1/1/2000'''
        dateFind = re.compile(r'2\d{3}-\d{2}-\d{2}')
        if noMatch != []:
            self.failures.append(ticker)
            print('Could not find earnings report dates for '+ticker)
            return None
        dateList = []
        dateList.append(['EarningsDates'])
        for tr in trElems:
            tdElems = tr.select('td')
            if len(tdElems) == 5 and dateFind.search(tdElems[3].getText()) != None:
                date = tdElems[3].getText()
                converted = datetime.datetime.strptime(date,'%Y-%m-%d').strftime('%m/%d/%Y')
                dateList.append([converted])
        return dateList

    '''Print tickers program was unable to get dates from'''
    def printFailures(self):
        print('\nCould not look up the following ticker(s):')
        for i in range(len(self.failures)):
            print(self.failures[i])
        print('Try looking up \'<ticker> CIK\' and entering that number instead of the ticker')

    '''Loop to either get S&P 500 list, individual stocks, or quit program'''
    def usageLoop(self):
        while True:
            self.whatToDo()

def main():
    Earnings = EarningsDates()
    Earnings.usageLoop()

if __name__ == '__main__':
    main()
