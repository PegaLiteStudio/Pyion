from pynova import Person, PhoneNumber, EmailAddress, URL, Address

print("=== PyNova Demonstration ===")

# Smart data types

person = Person("Sahil Hossain")
phone = PhoneNumber("+919876543210")
email = EmailAddress("sahil@example.com")
website = URL("https://example.com/docs")
address = Address(
    city="Agartala",
    state="Tripura",
    country="India",
    postal_code="799001"
)

print("\nPerson:")
print(person.full_name)
print(person.initials)

print("\nPhone:")
print(phone.number)
print(phone.country_code)
print(phone.is_valid)

print("\nEmail:")
print(email.username)
print(email.domain)
print(email.is_valid)

print("\nWebsite:")
print(website.protocol)
print(website.domain)
print(website.is_secure)

print("\nAddress:")
print(address.formatted)

# repeat

print("\nRepeat demonstration:")

repeat 3:
    print("Welcome to PyNova!")

# safe

print("\nSafe demonstration:")

safe:
    number = int("not-a-number")
    print(number)

print("Program continues after the handled error.")

# wait

print("\nWait demonstration:")
print("Waiting...")
wait 2
print("Wait completed.")

# between

print("\nBetween demonstration:")

age = 25

if age between 18 and 60:
    print("Age is within the permitted range.")

print("\nPyNova demonstration completed.")
