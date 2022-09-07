import psycopg2
import psycopg2.extras
from app.config.database import database


class DbConnection():
    def connection(self):
        connection = psycopg2.connect(
            host=database["host"],
            database=database["database"],
            user=database["user"],
            password=database["password"]
        )
        return connection

    def check_user(self, user):
        connection = self.connection()
        cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute("SELECT * FROM users WHERE username = %s", (user,))
            result = cur.fetchone()
        except Exception as error:
            print(error)
        connection.close()
        return result

    def insert_user(self, user, password):
        connection = self.connection()
        cur = connection.cursor()
        try:
            cur.execute( "INSERT INTO users (username, password) VALUES (%s, %s)", (user, password) )
            connection.commit()
        except Exception as error:
            print(error)
        connection.close()

    def delete_user(self, id):
        connection = self.connection()
        cur = connection.cursor()
        try:
            cur.execute( "DELETE FROM users WHERE id = %s" % id)
            connection.commit()
        except Exception as error:
            print(error)
        connection.close()

    def update_user(self, id, user, password):
        connection = self.connection()
        cur = connection.cursor()
        try:
            cur.execute( "UPDATE users SET username='%s', password='%s' WHERE id = %s" % (user, password, id))
            connection.commit()
        except Exception as error:
            print(error)
        connection.close()

    def read_user(self):
        connection = self.connection()
        cur = connection.cursor()
        try:
            cur.execute( "SELECT id, username, password FROM users" )
            result = cur.fetchall()
        except Exception as error:
            print(error)
        connection.close()
        return result

    def create_row(self, id, username, password):
        return "<tr><td><input name='id' readonly=1 value='%s'></td><td><input name='username' readonly=1 value='%s'></td><td><input name='password' readonly=1 value='%s'></td>" % (id, username, password)

    def create_row_update(self, id, username, password):
        return "<tr><td><input name='id' readonly=1 value='%s'></td><td><input name='username' value='%s'></td><td><input name='password' value='%s'></td>" % (id, username, password)

    def concat_read(self):
        result = self.read_user()
        rows = ""
        for id, username, password in result:
            rows += self.create_row(id, username, password)  + "</tr>"
        return rows

    def concat_update(self):
        result = self.read_user()
        rows = ""
        for id, username, password in result:
            rows += self.create_row_update(id, username, password) + "<td><button type='submit' class='btn btn-primary'>Update</button></td></tr>"
        return rows

    def concat_delete(self):
        result = self.read_user()
        rows = ""
        for id, username, password in result:
            rows += self.create_row(id, username, password) + "<td><button type='submit' class='btn btn-primary'>Delete</button></td></tr>"
        return rows
