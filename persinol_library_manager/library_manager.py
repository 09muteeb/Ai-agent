import json
import os

# File name for saving/loading the library
LIBRARY_FILE = "library.txt"

# Load library from file (if exists)
def load_library():
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            print("⚠ Error reading file. Starting with an empty library.")
            return []
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)
    print("📁 Library saved to file. Goodbye!")

# Add a book
def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    
    while True:
        try:
            year = int(input("Enter the publication year: ").strip())
            break
        except ValueError:
            print("❌ Please enter a valid year.")

    genre = input("Enter the genre: ").strip()
    read_status = input("Have you read this book? (yes/no): ").strip().lower()
    read = True if read_status == "yes" else False

    library.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    })

    print("✅ Book added successfully!")

# Remove a book
def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip()
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            print("✅ Book removed successfully!")
            return
    print("❌ Book not found.")

# Search for a book
def search_book(library):
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ").strip()
    query = input("Enter your search term: ").strip().lower()

    results = []
    if choice == "1":  # Search by title
        results = [b for b in library if query in b["title"].lower()]
    elif choice == "2":  # Search by author
        results = [b for b in library if query in b["author"].lower()]
    else:
        print("❌ Invalid choice.")
        return

    if results:
        print("\nMatching Books:")
        for i, b in enumerate(results, start=1):
            status = "Read" if b["read"] else "Unread"
            print(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {status}")
    else:
        print("❌ No matching books found.")

# Display all books
def display_all_books(library):
    if not library:
        print("📚 Your library is empty.")
        return
    print("\nYour Library:")
    for i, b in enumerate(library, start=1):
        status = "Read" if b["read"] else "Unread"
        print(f"{i}. {b['title']} by {b['author']} ({b['year']}) - {b['genre']} - {status}")

# Display statistics
def display_statistics(library):
    total_books = len(library)
    if total_books == 0:
        print("📊 No books in the library.")
        return
    read_books = sum(1 for b in library if b["read"])
    percentage_read = (read_books / total_books) * 100
    print(f"📊 Total books: {total_books}")
    print(f"📖 Percentage read: {percentage_read:.1f}%")

# Main menu loop
def main():
    library = load_library()
    while True:
        print("\n📚 Welcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_all_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            save_library(library)
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()