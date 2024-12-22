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

# Load the dataset
data = pd.read_csv('heart_2020_cleaned.csv' )

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

# Define the age order
age_order = ['18-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80 or older']

# Create a count plot for Heart Disease by Age Category
plt.figure(figsize=(12, 6))
sns.countplot(x='AgeCategory', hue='HeartDisease', data=data, order=age_order)
plt.title('Heart Disease Count by Age Category', fontsize=16)
plt.xlabel('Age Category', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend(title='Heart Disease', loc='upper right', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# Calculate the counts of each category
grouped_data = data.groupby(['Sex', 'HeartDisease']).size().reset_index(name='count')

# Calculate the percentage for each group
total_counts = grouped_data.groupby('Sex')['count'].transform('sum')
grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

# Set up the figure and axes
fig, axes = plt.subplots(1, 1, figsize=(10, 6))

# Create the bar plot with percentages
sns.barplot(ax=axes, x='Sex', y='percentage', hue='HeartDisease', data=grouped_data, palette='Set2')

# Customize the plot
axes.set_title('Heart Disease Percentage by Sex', fontsize=16)
axes.set_ylabel('Percentage (%)', fontsize=14)

# Set the legend
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles=handles, labels=['No Heart Disease', 'Heart Disease'], title='Heart Disease')

# Add percentages on top of the bars
for container in axes.containers:
    for bar in container:
        height = bar.get_height()
        axes.annotate(f'{height:.1f}%',
                      (bar.get_x() + bar.get_width() / 2, height),
                      ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()

# Calculate the counts of each category
grouped_data = data.groupby(['Smoking', 'HeartDisease']).size().reset_index(name='count')

# Calculate the percentage for each group
total_counts = grouped_data.groupby('Smoking')['count'].transform('sum')
grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

# Set up the figure and axes
fig, axes = plt.subplots(1, 1, figsize=(10, 6))

# Create the bar plot with percentages
sns.barplot(ax=axes, x='Smoking', y='percentage', hue='HeartDisease', data=grouped_data, palette='Set2')

# Customize the plot
axes.set_title('Heart Disease Percentage by Smoking Status', fontsize=16)
axes.set_ylabel('Percentage (%)', fontsize=14)

# Set the legend
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles=handles, labels=['No Heart Disease', 'Heart Disease'], title='Heart Disease')

# Add percentages on top of the bars
for container in axes.containers:
    for bar in container:
        height = bar.get_height()
        axes.annotate(f'{height:.1f}%',
                      (bar.get_x() + bar.get_width() / 2, height),
                      ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()

# Calculate the counts of each category
grouped_data = data.groupby(['AlcoholDrinking', 'HeartDisease']).size().reset_index(name='count')

# Calculate the percentage for each group
total_counts = grouped_data.groupby('AlcoholDrinking')['count'].transform('sum')
grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

# Set up the figure and axes
fig, axes = plt.subplots(1, 1, figsize=(10, 6))

# Create the bar plot with percentages
sns.barplot(ax=axes, x='AlcoholDrinking', y='percentage', hue='HeartDisease', data=grouped_data, palette='Set2')

# Step 5: Customize the plot
axes.set_title('Heart Disease Percentage by Alcohol Drinking Status', fontsize=16)
axes.set_ylabel('Percentage (%)', fontsize=14)

# Set the legend
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles=handles, labels=['No Heart Disease', 'Heart Disease'], title='Heart Disease')


# Add percentages on top of the bars
for container in axes.containers:
    for bar in container:
        height = bar.get_height()
        axes.annotate(f'{height:.1f}%',
                      (bar.get_x() + bar.get_width() / 2, height),
                      ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()
# Calculate the counts of each category
grouped_data = data.groupby(['PhysicalActivity', 'HeartDisease']).size().reset_index(name='count')

# Calculate the percentage for each group
total_counts = grouped_data.groupby('PhysicalActivity')['count'].transform('sum')
grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

# Set up the figure and axes
fig, axes = plt.subplots(1, 1, figsize=(10, 6))

# Create the count plot with percentages
sns.barplot(ax=axes, x='PhysicalActivity', y='percentage', hue='HeartDisease', data=grouped_data, palette='Set2')

# Customize the plot
axes.set_title('Heart Disease Percentage by Physical Activity', fontsize=16)
axes.set_ylabel('Percentage (%)', fontsize=14)

# Set the legend
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles=handles, labels=['No Heart Disease', 'Heart Disease'], title='Heart Disease')

# Add percentages on top of the bars
for container in axes.containers:
    for bar in container:
        height = bar.get_height()
        axes.annotate(f'{height:.1f}%',
                      (bar.get_x() + bar.get_width() / 2, height),
                      ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()

# Calculate the counts of each category
grouped_data = data.groupby(['GenHealth', 'HeartDisease']).size().reset_index(name='count')

# Calculate the percentage for each group
total_counts = grouped_data.groupby('GenHealth')['count'].transform('sum')
grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

# Sort the data by percentage
grouped_data = grouped_data.sort_values(by='percentage', ascending=False)

# Set up the figure and axes
fig, axes = plt.subplots(1, 1, figsize=(12, 6))

# Create the bar plot with percentages
sns.barplot(ax=axes, x='GenHealth', y='percentage', hue='HeartDisease', data=grouped_data, palette='Set2')

# Customize the plot
axes.set_title('Heart Disease Percentage by General Health', fontsize=16)
axes.set_ylabel('Percentage (%)', fontsize=14)

# Set the legend
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles=handles, labels=['No Heart Disease', 'Heart Disease'], title='Heart Disease')

# Add percentages on top of the bars
for container in axes.containers:
    for bar in container:
        height = bar.get_height()
        axes.annotate(f'{height:.1f}%',
                      (bar.get_x() + bar.get_width() / 2, height),
                      ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()

# Calculate the counts of each category
grouped_data = data.groupby(['Race', 'HeartDisease']).size().reset_index(name='count')

# Calculate the percentage for each group
total_counts = grouped_data.groupby('Race')['count'].transform('sum')
grouped_data['percentage'] = (grouped_data['count'] / total_counts) * 100

# Sort the data by percentage
grouped_data = grouped_data.sort_values(by='percentage', ascending=False)

# Set up the figure and axes
fig, axes = plt.subplots(1, 1, figsize=(12, 6))

# Create the bar plot with percentages, ordered by percentage
sns.barplot(ax=axes, x='Race', y='percentage', hue='HeartDisease', data=grouped_data, palette='Set2')

# Customize the plot
axes.set_title('Heart Disease Percentage by Race', fontsize=16)
axes.set_ylabel('Percentage (%)', fontsize=14)

# Set the legend
handles, labels = axes.get_legend_handles_labels()
axes.legend(handles=handles, labels=['No Heart Disease', 'Heart Disease'], title='Heart Disease' ,loc='center right')

# Add percentages on top of the bars
for container in axes.containers:
    for bar in container:
        height = bar.get_height()
        axes.annotate(f'{height:.1f}%',
                      (bar.get_x() + bar.get_width() / 2, height),
                      ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()

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
encoded_data.head()

# Nominal columns
nominal_columns = ['Race', 'Diabetic']

# Apply OneHot encoding
encoded_data = pd.get_dummies(encoded_data, columns=nominal_columns).astype(int)
encoded_data.head()

# Calculate the correlation matrix
correlation_matrix = encoded_data.corr()

# the correlation of each variable with 'HeartDisease'
heart_disease_correlation = correlation_matrix['HeartDisease'].sort_values(ascending=False)

heart_disease_correlation

# Create a mask to highlight correlations above 0.3 or below -0.3
mask = (correlation_matrix > 0.3) | (correlation_matrix < -0.3)

# Plotting the heatmap to visualize the correlation between variables
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, fmt=".2f", mask=~mask)
plt.title('Correlation Heatmap (Highlighting correlations > 0.3 or < -0.3)')
plt.show()

# Define features (X) and target (y)
X = encoded_data.drop('HeartDisease', axis=1)
y = encoded_data['HeartDisease']

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




#### hồi quy logistic
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