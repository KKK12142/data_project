import requests
import re
import pandas as pd

#잔반량 데이터 전처리
def leftover_normalization(filename):
    year = filename.replace(".xlsx", '') #파일이름으로 년도를 가져온다...
    all_dfs = [] #모든 시트의 데이터를 저장할 리스트임
    all_sheets = pd.read_excel(filename, sheet_name=None)
    
    for sheet_name, df in all_sheets.items(): # all_sheets는 dict 형태임.. 지금 각 시트별로 돌면서 df를 만드는중...
        df = df.iloc[:-2]
        df = df.drop(index=range(0,8))
        df = df.drop(df.columns[[1,2,4,5,7,8,10,11,12,13]], axis=1)
        df['month'] = df['음식물폐기물 처리 관리대장'].str.split('월').str[0].str.zfill(2)
        df['day'] = df['음식물폐기물 처리 관리대장'].str.split('월').str[1].str.strip().str.replace('일', '').str.zfill(2)
        df['year'] = year
        #이 라인 질문하기...
        df = df[['year','month', 'day'] + [col for col in df if col not in ['year','month','day']]]
        df = df.drop(columns=['음식물폐기물 처리 관리대장'])
        df.columns = ['year','month','day', '조식', '중식', '석식']
        #위 데이터 프레임을 split 해서 새로운 data 프레임을 만든다.
        df_breakfast = df[['year','month','day', '조식']].rename(columns={'조식':'leftover'})
        df_breakfast['sc_code'] = 1

        df_lunch = df[['year','month','day', '중식']].rename(columns={'중식':'leftover'})
        df_lunch['sc_code'] = 2

        df_dinner = df[['year','month','day', '석식']].rename(columns={'석식':'leftover'})
        df_dinner['sc_code'] = 3

        final_df = pd.concat([df_breakfast, df_lunch, df_dinner], ignore_index=True)
        final_df = final_df[['year','month','day','sc_code','leftover']]
        final_df = final_df.dropna(subset=['month','day','leftover'])
        final_df = final_df.query("leftover != 0")

        all_dfs.append(final_df) #위에서만든 리스트에 데이터프레임 추가하기

    final_df = pd.concat(all_dfs, ignore_index=True) #concat() 이용해서 수직으로 df를 연결한다. 그 후 인덱스를 0부터 다시 시작함.
    final_df.to_excel(f'{year}_norm.xlsx', index=False)
    return final_df
#나이스 교육정보 개방포털 API호출하고 데이터 전처리
def get_meal_info(api_key, atpt_ofcdc_sc_code, sd_schul_code, mlsv_ymd=None, mlsv_from_ymd=None, mlsv_to_ymd=None):
    base_url = "https://open.neis.go.kr/hub/mealServiceDietInfo"
    #파라미터 설정
    params ={
        "KEY": api_key,
        "TYPE": "json",
        "pIndex": 1,
        'pSize': 1000,
        "ATPT_OFCDC_SC_CODE": atpt_ofcdc_sc_code,
        "SD_SCHUL_CODE": sd_schul_code
    }
    #API 호출 3번 호출해야함 sc_code = 1, 2, 3
    meal_infos = []
    for i in range(1, 4):
        params["MMEAL_SC_CODE"] = i
        response = requests.get(base_url, params=params)
        #결과 확인 및 반환
        if response.status_code == 200:
            rows = response.json().get("mealServiceDietInfo")[1].get("row")
            for row in rows:
                ddish_nm = row.get("DDISH_NM")
                year = row.get("MLSV_YMD")[:4]
                month = row.get("MLSV_YMD")[4:6].zfill(2)
                day = row.get("MLSV_YMD")[6:].zfill(2)
                sc_code = row.get("MMEAL_SC_CODE")
                # <br/> 태그를 ,로 대체
                ddish_nm = re.sub(r'<br/>', ',', ddish_nm)
                # 알레르기 숫자 제거
                ddish_nm = re.sub(r'[\d\.<>/]+', '', ddish_nm)
                # () 제거
                ddish_nm = re.sub(r'\([^)]*\)', '', ddish_nm)
                # 공백 제거
                ddish_nm = re.sub(r' ', '', ddish_nm)
                ddish_nm.strip()
                meal_info = [year, month, day,sc_code, ddish_nm]
                meal_infos.append(meal_info)
    # 최대 메뉴 개수 파악
    max_menu_count = max([len(data[4].split(',')) for data in meal_infos])
    menu_columns = ["Menu" + str(i+1) for i in range(max_menu_count)]
    # 열 이름 생성
    columns = ["year","month","day","sc_code"] + menu_columns
    
    # 데이터를 df로 변환
    expanded_data_list = []
    for data in meal_infos:
        menu_items = data[4].split(',')
        expanded_data = data[:4] + menu_items + ['']*(max_menu_count - len(menu_items))
        expanded_data_list.append(expanded_data)

    df = pd.DataFrame(expanded_data_list, columns=columns)

    df.to_excel('meal_infos.xlsx', index=False, engine='openpyxl')
    return df
#잔반량 데이터와 식단 데이터 병합하기
def merge_and_insert_values(df_leftover1, df_leftover2, df_meal):
    #계속 자료형 오류나서 다 str로 변경
    df_leftover1['year'] = df_leftover1['year'].astype(str)
    df_leftover1['month'] = df_leftover1['month'].astype(str)
    df_leftover1['day'] = df_leftover1['day'].astype(str)
    df_leftover1['sc_code'] = df_leftover1['sc_code'].astype(str)

    df_leftover2['year'] = df_leftover2['year'].astype(str)
    df_leftover2['month'] = df_leftover2['month'].astype(str)
    df_leftover2['day'] = df_leftover2['day'].astype(str)
    df_leftover2['sc_code'] = df_leftover2['sc_code'].astype(str)
    #2022_norm.xlsx 와 2023_norm.xlsx를 리스트형태로 만들어 수직으로 합치기
    temp = []
    temp.append(df_leftover1)
    temp.append(df_leftover2)
    df_leftover = pd.concat(temp, ignore_index=False)
    #meal_infos 도 str로 바꿔줌
    df_meal['year'] = df_meal['year'].astype(str)
    df_meal['month'] = df_meal['month'].astype(str)
    df_meal['day'] = df_meal['day'].astype(str)
    df_meal['sc_code'] = df_meal['sc_code'].astype(str)
    # 'year', 'month', 'day', 'sc_code'를 기준으로 병합

    merged_df = pd.merge(df_meal, df_leftover, on=['year', 'month', 'day', 'sc_code'], how='left')
    if 'leftover' in merged_df.columns:
        cols = merged_df.columns.tolist()
        cols.insert(cols.index('sc_code')+1, cols.pop(cols.index('leftover')))
        merged_df = merged_df[cols]
    
    return merged_df

#파라미터 값 설정
api_key = "0ac229e82ed14b288bd6ead6129a9cd6"
atpt_ofcdc_sc_code = "N10"
sd_schul_code = "8140192"
mlsv_from_ymd = "20220302"
mlsv_to_ymd = '20230925'
#API 호출
a = get_meal_info(api_key, atpt_ofcdc_sc_code, sd_schul_code, mlsv_from_ymd = mlsv_from_ymd, mlsv_to_ymd = mlsv_to_ymd)
#잔반데이터 전처리
df_leftover_1 = leftover_normalization('2022.xlsx')
df_leftover_2 = leftover_normalization('2023.xlsx')
#식단데이터, 잔반데이터 연월일에 맞춰 병합하고 엑셀로저장
df_final = merge_and_insert_values(df_leftover_1, df_leftover_2, a)
df_final.to_excel('result.xlsx', index=False)
