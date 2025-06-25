# models/User.py
from piccolo.table import Table
from piccolo.columns import Varchar

class AppUser(Table):
    name = Varchar()
