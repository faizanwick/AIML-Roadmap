name = input("Enter employee name: ")
age = int(input("Enter employee age: "))
salary = int(input("Enter employee salary: "))
designation = input("Enter employee designation: ")
e_status = input("Enter employement status: ")

print(f"My name is {name}. I am {age} years old and work as {designation}.")
print(f"""
    Employee name: {name}\n
    Designation: {designation}\n
    Salary: {salary:.2f}\n
    Employement Status: {e_status}
    """)
