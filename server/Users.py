
class User:
    def __init__(self,username_,password_,email_,name_): # constructor for User-class
        self.username = username_
        self.password = password_
        self.email = email_
        self.name = name_
        self.activeInChat = False

    def isTheUser(self,username_,password_): # does a specific user match (username && passwd)?
        if password_ == self.password and username_ == self.username:
            return True
        else:
            return False

class CollectionOfUsers:
    def __init__(self):
        self.list_of_users = [] # a list for User-objects

    def add_user(self,username_,password_,email_,name_): # add a user to list_of_users
        usernameExists = False
        for user in self.list_of_users:
            if user.username == username_:
                usernameExists = True # if username already exist, we break --> and return False
                break
        if usernameExists == True:
            return False
        else:
            user = User(username_,password_,email_,name_) # if username is available, we add the user
            self.list_of_users.append(user)
            return True

    def doesThisUserExistAndNotActive(self,username_,password_):
        for user in self.list_of_users:
            if user.isTheUser(username_,password_):
                if user.activeInChat == False:  # if the user exist (in RAM), and activeInChat is False, we set True
                    user.activeInChat = True
                    return True
                else:
                    return False
        return False

    def inactiveUser(self,usernameToInactive): # function to disable a user in the chat
        for user in self.list_of_users:
            if user.username == usernameToInactive:
                user.activeInChat = False

    def remove_user(self,username_):
        for i in range(len(self.list_of_users)):
            if self.list_of_users[i].username == username_:
                self.list_of_users.pop(i) # we remove the specific user from the list
                return True

        return False

    def getUserObjByUsername(self,username_): # search the list of user-objects to match on username
        for i in range(len(self.list_of_users)):
            if self.list_of_users[i].username == username_:
                return self.list_of_users[i]

        return "non"

    def readUsersFromFile(self, file):
        try:
            file = open(file,'r') # (this need to be "server/users.txt")
            allLines = file.read().split('\n') # reading the entire text file to one variable (list)
            file.close()
        except:
            return False

        index_of_current_line = 0 # this index-variable will go through the list, one text line at a time

        while True:
            username = allLines[index_of_current_line] # username, password, email, name and 1 empty line
            index_of_current_line+=1
            if username == "":
                return True

            password = allLines[index_of_current_line]
            index_of_current_line += 1
            if password == "":
                return False

            email = allLines[index_of_current_line]
            index_of_current_line += 1
            if email == "":
                return False

            name = allLines[index_of_current_line]
            index_of_current_line += 1
            if name == "":
                return False

            emptyLine = allLines[index_of_current_line]
            index_of_current_line+=1
            if emptyLine != "":
                return False

            self.add_user(username,password,email,name)

            if index_of_current_line == len(allLines):
                return True


    def writeUsersToFile(self, file): # writing the content of the user-list in RAM to file
        allContent = ""

        for user in self.list_of_users:
            allContent+=user.username+"\n"
            allContent+=user.password+"\n"
            allContent+=user.email+"\n"
            allContent+=user.name+"\n"
            allContent+="\n"

        try:
            file = open(file,'w') # this need to be "server/users.txt"
            file.write(allContent)  # opening the txt file in write mode, adding the user database (the latest)
            file.close()
            return True
        except:
            return False
