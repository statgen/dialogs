#!/usr/bin/env python2

import sys
import dialogs
from dialogs import Dialog, Button, Label, Textfield
import time

dialog = None
txtInput = None

def ok(button):
   info = Dialog("", 40, 6)
   bInfoOk = Button(1, "Ok")
   label = Label("", 38)
   info.addComponent(label, 1, 2)
   info.addComponent(bInfoOk, 31, 4)
   info.center()

   label.setText("Entered: " + "".join(txtInput.text))

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
      dialogs.initScreen()
      dialogs.setTitle("DEMO")

      dialog = Dialog("Dialog", 60, 12)
      txtInput = Textfield(1, 58)
      bOk = Button(2, "Ok")
      bCancel = Button(3, "Cancel")
      bOk.setCallback(ok)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Enter text and press 'Ok' button:", 58), 1, 2)
      dialog.addComponent(txtInput, 1, 4)
      dialog.addComponent(bOk, 39, 10)
      dialog.addComponent(bCancel, 47, 10)
      dialog.center()

      txtInput.setText("default text")
      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
