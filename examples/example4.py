#!/usr/bin/env python2

import sys
import dialogs
from dialogs import Dialog, Button, Label, Progressbar
import time

dialog = None

def start(button):
   progressDialog = Dialog("", 40, 5)
   progress = Progressbar(38, 0, 10)
   progressDialog.addComponent(progress, 1, 2)
   progressDialog.center()

   dialog.unfocus()
   progressDialog.draw()
   progressDialog.focus()

   for i in range(1, 11):
      time.sleep(0.5)
      progress.setValue(i)
   time.sleep(0.5)

   progressDialog.destroy()
   dialog.focus() 
 
def cancel(button):
   dialogs.stop()

if __name__ == '__main__':
   try:
      dialogs.initScreen()
      dialogs.setTitle("DEMO")

      dialog = Dialog("Dialog", 60, 9)
      bStart = Button(1, "Start")
      bCancel = Button(2, "Cancel")
      bStart.setCallback(start)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Press 'Start' button to show progress bar.", 58), 1, 2)
      dialog.addComponent(bStart, 36, 7)
      dialog.addComponent(bCancel, 47, 7)
      dialog.center()

      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
