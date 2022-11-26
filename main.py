
# Supermarket Receipt generator
# Authors: Saurav Dhakal & Sakar Shrestha

import sqlite3

conn=sqlite3.connect("item.db")
cur=conn.cursor()
# Receipt Table
create_bill='''CREATE TABLE IF NOT EXISTS items(SN INT NOT NULL,ItemName VARCHAR(50) NOT NULL,Price INT NOT NULL,Quantity INT NOT NULL,Total INT NOT NULL)'''
cur.execute(create_bill)

# Inventory Table
item_collection='''CREATE TABLE IF NOT EXISTS items_collection(ItemId INT PRIMARY KEY, Name VARCHAR(50) NOT NULL, Price INT NOT NULL)'''
cur.execute(item_collection)

# Insert Into Invertory
# insert='''INSERT INTO items_collection(ItemId,Name,Price) VALUES (8,"Mayonnaise",350)'''
# cur.execute(insert)
# conn.commit()

# Check Inventory Values
# read = f'''SELECT * FROM items_collection WHERE ItemId=4'''
#
# result=cur.execute(read)
#
# for data in result:
#     n=data[1]
#     p=data[2]
#     print(f"Id: {data[0]}")
#     print(f"Name:",n)
#     print(f"Price:",p)


class Items:
    def __init__(self,name,quantity,price):
        self.name=name
        self.quantity=quantity
        self.price=price

    def totalFunction(self):
        return self.quantity*self.price

i=0
cost=0
#No. of Items in Cart
n=int(input("How many items are there? : "))
print("1. Chocolate\n2. Eggs\n3. Milk\n4. Lamb\n5. Ketchup\n6. Soda\n7. Doritoes\n8. Mayonnaise")
for items in range(n):
    entry=int(input("Enter corresponding number to add the items : "))
    i=i+1
    qua=int(input("Enter quantity : "))
    print("\n")
    # Read Name and corresponding Price from Inventory Table
    select_item = f'''SELECT * FROM items_collection WHERE ItemId={entry}'''
    getName=cur.execute(select_item)
    for itemi in getName:
        name=itemi[1]
        price=itemi[2]
    item1 = Items(name,qua,price)
    try:
        #Insert Into Receipt Table
        insert_script = f'''INSERT INTO items VALUES ({i},"{item1.name}",{item1.price},{item1.quantity},{item1.totalFunction()})'''
        cur.execute(insert_script)
        conn.commit()
    except:
        print("Can't Connect to database")

    cost+=item1.totalFunction(); # Calculate Total price of shopping
print("***********************"*5)
print("\t\t\t\t\t\t   Python Mart")
print("***********************"*5)
select_script = '''SELECT * FROM items''' # Read from Receipt Table
try:
    readvar=cur.execute(select_script)
except:
    print("Can't read data from the database")
print("\tS.N\t\t\t Name\t\t   Price\t      Quantity\t\tTotal")
#Display From Receipt Table
for data in readvar:
    # print(f"\t",data[0],"\t\t\t",data[1],"\t\t\t",data[2],"\t\t\t",data[3],"\t\t\t\t",data[4],"\t")
    print("\t", data[0], "\t\t\t",data[1], " "*(16-len(data[1])), data[2], " "*(17-len(str(data[2]))), data[3], " "*(16-len(str(data[3]))), data[4])
print("\n", " "*84, "=", cost)

delete_script= '''DELETE FROM items''' # Clear Receipt Table for next user
cur.execute(delete_script)
conn.commit()
conn.close()
