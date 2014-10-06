import sublime, sublime_plugin, re, os, os.path

class EditInNewBufferCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if len(self.view.sel()) == 1:
            sel = self.view.substr(self.view.word(self.view.sel()[0]))
            window = self.view.window()
            syntax = self.view.settings().get('syntax')
            new_view = window.new_file()
            new_view.set_syntax_file(syntax)
            window.focus_view(new_view)
            new_view.run_command("append", {"characters": sel });
            settings = sublime.load_settings("EditInNewBuffer.sublime-settings")
            settings.set("currently_editing_view_id", self.view.id());
            settings.set("active_view_id", new_view.id());
        else:
            print("Error: No text highlighted")

class EditBufferEvent(sublime_plugin.EventListener):
    def on_modified(self, view):
        settings = sublime.load_settings("EditInNewBuffer.sublime-settings")
        target_view_id = settings.get("currently_editing_view_id")
        active_view_id = settings.get("active_view_id")
        if view.id() == active_view_id:
            all_views = view.window().views()
            target_view = None
            for v in all_views:
                if(v.id() == target_view_id):
                    target_view = v

            if target_view == None:
                print("Could not find target view with id: " + str(target_view_id))
            else:
                target_view.run_command("append", {"characters": "TEST APPEND"})