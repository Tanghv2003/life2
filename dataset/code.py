# Import necessary libraries
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

%matplotlib inline

# Load the dataset
data = pd.read_csv('/kaggle/input/personal-key-indicators-of-heart-disease/2020/heart_2020_cleaned.csv' )

# Display the data shape
data.shape
data.info()

# Display the top 5 columns
data.head()

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
data.describe()
# Create box plots to check for outliers
numerical_cols = ['BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']

plt.figure(figsize=(15, 10))
for i, col in enumerate(numerical_cols,1):
    plt.subplot(2, 2, i)
    sns.boxplot(y=data[col], color='skyblue')
    plt.title(f'Box Plot for {col}', fontsize=14)

plt.tight_layout()
plt.show()

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

# Calculate heart disease counts
heart_disease_counts = data['HeartDisease'].value_counts()

# Calculate percentages
heart_disease_percentage = heart_disease_counts / heart_disease_counts.sum() * 100

# Plot the heart disease distribution as a pie chart
plt.figure(figsize=(8, 6))
plt.pie(heart_disease_percentage, labels=heart_disease_percentage.index, autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'red'])
plt.title('Heart Disease Percentage in the Dataset', fontsize=16)
plt.axis('equal')
plt.show()

# Display the heart disease counts and percentages
print(heart_disease_counts)
print(heart_disease_percentage)

# Calculate gender counts
gender_counts = data['Sex'].value_counts()

# Calculate percentages
gender_percentage = gender_counts / gender_counts.sum() * 100

# Plot the gender distribution as a pie chart
plt.figure(figsize=(8, 6))
plt.pie(gender_percentage, labels=gender_percentage.index, autopct='%1.1f%%', startangle=140, colors=['lightblue', 'lightcoral'])
plt.title('Gender Percentage in the Dataset', fontsize=16)
plt.axis('equal')
plt.show()

# Display the gender counts and percentages
print(gender_counts)
print(gender_percentage)

# Set the aesthetics for the plots
sns.set(style="whitegrid")

# Create a histogram for BMI
plt.figure(figsize=(10, 6))
sns.histplot(data['BMI'], bins=30, kde=True, color='blue', edgecolor='black')
plt.title('Distribution of BMI', fontsize=16)
plt.xlabel('BMI', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.show()

# Create a histogram for Sleep Time
plt.figure(figsize=(10, 6))
sns.histplot(data['SleepTime'], bins=30, kde=True, color='purple', edgecolor='black')
plt.title('Distribution of Sleep Time', fontsize=16)
plt.xlabel('Sleep Time (Hours)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(True)
plt.show()

# Create a figure with subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Mental Health Distribution
sns.histplot(data['MentalHealth'], bins=30, kde=True, color='orange', edgecolor='black', ax=axes[0])
axes[0].set_title('Distribution of Mental Health', fontsize=16)
axes[0].set_xlabel('Mental Health (Days)', fontsize=14)
axes[0].set_ylabel('Frequency', fontsize=14)

# Physical Health Distribution
sns.histplot(data['PhysicalHealth'], bins=30, kde=True, color='green', edgecolor='black', ax=axes[1])
axes[1].set_title('Distribution of Physical Health', fontsize=16)
axes[1].set_xlabel('Physical Health (Days)', fontsize=14)
axes[1].set_ylabel('Frequency', fontsize=14)

plt.tight_layout()
plt.show()
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
