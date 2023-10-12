"""
Database code for communicating with a sqlite database
"""
import logging
import sqlite3 as sql

class Database:
    """
    The database handler where all the information will be saved to file
    """

    def __init__(self, filename):
        self.__filename = filename

        self.__conn = sql.connect(filename)
        self.__cursor = self.__conn.cursor()
        self.__create_database()

    def __create_database(self):
        """
        Creates the database if it does not exist
        """
        try:
            self.__cursor.execute(
                """CREATE TABLE IF NOT EXISTS main(id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT, expiredate TEXT, desc TEXT, cat TEXT)""")
            self.__cursor.execute("CREATE TABLE IF NOT EXISTS categories(name TEXT PRIMARY KEY)")
            self.__cursor.execute("INSERT INTO categories (name) VALUES('Other')")
            self.__conn.commit()
        except:
            pass

    def get_all_categories(self):
        self.__cursor.execute("SELECT name FROM categories")
        temp_list = []
        for row in self.__cursor:
            temp_list.append(row[0])
        return tuple(temp_list)

    def get_all_entries(self):
        """
        Returns all of entries in the database
        """
        self.__cursor.execute("SELECT * FROM main")
        return self.__cursor.fetchall()
 
    def del_id(self, idtofind):
        """
        delete a entry by the given id
        """
        logging.debug("deleting data by id: {idtofind}")
        self.__cursor.execute("DELETE FROM main WHERE id='{idtofind}'")
        self.__conn.commit()

    def get_by_id(self, idtofind):
        """
        Returns a entry by the given id
        """
        logging.debug("getting data by id: {idtofind}")
        self.__cursor.execute("SELECT name,expiredate,desc,cat FROM main WHERE id='{idtofind}'")
        return self.__cursor.fetchone()

    def add_entry(self, name, expiredate, desc, cat):
        """
        Adds a new entry to the database
        """
        self.__cursor.execute(
            "INSERT INTO main(name,expiredate,desc,cat) VALUES(?,?,?,?)", (name, expiredate, desc, cat))
        self.__conn.commit()

    def add_category(self, name):
        try:
            self.__cursor.execute("INSERT INTO categories (name) VALUES('{name}')")
            self.__conn.commit()
        except sql.IntegrityError:
            logging.debug("{name} category already exists so not going to add")

    def update_value(self, dataid, nameofvalue, thevalue):
        self.__cursor.execute("UPDATE main SET {nameofvalue}='{thevalue}' WHERE id='{dataid}'")
        self.__conn.commit()

    def reset(self):
        """
        Resets the database to default
        """
        self.__conn.execute("DELETE * FROM main")
        self.__conn.execute("DELETE FROM sqlite_sequence WHERE name='main'")

    def close(self):
        """
        Closes the database
        """
        self.__conn.close()
        logging.info("Database closed")
