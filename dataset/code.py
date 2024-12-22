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


# Models
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb

# Load the dataset
data = pd.read_csv('heart_2020_cleaned.csv' )
print(data.info())
print(data.head())

#clean data
# Retrieve Columns name
columns_df = list(data.columns.values)

# Display all unique values of each column in the dataframe
for column in columns_df:
    print(column, ':', str(data[column].unique()))

# Display the number of missing values
data.isnull().sum()
# Display the number of duplicates
print(f"Number of duplicates found: {data.duplicated().sum()}")
# Remove duplicates
data.drop_duplicates(inplace= True)
# Display Data shape after removing duplicates
data.shape
# Show description numeric Values
print(data.describe())

# Remove outliers for SleepTime as they are unrealistic

# Calculate Q1 and Q3
Q1 = data['SleepTime'].quantile(0.25)
Q3 = data['SleepTime'].quantile(0.75)
IQR = Q3 - Q1

# Define the non-outliers ranges
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Identify outliers
outliers = data[(data['SleepTime'] < lower_bound) | (data['SleepTime'] > upper_bound)]

# Remove outliers
data = data[(data['SleepTime'] >= lower_bound) & (data['SleepTime'] <= upper_bound)]

# Display the number of outliers removed
num_outliers_removed = outliers.shape[0]
print(f"Number of outliers removed: {num_outliers_removed}")

# Display the shape of the cleaned dataset

print("Cleaned Dataset Shape:", data.shape)

# Copy the original dataset
encoded_data = data.copy()

# Binary Columns
binary_columns = ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking','Sex', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']

# Apply label encoding
binary_encoder =  LabelEncoder()
for col in binary_columns:
    encoded_data[col] = binary_encoder.fit_transform(encoded_data[col])
encoded_data.head()

# Ordinal Columns
ordinal_columns = ['GenHealth', 'AgeCategory' ]

# Order for ordinal columns
GenHealth = ['Poor', 'Fair', 'Good', 'Very good', 'Excellent']
AgeCategory =['18-24', '25-29', '30-34', '35-39', '40-44', '45-49','50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']


# Apply ordinal encoding
ordinal_encoder = OrdinalEncoder(categories=[GenHealth, AgeCategory])
encoded_data[ordinal_columns] = ordinal_encoder.fit_transform(encoded_data[ordinal_columns])
print(encoded_data.head())

# Nominal columns
nominal_columns = ['Race', 'Diabetic']

# Apply OneHot encoding
encoded_data = pd.get_dummies(encoded_data, columns=nominal_columns).astype(int)
print(encoded_data.head())

# Define features (X) and target (y)
X = encoded_data.drop('HeartDisease', axis=1)
y = encoded_data['HeartDisease']

print("Features (X):")
print(X.head())
X.to_csv('features.csv', index=False)

print("\nTarget (y):")
print(y.head())
# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale the features
scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Resampling methods
oversampler = RandomOverSampler(random_state=42)
undersampler = RandomUnderSampler(random_state=42)
smote_sampler = SMOTE(random_state=42)

# Apply oversampling
X_train_oversampled, y_train_oversampled = oversampler.fit_resample(X_train_scaled, y_train)

# Apply undersampling
X_train_undersampled, y_train_undersampled = undersampler.fit_resample(X_train_scaled, y_train)

# Apply SMOTE
X_train_smote, y_train_smote = smote_sampler.fit_resample(X_train_scaled, y_train)

# Check the distribution of classes after resampling
print("Original training set class distribution:\n", y_train.value_counts())
print("\nOversampled training set class distribution:\n", pd.Series(y_train_oversampled).value_counts())
print("\nUndersampled training set class distribution:\n", pd.Series(y_train_undersampled).value_counts())
print("\nSMOTE training set class distribution:\n", pd.Series(y_train_smote).value_counts())

# Initialize the GradientBoostingClassifier model
# model = LogisticRegression()
# model = DecisionTreeClassifier()
# model = RandomForestClassifier()
# model = KNeighborsClassifier()
model = GradientBoostingClassifier()
# model = xgb.XGBClassifier()
# model =  AdaBoostClassifier()

# Dictionary to store results
results = {}

# Training and evaluating with oversampling
model.fit(X_train_oversampled, y_train_oversampled)
y_pred_oversample = model.predict(X_test_scaled)
results['Oversampling'] = {
    'Accuracy': accuracy_score(y_test, y_pred_oversample),
    'Classification Report': classification_report(y_test, y_pred_oversample)
}

# Training and evaluating with undersampling
model.fit(X_train_undersampled, y_train_undersampled)
y_pred_undersample = model.predict(X_test_scaled)
results['Undersampling'] = {
    'Accuracy': accuracy_score(y_test, y_pred_undersample),
    'Classification Report': classification_report(y_test, y_pred_undersample)
}

# Training and evaluating with SMOTE
model.fit(X_train_smote, y_train_smote)
y_pred_smote = model.predict(X_test_scaled)
results['SMOTE'] = {
    'Accuracy': accuracy_score(y_test, y_pred_smote),
    'Classification Report': classification_report(y_test, y_pred_smote)
}

# Step 5: Display the results for each resampling method
for method, metrics in results.items():
    print(f"Results for {model}:")
    print(f"Results for {method}:")
    print(f"Accuracy: {metrics['Accuracy']}")
    print(f"Classification Report:\n{metrics['Classification Report']}\n")





# Save the evaluation metrics for all models
model_results = {}

# Build Logistic Regression model
model = LogisticRegression(random_state=42)
model.fit(X_train_undersampled, y_train_undersampled)

# Make predictions
y_pred = model.predict(X_test_scaled)
y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

# Evaluation Metrics
accuracy = accuracy_score(y_test, y_pred)
C_report = classification_report(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred_proba)

# Specificity
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
specificity = tn / (tn + fp)

# Print Evaluation Metrics
print(f"Model: Logistic Regression")
print(f"Accuracy: {accuracy:.2f}")
print(f"Classification Report:\n{C_report}\n")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"Specificity: {specificity:.2f}")
print(f"F1 Score: {f1:.2f}")
print(f"ROC AUC: {roc_auc:.2f}")


# Store evaluation metrics in dictionary
model_results['Logistic Regression'] = {
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'Specificity': specificity,
    'F1 Score': f1,
    'ROC AUC': roc_auc
}

# Confusion Matrix Visualization
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

# ROC Curve and AUC Visualization
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random Guessing")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel("False Positive Rate (1 - Specificity)")
plt.ylabel("True Positive Rate (Recall)")
plt.title("Receiver Operating Characteristic (ROC) Curve")
plt.legend(loc="lower right")
plt.show()




data = pd.read_csv('features.csv')
# Giả sử dữ liệu đã được chuẩn hóa trước khi huấn luyện mô hình. Nếu không, bạn cần chuẩn hóa mẫu này.
# Trích xuất dòng đầu tiên từ tập CSV (mẫu đầu tiên)
new_sample = data.iloc[0].values  # Loại bỏ cột mục tiêu nếu có (thay 'target_column' bằng tên cột mục tiêu)

# Nếu bạn đã chuẩn hóa dữ liệu huấn luyện, bạn cần sử dụng cùng một chuẩn hóa cho mẫu này
# Ví dụ: nếu bạn đã sử dụng StandardScaler
new_sample_scaled = scaler.transform([new_sample])  # Giả sử 'scaler' là đối tượng StandardScaler đã được huấn luyện

# Dự đoán nhãn cho mẫu mới
y_pred_new = model.predict(new_sample_scaled)  # Dự đoán nhãn
y_pred_proba_new = model.predict_proba(new_sample_scaled)[:, 1]  # Dự đoán xác suất cho lớp 1

# In kết quả dự đoán
print("Dự đoán nhãn cho mẫu đầu tiên:", y_pred_new)
print("Xác suất của lớp 1 cho mẫu đầu tiên:", y_pred_proba_new)