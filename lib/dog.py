import sqlite3
import ipdb

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    def __init__(self, name, breed, id = None):
        self.name = name
        self.breed = breed
        self.id = id

    @classmethod
    def create_table(cls):
        create_sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(create_sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        drop_sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(drop_sql)
        CONN.commit()

    def save(self):
        save_sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(save_sql, (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, breed):
        dog = cls(
            name,
            breed
        )
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        dog_inst = cls(
            name = row[1],
            breed = row[2],
            id = row[0]
        )

        return dog_inst
    
    @classmethod
    def get_all(cls):
        get_all_sql = """
            SELECT * FROM dogs
        """
        all_dogs = CURSOR.execute(get_all_sql).fetchall()
        # CONN.commit()
        
        return [cls.new_from_db(dog) for dog in all_dogs]
    
    @classmethod
    def find_by_name(cls, name):
        find_by_name_sql = """
            SELECT * FROM dogs
            WHERE name = ?
            LIMIT 1
        """
        one_dog_inst = CURSOR.execute(find_by_name_sql, (name,)).fetchone()
        # CONN.commit()

        if not one_dog_inst:
            return None

        return cls.new_from_db(one_dog_inst)
    
    @classmethod
    def find_by_id(cls, id):
        find_by_id_sql = """
            SELECT * FROM dogs
            WHERE id = ?
            LIMIT 1
        """
        one_dog_inst = CURSOR.execute(find_by_id_sql, (id,)).fetchone()
        # CONN.commit()

        if not one_dog_inst:
            return None

        return cls.new_from_db(one_dog_inst)

    @classmethod
    def find_or_create_by(cls, name, breed):
        find_by_sql = """
            SELECT * FROM dogs
            WHERE (name, breed) = (?, ?)
            LIMIT 1
        """
        found_dog = CURSOR.execute(find_by_sql, (name, breed,)).fetchone()

        if not found_dog:
            return cls.create(name, breed)

        return found_dog
    
    def update(self):
        update_sql = """
            UPDATE dogs
            SET name = ?,
                breed = ?
            WHERE id = ?
        """
        CURSOR.execute(update_sql, (self.name, self.breed, self.id))
        CONN.commit()



# Dog.drop_table()
# Dog.create_table()

# nigel = Dog("Nigel", "Black Lab")
# # nigel.create("nigel", "Black Lab")

# Dog.create("Nigel", "Black Lab")
# Dog.create("Olive", "Boston Terrier")
# Dog.create("Charlie", "Mutt")

# current_dog = "Nigel"

# print("Searched Dog Name:", Dog.find_by_name(current_dog).name)
# print("Searched Dog Breed:", Dog.find_by_name(current_dog).breed)
# print("Searched Dog ID:", Dog.find_by_name(current_dog).id)

# print(nigel.name)
# nigel.name = "nigel"
# nigel.update()
# print("Updated Dog:", Dog.find_by_name("Nigel").name)

# print(Dog.find_by_name("Nigel"))