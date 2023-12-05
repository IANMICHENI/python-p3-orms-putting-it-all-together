import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self,name ,breed):
        self.id = None
        self.name = name
        self.breed = breed
        
    @classmethod
    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name STRING,
            breed STRING
            )
        """
        CURSOR.execute(sql)
        
    @classmethod
    def drop_table(cls):
        sql = """DROP TABLE IF EXISTS dogs"""
        CURSOR.execute(sql)
        
        
    def save(self):
       if self.id is None:
            sql = """
        INSERT INTO dogs (name, breed)
        VALUES(?,?)
        """   
        
            CURSOR.execute(sql,(self.name ,self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
            
       else:
           sql = """ UPDATE dogs SET name = ?, breed = ? WHERE id = ? """
           CURSOR.execute(sql, (self.name, self.breed, self.id))
           CONN.commit()
           
           
    @classmethod
    def create(cls,name,breed):
        dog = Dog(name,breed)
        dog.save()
        return dog
   
    @classmethod
    def new_from_db(cls,row):
        id, name, breed = row
        new_dog = cls(name,breed)
        new_dog.id = id
        return new_dog
    
    @classmethod
    def get_all(cls):
        sql = """SELECT * FROM dogs"""
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        dogs = [cls.new_from_db(row) for row in rows]
        return dogs
    @classmethod
    def find_by_name(cls, name):
        sql = """SELECT * FROM dogs WHERE name = ?"""
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()

        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, dog_id):
        sql = """SELECT * FROM dogs WHERE id = ?"""
        CURSOR.execute(sql, (dog_id,))
        row = CURSOR.fetchone()

        if row:
            return cls.new_from_db(row)
        else:
            return None
    @classmethod
    def find_or_create_by(cls, name, breed):
        existing_dog = cls.find_by_name(name)

        if existing_dog:
            return existing_dog
        else:
            return cls.create(name, breed)

    def update(self):
        self.save()
