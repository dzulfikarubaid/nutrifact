import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from sklearn import preprocessing
import joblib
import pymysql
import json

# Mengganti nilai berikut sesuai dengan informasi koneksi MySQL Anda
def predict():
    host = "34.101.221.64"
    user = "root"
    password = "capstone-project-CH2-PS588"
    database = "capstone-project"

    # Membuat koneksi ke MySQL
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Membuat objek cursor
    cursor = conn.cursor()

    # Contoh eksekusi query
    query = "SELECT * FROM product"
    cursor.execute(query)

    # Mendapatkan hasil query
    results = cursor.fetchall()

    # Membuat DataFrame Pandas dari hasil query
    columns = [i[0] for i in cursor.description]
    df1 = pd.DataFrame(results, columns=columns)
    # Menampilkan DataFrame
    print(df1)

    # Koneksi dan kursor akan ditutup secara otomatis ketika keluar dari blok with
    cursor.close()
    conn.close()

    X = df1[['calories', 'protein', 'total_fat', 'total_carbohydrate']]
    loaded_model = joblib.load('svm_model_linear.joblib')

    X['protein'][0] = "0 g"
    X['protein'][21] = "0 g"

    X['calories'] = X['calories'].str.replace('[^0-9]', '', regex=True).astype('float64')
    X['protein'] = X['protein'].str.replace('[^0-9]', '', regex=True).astype('float64')

    X['total_fat'] = pd.to_numeric(X['total_fat'].str.replace('[^0-9.]', '', regex=True), errors='coerce')

    X['total_carbohydrate'] = X['total_carbohydrate'].str.replace('[^0-9]', '', regex=True).astype('float64')

    print(X)
    from sklearn.preprocessing import MinMaxScaler
    scalerBAD = MinMaxScaler(feature_range=(1, 10))
    X['calories'] = scalerBAD.fit_transform(X[['calories']])

    X['total_fat'] = scalerBAD.fit_transform(X[['total_fat']])


    X['total_carbohydrate'] = scalerBAD.fit_transform(X[['total_carbohydrate']])


    scalerGOOD = MinMaxScaler(feature_range=(1, 5))
    X['protein'] = scalerGOOD.fit_transform(X[['protein']])

    print("AFTER SCALE")
    print(X)
    index = 0
    # Prediksi dengan model SVM
    pred = pd.Series(loaded_model.predict(X))

    df1['nutrition_level'] = pred
    for i in range(0, len(df1)):
        if(df1['nutrition_level'][i] == 0):
            df1['nutrition_level'][i] = 'A'
        elif(df1['nutrition_level'][i] == 1):
            df1['nutrition_level'][i] = 'B'
        elif(df1['nutrition_level'][i] == 2):
            df1['nutrition_level'][i] = 'C'
        elif(df1['nutrition_level'][i] == 3):
            df1['nutrition_level'][i] = 'D'
    print(df1['nutrition_level'])
    result = df1.to_json(orient="columns")
    return result
