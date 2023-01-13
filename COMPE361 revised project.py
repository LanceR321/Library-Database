from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import pandas as pd

# for delete pop up window
from PyQt5.QtWidgets import QMessageBox

class orders(QMainWindow):
    def __init__(self,id):
        super(orders, self).__init__()
        uic.loadUi('orders.ui', self)
        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')
        self.df_orders = pd.read_excel('Orders.xlsx', sheet_name='orders')
        self.df_order_id = pd.read_excel('order_id.xlsx', sheet_name='info')

        self.id = id
        self.load_table_orders()
        self.load_table_orders_id()
        self.valid2 = valid()

        self.valid2.btn_no.clicked.connect(self.no_clicked)
        self.valid2.btn_yes.clicked.connect(self.yes_clicked)

        self.btn_order.clicked.connect(self.make_order_clicked)
        self.btn_cancel_order.clicked.connect(self.cancel_clicked)
        self.btn_update_order.clicked.connect(self.update_clicked)
        #self.users.btn_login.clicked.connect(self.login_clicked)

    def update_clicked(self):
        self.setting = 3
        self.check_input()

    def cancel_clicked(self):
        self.setting = 2
        self.check_input()

    def make_order_clicked(self):
        self.setting = 1
        self.check_input()

    def no_clicked(self):
        self.valid2.close()

    def yes_clicked(self):
        self.valid2.close()
        if self.setting ==1:
            self.make_order(self.id)

        if self.setting == 2:
            self.cancel()

        if self.setting ==3:
            self.update()

    ## need fix update
    def update(self):
        self.read_lines()
        self.read_values()

        self.new_book = self.df_books[self.df_books.id == int(self.new_bookID)]
        self.new_price = self.new_book[self.new_book.Price == self.new_book.Price.values].Price.item()

        self.find_id = self.df_orders[self.df_orders.Customer_Name == self.name]
        self.find_id = self.find_id[self.find_id.Total_Price == self.price]

        print(self.find_id)
        self.row_id = self.find_id.id.item() ## not able to order same books. maybe delete by number

        self.df_orders.iloc[self.row_id -1 , 4] = self.new_price
        self.df_orders.to_excel('Orders.xlsx', sheet_name='orders', index=False)

        self.df_order_id.iloc[self.row_id -1,1] = self.new_bookID
        self.df_order_id.iloc[self.row_id - 1, 2] = self.new_number

        self.df_order_id.to_excel('order_id.xlsx', sheet_name='info', index=False)
        self.refresh_tables()

    def cancel(self):
        self.read_lines()
        self.read_values()

        self.condense = self.df_orders[self.df_orders.Customer_Name == self.name]
        self.condense2 = self.condense[self.condense.Total_Price == self.price]
        #print(self.condense2)
        #print(self.condense2.iloc[0,0])
        number = self.condense2.iloc[0,0]
       # print(self.condense.index[0])

        self.df_orders.drop(self.df_orders.index[number -1], inplace=True)
        self.df_orders.to_excel('Orders.xlsx', sheet_name='orders', index=False)

        self.df_order_id.drop(self.df_order_id.index[number -1], inplace=True)
        self.df_order_id.to_excel('order_id.xlsx', sheet_name='info', index=False)

        self.refresh_tables()




    def make_order(self, id):
        self.read_lines()
        self.read_values()

        self.df_orders.loc[len(self.df_orders)] = [len(self.df_orders) + 1, id, self.name, self.date,self.price]
        self.df_orders.to_excel('Orders.xlsx', sheet_name='orders', index=False)

        self.df_order_id.loc[len(self.df_order_id)] = [len(self.df_orders), self.bookID, self.number]
        self.df_order_id.to_excel('order_id.xlsx', sheet_name='info', index=False)
        self.refresh_tables()


    def refresh_tables(self):
        self.load_table_orders()
        self.load_table_orders_id()
        self.clear_lines()

    def read_values(self):
        self.name = self.df_users.iloc[int(self.id -1),1]
        self.book = self.df_books[self.df_books.id == int(self.bookID)]
        self.price = self.book[self.book.Price == self.book.Price.values].Price.item()

    def check_input(self):
        self.read_lines()

        if int(self.bookID) <= len(self.df_books):
            if self.setting <= 2:
                self.valid2.show()
        else:
            self.le_BookID_warning.setText("BookID input not in range")

        if int(self.new_bookID) <= len(self.df_books):
            if self.setting == 3:
                self.valid2.show()
        else:
            self.le_new_bookid_warning.setText("New BookID input not in range")

    def load_table_orders(self):

        for x in range(len(self.df_orders)):
            self.table_orders.setItem(x, 0, QTableWidgetItem(str(self.df_orders.iloc[x, 0])))
            self.table_orders.setItem(x, 1, QTableWidgetItem(str(self.df_orders.iloc[x, 1])))
            self.table_orders.setItem(x, 2, QTableWidgetItem(str(self.df_orders.iloc[x, 2])))
            self.table_orders.setItem(x, 3, QTableWidgetItem(str(self.df_orders.iloc[x, 3])))
            self.table_orders.setItem(x, 4, QTableWidgetItem(str(self.df_orders.iloc[x, 4])))

    def load_table_orders_id(self):
        for y in range(len(self.df_order_id)):
            self.table_orders_id.setItem(y, 0, QTableWidgetItem(str(self.df_order_id.iloc[y, 0])))
            self.table_orders_id.setItem(y, 1, QTableWidgetItem(str(self.df_order_id.iloc[y, 1])))
            self.table_orders_id.setItem(y, 2, QTableWidgetItem(str(self.df_order_id.iloc[y, 2])))

    def read_lines(self):
        self.date = self.le_date.text()
        self.bookID = self.le_bookid.text()
        self.number = self.le_number.text()

        self.new_bookID = self.le_new_bookid.text()
        self.new_number = self.le_new_number.text()

    def clear_lines(self):
       self.le_bookid.clear()
       self.le_number.clear()

       self.le_new_bookid.setText("0")
       self.le_new_number.clear()

       self.le_BookID_warning.clear()
       self.le_new_bookid_warning.clear()



class book_options(QMainWindow):
    def __init__(self):
        super(book_options, self).__init__()
        uic.loadUi('book_menu.ui', self)

        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')

        self.btn_add_book.clicked.connect(self.add)

    def add(self):
        self.read_lines()
        self.df_books.loc[len(self.df_books.index)] = [len(self.df_books)+1, self.name, self.author,self.number,self.price,"images/default.png"]
        self.df_books.to_excel('books.xlsx', sheet_name='books', index=False)
        self.refresh()

    def read_lines(self):
        self.name = self.le_name.text()
        self.author = self.le_author.text()
        self.price = self.le_price.text()
        self.number = self.le_number.text()

    def clear_lines(self):
        self.le_name.clear()
        self.le_author.clear()
        self.le_price.clear()
        self.le_number.clear()

    def refresh(self):
        self.close()
        self.clear_lines()




class valid(QMainWindow):
    def __init__(self):
        super(valid,self).__init__()
        uic.loadUi('validation.ui', self)

class book_gui(QMainWindow):
    def __init__(self, id):
        super(book_gui,self).__init__()
        uic.loadUi('book_data.ui', self)
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')

        self.book = self.df_books.loc[self.df_books.id == id].reset_index()

        self.le_name.setText(str(self.book.Name[0]))
        self.le_author.setText(str(self.book.Author[0]))
        self.le_number.setText(str(self.book.Number[0]))
        self.le_price.setText(str(self.book.Price[0]))

        self.lbl_photo.setPixmap(QPixmap(str(self.book.photo_path[0])))
        self.lbl_photo.setFixedWidth(300)
        self.lbl_photo.setFixedHeight(300)
        #self.show()

        self.cur_name = self.le_name.text()
        self.cur_author = self.le_author.text()
        self.cur_number = self.le_number.text()
        self.cur_price = self.le_price.text()

        self.valids = valid()
        self.options = book_options()

        self.btn_add_book.clicked.connect(self.add_clicked)
        self.btn_delete_book.clicked.connect(self.delete_clicked)
        self.btn_update_book.clicked.connect(self.update_clicked)
        self.valids.btn_no.clicked.connect(self.no_clicked)
        self.valids.btn_yes.clicked.connect(self.yes_clicked)

    def show_books(self):
        self.show()

    def delete_clicked(self):
        self.setting = 3
        self.valids.show()

    def add_clicked(self):
        self.setting = 2
        self.valids.show()

    def update_clicked(self):
        self.setting = 1
        self.valids.show()

    def no_clicked(self):
        self.valids.close()

    def yes_clicked(self):
        self.valids.close()
        if self.setting ==1:
           self.updated()

        if self.setting ==2:
            self.options.show()

        if self.setting ==3:
            self.delete()

        #self.setting =0

    def delete(self):
        self.df_books.drop(self.df_books[self.df_books['Name'] == self.cur_name].index, inplace=True)
        self.df_books.to_excel('books.xlsx', sheet_name='books', index=False)

    def updated(self):
        self.read_lines()
        self.df_books.replace(to_replace=self.cur_name, value=self.name, inplace=True)
        self.df_books.replace(to_replace=self.cur_author, value=self.author, inplace=True)
        self.df_books.replace(to_replace =float(self.cur_number), value =float(self.number), inplace=True)
        self.df_books.replace(to_replace= float(self.cur_price), value= float(self.price), inplace=True)
        self.df_books.to_excel('books.xlsx', sheet_name='books', index=False)

    def read_lines(self):
        self.name = self.le_name.text()
        self.author = self.le_author.text()
        self.price = self.le_price.text()
        self.number = self.le_number.text()



class book_list(QMainWindow):

    def __init__(self):
        super(book_list,self).__init__()
        uic.loadUi('book_photos.ui', self)
        self.row_length = 6
        #self.show()
        self.load_books_data()
        self.id = 0
        self.check = 0


    def load_books_data(self):
        self.df_books = pd.read_excel('books.xlsx', sheet_name='books')

        row_index = -1
        for i in range(len(self.df_books)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            user = QLabel()
            user.setPixmap(QPixmap(self.df_books.photo_path[i]))
            user.setScaledContents(True)
            user.setFixedWidth(200)
            user.setFixedHeight(200)
            user.mousePressEvent = lambda e, id = self.df_books.id[i]: self.show_b(id)
            self.layout_users.addWidget(user, row_index, column_index)




    def refresh(self):
        self.load_books_data()

    def show_b(self, id):
        self.books = book_gui(id)
        self.books.show_books()
        self.books.btn_refresh.clicked.connect(self.refresh)

    def show_wind(self):
        self.show()


class new_user(QMainWindow):
    def __init__(self):
        super(new_user, self).__init__()
        uic.loadUi('add_user.ui', self)

        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        self.add_username = self.new_username.text()
        self.add_password = self.new_password.text()
        self.btn_add.clicked.connect(self.check_user)
        self.btn_delete.clicked.connect(self.delete)


    def check_user(self):

        self.read_lines()
        current_users = self.df_users[self.df_users.username == self.add_username]

        if current_users.empty:
            self.add_user()
        else:
            self.user_taken()

    def read_lines(self):
        self.add_username = self.new_username.text()
        self.add_password = self.new_password.text()

    def add_user(self):
        self.df_users.loc[len(self.df_users.index)] = [len(self.df_users) + 1, self.add_username, self.add_password,"images/default.png",
                                                       "User"]
        self.df_users.to_excel('Project.xlsx', sheet_name='users', index=False)
        self.clear_user()
        self.close()
        window.load_users_data()

    def delete(self):
        ## pop up a warning
        self.read_lines()
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("The user will be deleted.")
        msg.setIcon(QMessageBox.Warning)  # warning icon

        text = msg.exec()

        if text == QMessageBox.Ok:  ## fix ok and button press
            # delete user (row) from excel
            print(self.add_username)
            print(self.df_users)
            username = self.add_username
            self.df_users.drop(self.df_users[self.df_users['username'] == username].index, inplace=True)

            self.df_users.to_excel('Project.xlsx', sheet_name='users', index=False)
            print(self.df_users)
            self.close()
            self.clear_user()
            window.load_users_data()

    def user_taken(self):
        msg2 = QMessageBox()
        msg2.setWindowTitle("Warning")
        msg2.setText("Usernames must be unique!")
        msg2.setIcon(QMessageBox.Information)  # information icon
        text = msg2.exec()
        self.clear_user()

    def clear_user(self):
        self.new_username.clear()
        self.new_password.clear()


class update_user(QMainWindow):
    def __init__(self):
        super(update_user,self).__init__()
        uic.loadUi('update_user.ui',self)
        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        self.btn_update.clicked.connect(self.update_clicked)
        self.var = 0


    def update_clicked(self):
        self.read_lines()
        self.check1 = self.df_users[self.df_users.username == self.old_username]
        self.check2 = self.df_users[self.df_users.username == self.old_password]
        self.current_users = self.df_users[self.df_users.username == self.new1_username]

        if self.check1.empty:
            self.label_7.setText("Current username not found")
        else:
            self.var = self.var + 1

        if self.check1.empty:
            self.label_8.setText("Current password not found")
        else:
            self.var = self.var + 1


        if self.current_users.empty:
            if self.var ==2:
               print("update")
               self.update()
               self.var = 0
        else:
            self.label_6.setText("Username has been taken")

    def update(self):
        ##update df
        self.df_users.replace(to_replace=self.old_username, value=self.new1_username, inplace=True)
        self.df_users.replace(to_replace=self.old_password, value=self.new1_password, inplace=True)

        # update excel
        self.df_users.to_excel('Project.xlsx', sheet_name='users', index=False)
        self.close()

    def read_lines(self):
        self.old_username = self.cur_username.text()
        self.old_password = self.cur_password.text()
        self.new1_username = self.new_username.text()
        self.new1_password = self.new_password.text()

    def show_update(self):
        self.show()


class verify(QMainWindow):
    def __init__(self):
        super(verify,self).__init__()
        uic.loadUi('login.ui',self)
        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        self.ad_username = self.admin_username.text()
        self.ad_password = self.admin_password.text()

    def warning(self):
        msg = QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText("Enter valid Admin credentials")
        msg.setIcon(QMessageBox.Information)  # information icon
        text = msg.exec()
        self.clear_line()

    def clear_line(self):
        self.admin_username.clear()
        self.admin_password.clear()

    def read_line(self):
        self.ad_username = self.admin_username.text()
        self.ad_password = self.admin_password.text()


class ShowUserGui(QMainWindow):

    def __init__(self, id):
        super(ShowUserGui,self).__init__()
        uic.loadUi('show_user.ui', self)
        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        self.user = self.df_users.loc[self.df_users.id == id].reset_index()
        self.le_username.setText(str(self.user.username[0]))
        self.le_password.setText(str(self.user.password[0]))
        self.lbl_photo.setPixmap(QPixmap(str(self.user.photo_path[0])))
        self.lbl_photo.setFixedWidth(300)
        self.lbl_photo.setFixedHeight(300)
        self.state_status.setText(str(self.user.admin_status[0]))
        self.status = self.user.admin_status[0]

        self.valid3 = valid()
        self.valid3.btn_no.clicked.connect(self.no_clicked)
        self.valid3.btn_yes.clicked.connect(self.yes_clicked)

        self.btn_orders.clicked.connect(self.show_orders)
        self.btn_list_users.clicked.connect(self.list_users_clicked)
        self.btn_update.clicked.connect(self.update_clicked)  ## connects update button to function update clicked
        self.btn_delete.clicked.connect(self.delete_clicked)  ## connects delete button to function delete clicked
        self.btn_add_users.clicked.connect(self.add_users_clicked)
        self.btn_books.clicked.connect(self.show_books)

        ## store orginal username and password
        self.old_username = self.le_username.text()
        self.old_password = self.le_password.text()

        self.setting = 0
        self.user_id = id

        self.update_use = update_user()  #update_user.ui
        self.user_new = new_user()       # add_user.ui
        self.books = book_list()         # book_menu.ui


        self.show()

    def no_clicked(self):
        self.valid3.close()

    def yes_clicked(self):
        self.valid3.close()
        self.admin_settings()

    def show_orders(self):
        self.orders = orders(self.user_id)
        self.orders.show()

    def show_books(self):
        self.books.show()

    def admin_settings(self):
        if self.setting == 1:
            self.update_use.show_update()
            #self.update()

        if self.setting == 2:
            self.user_new.show()

        if self.setting == 3:
            self.list_users()

        if self.setting == 4:
           self.user_new.show()
        # self.setting = 0

    def add_users_clicked(self):
        self.setting = 4
        self.check_status()

    def check_status(self):

        if self.status == "Admin":
            #self.admin_settings()
            self.valid3.show()
        else:
            msg1 = QMessageBox()
            msg1.setWindowTitle("Warning")
            msg1.setText("Only an Admin has access")
            msg1.setIcon(QMessageBox.Warning)  # warning icon
            text = msg1.exec()

    def update_clicked(self):
        self.setting = 1
        self.check_status()

    def list_users_clicked(self):
        self.setting = 3
        self.check_status()

    def list_users(self):
        all_users = self.df_users.loc[:, ("id","username")]
        pop_msg = QMessageBox()
        pop_msg.setWindowTitle("List all users")
        pop_msg.setText(all_users.to_string(index = False))
        text = pop_msg.exec()

    def delete_clicked(self):
        self.setting = 2
        self.check_status()




class UsersGui(QMainWindow):

    def __init__(self):
        super(UsersGui,self).__init__()
        uic.loadUi('users_photo.ui', self)
        self.row_length = 6
        self.show()
        self.load_users_data()
        self.id = 0

        self.login_win = verify()
        self.check = 0

        self.login_win.btn_login.clicked.connect(self.login_clicked)

    def load_users_data(self):
        self.df_users = pd.read_excel('Project.xlsx', sheet_name='users')
        row_index = -1
        for i in range(len(self.df_users)):
            column_index = i % self.row_length
            if column_index == 0:
                row_index += 1

            user = QLabel()
            user.setPixmap(QPixmap(self.df_users.photo_path[i]))
            user.setScaledContents(True)
            user.setFixedWidth(200)
            user.setFixedHeight(200)
            user.mousePressEvent = lambda e, id=self.df_users.id[i]: self.show_and_save(id)
            self.layout_users.addWidget(user, row_index, column_index)  # keep

    def show_and_save(self,id):
        self.login_win.show()
        self.id = id

    def login_clicked(self):
        self.login_win.read_line()

        if self.df_users.iloc[int(self.id -1),1] == self.login_win.ad_username:
            self.check = self.check +1
        else:
            self.login_win.le_msg_2.setText("Username not valid")

        if self.df_users.iloc[int(self.id -1),2] == self.login_win.ad_password:
            self.check = self.check +1
        else:
            self.login_win.le_msg_3.setText("Password not valid")

        if self.check ==2:
            self.check =0
            self.login_win.close()
            self.login_win.clear_line()
            self.show_user(self.id)
        else:
            self.login_win.le_msg.setText("Invalid credentials entered")
            self.login_win.clear_line()
            self.check =0

    def refresh(self):
        self.load_users_data()
        self.close()
        self.show()



    def show_user(self, id):
        self.show_user_gui = ShowUserGui(id)



app = QApplication([])
window = UsersGui()
app.exec()
