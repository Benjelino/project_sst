import json
from kivy.app import App
import pandas as pd
from os.path import join, exists
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from project_sst.uix.screens.maincontrol import MainScreen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty
from project_sst.uix.screens.createscreen import Multichoice, QuestionChoice
from project_sst.uix.screens.surveyscreen import SurveyScreen
from project_sst.uix.screens.takesurvey import OptionsCards, MultiOptionCard, SingleOptionCard, OpenEndedCard, OtherCard, RatingCard
from project_sst.uix.screens.questionlist import OptionsCard, MultiOption, QuestionList, OpenEnded, Other, LikertCard, Rating


class MainApp(App):
    isShownMenu = BooleanProperty(False)
    view = SurveyScreen(name='survey')
    key = StringProperty()
    index = NumericProperty()
    store = QuestionList().store
    option = ListProperty()

    def build(self):
        return MainScreen()

    def on_start(self):
        if not exists(self.notes_fn):
            return
        with open(self.notes_fn) as fd:
            data = json.load(fd)
        self.view.data = data

    def save_notes(self):
        with open(self.notes_fn, 'w') as fd:
            json.dump(self.view.data, fd)

    def create_json(self, title):
        filename = self.data_fn(title)
        data = JsonStore(filename=filename, indent=4, sort_keys=False)
        self.store = data

    def create_survey(self, index):
        self.index = index

    def take_survey(self, index):
        # take survey
        title = self.view.data[index]
        self.create_survey(index)
        self.create_json(title['title'])
        self.on_take_refresh()
        self.root.ids['take_survey'].title = title['title']
        self.root.ids['take_survey'].store = self.store
        self.root.current = 'take'

    def edit_survey(self, index):
        # edits the project when the edit survey button is clicked
        title = self.view.data[index]
        self.create_json(title['title'])
        self.on_refresh()
        self.root.ids['question_list'].ids['title'].text = title["title"]
        self.root.ids['question_list'].ids['title'].disabled = True
        self.root.ids['question_list'].ids['description'].text = title['description']
        self.root.ids['question_list'].ids['description'].disabled = True
        self.root.ids['question_list'].store = self.store
        self.hide_widget(self.root.ids['create_screen'].ids['likert_scale'])
        self.root.current = 'list'

    def check_done(self):
        if self.root.ids['question_list'].ids['title'].text == '':
            self.root.ids['question_list'].ids['title'].highlight_color1 = (1, 0.2, 0, 1)

        elif self.root.ids['question_list'].ids['description'].text == '':
            self.root.ids['question_list'].ids['description'].highlight_color1 = (1, 0.2, 0, 1)
        else:
            self.root.ids['question_list'].remove_optioncard()
            self.root.ids['question_list'].clear_text()
            self.isShownMenu = False
            self.root.ids['question_list'].ids['title'].highlight_color1 = (0.498, 0.549, 0.552, 1.0)
            self.root.current = 'main'

    def check_tnd(self):
        # checks whether the title or description is filled else red line, called when the plus button is clicked
        # There is a bug here, concerning the the Done button when there is nothing in the descriptions
        if self.root.ids['question_list'].ids['title'].text == '':
            self.root.ids['question_list'].ids['title'].highlight_color1 = (1, 0.2, 0, 1)

        elif self.root.ids['question_list'].ids['description'].text == '':
            self.root.ids['question_list'].ids['description'].highlight_color1 = (1, 0.2, 0, 1)

        else:
            self.root.ids['question_list'].ids['title'].disabled = True
            self.root.ids['question_list'].ids['description'].disabled = True
            self.isShownMenu = not self.isShownMenu
            title = self.root.ids['question_list'].ids['title'].text
            self.create_json(title)

    def on_refresh(self):
        # when the save or edit survey button is clicked,
        # it populates the question list screen with the questions
        container_grid = self.root.ids['question_list'].ids['survey_grid']
        for key, surv_opt in self.store.find():
            if surv_opt['optiontype'] == 'Likert scale':
                M = OptionsCard('Please rank the following', str(key))
                for item in surv_opt['question']:
                    L = LikertCard(item)
                    M.bind(on_del_optioncard=self.delete_optioncard)
                    for options in surv_opt['options']:
                        L.add_widget(MultiOption(options, 'question'))
                    M.add_widget(L)
                container_grid.add_widget(M)
            else:
                M = OptionsCard(surv_opt['question'], str(key))
                M.bind(on_del_optioncard=self.delete_optioncard)
            if surv_opt['optiontype'] == 'Open ended':
                M.add_widget(OpenEnded())
            elif surv_opt['optiontype'] == 'Rating':
                M.add_widget(Rating())
            else:
                if surv_opt['optiontype'] == 'Likert scale':
                    pass
                else:
                    for item in surv_opt['options']:
                        M.add_widget(MultiOption(item, surv_opt['question']))
                if surv_opt['other'] == True:
                    M.add_widget(Other())
            if surv_opt['optiontype'] == 'Likert scale':
                pass
            else:
                container_grid.add_widget(M)

    def delete_optioncard(self, instance):
        self.root.ids['question_list'].ids['survey_grid'].remove_widget(instance)

    def on_take_refresh(self):
        # when the take survey is clicked,
        # the take survey screen is populated with the questions
        count = -1
        container_grid = self.root.ids['take_survey'].ids['carousel']
        for key, surv_opt in self.store.find():
            count += 1
            if surv_opt['optiontype'] == 'Likert scale':
                for item in surv_opt['question']:
                    M = OptionsCards(item, str(key), surv_opt['required'])
                    M.index = count
                    M.bind(on_del_optioncard=self.delete_optioncard)
                    for options in surv_opt['options']:
                        M.add_widget(SingleOptionCard(options, item))
                    container_grid.add_widget(M)
            else:
                M = OptionsCards(surv_opt['question'], str(key), surv_opt['required'])
                O = OtherCard(surv_opt['question'])
                M.index = count
            if surv_opt['optiontype'] == "Open ended":
                M.add_widget(OpenEndedCard(surv_opt['question']))
            elif surv_opt['optiontype'] == "Rating":
                M.add_widget(RatingCard(surv_opt['question']))
            else:
                if surv_opt['optiontype'] == 'Likert scale':
                    pass
                else:
                    for item in surv_opt['options']:
                        if surv_opt['optiontype'] == "Single answer":
                            M.add_widget(SingleOptionCard(item, surv_opt['question']))
                        elif surv_opt['optiontype'] == "Multiple choice":
                            M.add_widget(MultiOptionCard(item, surv_opt['question']))
                if surv_opt['other'] == True:
                    if surv_opt['optiontype'] == "Multiple choice":
                        O.ids['check_other'].group = ''
                        M.add_widget(O)
                    elif surv_opt['optiontype'] == "Single answer":
                        O.ids['check_other'].group = surv_opt['question']
                        M.add_widget(O)
            if surv_opt['optiontype'] == 'Likert scale':
                pass
            else:
                container_grid.add_widget(M)
        if self.root.ids['take_survey'].carousel.anim_move_duration == 0:
            self.root.ids['take_survey'].carousel.anim_move_duration = 1

    def on_edit(self, key):
        # When the edit button on instance is clicked,
        # this function makes it editable
        data = self.store[key]
        self.key = key
        self.option = data['options']
        self.root.ids['create_screen'].key = key
        if data['optiontype'] == 'Likert scale':
            self.hide_widget(self.root.ids['create_screen'].ids['sol_widget'])  # hides the sol_widget
            self.hide_widget(self.root.ids['create_screen'].ids['likert_scale'], False)  # Unhides the likert_scale
            self.root.ids['create_screen'].ids['likert_scale'].ids['required'].active = data['required']
            self.root.ids['create_screen'].ids['likert_scale'].height = self.root.ids['create_screen'].ids[
                'likert_scale'].minimum_height
            for item in data['question']:
                options_cont = self.root.ids['create_screen'].ids['likert_scale'].ids['likertque_input']
                Q = QuestionChoice(item)
                options_cont.add_widget(Q)
        else:
            self.root.ids['create_screen'].ids['sol_widget'].ids['required'].active = data['required']
            self.root.ids['create_screen'].ids['sol_widget'].ids['other'].active = data['other']
            self.root.ids['create_screen'].ids['sol_widget'].ids['inp_idea'].text = data['question']
            self.hide_widget(self.root.ids['create_screen'].ids['sol_widget'], False)
            self.hide_widget(self.root.ids['create_screen'].ids['likert_scale'])

        if data['optiontype'] == 'Open ended':
            self.root.ids['create_screen'].ids['sol_widget'].ids['add_option'].opacity = 0
            self.root.ids['create_screen'].ids['sol_widget'].ids['option_type'].text = "Open ended"
            self.root.ids['create_screen'].ids['sol_widget'].ids['add_option'].disabled = True
            self.root.ids['create_screen'].ids['sol_widget'].ids['other_box'].size_hint = 0, 0
            self.root.ids['create_screen'].ids['sol_widget'].ids['other'].opacity = 0
        else:
            if data['optiontype'] == 'Multiple choice':
                self.root.ids['create_screen'].ids['sol_widget'].ids['option_type'].text = "Multiple choice"
            elif data['optiontype'] == 'Single answer':
                self.root.ids['create_screen'].ids['sol_widget'].ids['option_type'].text = "Single answer"
            elif data['optiontype'] == 'Likert scale':
                self.root.ids['create_screen'].ids['likert_scale'].ids['option_type'].text = "Likert scale"
            for item in data['options']:
                if data['optiontype'] == 'Likert scale':
                    options_cont = self.root.ids['create_screen'].ids['likert_scale'].ids['ans_input']
                else:
                    options_cont = self.root.ids['create_screen'].ids['sol_widget'].ids['ans_input']
                M = Multichoice(item)
                options_cont.add_widget(M)

    def clear_screen(self, options):
        # clears the question and options in the sol_widget
        self.root.ids['create_screen'].ids['sol_widget'].ids['inp_idea'].text = ''
        self.root.ids['create_screen'].ids['sol_widget'].ids['required'].active = False
        for i in range(len(options) + 2):
            for child in self.root.ids['create_screen'].ids['sol_widget'].ids['ans_input'].children:
                self.root.ids['create_screen'].ids['sol_widget'].ids['ans_input'].remove_widget(child)

    def clear_likert_screen(self, questions, options):
        # when the save button is pressed and the option type was a likert scale,
        # this function removes the questions and answers
        for i in range(len(questions) + 5):
            for child in self.root.ids['create_screen'].ids['likert_scale'].ids['likertque_input'].children:
                self.root.ids['create_screen'].ids['likert_scale'].ids['likertque_input'].remove_widget(child)
        self.root.ids['create_screen'].ids['likert_scale'].ids['required'].active = False
        for i in range(len(options) + 5):
            for child in self.root.ids['create_screen'].ids['likert_scale'].ids['ans_input'].children:
                self.root.ids['create_screen'].ids['likert_scale'].ids['ans_input'].remove_widget(child)

    def del_optioncard(self, key):
        self.store.delete(key)

    def get_last_id(self):
        # numbering the questions
        last_survey = self.store.count()
        if self.key:
            return self.key
        elif last_survey == 0:
            return 1
        else:
            return last_survey + 1

    def post_survey(self):
        # saves the survey
        question = self.root.ids['create_screen'].ids['sol_widget'].ids['inp_idea'].text
        lik_q = [child.text for child in self.root.ids['create_screen'].ids['likert_scale'].ids['likertque_input'].children][::-1]
        likert_question = [item for item in lik_q if item != '']
        lik_o = [child.text for child in self.root.ids['create_screen'].ids['likert_scale'].ids['ans_input'].children][::-1]
        likert_option = [item for item in lik_o if item != '']
        optiontype = self.root.ids['create_screen'].ids['sol_widget'].ids['option_type'].text
        likert_optiontype = self.root.ids['create_screen'].ids['likert_scale'].ids['option_type'].text
        required = self.root.ids['create_screen'].ids['sol_widget'].ids['required'].active
        likert_required = self.root.ids['create_screen'].ids['likert_scale'].ids['required'].active
        other = self.root.ids['create_screen'].ids['sol_widget'].ids['other'].active
        first_options = [child.text for child in self.root.ids['create_screen'].ids['sol_widget'].ids['ans_input'].children][::-1]
        self.option = [item for item in first_options if item != '']
        if likert_optiontype == 'Likert scale':
            if likert_required == True:
                self.store.put(self.get_last_id(), question=question + '**', optiontype=likert_optiontype, required=likert_required, other=other,
                               options=self.option)
            else:
                self.store.put(self.get_last_id(), question=likert_question, optiontype=likert_optiontype, required=likert_required,
                               other=other, options=likert_option)
            self.clear_likert_screen(likert_question, likert_option)
            self.key = ''
            self.on_refresh()
            self.store.store_load() # don't know what this really do
            self.hide_widget(self.root.ids['create_screen'].ids['sol_widget'], False)
            self.hide_widget(self.root.ids['create_screen'].ids['likert_scale'])
            self.root.current = 'list'

        elif len(str(question)) == 0:
            self.root.ids['create_screen'].ids['sol_widget'].ids['inp_idea'].highlight_color1 = (1, 0.2, 0, 1)

        else:
            if required == True:
                self.store.put(self.get_last_id(), question=question + '**', optiontype=optiontype, required=required, other=other,
                               options=self.option)
            else:
                self.store.put(self.get_last_id(), question=question, optiontype=optiontype, required=required, other=other,
                               options=self.option)
            self.clear_screen(self.option)
            self.key = ''
            self.on_refresh()  # reloads the questions into the question list screen
            self.store.store_load() # don't know what this really do
            self.root.ids['create_screen'].ids['sol_widget'].ids['add_option'].opacity = 1  # makes the Add Option button visible
            self.root.ids['create_screen'].ids['sol_widget'].ids['add_option'].disabled = False  # makes the Add Option button active
            self.root.ids['create_screen'].ids['sol_widget'].ids['other_box'].size_hint = 1, None   # makes the the Boxlayout containing 'other' button visible
            self.root.ids['create_screen'].ids['sol_widget'].ids['other_box'].height = dp(45)
            self.root.ids['create_screen'].ids['sol_widget'].ids['other'].opacity = 1  # makes the other switch visible
            self.root.ids['create_screen'].ids['sol_widget'].ids['other'].active = False
            self.root.current = 'list'

    def cancel(self):
        # cancel
        lik_q = [child.text for child in
                 self.root.ids['create_screen'].ids['likert_scale'].ids['likertque_input'].children][::-1]
        likert_question = [item for item in lik_q if item != '']
        lik_o = [child.text for child in self.root.ids['create_screen'].ids['likert_scale'].ids['ans_input'].children][
                ::-1]
        likert_option = [item for item in lik_o if item != '']
        self.root.ids.question_list.remove_optioncard()
        self.clear_likert_screen(likert_question, likert_option)
        self.clear_screen(self.option)
        self.key = ''
        self.on_refresh()
        self.store.store_load()  # don't know what this really do
        self.root.ids['create_screen'].ids['sol_widget'].ids['add_option'].opacity = 1
        self.root.ids['create_screen'].ids['sol_widget'].ids['add_option'].disabled = False
        self.root.ids['create_screen'].ids['sol_widget'].ids['other_box'].size_hint = 1, None
        self.root.ids['create_screen'].ids['sol_widget'].ids['other_box'].height = dp(45)
        self.root.ids['create_screen'].ids['sol_widget'].ids['other'].opacity = 1
        self.root.ids['create_screen'].ids['sol_widget'].ids['other'].active = False
        self.hide_widget(self.root.ids['create_screen'].ids['sol_widget'], False)
        self.hide_widget(self.root.ids['create_screen'].ids['likert_scale'])
        self.root.current = "list"

    def hide_widget(self, wid, dohide=True):
        # hides the widgets either sol_widget or likert_scale
        if hasattr(wid, 'saved_attrs'):
            if not dohide:
                wid.height, wid.size_hint_y, wid.size_hint_x, wid.opacity, wid.disabled = wid.saved_attrs
                del wid.saved_attrs
        elif dohide:
            wid.saved_attrs = wid.height, wid.size_hint_y, wid.size_hint_x, wid.opacity, wid.disabled
            wid.height, wid.size_hint_y, wid.size_hint_x, wid.opacity, wid.disabled = 0, None, None, 0, True

    def add_project(self):
        # create_survey recycle view label
        self.view.data.append({'title': 'New note', 'description': ''})
        index = len(self.view.data) - 1
        self.create_survey(index)
        self.hide_widget(self.root.ids['create_screen'].ids['likert_scale'])

    def set_description(self, description):
        # inputs the description into the json projects file
        index = self.index
        self.root.ids['question_list'].ids['description'].highlight_color1 = (0.498, 0.549, 0.552, 1.0)
        self.view.data[index]['description'] = description
        data = self.view.data
        self.view.data = []
        self.view.data = data
        self.save_notes()
        self.refresh_notes()

    def set_title(self, title):
        # inputs the title into the json projects file
        index = self.index
        checker = [item.get('title') for item in self.view.data]
        if title in checker:
            self.root.ids['question_list'].ids['title'].highlight_color1 = (1, 0.2, 0, 1)
            return self.title_info('The Title already exist')
        self.root.ids['question_list'].ids['title'].highlight_color1 = (0.498, 0.549, 0.552, 1.0)
        self.view.data[index]['title'] = title
        self.save_notes()
        self.refresh_notes()

    def refresh_notes(self):
        # recycle  on_refresh
        data = self.view.data
        self.view.data = []
        self.view.data = data

    def del_project(self, index):
        del self.view.data[index]
        self.save_notes()
        self.refresh_notes()

    def _show_title_toast(self, text):
        # show toast if title already exists
        self.root.ids['question_list'].ids['toast'].show(text)

    def _show_toast(self, text):
        # show toast when file has been exported
        self.root.ids['main_control'].ids['survey_screen'].ids['toast'].show(text)

    def title_info(self, error):
        # calls title toast
        self._show_title_toast(error)

    def export_info(self, error):
        # calls export toast
        self._show_toast(error)

    def export_data(self, title):
        answers = self.answers_fn(title)
        if not exists(answers):
            self.export_info('You have not taken the survey yet')
            return
        with open(answers) as fd:
            data = json.load(fd)
            survey = data
        d = {}
        for key, val in survey:
            d.setdefault(key, []).append(val)
        self.pad_dict_list(d, title)

    def pad_dict_list(self, dict_list, title, padel=''):
        # fills in the missing database info with NaN
        # required because of pandas error when length of
        # database is not equal
        lmax = 0
        for lname in dict_list.keys():
            lmax = max(lmax, len(dict_list[lname]))
        for lname in dict_list.keys():
            ll = len(dict_list[lname])
            if ll < lmax:
                dict_list[lname] = [padel] * (lmax - ll) + dict_list[lname]
        self.export_answers(dict_list, title)

    def export_answers(self, dict_list, title):
        d = self.survey_fn(title)
        with open(d, 'w') as fd:
            json.dump(dict_list, fd, indent=4)

        pd.read_json(d).to_excel(title + '.xlsx', index=False)  # exports file to excel
        self.export_info('Your file has been created')

    @property
    def notes_fn(self):
        return join(self.user_data_dir, 'projects.json')

    def survey_fn(self, title):
        d = title + '_survey.json'
        return join(self.user_data_dir, d)

    def answers_fn(self, title):
        answers = title + '_answers.json'
        return join(self.user_data_dir, answers)

    def data_fn(self, title):
        filename = title + '.json'
        return join(self.user_data_dir, filename)


if __name__ == "__main__":
    MainApp().run()
