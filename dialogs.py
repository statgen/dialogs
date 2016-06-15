# contact Daniel Taliun dtaliun@umich.edu in case you have questions

import sys
import curses
import curses.ascii
import curses.panel
import math

__screen__ = None
__run__ = False
__listener__ = None
__input__ = None

DIALOG_DECO = {
   'shadow': 1,
   'background': 4,
   'border': 4,
   'title': 5,
}

BUTTON_DECO = {
   'focused': 2,
   'unfocused': 4
}

CHECKBOX_DECO = {
   'focused': 6,
   'unfocused': 4
}

TEXTFIELD_DECO = {
   'background': 6
}

COMBOBOX_DECO = {
   'background': 6,
   'selection': 7
}

DROPDOWN_DECO = {
   'background': 6,
   'unfocused': 5,
   'focused': 2,
   'selection': 7
}

PROGRESSBAR_DECO = {
   'background': 4,
   'emptybin': 6,
   'filledbin': 1
}

LABEL_DECO = {
   'background': 4
}

ALERT_DIALOG_DECO = {
   'shadow': 1,
   'background': 4,
   'border': 8,
   'title': 9
}

ALERT_BUTTON_DECO = {
   'focused': 9,
   'unfocused': 4 
}


def isListening(component):
   global __listener__
   if __listener__ is None:
      return False
   return id(__listener__) == id(component)

def setListener(component):
   global __listener__

   if isinstance(component, Listener):
      curses.flushinp()
      __listener__ = component

def clearListener():
   global __listener__
   curses.flushinp()
   __listener__ = None

def getInput():
   global __input__
   return __input__

def popInput():
   global __input__
   copy = __input__
   __input__ = None 
   return copy

def clearInput():
   global __input__
   __input__ = None

def initScreen(title):
   global __screen__

   if not __screen__ is None:
      return 

   __screen__ = curses.initscr()
   maxY, maxX = __screen__.getmaxyx()

   curses.start_color() 
   curses.noecho()
   curses.cbreak()    

   curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK) 
   curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLUE)
   curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_WHITE)
   curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_WHITE)
   curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)    
   curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_CYAN) 
   curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)
   curses.init_pair(8, curses.COLOR_RED, curses.COLOR_WHITE)
   curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_RED) 

   __screen__.keypad(1)
   __screen__.bkgd(' ', curses.color_pair(2))
   __screen__.addstr(1, 1, title, curses.A_BOLD);
   __screen__.hline(2, 1, curses.ACS_HLINE, maxX - 2)
   __screen__.refresh()

def getScreenWidth():
   if __screen__ is not None:
      return __screen__.getmaxyx()[1]
   return None

def getScreenHeight():
   if __screen__ is not None:
      return __screen__.getmaxyx()[0]
   return None

def start():
   global __screen__
   global __run__
   global __input__
   global __listener__

   if __screen__ is None:
      return

   __run__ = True
 
   while __run__:
      __input__ = __screen__.getch()
      while __input__ is not None:
         if __listener__ is not None:
            __listener__.run()
         else:
            __input__ = None
  
def stop():
   global __run__
   __run__ = False

def closeScreen():
   global __screen__
   if __screen__ is not None:
      __screen__.keypad(0)
      __screen__ = None
      curses.nocbreak()
      curses.echo()
      curses.endwin() 

# Any visual element must inherit Component
class Component(object):

   def setXY(self, x, y):
      pass
     
   def getX(self):
      return 0

   def getY(self):
      return 0

   def destroy(self):
      pass

   def bringToFront(self):
      pass

   # returns True if draw() method was called
   def isDisplayed(self):
      return False

   # erase component from screen if isDisplayed() == True
   def erase(self):
      pass

   # draw component on screen if isVisible() == True
   def draw(self):
      pass

   def isVisible(self):
      return False

   def setVisible(self, flag):
      pass

# Any control that can listen for input events must inherit Listener
class Listener(object):

   def setParentDialog(self, component):
      pass

   def getRank(self):
      return 0

   def run(self):
      pass

   def unfocus(self):
      pass

   def focus(self):
      pass

class Dialog(Component, Listener):

   def __find_active_control(self):
      if self.activeControl is None:
         controls = range(0, len(self.controls))
      else:
         controls = range(self.activeControl, len(self.controls))
         controls.extend(range(0, min(self.activeControl, len(self.controls))))
         self.activeControl = None   

      for i in controls:
         if self.controls[i].isDisplayed():
            self.activeControl = i
            break

   def __next_active_control(self, forward = True):
      if self.activeControl is None:
         controls = range(0, len(self.controls))
      elif forward:
         controls = range(self.activeControl + 1, len(self.controls))
         controls.extend(range(0, min(self.activeControl + 1, len(self.controls))))
         self.activeControl = None
      else:
         controls = range(0, min(self.activeControl, len(self.controls)))
         controls.reverse()
         tail = range(self.activeControl, len(self.controls))
         tail.reverse()
         controls.extend(tail)
         self.activeControl = None
      
      for i in controls:
         if self.controls[i].isDisplayed():
            self.activeControl = i
            break

   def setCallback(self, callback):
      self.callback = callback
     
   def addComponent(self, component, x = 0, y = 0):
      windowY, windowX = self.window.getbegyx()
      component.setXY(windowX + x, windowY + y)
      if isinstance(component, Listener):
         component.setParentDialog(self)
         inserted = False
         for i in xrange(0, len(self.controls)):
            if component.getRank() <= self.controls[i].getRank():
               self.controls.insert(i, component)
               inserted = True
               break
         if not inserted:
            self.controls.append(component)
      self.components.append(component)

   def center(self):
      self.setXY(int(getScreenWidth() / 2) - int(self.width / 2), int(getScreenHeight() / 2) - int(self.height / 2))

   def run(self):
      ch = popInput() 
      if ch == curses.KEY_LEFT or ch == curses.KEY_UP:
         self.__next_active_control(False)
         if not self.activeControl is None:
            self.controls[self.activeControl].focus() 
      elif ch == curses.KEY_RIGHT or ch == curses.KEY_DOWN:
         self.__next_active_control(True)
         if not self.activeControl is None: 
            self.controls[self.activeControl].focus()
      elif not self.callback is None:
         self.callback(self, ch)

   def focus(self):
      if self.displayed:
         self.bringToFront()
         self.window.move(self.height - 1, self.width - 1)
         self.window.refresh()
         setListener(self)
         self.__find_active_control()
         if self.activeControl is not None:
            self.controls[self.activeControl].focus()
       
   def unfocus(self):
      if self.displayed:
         if self.activeControl is not None:
            self.controls[self.activeControl].unfocus()
            self.activeControl = None
         if isListening(self):
            clearListener()

   def setXY(self, x, y):
      windowY, windowX = self.window.getbegyx()
      dX = x - windowX
      dY = y - windowY
      self.shadowPanel.move(y + 1, x + 2)
      self.windowPanel.move(y, x)
      for c in self.components: c.setXY(c.getX() + dX, c.getY() + dY)
      curses.panel.update_panels()
      curses.doupdate()
  
   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]
 
   def destroy(self):
      self.erase()
      if isListening(self):
         clearListener()
      self.callback = None
      for c in self.components: c.destroy()
      del self.shadowPanel 
      self.shadowPanel = None
      del self.shadow
      self.shadow = None
      del self.windowPanel
      self.windowPanel = None
      del self.window
      self.window = None
      curses.panel.update_panels()

   def bringToFront(self):
      self.shadowPanel.top()
      self.windowPanel.top()
      if not self.displayed:
         self.shadowPanel.hide()
         self.windowPanel.hide()
      curses.panel.update_panels()
      for c in self.components:
         c.bringToFront()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         for c in self.components: 
            if c.isDisplayed():
               c.erase()
         self.shadowPanel.hide()
         self.windowPanel.hide()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True

   def draw(self):
      if self.visible:
         self.shadowPanel.show()
         self.windowPanel.show()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True
         for c in self.components:
            if c.isVisible():
               c.draw()
                 
   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag

   def __init__(self, title, width = 80, height = 20, decoration = DIALOG_DECO, x = 0, y = 0):
      self.width = width
      self.height = height
      self.decoration = decoration
      self.controls = []
      self.activeControl = None
      self.components = []
      self.visible = True
      self.displayed = False
      self.callback = None

      if title:
         self.title = " " + title + " "
      else:
         self.title = None

      self.shadow = curses.newwin(self.height, self.width, y + 1, x + 2)
      self.window = curses.newwin(self.height, self.width, y, x)
    
      self.shadow.bkgd(' ', curses.color_pair(self.decoration['shadow']))      
      self.window.bkgd(' ', curses.color_pair(self.decoration['background']))

      self.window.attrset(curses.color_pair(self.decoration['border']))
      self.window.border(0)

      if self.title is not None:
         self.window.addstr(0, int(self.width / 2) - int(len(self.title) /  2), self.title, (curses.color_pair(self.decoration['title']))) 
 
      self.shadowPanel = curses.panel.new_panel(self.shadow)
      self.shadowPanel.top()
      self.shadowPanel.hide()

      self.windowPanel = curses.panel.new_panel(self.window)
      self.windowPanel.top()
      self.windowPanel.hide()

      curses.panel.update_panels()


class Button(Component, Listener):

   def setCallback(self, callback):
      self.callback = callback

   def setParentDialog(self, component):
      self.parent = component

   def getRank(self):
      return self.rank

   def run(self):
      ch = getInput()      
      if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
         clearInput()
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed(): 
            self.parent.focus()
         if not self.callback is None:
            self.callback(self)
      elif ch == curses.KEY_LEFT or ch == curses.KEY_RIGHT or ch == curses.KEY_UP or ch == curses.KEY_DOWN:
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed(): 
            setListener(self.parent)
      else:
         clearInput() 

   def unfocus(self):
      if self.displayed:
         self.window.chgat(0, 0, curses.color_pair(self.decoration['unfocused']))
         self.window.refresh()
         if isListening(self):
            clearListener()

   def focus(self):
      if self.displayed:
         self.bringToFront()
         self.window.chgat(0, 0, curses.color_pair(self.decoration['focused']))
         self.window.move(0, 3)
         self.window.refresh()
         setListener(self)

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()

   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]

   def destroy(self):
      self.erase()
      if isListening(self):
         clearListener()
      self.parent = None
      self.callback = None
      del self.panel
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels()

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
         self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = False
         
   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True

   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag
  
   def __init__(self, rank, text, decoration = BUTTON_DECO, x = 0, y = 0):
      self.rank = rank
      self.text = text
      self.deco_text = "< " + self.text + " >"
      self.decoration = decoration
      self.width = len(self.deco_text) + 2
      self.height = 1
      self.visible = True
      self.displayed = False
      self.parent = None
      self.callback = None
 
      self.window = curses.newwin(self.height, self.width, y, x)
      self.window.bkgd(' ', curses.color_pair(self.decoration["unfocused"]))
      self.window.addstr(0, 1, self.deco_text)
      self.window.keypad(1)

      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()

      curses.panel.update_panels()


class Checkbox(Component, Listener):

   def check(self):
      self.checked = True
      attr = self.window.inch(0, 1) & 0xFF00
      self.window.addch(0, 1, '*', attr)
      self.window.move(0, 1)
      if self.displayed:
         self.window.refresh()
      
   def uncheck(self):
      self.checked = False
      attr = self.window.inch(0, 1) & 0xFF00
      self.window.addch(0, 1, ' ', attr)
      self.window.move(0, 1)
      if self.displayed:
         self.window.refresh()

   def setCallback(self, callback):
      self.callback = callback

   def setParentDialog(self, component):
      self.parent = component

   def getRank(self):
      return self.rank

   def run(self):
      ch = getInput()
      if ch == curses.KEY_ENTER or ch == 10 or ch == 13 or ch == curses.ascii.SP:
         clearInput()
         if not self.checked:
            self.check()
         else:
            self.uncheck()
         if self.callback is not None:
            self.callback(self)
      elif ch == curses.KEY_LEFT or ch == curses.KEY_RIGHT or ch == curses.KEY_UP or ch == curses.KEY_DOWN:
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed():
            setListener(self.parent)
      else:
         clearInput()

   def unfocus(self):
      if self.displayed:
         self.window.chgat(0, 0, curses.color_pair(self.decoration['unfocused']))
         self.window.refresh()
         if isListening(self):
            clearListener()

   def focus(self):
      if self.displayed:
         self.bringToFront()
         self.window.chgat(0, 0, curses.color_pair(self.decoration['focused']))
         self.window.move(0, 1)
         self.window.refresh()
         setListener(self)

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()

   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]

   def destroy(self):
      self.erase()
      if isListening(self):
         clearListener()
      self.parent = None
      self.callback = None
      del self.panel
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels()

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
         self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = False

   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True

   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag

   def __init__(self, rank, text, width = 80, decoration = CHECKBOX_DECO, x = 0, y = 0):
      self.rank = rank
      self.width = width
      self.height = 1
      self.decoration = decoration
      self.text = text
      self.visible = True
      self.displayed = False 
      self.parent = None
      self.callback = None
      self.checked = False

      self.window = curses.newwin(self.height, self.width, y, x)
      self.window.bkgd(' ', curses.color_pair(self.decoration['unfocused']))
      self.window.keypad(1)

      self.window.addstr(0, 0, "[ ] " + self.text)

      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()
      
      curses.panel.update_panels()


class Textfield(Component, Listener):

   def setText(self, text):
      self.text = []
      self.i = 0
      self.fieldOffset = 0
      for character in text:
         self.text.append(character)
         self.i += 1
         if self.i > self.fieldOffset + self.width - 1:
            self.fieldOffset += 1
      self.window.clear()
      self.window.addnstr(0, 0, "".join(self.text[self.fieldOffset:]), self.width - 1)
      if self.displayed:      
         self.window.refresh()

   def setCallback(self, callback):
      self.callback = callback

   def setParentDialog(self, component):
      self.parent = component

   def getRank(self):
      return self.rank

   def run(self):
      ch = getInput()   
      if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
         clearInput()
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed():
            self.parent.focus()
         if not self.callback is None:
            self.callback() 
      elif ch == curses.KEY_UP or ch == curses.KEY_DOWN:
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed():
            setListener(self.parent)
      else:
         clearInput()
         if ch == curses.KEY_LEFT:
            if self.i > 0:
               self.i -= 1
               if self.i < self.fieldOffset: self.fieldOffset = self.i
         elif ch == curses.KEY_RIGHT:
            if self.i < len(self.text):
               self.i += 1
               if self.i > self.fieldOffset + self.width - 1: self.fieldOffset += 1
         elif ch == curses.KEY_DC:
            if self.i < len(self.text):
               self.text.pop(self.i)
         elif ch == curses.KEY_BACKSPACE or ch == curses.ascii.DEL:
            if self.i > 0:
               self.i -= 1
               self.text.pop(self.i)
               if self.i < self.fieldOffset: self.fieldOffset = self.i 
         elif curses.ascii.isprint(ch):
            self.text.insert(self.i, curses.ascii.unctrl(ch))
            self.i += 1
            if self.i > self.fieldOffset + self.width - 1: self.fieldOffset += 1
         self.window.clear()
         self.window.addnstr(0, 0, "".join(self.text[self.fieldOffset:]), self.width - 1)
         self.window.move(0, self.i - self.fieldOffset)
         self.window.refresh()

   def unfocus(self):
      if self.displayed:
         if isListening(self):
            clearListener()
 
   def focus(self):
      if self.displayed:
         self.bringToFront()
         self.window.move(0, self.i - self.fieldOffset)
         self.window.refresh()
         setListener(self)

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()

   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]
 
   def destroy(self):
      self.erase()
      if isListening(self):
         clearListener()
      self.parent = None
      self.callback = None
      del self.panel 
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels() 

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
         self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels() 
         curses.doupdate()
         self.displayed = False

   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels() 
         curses.doupdate()
         self.displayed = True
  
   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag
 
   def __init__(self, rank, width = 80, decoration = TEXTFIELD_DECO, x = 0, y = 0):
      self.rank = rank
      self.width = width
      self.height = 1
      self.decoration = decoration
      self.text = []
      self.visible = True
      self.displayed = False
      self.parent = None   
      self.i = 0
      self.fieldOffset = 0
      self.callback = None

      self.window = curses.newwin(self.height, self.width, y, x) 
      self.window.bkgd(' ', curses.color_pair(self.decoration['background']))
      self.window.keypad(1)
      
      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()
      
      curses.panel.update_panels()


class Combobox(Component, Listener):

   def __create_popup(self):
      if len(self.__popup_items) > self.popupPageSize:
         self.__popup_height = self.popupPageSize + 2
      else:
         self.__popup_height = len(self.__popup_items) + 2
      self.__popup_width = self.popupWidth + 2
     
      self.popupWindow = curses.newwin(self.__popup_height, self.__popup_width, self.getY() + 1, self.getX()) 
      self.popupWindow.bkgd(' ', curses.color_pair(self.decoration['background']))            
      self.popupWindow.border(0)

      self.popupPanel = curses.panel.new_panel(self.popupWindow)
      self.popupPanel.top()
            
      curses.panel.update_panels()

      self.__popup_i = 0
      self.__popup_offset = 0
      self.__popup_pages = int(math.ceil(len(self.__popup_items) / float(self.popupPageSize)))
      self.__popup_page = 1
      self.__popup = True

   def __load_popup_items(self):
     if self.__popup:
        self.popupWindow.clear()
        self.popupWindow.border(0)
        for i, y in zip(xrange(self.__popup_offset, len(self.__popup_items)), xrange(1, self.__popup_height - 1)):
           self.popupWindow.addnstr(y, 1, self.__popup_items[i]["popup_text"][:self.popupWidth], self.__popup_width - 2)
        self.popupWindow.addstr(self.__popup_height - 1, 1, " " + str(self.__popup_page) + "/" + str(self.__popup_pages) + " ")
        self.popupWindow.refresh()

   def __select_popup_item(self):
      if self.__popup:
         y = self.__popup_i - self.__popup_offset + 1
         self.popupWindow.chgat(y, 1, self.__popup_width - 2, curses.color_pair(self.decoration['selection']))
         self.popupWindow.refresh()

   def __deselect_popup_item(self):
      if self.__popup:
         y = self.__popup_i - self.__popup_offset + 1
         self.popupWindow.chgat(y, 1, self.__popup_width - 2, curses.color_pair(self.decoration['background']))
         self.popupWindow.refresh()

   def __destroy_popup(self):
      if self.__popup:
         self.popupPanel.hide()
         del self.popupPanel
         self.popupPanel = None
         del self.popupWindow
         self.popupWindow = None
         curses.panel.update_panels()     
         self.__popup = False 

   def setText(self, text):
      self.text = []
      self.__field_i = 0
      self.__field_offset = 0
      for character in text:
         self.text.append(character)
         self.__field_i += 1
         if self.__field_i > self.__field_offset + self.width - 1:
            self.__field_offset += 1
      self.window.clear()
      self.window.addnstr(0, 0, "".join(self.text[self.__field_offset:]), self.width - 1)
      if self.displayed:      
         self.window.refresh()

   def setPopupWidth(self, width):
      self.popupWidth = width
  
   def setPopupPageSize(self, size):
      self.popupPageSize = size

   def setPopupCallback(self, callback):
      self.popupCallback = callback

   def setCallback(self, callback):
      self.callback = callback

   def getRank(self):
      return self.rank

   def setParentDialog(self, component):
      self.parent = component

   def run(self):
      ch = getInput()

      if self.__popup:
         if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
            clearInput()
            self.text = []
            self.__field_i = 0
            self.__field_offset = 0
            for character in self.__popup_items[self.__popup_i]["textfield_text"]:
               self.__field_i += 1
               if self.__field_i > self.__field_offset + self.width - 1:
                  self.__field_offset += 1
               self.text.append(character)
            self.__destroy_popup()
            self.window.clear()
            self.window.addnstr(0, 0, "".join(self.text[self.__field_offset:]), self.width - 1)
            self.window.move(0, self.__field_i - self.__field_offset)
            self.window.refresh()
            return
         elif ch == curses.KEY_UP:
            clearInput()
            if self.__popup_i > 0:
               self.__deselect_popup_item()
               self.__popup_i -= 1
               if self.__popup_i < self.__popup_offset:
                  self.__popup_page -= 1
                  self.__popup_offset -= self.popupPageSize 
                  self.__load_popup_items()
               self.__select_popup_item()
            return
         elif ch == curses.KEY_DOWN:
            clearInput()
            if self.__popup_i < len(self.__popup_items) - 1:
               self.__deselect_popup_item()
               self.__popup_i += 1
               if self.__popup_i > self.__popup_offset + self.popupPageSize - 1: 
                  self.__popup_page += 1
                  self.__popup_offset += self.popupPageSize
                  self.__load_popup_items()
               self.__select_popup_item()
            return
         elif ch == curses.ascii.TAB:
            clearInput()
            self.__destroy_popup()
            self.window.refresh()
            return
         else:
            self.__destroy_popup()

      if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
         clearInput()
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed():
            self.parent.focus()
         if not self.callback is None:
            self.callback()
      elif ch == curses.KEY_UP or ch == curses.KEY_DOWN:
         self.unfocus()
         if self.parent is not None and self.parent.isDisplayed():
            setListener(self.parent)
      else:
         clearInput()
         if ch == curses.KEY_LEFT:
            if self.__field_i > 0:
               self.__field_i -= 1
               if self.__field_i < self.__field_offset: 
                  self.__field_offset = self.__field_i
         elif ch == curses.KEY_RIGHT:
            if self.__field_i < len(self.text):
               self.__field_i += 1
               if self.__field_i > self.__field_offset + self.width - 1: 
                  self.__field_offset += 1
         elif ch == curses.KEY_DC:
            if self.__field_i < len(self.text):
               self.text.pop(self.__field_i)
         elif ch == curses.KEY_BACKSPACE or ch == curses.ascii.DEL:
            if self.__field_i > 0:
               self.__field_i -= 1
               self.text.pop(self.__field_i)
               if self.__field_i < self.__field_offset: 
                  self.__field_offset = self.__field_i
         elif ch == curses.ascii.TAB:
            if self.popupCallback is not None:
               self.__popup_items = self.popupCallback(self)     
               if self.__popup_items:
                  self.__create_popup()
                  self.__load_popup_items()
                  self.__select_popup_item()
         elif curses.ascii.isprint(ch):
            self.text.insert(self.__field_i, curses.ascii.unctrl(ch))
            self.__field_i += 1
            if self.__field_i > self.__field_offset + self.width - 1:
               self.__field_offset += 1
         self.window.clear()
         self.window.addnstr(0, 0, "".join(self.text[self.__field_offset:]), self.width - 1)
         self.window.move(0, self.__field_i - self.__field_offset)
         self.window.refresh()

   def unfocus(self):
      if self.displayed:
         if isListening(self):
            clearListener()

   def focus(self):
      if self.displayed:
         self.bringToFront()
         self.window.move(0, self.__field_i - self.__field_offset)
         self.window.refresh()
         setListener(self)

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()
      
   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]
 
   def destroy(self):
      self.erase()
      if isListening(self):
         clearListener()
      self.parent = None
      self.popupCallback = None
      self.callback = None
      del self.panel 
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels() 

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
         self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels() 
         curses.doupdate()
         self.displayed = False

   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels() 
         curses.doupdate()
         self.displayed = True

   def isVisible(self):
      return self.visible   

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag
 
   def __init__(self, rank, width = 80, decoration = COMBOBOX_DECO, x = 0, y = 0):
      self.rank = rank
      self.width = width
      self.height = 1
      self.decoration = decoration
      self.text = []
      self.visible = True
      self.displayed = False
      self.parent = None   
      self.popupCallback = None
      self.callback = None

      self.__field_i = 0
      self.__field_offset = 0

      self.__popup = False
      self.popupPageSize = 10
      self.popupWidth = self.width - 2
      
      self.__popup_height = self.popupPageSize + 2
      self.__popup_width = self.popupWidth + 2
      self.__popup_items = []
      self.__popup_pages = 0
      self.__popup_page = 0
      self.__popup_i = 0
      self.__popup_offset = 0

      self.window = curses.newwin(self.height, self.width, y, x) 
      self.window.bkgd(' ', curses.color_pair(self.decoration['background']))
      self.window.keypad(1)
      
      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()
      
      curses.panel.update_panels()

class Dropdown(Component, Listener):

   def __create_popup(self):
      if len(self.__popup_items) > self.popupPageSize:
         self.__popup_height = self.popupPageSize + 2
      else:
         self.__popup_height = len(self.__popup_items) + 2
      self.__popup_width = self.popupWidth + 2
     
      self.popupWindow = curses.newwin(self.__popup_height, self.__popup_width, self.getY() + 1, self.getX()) 
      self.popupWindow.bkgd(' ', curses.color_pair(self.decoration['background']))            
      self.popupWindow.border(0)

      self.popupPanel = curses.panel.new_panel(self.popupWindow)
      self.popupPanel.top()
            
      curses.panel.update_panels()

  #    self.__popup_i = 0
  #    self.__popup_offset = 0
      self.__popup_pages = int(math.ceil(len(self.__popup_items) / float(self.popupPageSize)))
  #    self.__popup_page = 1
      self.__popup = True

   def __load_popup_items(self):
     if self.__popup:
        self.popupWindow.clear()
        self.popupWindow.border(0)
        for i, y in zip(xrange(self.__popup_offset, len(self.__popup_items)), xrange(1, self.__popup_height - 1)):
           self.popupWindow.addnstr(y, 1, self.__popup_items[i]["label"][:self.popupWidth], self.__popup_width - 2)
        self.popupWindow.addstr(self.__popup_height - 1, 1, " " + str(self.__popup_page) + "/" + str(self.__popup_pages) + " ")
        self.popupWindow.refresh()


   def __select_popup_item(self):
      if self.__popup:
         y = self.__popup_i - self.__popup_offset + 1
         self.popupWindow.chgat(y, 1, self.__popup_width - 2, curses.color_pair(self.decoration['selection']))
         self.popupWindow.refresh()

   def __deselect_popup_item(self):
      if self.__popup:
         y = self.__popup_i - self.__popup_offset + 1
         self.popupWindow.chgat(y, 1, self.__popup_width - 2, curses.color_pair(self.decoration['background']))
         self.popupWindow.refresh()

   def __destroy_popup(self):
      if self.__popup:
         self.popupPanel.hide()
         del self.popupPanel
         self.popupPanel = None
         del self.popupWindow
         self.popupWindow = None
         curses.panel.update_panels()     
         self.__popup = False 

  
   def getValue(self):
      if self.__popup_items:
         return self.__popup_items[self.__popup_i]
      return None

   def setPopupWidth(self, width):
      self.popupWidth = width

   def setPopupPageSize(self, size):
      self.popupPageSize = size

   def setCallback(self, callback):
      self.callback = callback

   def getRank(self):
      return self.rank

   def setParentDialog(self, component):
      self.parent = component

   def run(self):
      ch = getInput()
      if self.__popup:
         clearInput()
         if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
            self.__destroy_popup()
            self.window.clear()
            self.window.addnstr(0, 0, self.__popup_items[self.__popup_i]['label'], self.width - 2)
            self.window.insch(0, self.width - 1, 'v', curses.color_pair(self.decoration['focused'])) 
            self.window.move(0, self.width - 1) 
            self.window.refresh()
         elif ch == curses.KEY_UP:
            if self.__popup_i > 0:
               self.__deselect_popup_item()
               self.__popup_i -= 1
               if self.__popup_i < self.__popup_offset:
                  self.__popup_page -= 1
                  self.__popup_offset -= self.popupPageSize 
                  self.__load_popup_items()
               self.__select_popup_item()
         elif ch == curses.KEY_DOWN:
            if self.__popup_i < len(self.__popup_items) - 1:
               self.__deselect_popup_item()
               self.__popup_i += 1
               if self.__popup_i > self.__popup_offset + self.popupPageSize - 1: 
                  self.__popup_page += 1
                  self.__popup_offset += self.popupPageSize
                  self.__load_popup_items()
               self.__select_popup_item()
      else:
         if ch == curses.KEY_ENTER or ch == 10 or ch == 13:
            clearInput()
            if self.__popup_items:
               self.__create_popup()
               self.__load_popup_items()
               self.__select_popup_item()
         elif ch == curses.KEY_LEFT or ch == curses.KEY_RIGHT or ch == curses.KEY_UP or ch == curses.KEY_DOWN:
            self.unfocus()
            if self.parent is not None and self.parent.isDisplayed():
               setListener(self.parent)
         else:
            clearInput()

   def unfocus(self):
      if self.displayed:
         self.window.chgat(0, self.width - 1, curses.color_pair(self.decoration['unfocused']))
         self.window.refresh()
         if isListening(self):
            clearListener();

   def focus(self):
      if self.displayed:
         self.bringToFront()
         self.window.chgat(0, self.width - 1, curses.color_pair(self.decoration['focused']))
         self.window.move(0, self.width - 1)
         self.window.refresh()
         setListener(self)

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()

   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]

   def destroy(self):
      self.erase()
      if isListening(self):
         clearListener()
      self.parent = None
      self.callback = None
      del self.panel
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels()

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
         self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed 

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = False

   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True

   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag

   def __init__(self, rank, items, width = 80, decoration = DROPDOWN_DECO, x = 0, y = 0):
      self.rank = rank
      self.width = width 
      self.height = 1
      self.decoration = decoration
      self.visible = True
      self.displayed = False
      self.parent = None
      self.callback = None
     
      self.__popup = False
      self.popupPageSize = 10
      self.popupWidth = self.width - 2

      self.__popup_height = self.popupPageSize + 2
      self.__popup_width = self.popupWidth + 2
      self.__popup_items = items
      self.__popup_pages = 0
      self.__popup_page = 1
      self.__popup_i = 0
      self.__popup_offset = 0

      self.window = curses.newwin(self.height, self.width, y, x)
      self.window.bkgd(' ', curses.color_pair(self.decoration['background']))
      self.window.keypad(1)

      if self.__popup_items:
         self.window.addnstr(0, 0, self.__popup_items[self.__popup_i]['label'], self.width - 2)
      self.window.insch(0, self.width - 1, 'v', curses.color_pair(self.decoration['unfocused'])) 

      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()    

      curses.panel.update_panels() 

class Progressbar(Component):

   def computeProgress(self):
      nch = self.width - 2
      pr = (self.value - self.minValue)  / float(self.maxValue - self.minValue) 
      bins = int(math.floor(nch * pr))
      if not self.filledbins == bins:
         self.filledbins = bins 
         self.window.clear()
         self.window.addch(0, 0, curses.ACS_LTEE)
         for i in xrange(0, nch): self.window.addch(0, i + 1, ' ', curses.color_pair(self.decoration['emptybin']))
         for i in xrange(0, self.filledbins): self.window.addch(0, i + 1, ' ', curses.color_pair(self.decoration['filledbin']))  
         self.window.insch(0, self.width - 1, curses.ACS_RTEE) 
         if self.displayed:
            self.window.refresh()

   def changeMinMax(self, minValue, maxValue):
      self.minValue = minValue
      self.maxValue = maxValue
      self.value = minValue
      self.filledbins = None
      self.computeProgress()

   def setValue(self, value):
      if (value <= self.minValue):
         self.value = self.minValue
      elif (value >= self.maxValue):
         self.value = self.maxValue
      else:
         self.value = value
      self.computeProgress()

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()

   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0] 
   
   def destroy(self):
      self.erase()
      del self.panel
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels()  

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
         self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = False

   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True

   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag
 
   def __init__(self, width = 80, minValue = 0, maxValue = 100, decoration = PROGRESSBAR_DECO, x = 0, y = 0):
      self.width = width
      self.height = 1
      self.minValue = minValue
      self.maxValue = maxValue
      self.value = minValue
      self.filledbins = None
      self.decoration = decoration
      self.visible = True
      self.displayed = False
      self.window = curses.newwin(self.height, self.width, y, x)
      self.window.bkgd(' ', curses.color_pair(self.decoration['background']))

      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()

      curses.panel.update_panels()

      self.computeProgress()


class Label(Component):

   def __append_word(self, word):
      ncols = 0
      nnewcols = len(word)

      if len(self.aligned_text) > 0:
         ncols += len(self.aligned_text[-1])
      else:
         self.aligned_text.append("")

      if ncols + nnewcols >= self.width:
         if nnewcols >= self.width:
            self.aligned_text[-1] += "".join(word[:self.width - nnewcols - 1])
            word = word[self.width - nnewcols - 1:]
         self.aligned_text.append("")
         ncols = 0
      
      if ncols > 0:   
         self.aligned_text[-1] += " ";
      self.aligned_text[-1] += "".join(word)
      

   def setText(self, text):
      self.text = text
      self.aligned_text = []

      word = []

      for ch in self.text:
         if ch == ' ' or ch == '\t':
            self.__append_word(word)
            word = [] 
         elif ch == '\n':
            self.__append_word(word)
            word = []
            self.aligned_text.append("")
         else:
            word.append(ch)        
      
      if len(word) > 0:
         self.__append_word(word)
      
      self.height = max(1, len(self.aligned_text))
      self.window.clear()
      if self.displayed:
         self.window.refresh()
      self.window.resize(self.height, self.width)
      row = 0
      for line in self.aligned_text:
         self.window.addstr(row, 0, line)
         row += 1
      if self.displayed:
         self.window.refresh()

   def setXY(self, x, y):
      self.panel.move(y, x)
      curses.panel.update_panels()
      curses.doupdate()

   def getX(self):
      return self.window.getbegyx()[1]

   def getY(self):
      return self.window.getbegyx()[0]

   def destroy(self):
      self.erase()
      del self.panel 
      self.panel = None
      del self.window
      self.window = None
      curses.panel.update_panels()

   def bringToFront(self):
      self.panel.top()
      if not self.displayed:
          self.panel.hide()
      curses.panel.update_panels()

   def isDisplayed(self):
      return self.displayed

   def erase(self):
      if self.displayed:
         self.panel.hide()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = False  

   def draw(self):
      if self.visible:
         self.panel.show()
         curses.panel.update_panels()
         curses.doupdate()
         self.displayed = True

   def isVisible(self):
      return self.visible

   def setVisible(self, flag):
      if not flag:
         self.erase()
      self.visible = flag       
 
   def __init__(self, text, width = 80, decoration = LABEL_DECO, x = 0, y = 0):
      self.width = width
      self.height = 1
      self.decoration = decoration
      self.visible = True
      self.displayed = False
      self.text = text
      self.aligned_text = []

      self.window = curses.newwin(self.height, self.width, y, x)
      self.window.bkgd(' ', curses.color_pair(self.decoration['background']))

      self.panel = curses.panel.new_panel(self.window)
      self.panel.top()
      self.panel.hide()

      curses.panel.update_panels()

      self.setText(text)


