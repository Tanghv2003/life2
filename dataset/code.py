import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import classification_report, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, roc_curve, confusion_matrix, ConfusionMatrixDisplay

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb


data = pd.read_csv('heart_2020_cleaned.csv' )
print(data.info())  
print(data.head())


columns_df = list(data.columns.values)


for column in columns_df:
    print(column, ':', str(data[column].unique()))


data.isnull().sum()


print(f"Số lượng bản ghi trùng lặp: {data.duplicated().sum()}")
data.drop_duplicates(inplace=True)

data.shape

print(data.describe())

Q1 = data['SleepTime'].quantile(0.25)
Q3 = data['SleepTime'].quantile(0.75)
IQR = Q3 - Q1


lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = data[(data['SleepTime'] < lower_bound) | (data['SleepTime'] > upper_bound)]
data = data[(data['SleepTime'] >= lower_bound) & (data['SleepTime'] <= upper_bound)]
num_outliers_removed = outliers.shape[0]
print(f"Số lượng dl không hợp lệ đã bị xóa: {num_outliers_removed}")
print("Kích thước dữ liệu sau khi làm sạch:", data.shape)

encoded_data = data.copy()


binary_columns = ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking', 'Sex', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']

# Áp dụng mã hóa nhãn cho các cột nhị phân
binary_encoder = LabelEncoder()
for col in binary_columns:
    encoded_data[col] = binary_encoder.fit_transform(encoded_data[col])
encoded_data.head()
ordinal_columns = ['GenHealth', 'AgeCategory']
GenHealth = ['Poor', 'Fair', 'Good', 'Very good', 'Excellent']
AgeCategory = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']

# Áp dụng mã hóa thứ tự cho các cột thứ tự
ordinal_encoder = OrdinalEncoder(categories=[GenHealth, AgeCategory])
encoded_data[ordinal_columns] = ordinal_encoder.fit_transform(encoded_data[ordinal_columns])
print(encoded_data.head())

# Các cột danh mục
nominal_columns = ['Race', 'Diabetic']

encoded_data = pd.get_dummies(encoded_data, columns=nominal_columns).astype(int)
print(encoded_data.head())


X = encoded_data.drop('HeartDisease', axis=1)
y = encoded_data['HeartDisease']

print("Các đặc trưng (X):")
print(X.head())
X.to_csv('features.csv', index=False)

print("\nNhãn (y):")
print(y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

oversampler = RandomOverSampler(random_state=42)
undersampler = RandomUnderSampler(random_state=42)
smote_sampler = SMOTE(random_state=42)
X_train_oversampled, y_train_oversampled = oversampler.fit_resample(X_train_scaled, y_train)
X_train_undersampled, y_train_undersampled = undersampler.fit_resample(X_train_scaled, y_train)
# SMOTE
X_train_smote, y_train_smote = smote_sampler.fit_resample(X_train_scaled, y_train)

# Kiểm tra phân phối lớp sau khi lấy mẫu lại
print("Phân phối lớp trong bộ huấn luyện ban đầu:\n", y_train.value_counts())
print("\nPhân phối lớp trong bộ huấn luyện sau khi quá cân:\n", pd.Series(y_train_oversampled).value_counts())
print("\nPhân phối lớp trong bộ huấn luyện sau khi thiếu cân:\n", pd.Series(y_train_undersampled).value_counts())
print("\nPhân phối lớp trong bộ huấn luyện sau khi sử dụng SMOTE:\n", pd.Series(y_train_smote).value_counts())

# Khởi tạo mô hình GradientBoostingClassifier
# model = LogisticRegression()
# model = DecisionTreeClassifier()
# model = RandomForestClassifier()
# model = KNeighborsClassifier()
model = GradientBoostingClassifier()
# model = xgb.XGBClassifier()
# model =  AdaBoostClassifier()


results = {}

# Huấn luyện và đánh giá với phương pháp quá cân
model.fit(X_train_oversampled, y_train_oversampled)
y_pred_oversample = model.predict(X_test_scaled)
results['Oversampling'] = {
    'Accuracy': accuracy_score(y_test, y_pred_oversample),
    'Classification Report': classification_report(y_test, y_pred_oversample)
}

# Huấn luyện và đánh giá với phương pháp thiếu cân
model.fit(X_train_undersampled, y_train_undersampled)
y_pred_undersample = model.predict(X_test_scaled)
results['Undersampling'] = {
    'Accuracy': accuracy_score(y_test, y_pred_undersample),
    'Classification Report': classification_report(y_test, y_pred_undersample)
}

# Huấn luyện và đánh giá với phương pháp SMOTE
model.fit(X_train_smote, y_train_smote)
y_pred_smote = model.predict(X_test_scaled)
results['SMOTE'] = {
    'Accuracy': accuracy_score(y_test, y_pred_smote),
    'Classification Report': classification_report(y_test, y_pred_smote)
}

# Hiển thị kết quả cho từng phương pháp lấy mẫu lại
for method, metrics in results.items():
    print(f"Kết quả cho {model}:")
    print(f"Kết quả cho {method}:")
    print(f"Độ chính xác: {metrics['Accuracy']}")
    print(f"Báo cáo phân loại:\n{metrics['Classification Report']}\n")

# Lưu trữ các chỉ số đánh giá cho tất cả các mô hình
model_results = {}

# Xây dựng mô hình Logistic Regression
model = LogisticRegression(random_state=42)
model.fit(X_train_undersampled, y_train_undersampled)


y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]


accuracy = accuracy_score(y_test, y_pred)
C_report = classification_report(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)


tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
specificity = tn / (tn + fp)


print(f"Mô hình: Logistic Regression")
print(f"Độ chính xác: {accuracy:.2f}")
# print(f"Báo cáo phân loại:\n{C_report}\n")
# print(f"Precision: {precision:.2f}")
# print(f"Recall: {recall:.2f}")
# print(f"Specificity: {specificity:.2f}")
# print(f"F1 Score: {f1:.2f}")
# print(f"ROC AUC: {roc_auc:.2f}")

model_results['Logistic Regression'] = {
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'Specificity': specificity,
    'F1 Score': f1,
    'ROC AUC': roc_auc
}

# # Vẽ ma trận nhầm lẫn
# cm = confusion_matrix(y_test, y_pred)
# sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
# plt.title("Ma trận nhầm lẫn")
# plt.xlabel("Dự đoán")
# plt.ylabel("Thực tế")
# plt.show()

# # Vẽ đồ thị ROC và AUC
# fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

# plt.figure(figsize=(8, 6))
# plt.plot(fpr, tpr, label=f"Đường cong ROC (AUC = {roc_auc:.2f})")
# plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Dự đoán ngẫu nhiên")
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel("Tỷ lệ dương tính giả (1 - Specificity)")
# plt.ylabel("Tỷ lệ dương tính thật (Recall)")
# plt.title("Đường cong đặc trưng nhận diện (ROC)")
# plt.legend(loc="lower right")
# plt.show()


data = pd.read_csv('test.csv')



correct_predictions = 0
total_predictions = 0


for i in range(1, 20):  
    
    actual_value = data.iloc[i]['HeartDisease']  
    new_sample = data.iloc[i].drop('HeartDisease').values  
    
    
    new_sample_scaled = scaler.transform([new_sample])  
    
    
    y_pred_new = model.predict(new_sample_scaled)[0]  
    y_pred_proba_new = model.predict_proba(new_sample_scaled)[:, 1][0]  

   
    total_predictions += 1
    if y_pred_new == actual_value:
        correct_predictions += 1

    
    print(f"Dòng {i}:")
    print("Giá trị thực tế:", actual_value)
    print("Dự đoán:", y_pred_new)
    print("-" * 30)

accuracy = correct_predictions / total_predictions
print(f"Xác suất dự đoán đúng: {accuracy:.2%}")