class User():

    def __init__(self, id, first_name, password, last_name, username, account_type_id = "", email = "", created_on = "", active = ""):
        self.id = id
        self.first_name = first_name
        self.password = password
        self.last_name = last_name
        self.username = username
        self.account_type_id = account_type_id
        self.email = email
        self.created_on = created_on
        self.active = active
            