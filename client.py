import xmlrpc.client
import datetime

# Connect to the XML-RPC server
server = xmlrpc.client.ServerProxy("http://localhost:8000/RPC2")

#Get current timestamp from the host 
def get_current_timestamp():
    return datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")

def add_note():
    topic = input("Enter topic: ")
    note_name = input("Enter note title: ")
    text = input("Enter note text: ")

    # Automatic timestamp fillup for timestamp form also allow manual inputs
    default_timestamp = get_current_timestamp()
    timestamp = input(f"Enter timestamp (default: {default_timestamp}): ").strip()
    if timestamp == "":
        timestamp = default_timestamp

    response = server.add_note(topic, note_name, text, timestamp)
    print(response)

def get_notes():
    topic = input("Enter topic to view available notes: ")
    notes = server.get_notes(topic)

    if isinstance(notes, list):
        print(f"\nNotes for '{topic}':")
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
        print("\n--- Ibrahim's Personal Notebook Application ---")
        print("1. Add note")
        print("2. View my notes")
        print("3. Wikipedia Search")
        print("4. Exit")

        choice = input("Choose an option to start: ")

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
            print("Invalid choice, try again from the list.")

if __name__ == "__main__":
    main()
