#!/usr/bin/env python2

import sys
import dialogs
from dialogs import Dialog, Button, Label, Dropdown

dialog = None
dropdown = None

def ok(button):
   info = Dialog("", 40, 6)
   bInfoOk = Button(1, "Ok")
   label = Label("", 38)
   info.addComponent(label, 1, 2)
   info.addComponent(bInfoOk, 31, 4)
   info.center()

   value = dropdown.getValue()
   label.setText("Selected: " + value['label'] + " (" + value['value'] + ")")

   def infoOk(button):
      info.destroy()
      dialog.focus()

   bInfoOk.setCallback(infoOk)
   dialog.unfocus()
   info.draw()
   info.focus()
 
def cancel(button):
   dialogs.stop()

if __name__ == '__main__':
   try:
      items = [{"label": "Option {}".format(i), "value": "Value {}".format(i)} for i in xrange(1,35)]

      dialogs.initScreen("DEMO")

      dialog = Dialog("Dialog", 52, 8)
      dropdown = Dropdown(1, items, 12)
      bOk = Button(2, "Ok")
      bCancel = Button(3, "Cancel")
      dropdown.setPopupWidth(10)
      bOk.setCallback(ok)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Select option and press 'Ok' button:", 38), 1, 2)
      dialog.addComponent(dropdown, 38, 2)
      dialog.addComponent(bOk, 31, 6)
      dialog.addComponent(bCancel, 39, 6)
      dialog.center()

      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
