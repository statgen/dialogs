import sys
import dialogs
from dialogs import Dialog, Button, Label, Combobox
import os
import glob

dialog = None
cmbPath = None

def path(combobox):
   text = "".join(combobox.text)
   paths = glob.glob(text + "*")
   items = [None] * len(paths)
   for i in xrange(0, len(paths)):
      head, tail = os.path.split(paths[i])
      items[i] = {"popup_text": tail, "textfield_text": paths[i]}
   items.sort(key=lambda item: item["popup_text"])
   return items

def ok(button):
   info = Dialog("", 40, 6)
   bInfoOk = Button(1, "Ok")
   label = Label("", 38)
   info.addComponent(label, 1, 2)
   info.addComponent(bInfoOk, 31, 4)
   info.center()

   label.setText("Entered: " + "".join(cmbPath.text))

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

      dialog = Dialog("Dialog", 40, 12)
      cmbPath = Combobox(1, 36)
      bOk = Button(2, "Ok")
      bCancel = Button(3, "Cancel")
      cmbPath.setPopupCallback(path)
      cmbPath.setPopupWidth(60)
      bOk.setCallback(ok)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Enter file path (TAB for autocomplete) and press 'Ok' button:", 38), 1, 2)
      dialog.addComponent(cmbPath, 2, 5)
      dialog.addComponent(bOk, 19, 10)
      dialog.addComponent(bCancel, 27, 10)
      dialog.center()

      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
