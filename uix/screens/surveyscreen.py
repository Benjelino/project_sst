from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from kivy.uix.stacklayout import StackLayout
from project_sst.uix.applibs.swipetodelete import SwipeBehavior
from project_sst.uix.screens.widget import Toast
from kivy.properties import StringProperty, ListProperty, AliasProperty, NumericProperty


class CustomDropDown(DropDown):
    pass


class ProjectItem(SwipeBehavior, StackLayout):

    index = NumericProperty()
    title = StringProperty()
    description = StringProperty()
    projectName = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.move_to = self.x, self.y
            return super(ProjectItem, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            return super(ProjectItem, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.check_for_left()
            self.check_for_right()
            super(ProjectItem, self).on_touch_up(touch)

    def open(self):
        dropdown = CustomDropDown()
        self.ids['three_dot'].bind(on_release=dropdown.open)


class SurveyScreen(Screen):

    data = ListProperty()

    def _get_data_for_widgets(self):
        return [{
            'index': index,
            'description': item['description'],
            'title': item['title']}
            for index, item in enumerate(self.data)]

    data_for_widgets = AliasProperty(_get_data_for_widgets, bind=['data'])

