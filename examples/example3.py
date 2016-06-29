#!/usr/bin/env python2

import sys
import dialogs
from dialogs import Dialog, Button, Label

dialog = None

def showAlert(button):
   alert = Dialog("Alert", 40, 6, dialogs.ALERT_DIALOG_DECO)
   bOk = Button(1, "Ok", dialogs.ALERT_BUTTON_DECO)
   alert.addComponent(Label("Press 'Ok' button to close alert dialog.", 38), 1, 2)
   alert.addComponent(bOk, 31, 4)
   alert.center()

   def ok(button):
      alert.destroy()
      dialog.focus()
  
   bOk.setCallback(ok)
   dialog.unfocus()
   alert.draw()
   alert.focus()
   
 
def cancel(button):
   dialogs.stop()

if __name__ == '__main__':
   try:
      dialogs.initScreen("DEMO")

      dialog = Dialog("Dialog", 60, 10)
      bShowAlert = Button(1, "Alert")
      bCancel = Button(2, "Cancel")
      bShowAlert.setCallback(showAlert)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Press 'Alert' button to show alert dialog.", 58), 1, 2)
      dialog.addComponent(bShowAlert, 36, 8)
      dialog.addComponent(bCancel, 47, 8)
      dialog.center()

      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
