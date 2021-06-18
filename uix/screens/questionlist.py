from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty, NumericProperty


class TitleInput(StackLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_title_text')

    def on_title_text(self):
        pass


class Rating(BoxLayout):
    pass


class Other(BoxLayout):
    pass


class OpenEnded(BoxLayout):
    pass


class MultiOption(BoxLayout):

    option = StringProperty()
    group = StringProperty()

    def __init__(self, option, group, **kwargs):
        super().__init__(**kwargs)
        self.option = option
        self.group = group


class LikertCard(StackLayout):
    question = StringProperty()

    def __init__(self, question, **kwargs):
        super().__init__(**kwargs)
        self.question = question



class OptionsCard(StackLayout):

    question = StringProperty()
    options = StringProperty()
    key = StringProperty()
    check = ObjectProperty()

    def __init__(self, question, key, **kwargs):
        super().__init__(**kwargs)
        self.question = question
        self.key = key
        self.register_event_type('on_del_optioncard')

    def on_del_optioncard(self):
        pass


class QuestionList(Screen):

    isShownMenu = BooleanProperty(False)
    store = JsonStore(filename='data.jason', indent=4, sort_keys=False)
    index = NumericProperty()
    title = StringProperty()
    description = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def remove_optioncard(self):
        for i in range(len(self.store) + 10):
            for child in self.ids['survey_grid'].children:
                self.ids['survey_grid'].remove_widget(child)

    def clear_text(self):
        self.ids['title'].disabled = False
        self.ids['description'].disabled = False
        self.ids['title'].text = ''
        self.ids['description'].text = ''

