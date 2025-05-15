import tkinter as tk
from tkinter import ttk
import platform # To provide some platform-specific dummy apps
import subprocess # For launching applications
import os # For handling paths more robustly

class AppLauncher:
    """
    A simple application launcher GUI with dynamic filtering,
    application launching, and keyboard navigation.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Quick Launcher")
        
        # Configure style for a more modern look
        self.style = ttk.Style()
        self.style.theme_use('clam') 

        # --- Color Scheme & Fonts ---
        self.primary_bg = "#2E2E2E"    # Dark gray background
        self.secondary_bg = "#3C3C3C"  # Slightly lighter gray for entry/listbox
        self.text_color = "#E0E0E0"    # Light gray text
        self.accent_color = "#007ACC"  # Blue for selection/focus
        self.border_color = "#505050"  # Subtle border color
        self.error_color = "#FF6B6B"   # Red for error messages
        self.success_color = "#77DD77" # Green for success messages

        self.font_family = "Segoe UI" if platform.system() == "Windows" else "Helvetica"
        self.font_normal = (self.font_family, 11)
        self.font_large = (self.font_family, 12, "bold")
        self.font_small = (self.font_family, 9)

        self.root.configure(bg=self.primary_bg)
        
        # --- Center the window ---
        self.center_window(500, 500) # Increased height for status bar

        # --- Predefined applications (will be replaced by dynamic scanning) ---
        self.all_apps = [
            {'name': 'Notepad', 'path': 'notepad.exe'},
            {'name': 'Calculator', 'path': 'calc.exe'},
            {'name': 'Paint', 'path': 'mspaint.exe'},
            {'name': 'Wordpad', 'path': 'write.exe'},
            {'name': 'File Explorer', 'path': 'explorer.exe'},
            {'name': 'Command Prompt', 'path': 'cmd.exe'},
            {'name': 'Task Manager', 'path': 'taskmgr.exe'},
            {'name': 'Control Panel', 'path': 'control.exe'},
        ]
        # Add some platform-specific common apps for better demo
        if platform.system() == "Linux":
            self.all_apps.extend([
                {'name': 'Terminal', 'path': 'gnome-terminal'}, # Example, might vary
                {'name': 'Files (Nautilus)', 'path': 'nautilus'},
                {'name': 'Text Editor (gedit)', 'path': 'gedit'},
                {'name': 'Firefox', 'path': 'firefox'},
            ])
        elif platform.system() == "Darwin": # macOS
             self.all_apps.extend([
                {'name': 'Finder', 'path': 'open -a Finder'}, # Use 'open -a' for macOS apps
                {'name': 'Terminal', 'path': 'open -a Terminal'},
                {'name': 'TextEdit', 'path': 'open -a TextEdit'},
                {'name': 'Safari', 'path': 'open -a Safari'},
            ])
        
        # Sort apps by name for initial display
        self.all_apps.sort(key=lambda x: x['name'].lower())
        self.currently_displayed_apps = list(self.all_apps) # Keep track of filtered list

        # --- Main Frame ---
        self.main_frame = ttk.Frame(self.root, padding="15 15 10 15", style="Main.TFrame") # Reduced bottom padding
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.style.configure("Main.TFrame", background=self.primary_bg)

        # --- Input field ---
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(
            self.main_frame, 
            textvariable=self.search_var, 
            font=self.font_large,
            style="Search.TEntry"
        )
        self.search_entry.pack(pady=(0, 10), fill=tk.X) # Add some space below the entry
        self.search_entry.bind("<KeyRelease>", self.filter_apps) # Filter on any key release
        self.search_entry.bind("<Return>", self.launch_selected_app_from_entry) # Launch from entry on Enter
        self.search_entry.bind("<Down>", self.move_selection_down) # Navigate to listbox
        self.search_entry.focus_set() # Set focus to the entry field on startup

        # Style for Entry widget
        self.style.configure(
            "Search.TEntry",
            fieldbackground=self.secondary_bg,
            foreground=self.text_color,
            bordercolor=self.border_color,
            insertcolor=self.text_color, # Cursor color
            padding=10, # Inner padding
        )
        self.style.map(
            "Search.TEntry",
            bordercolor=[('focus', self.accent_color)],
        )


        # --- Listbox ---
        self.app_listbox = tk.Listbox(
            self.main_frame,
            font=self.font_normal,
            selectbackground=self.accent_color,
            selectforeground=self.text_color,
            background=self.secondary_bg,
            foreground=self.text_color,
            borderwidth=1,
            relief=tk.FLAT, # Flat border for a modern look
            highlightthickness=0, # No focus highlight border around listbox itself
            activestyle='none', # No underline or dot for active item
            height=10 # Initial height
        )
        self.app_listbox.pack(expand=True, fill=tk.BOTH)
        
        # Bind events for launching and navigation
        self.app_listbox.bind("<Double-Button-1>", self.launch_selected_app)
        self.app_listbox.bind("<Return>", self.launch_selected_app)
        self.app_listbox.bind("<Up>", self.move_selection_up)
        self.app_listbox.bind("<Down>", self.move_selection_down)

        # --- Status Bar ---
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root, # Add to root window, not main_frame
            textvariable=self.status_var, 
            font=self.font_small,
            padding="10 5 10 5", # Left/Right, Top/Bottom
            anchor=tk.W, # West align text
            background=self.primary_bg, # Match root background
            foreground=self.text_color
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.set_status("Type to search for applications.", "info")


        # --- Populate listbox initially ---
        self.update_listbox_display(self.all_apps)

    def center_window(self, width, height):
        """Centers the Tkinter window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.minsize(width, height) # Set minimum size

    def set_status(self, message, msg_type="info"):
        """Updates the status bar message and color."""
        self.status_var.set(message)
        if msg_type == "error":
            self.status_bar.configure(foreground=self.error_color)
        elif msg_type == "success":
            self.status_bar.configure(foreground=self.success_color)
        else: # info or default
            self.status_bar.configure(foreground=self.text_color)
        
        # Clear status after a delay, but not if it's an error message that should persist
        # or if the message is the default "Ready."
        if msg_type != "error" and message != "Ready.":
             self.root.after(5000, lambda: self.clear_status_if_not_persistent(message))


    def clear_status_if_not_persistent(self, original_message):
        """Clears the status bar if the current message is the original_message and not an error."""
        # Check if the current message is the one we set to clear, and it's not an error
        current_fg = str(self.status_bar.cget("foreground")) # Ensure string comparison
        
        if self.status_var.get() == original_message and current_fg != self.error_color:
            self.status_var.set("Ready.")
            self.status_bar.configure(foreground=self.text_color)


    def update_listbox_display(self, apps_to_display):
        """Clears and populates the listbox with the given list of apps."""
        self.app_listbox.delete(0, tk.END)  # Clear existing items
        self.currently_displayed_apps = [] # Reset the list of currently displayed apps
        for app in apps_to_display:
            self.app_listbox.insert(tk.END, app['name'])
            self.currently_displayed_apps.append(app) # Store the full app dict (name and path)
        
        # Select the first item if list is not empty
        if self.currently_displayed_apps:
            self.app_listbox.selection_set(0)
            self.app_listbox.activate(0)
            self.app_listbox.see(0) # Ensure the first item is visible
        else:
            # If no apps are displayed (e.g., after filtering yields no results)
            # update status but don't set to "Ready" immediately if it was an info message
            current_search = self.search_var.get()
            if current_search: # Only show "no results" if there's an active search
                self.set_status(f"No applications found matching '{current_search}'.", "info")
            # else: if search is empty, filter_apps handles the status


    def filter_apps(self, event=None):
        """Filters the application list based on the search entry text."""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            # If search term is empty, show all apps
            self.update_listbox_display(self.all_apps)
            self.set_status("Type to search for applications.", "info")
            return

        filtered_apps = [
            app for app in self.all_apps
            if search_term in app['name'].lower() # Simple substring matching
        ]
        self.update_listbox_display(filtered_apps)
        if filtered_apps:
             self.set_status(f"{len(filtered_apps)} application(s) found.", "info")
        # The 'else' case (no apps found) is handled by update_listbox_display


    def launch_selected_app_from_entry(self, event=None):
        """Handles Enter key press in the search entry. Launches the top selected item."""
        if self.app_listbox.size() > 0:
            # Ensure the first item is selected if nothing is explicitly selected
            if not self.app_listbox.curselection():
                self.app_listbox.selection_set(0)
                self.app_listbox.activate(0)
            self.launch_selected_app() # Call the common launch function
        else:
            self.set_status("No application selected or found to launch.", "error")


    def launch_selected_app(self, event=None):
        """Launches the selected application from the listbox."""
        selected_indices = self.app_listbox.curselection()
        if not selected_indices:
            # If nothing is selected but listbox has items, select the first one by default
            if self.app_listbox.size() > 0:
                self.app_listbox.selection_set(0)
                self.app_listbox.activate(0)
                selected_indices = (0,) # Use the first item
            else:
                self.set_status("No application selected to launch.", "error")
                return
        
        selected_index = selected_indices[0]
        
        # Get the app from the currently_displayed_apps list, which holds full dicts
        if 0 <= selected_index < len(self.currently_displayed_apps):
            app_to_launch = self.currently_displayed_apps[selected_index]
            app_name = app_to_launch['name']
            app_path = app_to_launch['path']
            
            self.set_status(f"Launching {app_name}...", "info")
            print(f"Attempting to launch: {app_name} (Path: {app_path})")
            
            try:
                # Platform-specific launching logic
                if platform.system() == "Darwin": # macOS
                    # 'open -a AppName' or 'open /path/to/App.app'
                    # subprocess.Popen expects a list of arguments
                    if app_path.startswith("open -a"):
                        subprocess.Popen(app_path.split())
                    else: # Assume it's a direct path to an executable or .app bundle
                        subprocess.Popen(['open', app_path])
                elif platform.system() == "Windows":
                    # For Windows, Popen with the direct path usually works for .exe
                    # os.startfile can be more general for opening files with associated apps
                    # For this launcher, direct Popen should be fine for executables.
                    subprocess.Popen(app_path)
                else: # Linux and other Unix-like
                    # Paths might be simple commands or full paths to executables
                    # If the path contains spaces or needs arguments, it should be handled
                    # For simple cases, splitting might not be necessary if it's a single command.
                    # However, if 'app_path' could contain arguments, splitting is safer.
                    # For now, assume app_path is the command/executable.
                    subprocess.Popen(app_path.split()) # Split if path includes arguments
                
                self.set_status(f"Successfully launched {app_name}.", "success")
                # Optionally, hide or close the launcher window after launch
                # self.root.withdraw() # Hides the window
                # self.root.destroy() # Closes the window
            except FileNotFoundError:
                error_msg = f"Error: App path not found for {app_name} ({app_path})."
                print(error_msg)
                self.set_status(error_msg, "error")
            except Exception as e:
                error_msg = f"Error launching {app_name}: {e}"
                print(error_msg)
                self.set_status(error_msg, "error")
        else:
            # This case should ideally not be reached if selection logic is correct
            self.set_status("Error: Selection index out of range.", "error")

    def move_selection_down(self, event=None):
        """Moves the selection in the listbox down by one."""
        if not self.app_listbox.winfo_viewable(): return # Do nothing if listbox not visible
        
        current_selection = self.app_listbox.curselection()
        list_size = self.app_listbox.size()

        if list_size == 0: return # No items in listbox

        if not current_selection: # If nothing selected, select the first item
            next_index = 0
        else:
            current_index = current_selection[0]
            next_index = current_index + 1
            if next_index >= list_size:
                next_index = list_size - 1 # Stay at the last item if already there
        
        self.app_listbox.selection_clear(0, tk.END)
        self.app_listbox.selection_set(next_index)
        self.app_listbox.activate(next_index)
        self.app_listbox.see(next_index) # Ensure the item is visible
        
        # If this event was triggered from the search_entry (by pressing Down arrow),
        # then transfer focus to the listbox.
        if event and event.widget == self.search_entry:
            self.app_listbox.focus_set()
        return "break" # Prevents default Tkinter handling for Down key, which might scroll etc.

    def move_selection_up(self, event=None):
        """Moves the selection in the listbox up by one."""
        if not self.app_listbox.winfo_viewable(): return

        current_selection = self.app_listbox.curselection()
        list_size = self.app_listbox.size()

        if list_size == 0: return

        if not current_selection: # If nothing selected, select the last item (or first)
            next_index = list_size -1 # Or 0, depending on desired behavior
        else:
            current_index = current_selection[0]
            next_index = current_index - 1
            if next_index < 0:
                next_index = 0 # Stay at the first item if already there
        
        self.app_listbox.selection_clear(0, tk.END)
        self.app_listbox.selection_set(next_index)
        self.app_listbox.activate(next_index)
        self.app_listbox.see(next_index)
        return "break" # Prevents default Tkinter handling for Up key


if __name__ == "__main__":
    root = tk.Tk()
    app = AppLauncher(root)
    root.mainloop()
