"""
@author: Kanhaiya
"""


class Directory:
    def __init__(self, name, parent=None):
        # Initialize a directory with a name, parent directory (default is None), and empty children and files
        # dictionaries
        self.name = name
        self.parent = parent
        self.children = {}
        self.files = {}


class FileSystem:
    def __init__(self):
        # Initialize the file system with a root directory and set the current directory to the root
        self.root = Directory('/')
        self.current_dir = self.root
        self.help()  # Print help message at the start

    def print_prompt(self):
        # Print the current directory prompt
        print(f"{self.current_dir.name} $ ", end="")

    def mkdir(self, name):
        # Create a new directory with the given name in the current directory
        if name in self.current_dir.children:
            print(f"Directory {name} already exists.")
        else:
            self.current_dir.children[name] = Directory(name, self.current_dir)

    def cd(self, path):
        # Change the current directory based on the provided path
        if path == '/':
            self.current_dir = self.root
        elif path == '..':
            # Move to the parent directory if it exists
            if self.current_dir.parent is not None:
                self.current_dir = self.current_dir.parent
        elif path in self.current_dir.children:
            # Move to the specified child directory
            self.current_dir = self.current_dir.children[path]
        else:
            print(f"No such directory: {path}")

    def ls(self):
        # List the contents of the current directory
        for name in self.current_dir.children:
            print(name + '/')  # Append '/' for directories
        for name in self.current_dir.files:
            print(name)

    def touch(self, name):
        # Create a new empty file with the given name in the current directory
        if name in self.current_dir.files:
            print(f"File {name} already exists.")
        else:
            self.current_dir.files[name] = ''

    def cat(self, name):
        # Display the contents of a file in the current directory
        if name in self.current_dir.files:
            print(self.current_dir.files[name])
        else:
            print(f"No such file: {name}")

    def echo(self, text, name):
        # Write text to a file in the current directory or create a new file if it doesn't exist
        if name in self.current_dir.files:
            self.current_dir.files[name] += text
        else:
            print(f"No such file: {name}")

    def mv(self, name, new_name):
        # Move a file or directory to a new location in the current directory
        if name in self.current_dir.children:
            if new_name in self.current_dir.children:
                print(f"Directory {new_name} already exists.")
            else:
                self.current_dir.children[new_name] = self.current_dir.children[name]
                del self.current_dir.children[name]
        elif name in self.current_dir.files:
            if new_name in self.current_dir.files:
                print(f"File {new_name} already exists.")
            else:
                self.current_dir.files[new_name] = self.current_dir.files[name]
                del self.current_dir.files[name]
        else:
            print(f"No such file or directory: {name}")

    def cp(self, name, new_name):
        # Copy a file or directory to a new location in the current directory
        if name in self.current_dir.files:
            if new_name in self.current_dir.files:
                print(f"File {new_name} already exists.")
            else:
                self.current_dir.files[new_name] = self.current_dir.files[name]
        else:
            print(f"No such file: {name}")

    def rm(self, name):
        # Remove a file or directory from the current directory
        if name in self.current_dir.children:
            del self.current_dir.children[name]
        elif name in self.current_dir.files:
            del self.current_dir.files[name]
        else:
            print(f"No such file or directory: {name}")

    @staticmethod
    def handle_invalid_command():
        # Handle invalid command by printing an error message
        print("Invalid command. Type 'help' for a list of commands.")

    @staticmethod
    def help():
        # Print a list of available commands and their usage
        print("""
        Available Commands:
        - mkdir <directory_name>
        - cd <directory_path>
        - ls
        - touch <file_name>
        - cat <file_name>
        - echo <file_name> <text>
        - mv <source> <destination>
        - cp <source> <destination>
        - rm <file_name>
        - exit
        """)

    @staticmethod
    def process_command(command):
        # Process the user command and execute the corresponding operation
        if command[0] == 'mkdir':
            if len(command) > 1:
                fs.mkdir(command[1])
            else:
                print("Usage: mkdir <directory_name>")
        elif command[0] == 'cd':
            if len(command) > 1:
                fs.cd(command[1])
            else:
                print("Usage: cd <directory_path>")
        elif command[0] == 'ls':
            fs.ls()
        elif command[0] == 'touch':
            if len(command) > 1:
                fs.touch(command[1])
            else:
                print("Usage: touch <file_name>")
        elif command[0] == 'cat':
            if len(command) > 1:
                fs.cat(command[1])
            else:
                print("Usage: cat <file_name>")
        elif command[0] == 'echo':
            if len(command) > 2:
                fs.echo(' '.join(command[2:]), command[1])
            else:
                print("Usage: echo <text> > <file_name>")
        elif command[0] == 'mv':
            if len(command) > 2:
                fs.mv(command[1], command[2])
            else:
                print("Usage: mv <source> <destination>")
        elif command[0] == 'cp':
            if len(command) > 2:
                fs.cp(command[1], command[2])
            else:
                print("Usage: cp <source> <destination>")
        elif command[0] == 'rm':
            if len(command) > 1:
                fs.rm(command[1])
            else:
                print("Usage: rm <file_name>")
        elif command[0] == 'help':
            fs.help()
        else:
            fs.handle_invalid_command()


# Create an instance of the FileSystem class
fs = FileSystem()

# Start the interactive shell
while True:
    fs.print_prompt()
    command = input().split()
    if not command:
        continue  # Ignore empty commands

    if command[0] == 'exit':
        break
    else:
        fs.process_command(command)
