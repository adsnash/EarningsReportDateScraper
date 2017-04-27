This program is designed to get a list of earnings report dates for publicly traded companies from 1/1/2000 (or as far back as they are available) to now and save it in CSV format. It will create a directory called EarningsDates in the current working directory when it does so. 

There are two options to run the program. One can give it the ticker symbols of individual stocks, or it can can get the S&P 500. 

Please note: it will not be able to look up every company. Tickers that are not entirely composed of letters (such as Berkshire Hathaway: BRK.B) will need to be searched by their CIK numbers. These can be obtained by searching the ticker name and CIK in the same query.

I was inspired to create this program while doing market research on a stock. I wanted to check how earnings reports impacted the stock's price, but was not able to find a simple list of historical earnings report dates. The most infuriating part was finding a partial list which required me to pay for the full dataset. 

Eventually I decided to go to the source and get the information from the SEC's website. After playing around with the search settings in the URL, I realized I could get to the respective page for pretty much any company by just slightly tweaking the URL. 

I wrote a web scraping script to get the information I was after, then wrapped it all up in a class to allow a user to get the information for any company and added an extra feature to get the information for the S&P 500. 

I have an issue with companies charging for free publicly available information, so please feel free to spread this script far and wide. Ok rant over, please enjoy!