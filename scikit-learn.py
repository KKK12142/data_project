import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV
from joblib import dump

data = pd.read_csv('result.csv')
data.fillna("없음", inplace=True)
data['leftover'] = pd.to_numeric(data['leftover'], errors='coerce')  # '없음'을 NaN으로 변환
data['leftover'].fillna(data['leftover'].mean(), inplace=True)  # NaN 값을 평균값으로 대체
data_encoded = pd.get_dummies(data, columns=[col for col in data.columns if 'Menu' in col])
from sklearn.model_selection import train_test_split

X = data_encoded.drop('leftover', axis=1)
y = data_encoded['leftover']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
from sklearn.metrics import mean_absolute_error, mean_squared_error

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")

from sklearn.model_selection import GridSearchCV

parameters = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(RandomForestRegressor(random_state=42), parameters, cv=5, scoring='neg_mean_absolute_error')
grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)
mae_best = mean_absolute_error(y_test, y_pred_best)
mse_best = mean_squared_error(y_test, y_pred_best)

print(f"Best Model - Mean Absolute Error: {mae_best}")
print(f"Best Model - Mean Squared Error: {mse_best}")

dump(best_model, 'best_model.joblib')
# 원-핫 인코딩된 열의 목록 저장
dump(X_train.columns, 'encoded_columns.joblib')
