from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np



rec_count = 0

# The values that'll be extracted from the wikipedia table
platform = []
type = []
firm = []
release = []
units_sold = []


# Setting up extraction of table
surl = 'https://en.wikipedia.org/wiki/List_of_best-selling_game_consoles'
html_text = requests.get(surl).text
soup = BeautifulSoup(html_text, 'lxml')
chart = soup.find('div', id='mw-content-text').find('table')

# Extracting data from the table
for row in chart.find_all('tr')[1:]:
        col = row.find_all('td')
        column1 = (col[0].find('a')['title'].strip())   # Returns the name of the platform from the table.
        column2 = col[1].string.strip()                 # Returns whether the console is a handheld or home console.
        column3 = col[2].find('a')['title'].strip()     # Returns the console's manufacturing firm.
        column4 = col[3].string.strip()                 # Returns the console's release year.
        column4 = column4[0:4]

        # If the row contains a <sup> tag or a <small> tag, col[4].string will return None
        # An if else statement is used to handle different tags

        if col[4].string is not None:
                column5 = col[4].string         # Returns the console's units sold in millions, if there is no <sup> or <small> tag in the column
        else:                                   # A second if else statement is used to handle the row, depending on whether it has a <sup> tag or a <small> tag
                if 'million' in col[4].next:    # Returns units sold if row contains a <small> tag
                        column5 = col[4].next
                else:                           # Returns units sold if row contains a <sup> tag
                        column5 = col[4].next.next.next.next

        # Removes text from the units sold and leaves just the raw number
        column5 = (column5.replace('million',''))
        column5 = (column5.replace('\n', ''))

        # Converts string into a numerical format with 2 decimal places.
        # Exception line covers cases where units sold lies in a range (eg. "82-84")
        try:
                column5 = round(float(column5),2)
        except:
                column5 = round(float(column5[:2]),2)


        # Adds data to all lists created earlier
        platform.append(column1)
        type.append(column2)
        firm.append(column3)
        release.append(column4)
        units_sold.append(column5)

        rec_count += 1

# Formatting columns for the database
columns = {'Platform': platform, 'Console_Type': type, 'Firm': firm, 'Release_Year': release, 'Units_Sold_in_Millions': units_sold}

print (rec_count)

# Ensuring "units_sold" column is in numeric format
df = pd.DataFrame(columns)
df[["Units_Sold_in_Millions"]] = df[["Units_Sold_in_Millions"]].apply(pd.to_numeric)

print(df)

df.index += 1
df = df[['Platform', 'Console_Type', 'Firm', 'Release_Year', 'Units_Sold_in_Millions']]
df.index.name = "Console_Rank"
df.to_csv("BestSellingConsoles.csv", sep=",", encoding='utf-8-sig')
