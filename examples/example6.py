import sys
import dialogs
from dialogs import Dialog, Button, Label, Checkbox

dialog = None
checkbox = [None] * 4

def check(button):
   if button.checked:
      for c in checkbox:
         if id(c) != id(button) and c.checked:
            c.uncheck()
      button.focus()
   else:
      button.check()

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
      for i in xrange(0, len(checkbox)):
         checkbox[i] = Checkbox(i, "Option " + str(i + 1), 48)
         checkbox[i].setCallback(check)
      bOk = Button(4, "Ok")
      bCancel = Button(5, "Cancel")
      bOk.setCallback(ok)
      bCancel.setCallback(cancel)
      dialog.addComponent(Label("Select single option and press 'Ok' button:", 48), 1, 2)
      for i in xrange(0, len(checkbox)):
         dialog.addComponent(checkbox[i], 1, i + 4)
      dialog.addComponent(bOk, 29, 10)
      dialog.addComponent(bCancel, 37, 10)
      dialog.center()

      checkbox[0].check()
      dialog.draw()
      dialog.focus()

      dialogs.start()

      dialogs.closeScreen()
   except:
      dialogs.closeScreen()
      print sys.exc_info()
