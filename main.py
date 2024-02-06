# import the 'testcases' file
import tests.testcases as tc
result = tc.execute_testcases()

# import the Python packages needed to develop the application
from PyQt6 import QtCore, QtGui, QtWidgets
import datetime
import sqlite3
import sys
import json
import os
# import the file 'dev_tools'
import dev_tools as dt

# generate the user interface if changes have been made
os.system("./gui/generate.sh")

# import the GUI files
from gui.gui import Ui_mainWindow


# application implementation
class mainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    wrong_password_counter = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        # add the messages that appear in the 'Log' panel
        self.add_data_to_log("Testcases results: {}".format(result))
        self.add_data_to_log("Application started!")
        self.add_data_to_log("Application version: {}".format(dt.get_version()))
        # add the messages that appear in the 'Test status' panel
        self.test_status_plainTextEdit.appendPlainText("UI: {}".format(result[0]))
        self.test_status_plainTextEdit.appendPlainText("Database: {}".format(result[1]))
        self.test_status_plainTextEdit.appendPlainText("Config: {}".format(result[2]))
        self.test_status_plainTextEdit.appendPlainText("Modules: {}".format(result[3]))
        self.test_status_plainTextEdit.appendPlainText("GUI Generation: {}".format(result[4]))

        # set the color for the connect_db button
        self.connect_db_pushButton.setStyleSheet("background-color: red")
        # initialize the progress bar
        self.progressBar.setValue(0)
        # set the labels in order to request authentication
        self.connection_status_label.setText("Please login to use the application!")
        self.status_label_query.setText("Please login to use the application!")

        # disable the buttons
        self.select_db_pushButton.setEnabled(False)
        self.connect_db_pushButton.setEnabled(False)
        self.create_table_pushButton.setEnabled(False)
        self.delete_table_pushButton.setEnabled(False)
        self.execute_query_pushButton.setEnabled(False)
        self.table_listWidget.setEnabled(False)
        self.query_plainTextEdit.setEnabled(False)

        # connect the buttons to their own function
        self.select_db_pushButton.clicked.connect(self.select_db)
        self.connect_db_pushButton.clicked.connect(self.connect_db)
        self.table_listWidget.itemClicked.connect(self.select_table)
        self.create_table_pushButton.clicked.connect(self.create_table)
        self.delete_table_pushButton.clicked.connect(self.delete_table)
        self.execute_query_pushButton.clicked.connect(self.execute_query)
        self.login_pushButton.clicked.connect(self.login)
    

    # the function with which we select the path to the database file
    def select_db(self):
        self.db_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Database", "", "SQLite3 Database (*.db)")
        self.db_path_lineEdit.setText(self.db_path)
        # add a message in the Log panel
        self.add_data_to_log("Selected database: {}".format(self.db_path))
    

    # database connection function
    def connect_db(self):
        # connect to the database
        self.conn = sqlite3.connect(self.db_path)
        self.progressBar.setValue(30)
        # get the cursor
        self.cursor = self.conn.cursor()
        # get the tables from the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.tables = self.cursor.fetchall()
        # display the tables in the list of tables
        for table in self.tables:
            self.table_listWidget.addItem(table[0])
        
        self.progressBar.setValue(70)
        # close the connection to the database
        self.conn.close()
        # change the message in the interface and the color of the button
        self.connection_status_label.setText("Connected to the database")
        self.connect_db_pushButton.setStyleSheet("background-color: green")
        self.progressBar.setValue(100)
        # add a message in the Log panel
        self.add_data_to_log("Connected to the database: {}".format(self.db_path))


    # the function for selecting a table
    def select_table(self):
        # get the selected table
        self.selected_table = self.table_listWidget.selectedItems()[0].text()
        # connect to the database
        self.conn = sqlite3.connect(self.db_path)
        # get the cursor
        self.cursor = self.conn.cursor()
        # get information about the columns of the table
        self.cursor.execute("PRAGMA table_info({})".format(self.selected_table))
        # set the rows and columns of the table to 0
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        self.columns = self.cursor.fetchall()
        # set the number of columns of the selected table
        self.tableWidget.setColumnCount(len(self.columns))
        # display the attributes of the columns in the table
        for column in self.columns:
            self.tableWidget.setHorizontalHeaderItem(self.columns.index(column), QtWidgets.QTableWidgetItem(column[1]))

        # get all the data from the table
        self.cursor.execute("SELECT * FROM {}".format(self.selected_table))
        self.data = self.cursor.fetchall()
        # set the number of rows of the selected table
        self.tableWidget.setRowCount(len(self.data))

        for row in self.data:
            for column in row:
                self.tableWidget.setItem(self.data.index(row), row.index(column), QtWidgets.QTableWidgetItem(str(column)))
        # close the connection to the database
        self.conn.close()


    # the function for creating a table
    def create_table(self):
        # check if we are connected to the database
        if self.connect_db_pushButton.styleSheet() == "background-color: red":
            # display a window with a message in the interface
            self.dialog = QtWidgets.QMessageBox.warning(self, "Database not connected", "Please connect to the database first.")
            return
        else:
            # connect to the database
            self.conn = sqlite3.connect(self.db_path)
            # get the cursor
            self.cursor = self.conn.cursor()
            # create a table and set its primary key
            self.cursor.execute("CREATE TABLE {} (id INTEGER PRIMARY KEY)".format(self.table_name_lineEdit.text()))
            # close the connection to the database
            self.conn.close()
            # add the table to the list
            self.table_listWidget.addItem(self.table_name_lineEdit.text())
            # add a message in the Log panel
            self.add_data_to_log("Created table: {}".format(self.table_name_lineEdit.text()))
            self.table_name_lineEdit.setText("")
    

    # the function to delete a table
    def delete_table(self):
        
        if self.connect_db_pushButton.styleSheet() == "background-color: red":
            self.dialog = QtWidgets.QMessageBox.warning(self, "Database not connected", "Please connect to the database first.")
            return
        else:
            # display a window with a message to confirm the deletion
            self.delete_dialog = QtWidgets.QMessageBox.question(self, "Delete Table", "Do you really want to delete the table?", QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

            if self.delete_dialog == QtWidgets.QMessageBox.StandardButton.Yes:
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                # delete the table
                self.cursor.execute("DROP TABLE {}".format(self.selected_table))
                self.conn.close()
                # delete the table from the list
                self.table_listWidget.takeItem(self.table_listWidget.currentRow())
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(0)
                self.add_data_to_log("Deleted table: {}".format(self.selected_table))
            else:
                pass


    # function to execute an SQL query
    def execute_query(self):
        self.progressBar.setValue(0)

        if self.connect_db_pushButton.styleSheet() == "background-color: red":
            self.dialog = QtWidgets.QMessageBox.warning(self, "Database not connected", "Please connect to the database first.")
            return
        else:
            # manage possible errors
            try:
                self.conn = sqlite3.connect(self.db_path)
                self.cursor = self.conn.cursor()
                #execute the instruction
                self.cursor.execute(self.query_plainTextEdit.toPlainText())
                # get the results of the query
                self.data = self.cursor.fetchall()
                # set the number of rows of the modified table
                self.tableWidget.setRowCount(len(self.data))
                # display all the row values in the table
                for row in self.data:
                    for column in row:
                        self.tableWidget.setItem(self.data.index(row), row.index(column), QtWidgets.QTableWidgetItem(str(column)))
                
                # apply all the changes made
                self.conn.commit()
                self.conn.close()
                # if the query is 'select', we do not refresh the table
                if self.query_plainTextEdit.toPlainText().split(" ")[0].lower() == "select":
                   pass
                else:
                   # refresh table
                   self.select_table()
    
                self.status_label_query.setText("Query executed successfully")
                self.progressBar.setValue(100)
                self.add_data_to_log("Executed query: {}".format(self.query_plainTextEdit.toPlainText()))

            except sqlite3.Error as e:
                self.status_label_query.setText("Error: {}".format(e))
                self.progressBar.setValue(100)
                self.add_data_to_log("Error: {}".format(e))
                return
        

     # login function
    def login(self):
        # get the user and password from the interface
        self.user = self.user_lineEdit.text()
        self.password = self.password_lineEdit.text() 
        # get the user and password from the 'config.json' file
        self.user_json = dt.get_parameter("user")
        self.password_json = dt.get_parameter("password")
        
        # check if the user and password entered in the interface are correct
        if self.user == self.user_json and self.password == dt.decrypt_password(self.password_json):
            # activate all the buttons in the interface to be able to use them
            self.select_db_pushButton.setEnabled(True)
            self.connect_db_pushButton.setEnabled(True)
            self.create_table_pushButton.setEnabled(True)
            self.delete_table_pushButton.setEnabled(True)
            self.execute_query_pushButton.setEnabled(True)
            self.table_listWidget.setEnabled(True)
            self.tableWidget.setEnabled(True)
            self.query_plainTextEdit.setEnabled(True)
        
            # change some messages in the interface and the color of two buttons
            self.user_status_label.setText("Logged in as {}".format(self.user))
            self.connection_status_label.setText("Database not connected")
            self.status_label_query.setText("No query executed")
            self.progressBar.setValue(0)
            self.login_pushButton.setStyleSheet("background-color: green")
            self.connect_db_pushButton.setStyleSheet("background-color: red")
             
            self.wrong_password_counter = 0
            self.add_data_to_log("Logged in as {}".format(self.user))

        else:
            self.dialog = QtWidgets.QMessageBox.warning(self, "Wrong user or password", "Please check your user and password.")
            self.progressBar.setValue(0)
            self.wrong_password_counter += 1

        # if we enter the wrong password 3 times
        if self.wrong_password_counter == 3:
            # display a window with a message in the interface
            self.dialog = QtWidgets.QMessageBox.warning(self, "Wrong user or password", "You have entered the wrong user or password 3 times. Please restart the application.")
            # close the application
            sys.exit()

    # function for displaying a message in the Log panel
    def add_data_to_log(self, data):
        self.current_date_time = datetime.datetime.now()
        self.current_date_time_string = self.current_date_time.strftime("%d/%m/%Y %H:%M:%S")
        self.log_plainTextEdit.appendPlainText("{}: {}".format(self.current_date_time_string, data))


app = QtWidgets.QApplication(sys.argv)
main = mainWindow()
sys.exit(app.exec())