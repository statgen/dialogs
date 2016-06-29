#!/usr/bin/env python2

import sys
import dialogs
from dialogs import Dialog, Button, Label, Checkbox

dialog = None

def ok(button):
   info = Dialog("", 40, 6)
   bInfoOk = Button(1, "Ok")
   label = Label("", 38)
   info.addComponent(label, 1, 2)
   info.addComponent(bInfoOk, 31, 4)
   info.center()

   selected = []
   for i in xrange(0, len(checkbox)):
      if checkbox[i].checked:
         selected.append(i + 1)

   label.setText("Selected: " + str(selected))

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
      dialogs.initScreen("DEMO")

      dialog = Dialog("Dialog", 50, 12)

      checkbox = [Checkbox(i, "Option {}".format(i+1), 48) for i in xrange(4)]
      bOk = Button(4, "Ok")
      bCancel = Button(5, "Cancel")
      bOk.setCallback(ok)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Select multiple options and press 'Ok' button.", 48), 1, 2)
      for i, cb in enumerate(checkbox):
         dialog.addComponent(cb, 1, i + 4)
      dialog.addComponent(bOk, 29, 10)
      dialog.addComponent(bCancel, 37, 10)
      dialog.center()

      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
