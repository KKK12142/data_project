import pandas as pd
from joblib import load

# 저장된 원-핫 인코딩된 열의 목록 로딩
encoded_columns = load('encoded_columns.joblib')

loaded_model = load("best_model.joblib")
# 학습 데이터셋의 모든 원-핫 인코딩된 열을 기반으로 new_data의 기본 틀을 생성
default_data = {col: [0] for col in encoded_columns}

# 주어진 메뉴 값들
given_menus = {
    'Menu1': '보리밥',
    'Menu2': '짬뽕순두부찌개',
    'Menu3': '불닭팽이버섯',
    'Menu4': '달다리장각오븐구이',
    'Menu5': '배추김치',
    'Menu6': '해물전'
}
#보리밥	얼갈이된장국	돈육고추장오븐구이	새우까스머스타드	배추김치


# 주어진 메뉴 값만 1로 설정
for menu_col, menu_val in given_menus.items():
    col_name = f"{menu_col}_{menu_val}"
    if col_name in default_data:
        default_data[col_name] = [1]

# sc_code 값 설정 조식 = 1, 중식 = 2, 석식 = 3
default_data['sc_code'] = [2]

new_data_df = pd.DataFrame(default_data)

# 예측
predicted_leftover = loaded_model.predict(new_data_df)

print(f"Predicted Leftover: {predicted_leftover[0]}")