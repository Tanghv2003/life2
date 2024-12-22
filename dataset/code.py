# Import necessary libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score
from sklearn.metrics import f1_score, roc_auc_score, confusion_matrix
from sklearn.linear_model import LogisticRegression


# Load and preprocess the dataset
def load_and_preprocess_data(file_path):
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Remove duplicates
    data.drop_duplicates(inplace=True)
    
    # Handle outliers in SleepTime
    Q1 = data['SleepTime'].quantile(0.25)
    Q3 = data['SleepTime'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    data = data[(data['SleepTime'] >= lower_bound) & (data['SleepTime'] <= upper_bound)]
    
    return data


# Encode the features
def encode_features(data):
    encoded_data = data.copy()
    
    # Binary encoding
    binary_columns = ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking',
                     'Sex', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer']
    binary_encoder = LabelEncoder()
    for col in binary_columns:
        encoded_data[col] = binary_encoder.fit_transform(encoded_data[col])
    
    # Ordinal encoding
    ordinal_columns = ['GenHealth', 'AgeCategory']
    GenHealth = ['Poor', 'Fair', 'Good', 'Very good', 'Excellent']
    AgeCategory = ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
                  '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older']
    
    ordinal_encoder = OrdinalEncoder(categories=[GenHealth, AgeCategory])
    encoded_data[ordinal_columns] = ordinal_encoder.fit_transform(encoded_data[ordinal_columns])
    
    # One-hot encoding
    nominal_columns = ['Race', 'Diabetic']
    encoded_data = pd.get_dummies(encoded_data, columns=nominal_columns)
    
    return encoded_data


# Prepare data for modeling
def prepare_data_for_modeling(encoded_data):
    X = encoded_data.drop('HeartDisease', axis=1)
    y = encoded_data['HeartDisease']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler


# Apply resampling methods
def apply_resampling(X_train_scaled, y_train):
    # Oversampling
    oversampler = RandomOverSampler(random_state=42)
    X_train_over, y_train_over = oversampler.fit_resample(X_train_scaled, y_train)
    
    # Undersampling
    undersampler = RandomUnderSampler(random_state=42)
    X_train_under, y_train_under = undersampler.fit_resample(X_train_scaled, y_train)
    
    # SMOTE
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train_scaled, y_train)
    
    return {
        'oversampling': (X_train_over, y_train_over),
        'undersampling': (X_train_under, y_train_under),
        'smote': (X_train_smote, y_train_smote)
    }


# Train and evaluate model
def train_and_evaluate_model(model, resampled_data, X_test_scaled, y_test):
    results = {}
    
    for method, (X_train_resampled, y_train_resampled) in resampled_data.items():
        # Train model
        model.fit(X_train_resampled, y_train_resampled)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        
        # Calculate specificity
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        specificity = tn / (tn + fp)
        
        results[method] = {
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'Specificity': specificity,
            'F1 Score': f1,
            'ROC AUC': roc_auc,
            'Classification Report': classification_report(y_test, y_pred)
        }
    
    return results


# Predict Heart Disease
def predict_heart_disease(model, scaler, input_data, encoder_info):
    """
    Dự đoán bệnh tim từ dữ liệu mới.
    
    Args:
        model: Mô hình Logistic Regression đã huấn luyện.
        scaler: Bộ chuẩn hóa StandardScaler đã huấn luyện.
        input_data: Dictionary chứa thông tin người dùng cần chuẩn đoán.
        encoder_info: Thông tin encoder (LabelEncoder, OrdinalEncoder) cho các cột.

    Returns:
        Dự đoán kết quả và xác suất mắc bệnh tim.
    """
    # Chuyển dictionary thành DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Mã hóa nhị phân
    binary_columns = encoder_info['binary_columns']
    binary_encoder = encoder_info['binary_encoder']
    for col in binary_columns:
        input_df[col] = binary_encoder[col].transform(input_df[col])
    
    # Mã hóa thứ tự
    ordinal_columns = encoder_info['ordinal_columns']
    ordinal_encoder = encoder_info['ordinal_encoder']
    input_df[ordinal_columns] = ordinal_encoder.transform(input_df[ordinal_columns])
    
    # One-hot encoding
    nominal_columns = encoder_info['nominal_columns']
    for col in nominal_columns:
        one_hot = pd.get_dummies(input_df[col], prefix=col)
        input_df = pd.concat([input_df, one_hot], axis=1)
        input_df.drop(columns=[col], inplace=True)
    
    # Chuẩn hóa dữ liệu
    input_scaled = scaler.transform(input_df)
    
    # Dự đoán
    prediction = model.predict(input_scaled)[0]
    prediction_proba = model.predict_proba(input_scaled)[0, 1]
    
    return prediction, prediction_proba


# Main execution function
def run_heart_disease_prediction(file_path, model):
    # Load and preprocess data
    data = load_and_preprocess_data(file_path)
    
    # Encode features
    encoded_data = encode_features(data)
    
    # Prepare data for modeling
    X_train_scaled, X_test_scaled, y_train, y_test, scaler = prepare_data_for_modeling(encoded_data)
    
    # Apply resampling methods
    resampled_data = apply_resampling(X_train_scaled, y_train)
    
    # Train and evaluate model
    results = train_and_evaluate_model(model, resampled_data, X_test_scaled, y_test)
    
    return results, scaler, encoded_data


# Example usage:
if __name__ == "__main__":
    # Initialize model
    model = LogisticRegression(random_state=42)
    
    # Run prediction pipeline
    file_path = 'heart_2020_cleaned.csv'  # Path to your dataset
    results, scaler, encoded_data = run_heart_disease_prediction(file_path, model)
    
    # Print results
    for method, metrics in results.items():
        print(f"\nResults for {method}:")
        print(f"Accuracy: {metrics['Accuracy']:.3f}")
        print(f"Precision: {metrics['Precision']:.3f}")
        print(f"Recall: {metrics['Recall']:.3f}")
        print(f"Specificity: {metrics['Specificity']:.3f}")
        print(f"F1 Score: {metrics['F1 Score']:.3f}")
        print(f"ROC AUC: {metrics['ROC AUC']:.3f}")
        print("\nClassification Report:")
        print(metrics['Classification Report'])

    # Thông tin cho encoder
    encoder_info = {
        'binary_columns': ['HeartDisease', 'Smoking', 'AlcoholDrinking', 'Stroke', 'DiffWalking',
                           'Sex', 'PhysicalActivity', 'Asthma', 'KidneyDisease', 'SkinCancer'],
        'binary_encoder': {col: LabelEncoder().fit(encoded_data[col]) for col in ['HeartDisease', 'Smoking', 'AlcoholDrinking', 
                                                                         'Stroke', 'DiffWalking', 'Sex', 'PhysicalActivity',
                                                                         'Asthma', 'KidneyDisease', 'SkinCancer']},
        'ordinal_columns': ['GenHealth', 'AgeCategory'],
        'ordinal_encoder': OrdinalEncoder(categories=[['Poor', 'Fair', 'Good', 'Very good', 'Excellent'],
                                                      ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
                                                       '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', 
                                                       '80 or older']]).fit(encoded_data[['GenHealth', 'AgeCategory']]),
        'nominal_columns': ['Race', 'Diabetic']
    }
    
    # Dữ liệu người dùng cần dự đoán
    new_data = {
        'Smoking': 'Yes',
        'AlcoholDrinking': 'No',
        'Stroke': 'No',
        'DiffWalking': 'No',
        'Sex': 'Female',
        'AgeCategory': '50-54',
        'Race': 'White',
        'Diabetic': 'Yes',
        'PhysicalActivity': 'Yes',
        'GenHealth': 'Good',
        'SleepTime': 7,
        'Asthma': 'No',
        'KidneyDisease': 'No',
        'SkinCancer': 'No'
    }
    
    # Dự đoán
    prediction, prediction_proba = predict_heart_disease(model, scaler, new_data, encoder_info)
    print(f"Dự đoán: {'Mắc bệnh tim' if prediction == 1 else 'Không mắc bệnh tim'}")
    print(f"Xác suất mắc bệnh: {prediction_proba:.2f}")
