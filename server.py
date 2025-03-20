from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
import threading
import requests
import os
import datetime

# XML Database File
DB_FILE = "notes.xml"

# XML existing file check
def init_db():
    if not os.path.exists(DB_FILE):
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(DB_FILE)

# Get current timestamp
def get_current_timestamp():
    return datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")

# Add new note
def add_note(topic, note_name, text, timestamp=None):
    tree = ET.parse(DB_FILE)
    root = tree.getroot()

    if timestamp is None:
        timestamp = get_current_timestamp()

    topic_elem = None
    for t in root.findall("topic"):
        if t.attrib["name"] == topic:
            topic_elem = t
            break

    if topic_elem is None:
        topic_elem = ET.SubElement(root, "topic", {"name": topic})

    note_elem = ET.SubElement(topic_elem, "note", {"name": note_name})
    text_elem = ET.SubElement(note_elem, "text")
    text_elem.text = text
    timestamp_elem = ET.SubElement(note_elem, "timestamp")
    timestamp_elem.text = timestamp

    tree.write(DB_FILE)
    return f"Note added under topic '{topic}'."

# Retrieve notes
def get_notes(topic):
    tree = ET.parse(DB_FILE)
    root = tree.getroot()

    for t in root.findall("topic"):
        if t.attrib["name"] == topic:
            notes = []
            for note in t.findall("note"):
                note_data = {
                    "name": note.attrib["name"],
                    "text": note.find("text").text,
                    "timestamp": note.find("timestamp").text,
                }
                notes.append(note_data)
            return notes
    return f"No notes found for topic '{topic}'."

# Search Wikipedia database and save in XML DB
def fetch_wikipedia_data(topic):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{topic}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        summary = data.get("extract", "No summary available.")
        link = data.get("content_urls", {}).get("desktop", {}).get("page", "No link available.")

        timestamp = get_current_timestamp()
        wiki_note = f"{summary}\n\nRead more: {link}"
        add_note(topic, "Wikipedia Summary", wiki_note, timestamp)

        return {"summary": summary, "link": link}
    else:
        return f"Could not find Wikipedia data for '{topic}'."

# Multi-threaded XML-RPC server
class ThreadingXMLRPCServer(SimpleXMLRPCServer):
    #This is a multi-threaded XML-RPC server to handle multiple clients at once
    def process_request_thread(self, request, client_address):
        #This handle each request in a new thread
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except Exception:
            self.handle_error(request, client_address)
            self.shutdown_request(request)

    def process_request(self, request, client_address):
        #This start a new thread for each incoming request
        thread = threading.Thread(target=self.process_request_thread, args=(request, client_address))
        thread.daemon = True
        thread.start()

# Start server
def run_server():
    init_db()
    server = ThreadingXMLRPCServer(("localhost", 8000), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)
    server.register_function(add_note, "add_note")
    server.register_function(get_notes, "get_notes")
    server.register_function(fetch_wikipedia_data, "fetch_wikipedia_data")

    print("Multi-threaded XML-RPC server is running on port 8000...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
