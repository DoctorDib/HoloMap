import sqlite3, traceback, sys

from config import Config

class BaseDataHandler:
    should_print = True
    connection = None
    command = None

    def __init__(self, _class, _validate_table : bool = False):
        DEV_MODE = len(sys.argv) > 1 and sys.argv[1] == "DEV"

        table_name = _class._table
        columns = _class.columns_with_type()
    
        self.connection = sqlite3.connect("{0}/{1}".format(Config.MainDir, Config.DEVDBName if DEV_MODE else Config.DBName))
        self.command = self.connection.cursor()
        self.initialise(table_name, columns)

        if (_validate_table):
            # Validating the table
            print("Validating {0} table".format(table_name))
            print("----------------------------------------")
            self.validate_table(table_name, _class)

    def print_sql_error(self, _class, err):
        if self.should_print:
            print("\n\n==============================================================")
            print('SQLite error for table "%s": "%s"' % (_class.__class__.__name__, ' '.join(err.args)))
            print("-----------------")
            print("Exception class is: ", err.__class__)
            print("-----------------")
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)
            print("==============================================================\n\n")
        self.connection.close()
        raise err

    def format_condition(self, _condition : list, _prefix : str = None):
        if (_condition is None):
            return ""

        items : list[str] = []

        for x in _condition:
            if (_prefix != None):
                items.append(x)
                continue

            val_type = type(x)
            
            if (val_type == str):
                if ("\"" in x):
                    items.append(x)
                else:
                    items.append("\"{0}\"".format(x))
            else:
                items.append(str(x))

        if ("WHERE" in _prefix):
            return "{0} {1}".format("" if _prefix is None else _prefix, " and ".join(items))
        return "{0} {1}".format("" if _prefix is None else _prefix, ", ".join(items))

    def format_where_condition (self, _condition : list[list[str]] = None):
        if (_condition is None):
            return ""
        # where [this and this] or [this and this]
        items : list[str] = []
        for and_conditions in _condition:
            ands : list[str] = []
            for x in and_conditions:
                ands.append(x)
            items.append(" and ".join(ands))
        return "WHERE {0}".format(" or ".join(items))

    def initialise(self, _table, _types):
        try:
            # Create the table if it does not exist
            self.command.execute('CREATE TABLE IF NOT EXISTS {0} ({1})'.format(_table, ", ".join(_types)))
            self.connection.commit()
        except sqlite3.Error as er:
            self.print_sql_error(_table, er)

    def validate_table(self, _table, _class):
        data = self.command.execute('PRAGMA table_info({0})'.format(_table))
        self.connection.commit()

        # Getting info
        table_info = []
        old_columns = []
        for row in data.fetchall():
            row_info = {} 
            row_info['cid'] = row[0]
            row_info['name'] = row[1]
            row_info['type'] = row[2]
            row_info['notnull'] = row[3]
            row_info['dflt_value'] = row[4]
            row_info['pk'] = row[5]

            table_info.append(row_info)
            old_columns.append(row[1])

        # Refresh flag
        refresh_required = False

        for index, column_key in enumerate(_class._columns):
            if (column_key == 'UNIQUE_CONSTRAINT'):
                continue

            if (index+1 > len(table_info)):
                refresh_required = True
                break

            # Checking if the order is the same
            if (column_key != table_info[index]['name']):
                refresh_required = True
                break
            # TODO - Come up with a type check method 
        
        # Ensuring they are the right length
        if (len(_class._columns) != len(old_columns)):
            refresh_required = True

        # SQLite table is validated and no update is requried
        if not refresh_required:
            return

        matched_columns = []
        for column_key in _class._columns:
            if (column_key == 'UNIQUE_CONSTRAINT'):
                continue
            
            if (column_key in old_columns):
                matched_columns.append(column_key)

        # SQLite table mismatch
        print("-----------------------------------------------------------------")
        print("SQLite table mismatch - refreshing {0}".format(_table))
        print("-----------------------------------------------------------------")

        temp_table_name = "temp_table"

        # Removing temp table if it failed to drop from last use
        self.command.execute('DROP TABLE IF EXISTS {0}'.format(temp_table_name))

        # Creating temp table
        self.command.execute('CREATE TABLE {0} ({1})'.format(temp_table_name, ", ".join(_class.columns_with_type())))

        # Transfering data from old table
        self.command.execute('INSERT INTO {0} ({1}) SELECT {1} FROM {2}'.format(temp_table_name, ", ".join(matched_columns), _table))
        
        # Removing old talbe and renaming the temp table
        self.command.execute('DROP TABLE {0}'.format(_table))
        
        # Removing old talbe and renaming the temp table
        self.command.execute('ALTER TABLE {0} RENAME TO {1}'.format(temp_table_name, _table))

        self.connection.commit()

    def get(self, _class : any, _key : str, _limit : int, _where_condition : list[list[str]] = None, get_multiple = True):
        try:
            limit = "" if _limit is None else "LIMIT {0}".format(_limit)
            where_condition = self.format_where_condition(_where_condition)
            # print(">>>>>", 'SELECT {0} FROM {1} {2} {3}'.format(_key, _class._table, where_condition, limit))
            results = self.command.execute('SELECT {0} FROM {1} {2} {3}'.format(_key, _class._table, where_condition, limit))
            if (get_multiple):
                return results.fetchall()
            return results.fetchone()
        except sqlite3.Error as er:
            self.print_sql_error(_class, er)

    def insert_data(self, _class : any, _columns : list[str], _values : list[object]):
        try:
            # print('INSERT INTO {0} {1} VALUES {2}'.format(_class._table, _columns, _values))
            self.command.execute('INSERT INTO {0} {1} VALUES {2}'.format(_class._table, _columns, _values))
            self.connection.commit()
        except sqlite3.Error as er:
            self.print_sql_error(_class, er)

    def insert_update(self, _class : any, _columns, _values):
        try:
            # print('INSERT OR REPLACE INTO {0} {1} VALUES {2}'.format(_class._table, _columns, _values))
            self.command.execute('INSERT OR REPLACE INTO {0} {1} VALUES {2}'.format(_class._table, _columns, _values))
            self.connection.commit()
        except sqlite3.Error as er:
            self.print_sql_error(_class, er)

    def remove(self, _class : any, _where_condition : list[list[str]] = None):
        try:
            where_condition = self.format_where_condition(_where_condition)
            self.command.execute('DELETE FROM {0} {1}'.format(_class._table, where_condition))
            self.connection.commit()
        except sqlite3.Error as er:
            self.print_sql_error(_class, er)

    def clear_table(self, _class : any):
        try:
            self.command.execute('DELETE FROM {0}'.format(_class._table))
            self.connection.commit()
        except sqlite3.Error as er:
            self.print_sql_error(_class, er)

    def set(self, _class : any, _set_condition : list[str], _where_condition : list[list[str]] = None):
        try:
            set_condition = self.format_condition(_set_condition, "SET")
            where_condition = self.format_where_condition(_where_condition)
            self.command.execute('UPDATE {0} {1} {2}'.format(_class._table, set_condition, where_condition))
            self.connection.commit()
        except sqlite3.Error as er:
            self.print_sql_error(_class, er)