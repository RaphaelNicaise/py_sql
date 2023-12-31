import mysql.connector
import pandas as pd

c = 0
cnx = mysql.connector.MySQLConnection(user='root',password='',host='localhost',
                                      database='PruebasPython',port='3306')
cursor = cnx.cursor()
while (True): 
    try:
        print("----| System Users |----")
        print("Option 1 - Insert User")
        print("Option 2 - Select Users")
        print("Option 3 - Select Specific User ")
        print("Option 4 - Average")
        print("Option 5 - Delete a User")
        print("Option 6 - Quit")
        choice = int(input("-> "))
        if choice == 1:
            print("Insert User ")
            while (True):
                name = input("Insert your name: ")
                if name.lower() == 'quit':
                    break
                surname = input("Insert your surname: ")
                if surname.lower() == 'quit':
                    break
                age_input = (input("Insert your age: "))
                if age_input.lower() == 'quit':
                    break
                age = int(age_input)
                cursor.callproc("INSERT_USER",(name,surname,age))
                print(f"The user {name} {surname} was added correctly!")
                print("|-----------------------------------------------|")
                cnx.commit()
                print("to leave write quit") 
                    
        elif choice == 2:
            cursor.execute("select * from user")
            users = cursor.fetchall()
            users_df = pd.DataFrame(users,columns=['ID','Name','Surname','Age'])
            print(users_df)
        
        elif choice == 3:
            print("Write the Name or/and Surname")
            var = input("----> ")
            cursor.execute(f"SELECT * FROM pruebaspython.user where concat(name,' ',surname) like '%{var}%'")
            userslike = cursor.fetchall()
            for i in userslike:
                c += 1
            if (len(userslike)) > 0: 
                userslike_df = pd.DataFrame(userslike, columns=['ID', 'Name', 'Surname', 'Age'])    
                 
                print(f"{c} Rows Returned")
                print(userslike_df)
               
            else:
                print(f"There's no user like {var}")  
            c = 0
        elif choice == 4:
            cursor.execute("SELECT avg(age) FROM pruebaspython.user")
            avg_age = cursor.fetchone()[0]
            print(f"The average age is: {round(avg_age)}")       
        elif choice == 5:
                print("Delete the user with the Complete Name & Surname")
                
                var = input("----> ")
                cursor.execute(f"select * from user where concat(name,' ',surname) like '{var}' ")
                
                users = cursor.fetchall()
                cnx.commit()
                print(f"User {var} gonna be deleted") 
                    
                resp = input("Are you sure you want to delete these Users? Y/N -> ")
                if resp.lower() == 'y':  
                    cursor.execute(f"delete from pruebaspython.user where concat(name,' ',surname) like '{var}' ")
                    cnx.commit()
                    print(f"User {var} deleted") 
    
        elif choice == 6:
            print("You are leaving the program, Goodbye")
            break
    except ValueError:
        print("You put a wrong character, Try again")    
cursor.close()
cnx.close()

