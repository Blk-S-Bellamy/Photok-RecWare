import os
from pathlib import Path
# HOME_PATH = os.getenv("HOME")  # only used for linux
HOME_PATH = str(Path.home())


# filter out certain filetypes/dirs when listing directory contents
def mode_filter(contents : list, directory : str, mode='directories'):
    keep = []
    try:
        # only folders allowed
        if mode == 'directories':
            for thing in contents:
                if os.path.isdir(os.path.join(directory, thing)):
                    keep.append(thing)
            contents = keep

        # only files allowed
        elif mode == 'files':
            for thing in contents:
                if os.path.isfile(os.path.join(directory, thing)):
                    keep.append(thing)
            contents = keep

        # all content allowed
        elif mode == 'any':
            pass
        else:
            raise ValueError(f"specified mode is not valid (any, directories, file): '{mode}'")
        
        # return the filtered contents
        return contents
    except Exception as e:
        raise e


# provides the tools for filesstem navigation
class DirEngine():
    def __init__(self, home=HOME_PATH, mode='directories'):
        self.history = []
        self.history_index = -1
        self.home = home
        self.mode = mode
        self.current = home
        self.selected = ""
        self.lasterror = ""
        # dir contents
        self.contents = []
        self.add_history(self.current)
        self.update_contents()

    def curr_mode_filter(self):
        self.contents = mode_filter(self.contents, self.current, self.mode)

    def filter_type(self, mode='any'):
        try:
            contents = mode_filter(self.contents, self.current, mode)
            return contents
        except Exception as e:
            print(e)
            return self.contents

    # update the contents of the cwd and filter selected filetypes
    def update_contents(self):
        try:
            self.contents = os.listdir(self.current)
            self.curr_mode_filter()
        except ValueError as e:
            print(f'failed to list dir {e}')

    # change currently selected history index to be one forward if possible
    def history_forward(self):
        # prevent going past list length
        if self.history_index != -1:
            try:
                self.history_index = self.history_index + 1
            except Exception:
                pass

    # change to currently selected hsitory index to be one backward if possible
    def history_backward(self):
        # prevent going past list length
        if self.history_index == 0:
            pass
        try:
            value = self.history_index - 1
            compat = self.history[value]
            self.history_index = value
        # skip if the result is out of range
        except IndexError as e:
            pass

    # adds an item to the history
    def add_history(self, pathway):
        if os.path.isdir(pathway) and pathway not in self.history:
            print(pathway)
            self.history.append(pathway)

    # change directory back to the preceding directory and update contents
    def back(self):
        self.history_backward()
        self.current = self.history[self.history_index]
        self.update_contents()

    # move forward in folder history
    def forward(self):
        self.history_forward()
        self.current = self.history[self.history_index]
        self.update_contents()

    # move up to parent folder
    def up(self):
        try:
            upone = os.path.split(self.current)[0]
            if os.path.isdir(upone) and upone != self.current:
                self.current = upone
                self.update_contents()
                self.add_history(self.current)
        except Exception:
            pass

    # make sure that there are correct permissions to cd into a directory
    def permcheck(pathway):
        ok = False
        try:
            if os.access(pathway, os.R_OK):  # read access 
                ok = True
            else:
                ok = False

            if os.access(pathway, os.W_OK):  # write access
                ok = True
            else:
                ok = False
        except Exception as e:
            print(e)
            return False
        return ok

    # change directory and update current folder contents
    def cd(self, pathway):
        try:
            if os.path.isdir(Path(pathway)) and DirEngine.permcheck(pathway):
                self.current = pathway
                self.update_contents()
                self.add_history(pathway)
            else:
                self.lasterror = f"can't change directory to {pathway}: no permission"
        except Exception as e:
            print(f'failed to cd{e}')
        return
