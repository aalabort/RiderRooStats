import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious
from kivy.properties import  ObjectProperty

#from KivyCalendar.calendarui import DatePicker


class SidePanel(BoxLayout):
    pass

class MainPanel(BoxLayout):
    pass

class AppActionBar(ActionBar):
    pass

class NavDrawer(NavigationDrawer):
    def __init__(self, **kwargs):
        super(NavDrawer, self).__init__( **kwargs)

    def quit(self):
        print 'App quit'
        self.stop()

    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'
    def toggle_sidepanel(self):
        self.toggle_state()

    def on_uno(self):
        print 'Payment... exec'
        self._switch_main_page('voce uno', ScreenPayment)

    def on_due(self):
        print 'Tips... exec'
        self._switch_main_page('voce due', ScreenTips)
    def on_tre(self):
        print 'TRE... exec'
        self._switch_main_page('voce tre',  PaginaTre)


    def close_sidepanel(self, animate=True):
        if self.state == 'open':
            if animate:
                self.anim_to_state('closed')
            else:
                self.state = 'closed'


class DeliverooApp(App):

    #
    # def build(self):
    #     self.navigationdrawer = NavDrawer()
    #     return self.navigationdrawer
    pass





if __name__ == '__main__':
    DeliverooApp().run()
