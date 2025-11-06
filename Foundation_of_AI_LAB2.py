import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import matplotlib.pyplot as plt

try:
    df = pd.read_csv('adult.csv')
except FileNotFoundError:
    print("Error: 'adult.csv' not found. Please ensure the file is in the correct directory.")
    exit()

df = df.replace('?', np.nan)
for col in ['workclass', 'occupation', 'native.country']:
    df[col].fillna(df[col].mode()[0], inplace=True)

X = df.drop('income', axis=1)
y = df['income'].apply(lambda x: 1 if x == '>50K' else 0)

categorical_features = X.select_dtypes(include=['object']).columns
numerical_features = X.select_dtypes(include=['int64']).columns

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ],
    remainder='passthrough'
)

X_processed = preprocessor.fit_transform(X)

feature_names = list(numerical_features)
ohe_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
feature_names.extend(ohe_feature_names)

X_train, X_test, y_train, y_test = train_test_split(
    X_processed, y, test_size=0.2, random_state=42, stratify=y
)

INPUT_DIM = X_train.shape[1]
OUTPUT_DIM = 1

def create_model_1(input_dim):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(input_dim,)),
        Dense(OUTPUT_DIM, activation='sigmoid')
    ], name='MLP_Model_1_Simple')
    return model

def create_model_2(input_dim):
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dropout(0.3),
        Dense(OUTPUT_DIM, activation='sigmoid')
    ], name='MLP_Model_2_Deeper')
    return model

def create_model_3(input_dim):
    model = Sequential([
        Dense(256, activation='relu', input_shape=(input_dim,)),
        Dense(128, activation='relu'),
        Dense(OUTPUT_DIM, activation='sigmoid')
    ], name='MLP_Model_3_Wider')
    return model

models = [
    create_model_1(INPUT_DIM),
    create_model_2(INPUT_DIM),
    create_model_3(INPUT_DIM)
]

EPOCHS = 50
BATCH_SIZE = 32
results = {}

for model in models:
    print(f"\n--- Training {model.name} ---")

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    history = model.fit(
        X_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.1,
        verbose=0
    )

    y_pred_proba = model.predict(X_test, verbose=0)
    y_pred_class =