from gi.repository import Gtk, Gdk
import passwordsafe.pathbar_button


class CustomKeypressHandler:
    #
    # Global Variables
    #

    unlocked_database = NotImplemented

    #
    # Init
    #

    def __init__(self, u_d):
        self.unlocked_database = u_d

    #
    # Special Keys (e.g. type-to-search)
    #

    def register_custom_keys(self):
        self.unlocked_database.window.connect("key-press-event", self.on_special_key_pressed)
        self.unlocked_database.window.connect("key-release-event", self.on_special_key_released)

    def on_special_key_pressed(self, window, eventkey):
        group_uuid = self.unlocked_database.database_manager.get_group_uuid_from_group_object(self.unlocked_database.current_group)

        if self.unlocked_database.window.container.page_num(self.unlocked_database.parent_widget) == self.unlocked_database.window.container.get_current_page():
            scrolled_page = self.unlocked_database.stack.get_child_by_name(group_uuid)
            if self.unlocked_database.database_locked is False and self.unlocked_database.selection_ui.selection_mode_active is False and self.unlocked_database.stack.get_visible_child() is not self.unlocked_database.stack.get_child_by_name("search") and scrolled_page.edit_page is True:
                if eventkey.keyval == Gdk.KEY_Tab:
                    if self.unlocked_database.window.get_focus() is None:
                        return

                    if "TabBox" in self.unlocked_database.window.get_focus().get_name():
                        self.tab_to_next_input_entry(scrolled_page)
                        return(True)

    def tab_to_next_input_entry(self, scrolled_page):
        focus_widget = self.unlocked_database.window.get_focus()
        focus_widget_index = focus_widget.get_parent().get_children().index(focus_widget)
        new_index = focus_widget_index + 1
        if new_index < len(focus_widget.get_parent().get_children()):
            if focus_widget.get_parent().get_children()[new_index].get_name() == "TabBox_Next":
                self.unlocked_database.window.set_focus(focus_widget.get_parent().get_children()[new_index])
                return

        rows = scrolled_page.properties_list_box.get_children()
        current_row = self.iterate_parents(self.unlocked_database.window.get_focus())
        current_index = rows.index(current_row)
        new_index = current_index + 1
        if new_index < len(rows):
            next_row = rows[new_index]
        else:
            next_row = rows[0]

        if next_row.get_name() == "ShowAllRow":
            next_row = rows[0]

        self.interate_to_next_input(next_row)

    def interate_to_next_input(self, parent):
        if parent.get_name() == "TabBox":
            self.unlocked_database.window.set_focus(parent)
            return

        if hasattr(parent, "get_children"):
            for child in parent.get_children():
                if child.get_name() == "TabBox":
                    self.unlocked_database.window.set_focus(child)
                else:
                    self.interate_to_next_input(child)

    def iterate_parents(self, child):
        if type(child) is Gtk.ListBoxRow:
            return child
        elif hasattr(child, "get_parent"):
            if type(child.get_parent()) is Gtk.ListBoxRow:
                return child.get_parent()
            else:
                return self.iterate_parents(child.get_parent())

    def on_special_key_released(self, window, eventkey):
        group_uuid = self.unlocked_database.database_manager.get_group_uuid_from_group_object(self.unlocked_database.current_group)

        if self.unlocked_database.window.container.page_num(self.unlocked_database.parent_widget) == self.unlocked_database.window.container.get_current_page():
            scrolled_page = self.unlocked_database.stack.get_child_by_name(group_uuid)
            if self.unlocked_database.database_locked is False and self.unlocked_database.selection_ui.selection_mode_active is False and self.unlocked_database.database_manager.check_is_group(self.unlocked_database.database_manager.get_group_uuid_from_group_object(self.unlocked_database.current_group)) and scrolled_page.edit_page is False:
                if self.unlocked_database.stack.get_visible_child() is not self.unlocked_database.stack.get_child_by_name("search"):
                    if eventkey.string.isalpha() or eventkey.string.isnumeric():
                        self.unlocked_database.search.set_search_headerbar(self.unlocked_database.builder.get_object("search_button"))
                        self.unlocked_database.builder.get_object("headerbar_search_entry").set_text(eventkey.string)
                        Gtk.Entry.do_move_cursor(self.unlocked_database.builder.get_object("headerbar_search_entry"), Gtk.MovementStep.BUFFER_ENDS, 1, False)
                    elif eventkey.keyval == Gdk.KEY_BackSpace:
                        uuid = self.unlocked_database.stack.get_visible_child_name()
                        if self.unlocked_database.database_manager.check_is_root_group(self.unlocked_database.current_group) is False:
                            if self.unlocked_database.database_manager.check_is_root_group(self.unlocked_database.database_manager.get_group_parent_group_from_uuid(uuid)) is True:
                                self.unlocked_database.pathbar.on_home_button_clicked(self.unlocked_database.pathbar.home_button)
                            else:
                                for button in self.unlocked_database.pathbar:
                                    if button.get_name() == "PathbarButtonDynamic" and type(button) is passwordsafe.pathbar_button.PathbarButton:
                                        if button.uuid == self.unlocked_database.database_manager.get_group_uuid_from_group_object(self.unlocked_database.database_manager.get_group_parent_group_from_uuid(uuid)):
                                            self.unlocked_database.pathbar.on_pathbar_button_clicked(button)
            elif self.unlocked_database.database_locked is False and self.unlocked_database.selection_ui.selection_mode_active is False and self.unlocked_database.stack.get_visible_child() is not self.unlocked_database.stack.get_child_by_name("search"):
                if eventkey.keyval == Gdk.KEY_Escape:
                    uuid = self.unlocked_database.stack.get_visible_child_name()
                    if self.unlocked_database.database_manager.check_is_group(uuid):
                        scrolled_page = self.unlocked_database.stack.get_child_by_name(uuid)
                        if self.unlocked_database.database_manager.check_is_root_group(self.unlocked_database.database_manager.get_group_parent_group_from_uuid(uuid)) is True:
                            self.unlocked_database.pathbar.on_home_button_clicked(self.unlocked_database.pathbar.home_button)
                        else:
                            if scrolled_page.edit_page is True:
                                for button in self.unlocked_database.pathbar:
                                    if button.get_name() == "PathbarButtonDynamic" and type(button) is passwordsafe.pathbar_button.PathbarButton:
                                        if self.unlocked_database.database_manager.get_group_object_from_uuid(uuid) is None:
                                            return
                                        if button.uuid == self.unlocked_database.database_manager.get_group_uuid_from_group_object(self.unlocked_database.database_manager.get_group_parent_group_from_uuid(uuid)):
                                            self.unlocked_database.pathbar.on_pathbar_button_clicked(button)
                    else:
                        if self.unlocked_database.database_manager.check_is_root_group(self.unlocked_database.database_manager.get_entry_parent_group_from_uuid(uuid)) is True:
                            self.unlocked_database.pathbar.on_home_button_clicked(self.unlocked_database.pathbar.home_button)
                        else:
                            for button in self.unlocked_database.pathbar:
                                if button.get_name() == "PathbarButtonDynamic" and type(button) is passwordsafe.pathbar_button.PathbarButton:
                                    if self.unlocked_database.database_manager.get_entry_object_from_uuid(uuid) is None:
                                        return
                                    if button.uuid == self.unlocked_database.database_manager.get_group_uuid_from_group_object(self.unlocked_database.database_manager.get_entry_parent_group_from_uuid(uuid)):
                                        self.unlocked_database.pathbar.on_pathbar_button_clicked(button)

