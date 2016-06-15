import sys
import dialogs
from dialogs import Dialog, Button, Label

dialog = None
label = None

def more(button):
   label.setText("To get started, you will need the Python interpreter or a Python IDE.\nPython programs are simply a collection of text files.  If you want something more sophisticated than notepad for editing, you will need a Python IDE (recommend). A Python IDE will make programming Python easier.\n\nFrom http://pythonprogramminglanguage.com web page.")
   button.setVisible(False)
   dialog.draw()
   dialog.focus() 
 
def ok(button):
   dialogs.stop()

if __name__ == '__main__':
   try:
      dialogs.initScreen("DEMO")

      dialog = Dialog("Dialog", 60, 14)
      bMore = Button(1, "More")
      bOk = Button(2, "Ok")
      label = Label("Python is a computer programming language that lets you work more quickly than other programming languages. Experienced programmers in any other language can pick up Python very quickly, and beginners find the clean syntax and indentation structure easy to learn.\n\nFrom http://pythonprogramminglanguage.com web page.", 58)
      bMore.setCallback(more)
      bOk.setCallback(ok)
      dialog.addComponent(label, 1, 2)
      dialog.addComponent(bMore, 41, 12)
      dialog.addComponent(bOk, 51, 12)
      dialog.center()

      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
