from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

pages = 20
rec_count = 0

# The values that'll be extracted from the vgchartz database.

rank = []
gname = []
platform = []
year = []
critic_score = []
publisher = []
developer = []
sales_na = []
sales_eu = []
sales_jp = []
sales_ot = []
sales_gl = []


urlhead = 'http://www.vgchartz.com/gamedb/?page='
urltail = '&console=&region=All&developer=&publisher=&genre=&boxart=Both&ownership=Both'
urltail += '&results=1000&order=Sales&showtotalsales=0&showtotalsales=1&showpublisher=0'
urltail += '&showpublisher=1&showvgchartzscore=0&shownasales=1&showdeveloper=1&showcriticscore=1'
urltail += '&showpalsales=0&showpalsales=1&showreleasedate=1&showuserscore=0&showjapansales=1'
urltail += '&showlastupdate=0&showothersales=1&showgenre=0&sort=GL'


# For-loop will allow for scraping of multiple pages
for page in range(1, 20):

    # Setting up extraction of table
    surl = urlhead + str(page) + urltail
    html_text = requests.get(surl).text
    soup = BeautifulSoup(html_text, 'lxml')
    chart = soup.find('div', id='generalBody').find('table')

    # Extracting data from the table
    for row in chart.find_all('tr')[3:]:
        try:
            col = row.find_all('td')

        # extract data into column data
            column_1 = col[0].string.strip()
            column_2 = col[2].find('a').string.strip()
            column_3 = col[3].find('img')['alt'].strip()
            column_4 = col[4].string.strip() #publisher
            column_5 = col[5].string.strip() #developer
            column_6 = col[6].string.strip() #Critic Score

            # Replace will remove non-numerical characters from columns for easier conversion
            column_7 = col[7].string.strip().replace("m","")
            column_8 = col[8].string.strip().replace("m","")
            column_9 = col[9].string.strip().replace("m","")
            column_10 = col[10].string.strip().replace("m","")
            column_11 = col[11].string.strip().replace("m","")
            column_12 = col[12].string.strip()

        # Add Data to columns
        # Adding data only if able to read all of the columns
            rank.append(column_1)
            gname.append(column_2)
            platform.append(column_3)
            publisher.append(column_4)
            developer.append(column_5)
            critic_score.append(column_6)
            sales_gl.append(column_7)
            sales_na.append(column_8)
            sales_eu.append(column_9)
            sales_jp.append(column_10)
            sales_ot.append(column_11)
            year.append(column_12)

            rec_count += 1

        except:
            print('Got Exception')
            continue

# Formatting columns for the database
columns = {'Game_Rank': rank, 'Name': gname, 'Platform': platform, 'Publisher': publisher, 'Developer': developer, 'Critic_Score': critic_score,
           'Global_Sales': sales_gl, 'NA_Sales': sales_na, 'EU_Sales': sales_eu, 'JP_Sales': sales_jp, 'Other_Sales': sales_ot, 'Release_Year':year}

print (rec_count)

df = pd.DataFrame(columns)

# Converts all string "N/A" values in columns to proper NaN values
df = df.replace("N/A", np.nan)

# Converting score column and sales columns to numeric columns
df[["Critic_Score", "Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]] = df[["Critic_Score", "Global_Sales", "NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].apply(pd.to_numeric)
print(df)
df = df[['Game_Rank', 'Name', 'Platform', 'Publisher','Developer', 'Critic_Score',
         'Global_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales','Release_Year'
         ]]

df = df[df['Platform'] != "Series"]
df = df[df['Platform'] != "All"]
df = df[df['Global_Sales'] > 1.0]
df = df.dropna(subset = ['Global_Sales'])
df["Game_Rank"] = np.arange(len(df)) + 1
df.index.name = None

df.to_csv("vgsales2021.csv", sep=",", encoding='utf-8', index=False)