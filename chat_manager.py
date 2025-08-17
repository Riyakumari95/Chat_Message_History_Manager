
# chat_manager.py
from collections import deque
from dataclasses import dataclass, asdict
from typing import List, Dict
import time, json, os

DATA_FILE = "chat_history.json"

@dataclass
class Message:
    text: str
    timestamp: float

class ChatManager:
    def __init__(self):
        self.incoming = deque()   # Queue for incoming messages
        self.sent: List[Message] = []            # Stack for sent messages
        self.redo_stack: List[Message] = []      # Stack for redo actions

    # --- Persistence ---
    def save(self):
        data = {
            "incoming": [{"text": m.text, "timestamp": m.timestamp} for m in self.incoming],
            "sent": [asdict(m) for m in self.sent],
            "redo": [asdict(m) for m in self.redo_stack],
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print("✔ Chat saved.")

    def load(self):
        if not os.path.exists(DATA_FILE):
            print("No save file yet.")
            return
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data: Dict = json.load(f)
        self.incoming = deque(Message(**m) for m in data.get("incoming", []))
        self.sent = [Message(**m) for m in data.get("sent", [])]
        self.redo_stack = [Message(**m) for m in data.get("redo", [])]
        print("✔ Chat loaded.")

    # --- Ops ---
    def send_message(self, text: str):
        msg = Message(text, time.time())
        self.incoming.append(msg)
        self.sent.append(msg)
        self.redo_stack.clear()  # invalidate redo after new action
        print(f"📩 Sent: {text}")

    def undo_message(self):
        if not self.sent:
            print("❌ No message to undo.")
            return
        msg = self.sent.pop()
        self.redo_stack.append(msg)
        print(f"↩️ Undo: '{msg.text}'")

    def redo_message(self):
        if not self.redo_stack:
            print("❌ Nothing to redo.")
            return
        msg = self.redo_stack.pop()
        self.sent.append(msg)
        print(f"🔁 Redo: '{msg.text}'")

    def view_history(self):
        if not self.sent:
            print("📭 No messages yet.")
            return
        print("\n--- Chat History ---")
        for i, msg in enumerate(self.sent, 1):
            ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg.timestamp))
            print(f"{i}) [{ts}] {msg.text}")
        print("--------------------")

def main():
    chat = ChatManager()
    while True:
        print("\n=== Chat Message Manager ===")
        print("1) Send Message")
        print("2) Undo Last")
        print("3) Redo")
        print("4) View History")
        print("5) Save")
        print("6) Load")
        print("7) Exit")
        ch = input("> ").strip()
        if ch == "1":
            chat.send_message(input("Message: "))
        elif ch == "2":
            chat.undo_message()
        elif ch == "3":
            chat.redo_message()
        elif ch == "4":
            chat.view_history()
        elif ch == "5":
            chat.save()
        elif ch == "6":
            chat.load()
        elif ch == "7":
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()
