import gi
import shutil
import pykeepass
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk
from pykeepass import PyKeePass
import database
from database import KeepassLoader
import config
import database_creation_gui
from database_creation_gui import DatabaseCreationGui
import container_page
from container_page import ContainerPage

class MainWindow(Gtk.Window):

    keepass_loader = NotImplemented
    container = NotImplemented

    def __init__(self):
        config.configure()
        self.assemble_window()


    def assemble_window(self):
        Gtk.Window.__init__(self, title="KeepassGtk")
        self.connect("destroy", Gtk.main_quit)
        self.set_default_size(800, 500)

        builder = Gtk.Builder()
        builder.add_from_file("ui/main_headerbar.ui")
        
        headerbar = builder.get_object("headerbar")
        self.set_titlebar(headerbar)

        file_open_button = builder.get_object("open_button")
        file_open_button.connect("clicked", self.open_filechooser)

        file_new_button = builder.get_object("new_button")
        file_new_button.connect("clicked", self.create_filechooser)

        # Add the tab bar (our container)
        self.create_container()

    def create_container(self):
        self.container = Gtk.Notebook()
        page = Gtk.Box()
        self.container.append_page(page, Gtk.Label("Start"))
        self.add(self.container)

    def destroy_container(self):
        self.container.destroy()
        

    # Events

    def open_filechooser(self, widget):
        dialog = Gtk.FileChooserDialog("Choose Keepass Database", self, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("File selected: " + dialog.get_filename())
            dialog.close()
        elif response == Gtk.ResponseType.CANCEL:
            print("File selection cancelled")
            dialog.close()

    def create_filechooser(self, widget):
        dialog = Gtk.FileChooserDialog("Create new Database", self, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_name("Database.kdbx")

        filter_text = Gtk.FileFilter()
        filter_text.set_name("Keepass 2 Database")
        filter_text.add_mime_type("application/x-keepass2")
        dialog.add_filter(filter_text)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Saving..." + dialog.get_filename())
            shutil.copy2('data/database.kdbx', dialog.get_filename())
            dialog.close()

            page_instance = ContainerPage(dialog.get_filename())
            self.container.append_page(page_instance, Gtk.Label(dialog.get_filename()))

            print("Setze Datenbank Pfad: " + dialog.get_filename())

            self.keepass_loader = KeepassLoader(dialog.get_filename(), "liufhre86ewoiwejmrcu8owe")

            print("Bekomme Datenbank Pfad: " + self.keepass_loader.get_database())
            print(page_instance.get_instance_text())

            DatabaseCreationGui(page_instance, self.keepass_loader)
            page_instance.show_all()
        elif response == Gtk.ResponseType.CANCEL:
            print("Database creation cancelled")
            dialog.close()

main_window = MainWindow()
main_window.show_all()
Gtk.main()
