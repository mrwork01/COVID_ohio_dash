import sqlite3
import pandas as pd

df = pd.read_csv('COVIDSummaryData.csv')

df = df[:-1]
df['Onset Date'] = pd.to_datetime(df['Onset Date'])

connection = sqlite3.connect('covid_oh.db')

cursor = connection.cursor()

create_table = '''CREATE TABLE IF NOT EXISTS cases(
			   ID INTEGER  PRIMARY KEY,
               county TEXT,
               sex TEXT,
               age_range TEXT,
               onset_date TEXT,
               case_count INTEGER,
               death_count INTEGER,
               hosp_count INTEGER);'''


for i in range(len(df)):
	insert_data = '''INSERT IF NOT EXISTS cases(ID,county,sex,age_range,onset_date,case_count,death_count,hosp_count) VALUES
				     ({},{},{},{},{},{},{},{});'''.format(df.index,
				     								   df['County'][i],
				     								   df['Sex'][i],
				     								   df['Age Range'][i],
				     								   df['Onset Date'][i],
				     								   df['Case Count'][i],
				     								   df['Death Count'][i],
				     								   df['Hospitalized Count'][i],)
	cursor.execute(insert_data)



#cursor.execute(create_table)





connection.commit()