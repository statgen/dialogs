#!/usr/bin/env python2

import sys
import dialogs
from dialogs import Dialog, Button

dialog1 = None
dialog2 = None

def next(button):
   dialog1.unfocus()
   dialog1.erase()
   dialog2.draw()
   dialog2.focus()

def back(button):
   dialog2.unfocus()
   dialog2.erase()
   dialog1.draw()
   dialog1.focus()

def finish(button):
   dialogs.stop()

def cancel(button):
   dialogs.stop()

if __name__ == '__main__':
   try:
      dialogs.initScreen("DEMO")

      dialog1 = Dialog("Dialog 1", 60, 8)
      bNext1 = Button(1, "Next")
      bCancel1 = Button(2, "Cancel")
      bNext1.setCallback(next)
      bCancel1.setCallback(cancel)
      dialog1.addComponent(bNext1, 37, 6)
      dialog1.addComponent(bCancel1, 47, 6)
      dialog1.center()

      dialog2 = Dialog("Dialog 2", 60, 8)
      bFinish2 = Button(1, "Finish")
      bBack2 = Button(2, "Back")
      bCancel2 = Button(3, "Cancel")
      bFinish2.setCallback(finish)
      bBack2.setCallback(back)
      bCancel2.setCallback(cancel)
      dialog2.addComponent(bFinish2, 25, 6)
      dialog2.addComponent(bBack2, 37, 6)
      dialog2.addComponent(bCancel2, 47, 6)
      dialog2.center()

      dialog1.draw()
      dialog1.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
