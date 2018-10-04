import json

class Persistence:
    def __init__(self):
        try:
            with open('users.json') as file:
                self.users = json.load(file)
        except FileNotFoundError:
            # Initialize for first start
            self.users = []

    # Registering a user
    def registerUser(self, id):
        self.users.append(id)
        self.save()

    # Unregistering a user
    def unregisterUser(self, id):
        self.users.remove(id)
        self.save()

    # Checking if user is registered
    def isRegisteredUser(self, id):
        return id in self.users

    # List all users
    def allUsers(self):
        return self.users

    # Save a user to file
    def save(self):
        with open('users.json', 'w') as outfile:
            json.dump(self.users, outfile)
