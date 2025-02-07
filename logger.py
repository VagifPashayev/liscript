import tkinter as tk

class Logger:
    def __init__(self):
        self.log_window = None
        self.log_text = None
        self.root = None  # Store reference to root

    def init_gui(self, root):
        """Initializes GUI log panel inside the main window."""
        self.root = root  # Store root reference
        self.log_window = tk.Frame(root)
        self.log_window.pack(fill=tk.BOTH, expand=True)

        self.log_text = tk.Text(self.log_window, height=15, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def log(self, message):
        """Appends a message to the log and refreshes the UI."""
        if self.log_text:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message + "\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
            self.root.update_idletasks()  # Refresh GUI immediately after appending the log entry
        print(message)  # Mirror to console for debugging

# Global logger instance
logger = Logger()
log = logger.log  # Convenience alias for calling log()
