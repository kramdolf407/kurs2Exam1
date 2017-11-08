from Users import User
from Users import CollectionOfUsers
import unittest

users = CollectionOfUsers()

users.readUsersFromFile()

class Tester(unittest.TestCase):
    def test_user(self):
        var = users.doesThisUserExistAndNotActive("a", "a")
        self.assertTrue(var, msg="This user did not exist")

if __name__ == '__main__':
    unittest.main()