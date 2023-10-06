import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("price.xlsx")
df['year'] = df['요금년월'].str.split('-').str[0]
df['month'] = df['요금년월'].str.split('-').str[1]
df = df.drop(columns=['요금년월'])
df = df[['year', 'month', '사용량(kWh)', '수납금액']]
df = df.sort_values(by=['year', 'month'], ascending=[True, True])

years = df['year'].unique() #중복되는 값을 제거하고 한개씩만 남김

#새로운 subset이라는 데이터프레임을 만듬
for year in years:
    subset = df[df['year'] == str(year)]
    if year == '2020':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='y', label='2020', marker='o')
    elif year == '2019':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='m', label='2019', marker='o')
    elif year == '2018':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='k', label='2018', marker='o')
    elif year == '2017':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='c', label='2017', marker='o')
    elif year == '2021':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='red', label='2021', marker='o')
    elif year == '2022':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='blue', label='2022', marker='o')
    elif year == '2023':
        plt.plot(subset['month'], subset['사용량(kWh)'], color='green', label='2023', marker='o')

plt.legend() #범례
plt.xlabel('Month') #x축 제목
plt.ylabel('Electrical Energy') #y축 제목
plt.title('Energy used per month') #제목
plt.show() 

