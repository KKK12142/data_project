import matplotlib.pyplot as plt
import pandas as pd

#데이터 시각화
def show_graph(filename):
    #엑셀파일 읽어오기
    df = pd.read_excel(f'{filename}', engine='openpyxl')
    #필터 설정하기
    filtered_df = df[(df['sc_code']==2) & (df['year']==2023) & (df['month'] == 7)]
    #색 조건 만들기
    colors = ['red' if value > 7.5 else 'blue' for value in filtered_df['leftover']]
    #그래프 그리기
    plt.bar(filtered_df['day'], filtered_df['leftover'], color = colors)
    plt.xlabel('day')
    plt.ylabel('leftover')
    plt.title('july')
    plt.grid(True)
    plt.xticks(range(min(filtered_df['day']), max(filtered_df['day']) + 1, 1))
    plt.yticks([i/2 for i in range(int(2*min(filtered_df['leftover'])), int(2*max(filtered_df['leftover']) + 1))])
    plt.show()

show_graph('result.xlsx')