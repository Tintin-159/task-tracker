from database import Database

def main():
    db = Database()
    db.create_database()

    # Program starts here

    db.close()

if __name__ == '__main__':
    main()