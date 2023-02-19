# SQL
import sqlite3
db = sqlite3.connect('data/ebookstore.db')
cursor = db.cursor()

# create table called 'books'
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books(
        id INTEGER UNIQUE PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        qty INTEGER NOT NULL)
""")

# add books to db
li_books = [
    (3001, 'A Tale of Two Cities', 'Charles Dickens', 30),
    (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40),
    (3003, 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', 25),
    (3004, 'The Lord of the Rings', 'J.R.R. Tolkien', 37),
    (3005, 'Alice in Wonderland', 'Lewis Carroll', 12)
]


cursor.executemany("""
    INSERT INTO books(id, title, author, qty)
    VALUES (?,?,?,?)""",
    li_books)
db.commit()


# Book class for default output
class Book(object):

    def __init__(self, id, title, author, qty):
        self.id = id
        self.title = title
        self.author = author
        self.qty = qty

    def get_qty(self):
        return self.qty

    def __str__(self):
        output = '\n───────────────────────────────────────────────\n'
        output += f'Title: {self.title}\n'
        output += f'Author: {self.author}\n'
        output += '───────────────────────────────────────────────'
        return output


# add new book to db
def enter_book():
    try:
        id = int(input('ID: '))

        title = input('Title: ')
        author = input('Author: ')
        qty = int(input('Quantity: '))

        cursor.execute("""
            INSERT INTO books(id, title, author, qty)
            VALUES(?,?,?,?) """,
            [id, title, author, qty])
        db.commit()

        print(f'\n{title} by {author} has successfully been added to database.')

    # raise Exceptions
    except Exception as e:
        db.rollback()
        raise e

    # return to menu
    finally:
        return


# update book information
def update_book():
    while True:
        id_input = int(input('Book ID: '))

        # display book information
        try:
            cursor.execute("""
                SELECT id, title, author, qty
                FROM books
                WHERE id=?""",
                [id_input])

            # display results
            results = cursor.fetchone()
            book = Book(results[0], results[1], results[2], results[3])
            print(book)

            # update options
            options = input("""
    What would you like to update?
    1. Title
    2. Author
    3. Quantity
    """)

            # update title
            if options == '1':
                try:
                    new_title = input('New title: ')

                    cursor.execute("""
                        UPDATE books
                        SET title=?
                        WHERE id=?""",
                        [new_title, id_input])
                    db.commit()

                    # display new book information
                    cursor.execute("""
                        SELECT id, title, author, qty
                        FROM books
                        WHERE id=?""",
                        [id_input])

                    results = cursor.fetchone()
                    book = Book(results[0], results[1], results[2], results[3])
                    print(book)

                # raise Exceptions
                except Exception as e:
                    db.rollback()
                    raise e

                # exit to menu
                finally:
                    return

            # update author
            if options == '2':
                try:
                    new_author = input('New author: ')

                    cursor.execute("""
                        UPDATE books
                        SET author=?
                        WHERE id=?""",
                        [new_author, id_input])
                    db.commit()

                    # display new book information
                    cursor.execute("""
                        SELECT id, title, author, qty
                        FROM books
                        WHERE id=?""",
                        [id_input])

                    results = cursor.fetchone()
                    book = Book(results[0], results[1], results[2], results[3])
                    print(book)

                # raise Exceptions
                except Exception as e:
                    db.rollback()
                    raise e

                # exit to menu
                finally:
                    return

            # update quantity
            if options == '3':
                try:
                    # current quantity
                    cursor.execute("""
                        SELECT qty
                        FROM books
                        WHERE id=?""",
                        [id_input])

                    qty = cursor.fetchone()
                    current_qty = qty[0]
                    print(f'\nCurrent quantity: {current_qty}')

                    # user options for editing quantity
                    while True:
                        chg_qty = input("""
        What would you like to do?
        1. Add stock
        2. Reduce stock
        3. Change total stock
        """)

                        # add stock
                        if chg_qty == '1':
                            try:
                                add_stock = int(input('Add quantity: ')) + current_qty

                                cursor.execute("""
                                    UPDATE books
                                    SET qty=?
                                    WHERE id=?""",
                                    [add_stock, id_input])
                                db.commit()

                                # display new quantity
                                cursor.execute("""
                                    SELECT qty
                                    FROM books
                                    WHERE id=?""",
                                    [id_input])

                                new_qty = cursor.fetchone()
                                int_new_qty = new_qty[0]
                                print(f'\nNew quantity: {int_new_qty}')

                            except Exception as e:
                                db.rollback()
                                raise e

                            finally:
                                return

                        if chg_qty == '2':
                            try:
                                remove_stock = current_qty - int(input('Remove quantity: '))

                                cursor.execute("""
                                    UPDATE books
                                    SET qty=?
                                    WHERE id=?""",
                                    [remove_stock, id_input])
                                db.commit()

                                # display new quantity
                                cursor.execute("""
                                    SELECT qty
                                    FROM books
                                    WHERE id=?""",
                                    [id_input])

                                new_qty = cursor.fetchone()
                                int_new_qty = new_qty[0]
                                print(f'\nNew quantity: {int_new_qty}')

                            except Exception as e:
                                db.rollback()
                                raise e

                            finally:
                                return

                        # update total quantity
                        if chg_qty == '3':
                            try:
                                chg_stock = int(input('New quantity: '))

                                cursor.execute("""
                                    UPDATE books
                                    SET qty=?
                                    WHERE id=?""",
                                    [chg_stock, id_input])
                                db.commit()

                                # display new quantity
                                cursor.execute("""
                                    SELECT qty
                                    FROM books
                                    WHERE id=?""",
                                    [id_input])

                                new_qty = cursor.fetchone()
                                int_new_qty = new_qty[0]
                                print(f'\nNew quantity: {int_new_qty}')

                            except Exception as e:
                                db.rollback()
                                raise e

                            finally:
                                return

                        # error handling
                        else:
                            print('Let\'s try again.')
                            continue

                except Exception as e:
                    db.rollback()
                    raise e

                finally:
                    break

        except Exception as e:
            db.rollback()
            raise e

        finally:
            break


# delete book
def del_book():
    while True:
        try:
            id_input = int(input('Book ID: '))

            cursor.execute("""
                SELECT id, title, author, qty
                FROM books
                WHERE id=?""",
                [id_input])

            result = cursor.fetchone()

            # error if book does not exist
            if result is None:
                print('\nThere is no book with that ID in our database.')
                break

            else:
                book = Book(result[0], result[1], result[2], result[3])
                print(book)

                # check selected book is correct
                correct_book = input(f'Is this the correct book? (Y/N)\n')

                if correct_book.upper() == 'Y':
                    cursor.execute("""
                        DELETE FROM books
                        WHERE id=?""",
                        [id_input])
                    db.commit()

                    print(f'{result[1]} by {result[2]} has been successfully deleted from the database.')

                else:
                    print('Okay, let\'s try again.')
                    break

        except Exception as e:
            db.rollback()
            raise e

        finally:
            break


# search for a specific book
def search_book():
    while True:
        options = input("""
Search by:
1. ID number
2. Title
3. Author
""")

        # search by ID
        if options == '1':
            try:
                search = input('Book ID: ')

                cursor.execute("""
                    SELECT id, title, author, qty
                    FROM books
                    WHERE id=?""",
                    [search])

                # display results
                results = cursor.fetchone()
                book = Book(results[0], results[1], results[2], results[3])
                print(book)

            except Exception as e:
                db.rollback()
                raise e

            finally:
                break

        # search by title
        if options == '2':
            try:
                search = input('Title: ')

                cursor.execute("""
                    SELECT id, title, author, qty
                    FROM books
                    WHERE title=?""",
                    [search])

                # display books
                results = cursor.fetchall()
                for row in results:
                    book = Book(row[0], row[1], row[2], row[3])
                    print(book)

                # if no books by that name
                if len(results) == 0:
                    print('There are no books by that name in our database.')

            except Exception as e:
                db.rollback()
                raise e

            finally:
                break

        # search by author
        if options == '3':
            try:
                search = input('Author: ')

                cursor.execute("""
                    SELECT id, title, author, qty
                    FROM books
                    WHERE author=?""",
                    [search])

                # display results
                results = cursor.fetchall()
                for row in results:
                    book = Book(row[0], row[1], row[2], row[3])
                    print(book)

                # if no author by that name
                if len(results) == 0:
                    print('There is no author by that name in our database.')

            except Exception as e:
                db.rollback()
                raise e

            finally:
                break

        # error handling
        else:
            print('That\'s not an option. Please try again.')
            continue


# user menu
while True:
    menu = input("""
What would you like to do?
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
""")

    # enter book
    if menu == '1':
        enter_book()
        continue

    # update book
    if menu == '2':
        update_book()
        continue

    # delete book
    if menu == '3':
        del_book()
        continue

    # search books
    if menu == '4':
        search_book()
        continue

    # exit
    if menu == '0':
        print('Goodbye.')

        db.close()
        exit()

    # error handling
    else:
        print('Whoops, something went wrong. Please try again.')
        continue
