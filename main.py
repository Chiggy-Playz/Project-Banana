try:
    from mysql.connector import connect
    from setup import setup_tables
    import os
    from tabulate import tabulate
except ModuleNotFoundError:
    print("Dependency not found. Please run 'pip install -r requirements.txt' to install all dependencies.")
    quit()


def cls():
    # Inter platform clear screen
    os.system("cls" if os.name == "nt" else "clear")


db = connect(
    host="localhost",
    user="root",
    password="1234",
)

cursor = db.cursor()

setup_tables(cursor)
cls()
# Display computer list
# Edit computer details
# Show software list
# Edit software details
# Edit current users
# Log out a pc
# Create a new user on a given pc

while True:
    try:
        cls()
        print("Welcome to Banana Cyber Cafe".center(100), "\n\n")
        print("Please choose an operation from the following list:- ")
        print("1. Show computer list")
        print("2. Manage computers")
        print("3. Show software list")
        print("4. Manage software")
        print("5. Show user list")
        print("6. Manage users")
        print("7. Log out a computer")
        print("8. Power off a computer")
        print("9. Exit")
        print()
        choice = input("Enter the number for the operation: ")

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 10. Press enter to continue.")
            input()
            continue

        if choice == 1:
            cursor.execute("SELECT * FROM computers;")
            all_computers = cursor.fetchall()
            # Convert the tuples into a dictionary
            all_computers = [
                {
                    "id": computer[0],
                    "name": computer[1],
                    "IP Address": computer[2],
                    "Status": computer[3],
                }
                for computer in all_computers
            ]
            cls()
            # No rows found
            if not all_computers:
                input("No computers found. Press enter to continue.")
            else:
                input(tabulate(all_computers, headers="keys", tablefmt="psql"))
        elif choice == 2:
            cls()
            print("Please choose an operation from the following list:- ")
            print("1. Add a new computer")
            print("2. Edit a computer")
            print("3. Delete a computer")
            print("4. Back")
            print()
            inner_choice = input("Enter the number for the operation: ")
            try:
                inner_choice = int(inner_choice)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4. Press enter to continue.")
                input()
                continue

            if inner_choice == 1:
                name = input("Enter the computer name: ")
                ip_address = input("Enter the computer IP address: ")
                cursor.execute(
                    """
                    INSERT INTO computers(name, ip_address, status) VALUES (%s, %s, %s);
                    """,
                    (name, ip_address, "Offline"),
                )
                db.commit()
                input("Computer added successfully. Press enter to continue.")
            elif inner_choice == 2:
                computer_identifier = input("Enter the computer's ID or Name or IP: ")
                cursor.execute(
                    """SELECT * FROM computers WHERE id = %s OR LOWER(name) LIKE %s OR ip_address = %s;""",
                    (computer_identifier, f"%{computer_identifier.lower()}%", computer_identifier),
                )
                computer = cursor.fetchone()
                if computer:
                    print("Current details:")
                    print("ID:", computer[0])
                    print("Name:", computer[1])
                    print("IP Address:", computer[2])
                    print("Status:", computer[3])
                    print()
                    print("Enter the new details or press ctrl + c to abort")
                    new_name = input("New Name: ")
                    new_ip_address = input("New IP Address: ")
                    new_status = input("New Status: ")
                    cursor.execute(
                        """
                        UPDATE computers
                        SET name = %s, ip_address = %s, status = %s
                        WHERE id = %s
                        """,
                        (new_name, new_ip_address, new_status, computer[0]),
                    )
                    db.commit()
                    input("Computer updated successfully. Press enter to continue.")
                else:
                    input("Computer not found. Press enter to continue.")
            elif inner_choice == 3:
                computer_identifier = input("Enter the computer's ID or Name or IP: ")
                cursor.execute(
                    """SELECT * FROM computers WHERE id = %s OR name LIKE %s OR ip_address = %s;""",
                    (computer_identifier, f"%{computer_identifier.lower()}%", computer_identifier),
                )
                computer = cursor.fetchone()
                if computer:
                    cursor.execute("DELETE FROM computers WHERE id = %s;", (computer[0],))
                    db.commit()
                    input("Computer deleted successfully. Press enter to continue.")
                else:
                    input("Computer not found. Press enter to continue.")
            elif inner_choice == 4:
                continue
        elif choice == 3:
            cls()
            print("Please choose an operation from the following list:- ")
            print("1. See software installed on a specific PC.")
            print("2. See software installed on all PCs.")
            print("3. Show all PCs with a specific software installed.")
            print("4. Back")
            print()
            inner_choice = input("Enter the number for the operation: ")
            try:
                inner_choice = int(inner_choice)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 4. Press enter to continue.")
                input()
                continue

            if inner_choice == 1:
                computer_identifier = input("Enter the computer's ID or Name or IP: ")
                cursor.execute(
                    """SELECT * FROM computers WHERE id = %s OR name LIKE %s OR ip_address = %s;""",
                    (computer_identifier, f"%{computer_identifier.lower()}%", computer_identifier),
                )
                computer = cursor.fetchone()
                if computer:
                    cursor.execute(
                        """
                        SELECT name, version FROM software_installed WHERE computer_id = %s;
                        """,
                        (computer[0],),
                    )
                    software = cursor.fetchall()
                    software = [
                        {
                            "Name": software[0],
                            "Version": software[1],
                        }
                        for software in software
                    ]
                    cls()
                    # No rows found
                    if not software:
                        input("No software found. Press enter to continue.")
                    else:
                        input(tabulate(software, headers="keys", tablefmt="psql"))
                else:
                    input("Computer not found. Press enter to continue.")
            elif inner_choice == 2:
                cursor.execute(
                    """
                    SELECT computers.name, computers.ip_address, software_installed.name, software_installed.version
                    FROM software_installed
                    INNER JOIN computers ON software_installed.computer_id = computers.id
                    ORDER BY computers.name;
                    """
                )
                software = cursor.fetchall()
                software = [
                    {
                        "Computer Name": software[0],
                        "Computer IP": software[1],
                        "Software Name": software[2],
                        "Software Version": software[3],
                    }
                    for software in software
                ]
                cls()
                # No rows found
                if not software:
                    input("No software found. Press enter to continue.")
                else:
                    input(tabulate(software, headers="keys", tablefmt="psql"))
            elif inner_choice == 3:
                software_name = input("Enter the software name: ")
                cursor.execute(
                    """
                    SELECT computers.name, computers.ip_address, software_installed.name, software_installed.version
                    FROM software_installed
                    INNER JOIN computers ON software_installed.computer_id = computers.id
                    WHERE software_installed.name = %s
                    ORDER BY computers.name;
                    """,
                    (f"%{software_name}%"),
                )
                software = cursor.fetchall()
                software = [
                    {
                        "Computer Name": software[0],
                        "Computer IP": software[1],                  
                        "Name": software[2],
                        "Version": software[3],
                    }
                    for software in software
                ]
                cls()
                # No rows found
                if not software:
                    input("No software found. Press enter to continue.")
                else:
                    input(tabulate(software, headers="keys", tablefmt="psql"))
            elif inner_choice == 4:
                continue
        elif choice == 4:
            cls()
            print("Please choose an operation from the following list:- ")
            print("1. Install software on a specific PC.")
            print("2. Install software on all PCs.")
            print("3. Remove software from a specific PC.")
            print("4. Remove software from all PCs.")
            print("5. Back")
            print()
            inner_choice = input("Enter the number for the operation: ")
            try:
                inner_choice = int(inner_choice)
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5. Press enter to continue.")
                input()
                continue
            
            if inner_choice == 1:
                computer_identifier = input("Enter the computer's ID or Name or IP: ")
                cursor.execute(
                    """SELECT * FROM computers WHERE id = %s OR name LIKE %s OR ip_address = %s;""",
                    (computer_identifier, f"%{computer_identifier.lower()}%", computer_identifier),
                )
                computer = cursor.fetchone()
                if computer:
                    software_name = input("Enter the software name: ")
                    software_version = input("Enter the software version: ")
                    cursor.execute(
                        """
                        INSERT INTO software_installed (computer_id, name, version)
                        VALUES (%s, %s, %s);
                        """,
                        (computer[0], software_name, software_version),
                    )
                    db.commit()
                    input("Software installed successfully. Press enter to continue.")
                else:
                    input("Computer not found. Press enter to continue.")
            elif inner_choice == 2:
                software_name = input("Enter the software name: ")
                software_version = input("Enter the software version: ")
                cursor.execute("SELECT id FROM computers;")
                all_computers = cursor.fetchall()
                cursor.executemany(
                    "INSERT INTO software_installed (computer_id, name, version);",
                    [(computer[0], software_name, software_version) for computer in all_computers],
                )
                db.commit()
                input(f"Software installed on {len(all_computers)} successfully. Press enter to continue.")
            elif inner_choice == 3:
                computer_identifier = input("Enter the computer's ID or Name or IP: ")
                cursor.execute(
                    """SELECT * FROM computers WHERE id = %s OR name LIKE %s OR ip_address = %s;""",
                    (computer_identifier, f"%{computer_identifier.lower()}%", computer_identifier),
                )
                computer = cursor.fetchone()
                if computer:
                    software_name = input("Enter the software name: ")
                    cursor.execute(
                        """
                        DELETE FROM software_installed
                        WHERE computer_id = %s AND name = %s;
                        """,
                        (computer[0], software_name),
                    )
                    db.commit()
                    input("Software removed successfully. Press enter to continue.")
                else:
                    input("Computer not found. Press enter to continue.")
            elif inner_choice == 4:
                software_name = input("Enter the software name: ")
                cursor.execute(
                    """
                    DELETE FROM software_installed
                    WHERE name = %s;
                    """,
                    (software_name),
                )
                db.commit()
                input("Software removed from all PCs successfully. Press enter to continue.")
            elif inner_choice == 5:
                continue

        elif choice == 9:
            break
        else:
            input("Invalid Choice. Please enter a number between 1 and 10. Press enter to continue.")
            cls()
    except KeyboardInterrupt:
        pass

cursor.close()
db.close()
print("Thank you for using Banana Cyber Cafe. Have a nice day :)")
