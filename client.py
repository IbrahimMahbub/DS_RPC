import xmlrpc.client

# Connect to the XML-RPC server
server = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")

def add_note():
    topic = input("Enter topic: ")
    note_name = input("Enter note title: ")
    text = input("Enter note text: ")
    timestamp = input("Enter timestamp (e.g., MM/DD/YY - HH:MM:SS): ")

    response = server.add_note(topic, note_name, text, timestamp)
    print(response)

def get_notes():
    topic = input("Enter topic to fetch notes: ")
    notes = server.get_notes(topic)

    if isinstance(notes, list):
        print(f"Notes for '{topic}':")
        for note in notes:
            print(f"\nTitle: {note['name']}")
            print(f"Text: {note['text']}")
            print(f"Timestamp: {note['timestamp']}")
    else:
        print(notes)

def fetch_wikipedia():
    topic = input("Enter topic to search Wikipedia: ")
    response = server.fetch_wikipedia_data(topic)

    if isinstance(response, dict):
        print("\nWikipedia Summary:")
        print(response["summary"])
        print("\nRead more:", response["link"])
    else:
        print(response)

def main():
    while True:
        print("\n--- Notebook Client ---")
        print("1. Add Note")
        print("2. Retrieve Notes")
        print("3. Fetch Wikipedia Info")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_note()
        elif choice == "2":
            get_notes()
        elif choice == "3":
            fetch_wikipedia()
        elif choice == "4":
            print("Exiting client.")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
