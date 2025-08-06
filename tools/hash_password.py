from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
password = input("Enter password to hash: ")
hashed = bcrypt.generate_password_hash(password).decode()
print("Hashed password:")
print(hashed)