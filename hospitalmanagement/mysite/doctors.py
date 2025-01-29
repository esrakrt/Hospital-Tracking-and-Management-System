import pyodbc
import json

# Veritabanı bağlantı bilgileri
server = 'SERVER_ADINIZ'
database = 'VERITABANI_ADINIZ'
username = 'KULLANICI_ADINIZ'
password = 'SIFRENIZ'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                      server+';DATABASE='+database+';UID='+username+';PWD='+ password)

cursor = cnxn.cursor()

# JSON dosyasını aç ve içeriği oku
with open('veriler/patients.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


# JSON'daki her bir kaydı veritabanına ekle
for item in data:
    insert_query = '''
    INSERT INTO Hastalar (Sutun1, Sutun2, Sutun3)
    VALUES (?, ?, ?)
    '''
    values = (item['key1'], item['key2'], item['key3'])
    cursor.execute(insert_query, values)

# İşlemleri kaydet ve bağlantıyı kapat
cnxn.commit()
cursor.close()
cnxn.close()