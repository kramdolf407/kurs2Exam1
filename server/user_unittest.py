from Users import User
from Users import CollectionOfUsers
import unittest

users = CollectionOfUsers()

users.add_user("Peter", "abc123", "peter@mail", "p")
users.add_user("Lars", "secure12", "lars@mail", "L")

class Tester(unittest.TestCase):
    def test_user(self):
        var = users.doesThisUserExistAndNotActive("Peter", "abc123")
        self.assertTrue(var, msg="This user did not exist")

if __name__ == '__main__':
    unittest.main()