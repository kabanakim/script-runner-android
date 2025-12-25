from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import json
import os

class ScriptCard(BoxLayout):
    def __init__(self, script, app, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=250, **kwargs)
        
        self.add_widget(Label(
            text=script['name'],
            font_size='20sp',
            size_hint_y=0.2,
            color=(1, 1, 1, 1)
        ))
        
        self.add_widget(Label(
            text=f"[{script['language']}]",
            font_size='14sp',
            size_hint_y=0.15,
            color=(0.4, 0.6, 1, 1)
        ))
        
        code_preview = script['code'][:80] + "..."
        self.add_widget(Label(
            text=code_preview,
            font_size='11sp',
            size_hint_y=0.35,
            color=(0.7, 0.7, 0.7, 1)
        ))
        
        btn_box = BoxLayout(size_hint_y=0.3, spacing=5, padding=5)
        
        run_btn = Button(text='▶ Run', background_color=(0.2, 0.8, 0.2, 1))
        run_btn.bind(on_press=lambda x: print(f"Running: {script['name']}"))
        btn_box.add_widget(run_btn)
        
        edit_btn = Button(text='Edit', background_color=(0.2, 0.5, 1, 1))
        edit_btn.bind(on_press=lambda x: app.edit_script(script))
        btn_box.add_widget(edit_btn)
        
        delete_btn = Button(text='Delete', background_color=(1, 0.2, 0.2, 1))
        delete_btn.bind(on_press=lambda x: app.delete_script(script))
        btn_box.add_widget(delete_btn)
        
        self.add_widget(btn_box)

class EditorScreen(BoxLayout):
    def __init__(self, app, script=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.script = script
        
        self.add_widget(Label(text='Script Editor', font_size='22sp', size_hint_y=0.08, bold=True))
        
        self.add_widget(Label(text='Name:', size_hint_y=0.04))
        self.name_input = TextInput(
            text=script['name'] if script else '',
            multiline=False,
            size_hint_y=0.08
        )
        self.add_widget(self.name_input)
        
        self.add_widget(Label(text='Language:', size_hint_y=0.04))
        self.lang_spinner = Spinner(
            text=script['language'] if script else 'python',
            values=('python', 'javascript', 'bash', 'ruby'),
            size_hint_y=0.08
        )
        self.add_widget(self.lang_spinner)
        
        self.add_widget(Label(text='Code:', size_hint_y=0.04))
        self.code_input = TextInput(
            text=script['code'] if script else '',
            multiline=True,
            size_hint_y=0.5
        )
        self.add_widget(self.code_input)
        
        btn_box = BoxLayout(size_hint_y=0.1, spacing=10, padding=10)
        
        save_btn = Button(text='Save', background_color=(0.2, 0.8, 0.2, 1))
        save_btn.bind(on_press=lambda x: self.save())
        btn_box.add_widget(save_btn)
        
        cancel_btn = Button(text='Cancel', background_color=(1, 0.2, 0.2, 1))
        cancel_btn.bind(on_press=lambda x: self.app.show_main())
        btn_box.add_widget(cancel_btn)
        
        self.add_widget(btn_box)
    
    def save(self):
        name = self.name_input.text.strip()
        code = self.code_input.text.strip()
        language = self.lang_spinner.text
        
        if not name or not code:
            return
        
        new_script = {'name': name, 'code': code, 'language': language}
        
        if self.script:
            idx = self.app.scripts.index(self.script)
            self.app.scripts[idx] = new_script
        else:
            self.app.scripts.append(new_script)
        
        self.app.save_scripts()
        self.app.show_main()

class MainScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        
        header = BoxLayout(size_hint_y=0.1, padding=10)
        header.add_widget(Label(text='Script Runner', font_size='24sp', bold=True))
        self.add_widget(header)
        
        create_btn = Button(
            text='+ New Script',
            size_hint_y=0.08,
            background_color=(0.4, 0.4, 1, 1)
        )
        create_btn.bind(on_press=lambda x: self.app.show_editor())
        self.add_widget(create_btn)
        
        self.scroll = ScrollView(size_hint_y=0.82)
        self.scripts_container = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        self.scripts_container.bind(minimum_height=self.scripts_container.setter('height'))
        self.scroll.add_widget(self.scripts_container)
        self.add_widget(self.scroll)
        
        self.refresh_scripts()
    
    def refresh_scripts(self):
        self.scripts_container.clear_widgets()
        if not self.app.scripts:
            self.scripts_container.add_widget(Label(
                text='No scripts yet\nTap + to create one',
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1)
            ))
        else:
            for script in self.app.scripts:
                card = ScriptCard(script, self.app)
                self.scripts_container.add_widget(card)

class ScriptRunnerApp(App):
    def build(self):
        self.scripts = [
            {'name': 'Hello World', 'code': 'print("Hello from Script Runner!")', 'language': 'python'},
            {'name': 'Test Script', 'code': 'for i in range(5):\n    print(i)', 'language': 'python'}
        ]
        self.load_scripts()
        self.main_screen = MainScreen(self)
        return self.main_screen
    
    def show_main(self):
        self.root.clear_widgets()
        self.main_screen = MainScreen(self)
        self.root.add_widget(self.main_screen)
    
    def show_editor(self, script=None):
        self.root.clear_widgets()
        editor = EditorScreen(self, script)
        self.root.add_widget(editor)
    
    def edit_script(self, script):
        self.show_editor(script)
    
    def delete_script(self, script):
        self.scripts.remove(script)
        self.save_scripts()
        self.show_main()
    
    def load_scripts(self):
        try:
            if os.path.exists('scripts.json'):
                with open('scripts.json', 'r') as f:
                    self.scripts = json.load(f)
        except:
            pass
    
    def save_scripts(self):
        try:
            with open('scripts.json', 'w') as f:
                json.dump(self.scripts, f, indent=2)
        except:
            pass

if __name__ == '__main__':
    ScriptRunnerApp().run()
