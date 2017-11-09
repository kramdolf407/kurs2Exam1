from Users import User
from Users import CollectionOfUsers
import unittest



class Tester(unittest.TestCase):

    def test_user(self):

        users = CollectionOfUsers()
        users.add_user("Peter", "abc123", "peter@mail", "p")
        users.add_user("Lars", "secure12", "lars@mail", "L")

        users.writeUsersToFile("test.txt")
        users.list_of_users =[]
        users.readUsersFromFile("test.txt")

        self.assertEqual(users.list_of_users[0].username, "Peter", msg="username is wrong")
        self.assertEqual(users.list_of_users[0].password, "abc123", msg="password is wrong")
        self.assertEqual(users.list_of_users[0].email, "peter@mail", msg="email is wrong")
        self.assertEqual(users.list_of_users[0].name, "p", msg="name is wrong")

        self.assertEqual(users.list_of_users[1].username, "Lars", msg="username is wrong")
        self.assertEqual(users.list_of_users[1].password, "secure12", msg="password is wrong")
        self.assertEqual(users.list_of_users[1].email, "lars@mail", msg="email is wrong")
        self.assertEqual(users.list_of_users[1].name, "L", msg="name is wrong")

if __name__ == '__main__':
    unittest.main()