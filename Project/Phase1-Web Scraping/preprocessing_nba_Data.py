import pandas as pd
import glob
from dateutil import parser
from datetime import datetime


#----------------------------------Combination---------------------------------------
# all=glob.glob('D:/Quera/Week7/Roster_Table/raw_data_all/2024/*.csv')
# df_combined_2020=pd.concat([pd.read_csv(a) for a in all], ignore_index=True)
# df_combined_2020.to_csv('roster_2024.csv', index=False)

#----------------------------------Combination---------------------------------------
# all=glob.glob('D:/Quera/Week7/roster_updated/*.csv')
# df_combined_2020=pd.concat([pd.read_csv(a) for a in all], ignore_index=True)
# df_combined_2020.to_csv('Roster_Table_concated.csv', index=False)

#--------------------------------------------edit Column -----------------------------
# df = pd.read_csv('D:/Quera/Week7/Roster_Table/Roster_Table_Final.csv')
# # df.rename(columns={'year': 'season'}, inplace=True)
# # df['season'] = df['season'].apply(lambda x: f"{int(x)-1}_{x}")

# # print(df.head())
# df.to_csv('Roster_Table_Final.csv', index=False)

#---------------------------------------------Age---------------------------------------

# df = pd.read_csv('D:\Quera\Week7\ALL_TEAMS_ROSTER.csv')
# def calculate_age(date_str):
#     try:
#         birth_date = parser.parse(date_str)
#         today = datetime.now()
#         age = today.year - birth_date.year
        
#         if (today.month, today.day) < (birth_date.month, birth_date.day):
#             age -= 1
            
#         return age
#     except:
#         return None

# df['age'] = df['birth_date'].apply(calculate_age)

#---------------------------------Add column _ agility $ innate_ability ----------------
# df = pd.read_csv('D:/Quera/Week7/Roster_Table_Final_Age_Added.csv')

# df['height_cm'] = pd.to_numeric(df['height_cm'], errors='coerce')
# df['weight'] = pd.to_numeric(df['weight'], errors='coerce')
# df['experience'] = pd.to_numeric(df['experience'], errors='coerce')
# df['age'] = pd.to_numeric(df['age'], errors='coerce')

# df['agility'] = round(df['height_cm'] / df['weight'], 2)
# df['innate_ability'] = round(df['experience'] / df['age'], 2)


# df.to_csv('Roster_Table_FINAL.csv', index=False)

#-----------------------------------------------missing_value_checking-----------------
df = pd.read_csv('D:\Quera\Week7\Roster_Table\Roster_Final.csv')
for i in df.columns:
    print(i)
    print(df[i].isna().sum())
    print('')

# df['innate_ability'] = df['innate_ability'].fillna(0)
# null_cells = df.index[df['experience'].isna()].tolist()
# print(f"rows of null for experience : {null_cells}")

# df.dropna(subset=['player_name', 'salary'], inplace=True)

#----------------------------- convert weight to kg & update agility column -----------------
# df['weight_kg'] = df['weight'].apply(lambda x: x * 0.453592)
# df['weight_kg'] = df['weight_kg'].round(0)
# df['agility'] = df['height_cm'] / df['weight_kg']
# df['agility'] = df['agility'].round(2)
# df.to_csv('Roster.csv', index=False)