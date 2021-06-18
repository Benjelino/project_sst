from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty


class Multichoice(BoxLayout):
    text = StringProperty()
    answer = ObjectProperty
    opt_remove = ObjectProperty(None)

    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.register_event_type('on_del_pressed')
        self.register_event_type('on_get_option_text')
    
    def on_del_pressed(self):
        pass

    def on_get_option_text(self):
        pass


class QuestionChoice(BoxLayout):
    text = StringProperty()
    answer = ObjectProperty
    opt_remove = ObjectProperty(None)

    def __init__(self, text='', **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.register_event_type('on_del_pressed')
        self.register_event_type('on_get_option_text')

    def on_del_pressed(self):
        pass

    def on_get_option_text(self):
        pass


class SolWidget(StackLayout):
    add_button = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_add_option')
        self.register_event_type('on_question_text')
        self.register_event_type('on_gotten_option')
    
    def on_add_option(self):
        pass

    def on_question_text(self):
        pass

    def on_gotten_option(self):
        pass


class LikertScale(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_add_likert_option')
        self.register_event_type('on_add_question')

    def on_add_likert_option(self):
        pass

    def on_add_question(self):
        pass


class AnsInput(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type("on_get_option_text")
        self.register_event_type("on_option_text")

    def on_get_option_text(self):
        pass

    def on_option_text(self):
        pass


class QuesInput(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_get_text')
        self.register_event_type('on_get_option_text')

    def on_get_text(self):
        pass

    def on_get_option_text(self):
        pass


class CreateScreen(BoxLayout, Screen):
    key = StringProperty()
    question = StringProperty()
    options = ListProperty()
    store = JsonStore(filename='data.json', indent=4, sort_keys=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
    
    def add_ans_input(self):
        my_create = self.ids['sol_widget'].ids['ans_input']
        multichoice = Multichoice()
        my_create.add_widget(multichoice)

    def add_ans_question(self):
        my_create = self.ids['likert_scale'].ids['likertque_input']
        Qchoice = QuestionChoice()
        my_create.add_widget(Qchoice)

    def add_likert_input(self):
        my_create = self.ids['likert_scale'].ids['ans_input']
        multichoice = Multichoice()
        my_create.add_widget(multichoice)
