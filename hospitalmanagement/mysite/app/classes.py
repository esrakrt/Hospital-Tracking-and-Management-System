import pyodbc

class Hasta:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=db_name;UID=user;PWD=password')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='hastalar' AND xtype='U')
            CREATE TABLE hastalar (
                HastaID varchar(100) PRIMARY KEY,
                Ad varchar(100),
                Soyad varchar(100),
                DogumTarihi date,
                Cinsiyet varchar(10),
                TelefonNumarasi varchar(15),
                Adres text
            )
        """)

class Doktor:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=db_name;UID=user;PWD=password')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='doktorlar' AND xtype='U')
            CREATE TABLE doktorlar (
                DoktorID varchar(100) PRIMARY KEY,
                Ad varchar(100),
                Soyad varchar(100),
                UzmanlikAlani varchar(100),
                CalistigiHastane varchar(100)
            )
        """)
class TibbiRaporlar:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=server_name;DATABASE=db_name;UID=user;PWD=password')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TibbiRaporlar' AND xtype='U')
            CREATE TABLE TibbiRaporlar (
                RaporID varchar(100) PRIMARY KEY,
                RaporTarihi date,
                RaporIcerigi text,
                GörüntüURL varchar(500),
                RaporJSON text,
                HastaID varchar(100),
                DoktorID varchar(100)
            )
        """)
    def rapor_sil(self, rapor_id):
        self.cursor.execute("DELETE FROM TibbiRaporlar WHERE RaporID = ?", rapor_id)
        self.conn.commit()
