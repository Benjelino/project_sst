import json
from os.path import exists
from kivy.app import App
from threading import Timer
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout


class FinishedCard(StackLayout):
    pass


class RatingCard(BoxLayout):
    group = StringProperty()

    def __init__(self, group, **kwargs):
        super().__init__(**kwargs)
        self.group = group


class OtherCard(BoxLayout):
    option = StringProperty()
    group = StringProperty()
    check_other = ObjectProperty()

    def __init__(self, group, **kwargs):
        super().__init__(**kwargs)
        self.group = group


class OpenEndedCard(BoxLayout):
    group = StringProperty()

    def __init__(self, group, **kwargs):
        super().__init__(**kwargs)
        self.group = group


class SingleOptionCard(BoxLayout):
    option = StringProperty()
    group = StringProperty()
    check = ObjectProperty()

    def __init__(self, option, group, **kwargs):
        super().__init__(**kwargs)
        self.option = option
        self.group = group


class MultiOptionCard(BoxLayout):
    option = StringProperty()
    check = ObjectProperty()
    group = StringProperty()

    def __init__(self, option, group, **kwargs):
        super().__init__(**kwargs)
        self.option = option
        self.group = group


class OptionsCards(StackLayout):
    question = StringProperty()
    options = StringProperty()
    key = StringProperty()
    check = ObjectProperty()
    active = True
    index = NumericProperty()
    required = BooleanProperty(False)

    def __init__(self, question, key, required=False, **kwargs):
        super().__init__(**kwargs)
        self.question = question
        self.key = key
        self.required = required


class TakeSurvey(Screen):
    isShownMenu = BooleanProperty(False)
    store = JsonStore(filename='data.json', indent=4, sort_keys=False)
    carousel = ObjectProperty()
    index = NumericProperty()
    title = StringProperty()
    description = StringProperty()
    answers = ListProperty()
    count = -1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def remove_optioncard(self):
        if self.carousel.previous_slide is None:
            self.carousel.clear_widgets()
            self.finishing()
        else:
            self.carousel.anim_move_duration = 0
            self.carousel.load_slide(self.carousel.slides[0])
            self.remove_questions()

    def remove_questions(self):
        t = Timer(0.000000001, self.remove_optioncard)
        t.start()

    def remove_finish(self):
        for i in range(len(self.store)):
            for child in self.ids['carousel'].slides:
                self.ids['carousel'].remove_widget(child)
        self.ids['done'].opacity = 1
        self.put_answers_in_json(self.title)

    def finishing(self):
        f = FinishedCard()
        self.ids['carousel'].add_widget(f)

    def check_something(self):
        for child in self.ids['carousel'].slides:
            for boxLayout in child.children:
                if boxLayout.active:
                    child.required = False
                    child.active = False
                    self.count += 1
                    self.answers.append([boxLayout.group, boxLayout.text])
                else:
                    pass
            if child.active is True:
                self.answers.append([child.question, ""])
            elif child.required == True:
                self.carousel.load_slide(self.carousel.slides[child.index])
                return self.required_info("This question requires an answer")
        self.remove_optioncard()
        self.ids['done'].opacity = 0

    def _show_toast(self, text):
        self.ids['toast'].show(text)

    def required_info(self, error):
        self._show_toast(error)

    def answers_json(self, title):
        self.answers = []
        app = App.get_running_app()
        d = app.answers_fn(title)
        if not exists(d):
            return
        with open(d) as fd:
            data = json.load(fd)
        self.answers = data

    def put_answers_in_json(self, title):
        app = App.get_running_app()
        d = app.answers_fn(title)
        with open(d, 'w') as fd:
            json.dump(self.answers, fd)
