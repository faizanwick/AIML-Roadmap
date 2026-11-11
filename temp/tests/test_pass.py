from app.cores.security import hash_password, verify_password

password = "0000000000000"

hashed = hash_password(password)

print(password)
print(hashed)
print(verify_password(password, hashed))
print(verify_password("World@hello", hashed))