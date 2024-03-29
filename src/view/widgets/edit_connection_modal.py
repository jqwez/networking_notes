import tkinter as tk
from tkinter import ttk

from model.dao.connection_dao import ConnectionDAO
from controller.connection_controller import ConnectionController


class EditConnectionModal(tk.Toplevel):
    def __init__(
        self, master=None, dao: ConnectionDAO = None, cb=None, *args, **kwargs
    ):
        super().__init__(master=None, *args, **kwargs)
        self.dao = dao
        self.cb = cb
        x, y = self.get_window_position()
        self.geometry(f"300x300+{x}+{y}")
        self.populate_fields()

    def populate_fields(self):
        self.action_label = ttk.Label(self, text="Edit Connection")
        self.action_label.grid(column=0, row=1)
        self.name_label = self.editable(text=self.dao.name, row=2, field="name")
        self.url_label = self.editable(text=self.dao.linkedin, row=3, field="linkedin")
        self.columnconfigure(0, weight=1)

    def editable(self, text: str, row: int = 0, field: str = "") -> ttk.Label:
        label: ttk.Label = ttk.Label(self, text=text)
        label.bind("<Button-1>", lambda e: self.handle_click_field(e, field))
        label.grid(column=0, row=row)
        return label

    def handle_cancel(self, event: tk.Event):
        self.destroy()

    def handle_click_field(self, event: tk.Event, field: str):
        widget: tk.Widget = event.widget
        content: str = widget.cget("text")
        grid_info: tk._GridInfo = widget.grid_info()
        widget.grid_forget()
        widget.destroy()
        entry = ttk.Entry(self, textvariable=content)
        entry.bind("<Return>", lambda e: self.handle_accept_entry(e, field))
        entry.bind("<FocusOut>", lambda e: self.handle_accept_entry(e, field))
        entry.delete(0, tk.END)
        entry.insert(0, content)
        entry.grid(column=grid_info["column"], row=grid_info["row"])

    def handle_accept_entry(self, event: tk.Event, field: str):
        widget: tk.Widget = event.widget
        content: str = widget.get()
        grid_info: tk._GridInfo = widget.grid_info()
        updated_dao = ConnectionController.update_connection(self.dao, field, content)
        if not updated_dao:
            raise Exception("failed to update")
        self.dao = updated_dao
        widget.grid_forget()
        widget.destroy()
        label = ttk.Label(self, text=self.dao.get(field))
        label.bind("<Button-1>", self.handle_cancel)
        label.grid(column=grid_info["column"], row=grid_info["row"])
        if self.cb:
            self.cb()

    def get_window_position(self) -> (int, int):
        if self.master:
            window = self.master
            x = window.winfo_x()
            y = window.winfo_y()
            return (x, y)
        else:
            return (self.winfo_screenwidth() // 2, self.winfo_screenheight // 2)
