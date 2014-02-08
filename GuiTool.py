import sys
from xml.dom.minidom import parseString, parse
import __future__

"""
In python3, tkinter is the name for TK interface.
In python2, tkinter as aliased as tkinter.
"""
if sys.version_info[0] == 3:
    import tkinter
    from tkinter import PhotoImage
    from tkinter.filedialog import LoadFileDialog
    from tkinter.font import Font   
else:
    import Tkinter as tkinter
    from Tkinter import PhotoImage
    import FileDialog

class CanvasBase (tkinter.Canvas):
    """
    Dummy canvas based on tkinter.Canvas.
    This is to show how to subclass Canvas.
    """
    def __init__ (self, master, **kargs):
        tkinter.Canvas.__init__ (self, master, kargs)
        self.config (bg='#888888')
        #self.canvasSize = (150, 150)
        #self.bind ('<Configure>', self.resize)

    def resize (self, evt):
        self.drawAll ()

    def drawAll (self):
        print ("Subclass must implement drawAll()")
        pass

def dummy ():
    pass   

class GuiNode:
    """
    Internal data structure representing a GUI node.
    """
    alist = ["tagName",
             "name", 
             "text",
             "items",
             "width", 
             "height",
             "font", 
             "row", 
             "col", 
             "sticky", 
             "colspan", 
             "rowspan", 
             "gridcnf",
             "var",
             "value",
             "items",
             "bg",
             "rowWeight",
             "colWeight",
             "padx",
             "pady",
             "ipadx",
             "ipady",
             "command"]
    
    def __init__(self, tag, attrs):
        self.childNodes = []
        self.tagName = tag
        self.setDefaults()
        for a in self.alist:
            try:
                self.__dict__[a] = attrs[a].value
            except:
                # ignore attribute if not defined
                pass
        self.reCast()
   
    def reCast (self):
        def genf (data):
            def dummy ():
                print ("dummy", data)
            return dummy
        self.row = int(self.row)
        self.col = int(self.col)
        self.colspan = int(self.colspan)
        self.rowspan = int(self.rowspan)
        self.width = int(self.width)
        self.height = int(self.height)
        self.command = genf(self.name)
        self.padx = int(self.padx)
        self.pady = int(self.pady)
        self.ipadx = int(self.ipadx)
        self.ipady = int(self.ipady)

    def setDefaults(self):
        self.name = "undefined"
        self.text = ""
        self.items = ""
        self.width = self.height = 1
        self.font = "Helvetica -12"
        self.row = self.col = 1
        self.rowspan = self.colspan = 1
        self.var = ""
        self.value = ""
        self.sticky = "NEWS"
        self.bg = "#aaaaaa"
        self.rowWeight = self.colWeight = 0
        self.padx = self.pady = 1
        self.ipadx = self.ipady = 1
        
    def addNode(self, node):
        self.childNodes.append (node)
        
    def show(self, indent=""):
        """
        Output the structure, for debugging.
        """
        for a in self.alist:
            val = self.__dict__.get(a) 
            if val == None:
                continue
            print (indent, a, "=", val)
        for n in self.childNodes:
            n.show(indent+"\t")

            
class FrameBase (tkinter.Frame):
    """
    Subclass tkinter.Frame.
    This is to be used as tabs.
    """
    def __init__(self, master):
        tkinter.Frame.__init__ (self, master)
    
    '''
    These are convenient functions.
    '''
    def methodFactory (self, meth, data):
        def f1 ():
            meth (data)
        return f1
    
    def addLabel (self, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        label = tkinter.Label (self, text=text, name=name, font=font, bg=bg)
        label.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
            padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        return label
    
    def addEntry (self, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        width = gnode.width
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        entry = tkinter.Entry(self, width=width, font=font, name=name, bg=bg)
        entry.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
            padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        return entry
    
    def addListbox (self, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        width = gnode.width
        height = gnode.height
        items = gnode.items
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        lbox = tkinter.Listbox (self, width=width, height=height, font=font, name=name, bg=bg)
        lbox.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
            padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        for it in items:
            lbox.insert(0, it)
        return lbox
    
    def addButton (self, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        command = gnode.command
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        button = tkinter.Button (self, text=text, command=command,
                                 name=name, font=font, bg=bg)
        button.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
            padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        return button
    
    def addCheckbox(self, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        command = gnode.command
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        button = tkinter.Checkbutton(self, text=text, command=command,
                                     font=font, bg=bg)
        button.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
            padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        return button
    
    def addRadiobutton(self, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        command = gnode.command
        var = gnode.var
        value = gnode.value
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        button = tkinter.Radiobutton(self, text=text, variable=var, 
                                     command=command,
                                     value=value, font=font, name=name, bg=bg)
        button.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
            padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        return button
    
    def addFrame (self, frm, gnode, gridcnf={}):
        text = gnode.text
        name = gnode.name
        font = gnode.font
        row = gnode.row
        col = gnode.col
        sticky = gnode.sticky
        colspan = gnode.colspan
        rowspan = gnode.rowspan
        bg = gnode.bg
        padx = gnode.padx
        pady = gnode.pady
        ipadx = gnode.ipadx
        ipady = gnode.ipady
        frm.grid (row=row, column=col, sticky=sticky, columnspan=colspan, rowspan=rowspan, 
                padx=padx, pady=pady, ipadx=ipadx, ipady=ipady, cnf=gridcnf)
        frm.configure (bg=bg)
        return frm

    def addNode (self, gnode):
        if gnode.tagName == "Frame":
            print ("new frame " + gnode.name)
            frm = FrameBase(self)
            for n in gnode.childNodes:
                frm.addNode(n)
            self.addFrame(frm, gnode)
        else:
            cstr = "self.add" + gnode.tagName + "(gnode)"
            eval (cstr)
        if gnode.rowWeight != 0:
            self.grid_rowconfigure (gnode.row, weight=gnode.rowWeight)
        if gnode.colWeight != 0:
            self.grid_columnconfigure (gnode.col, weight=gnode.colWeight)
            

class GuiBase:
    '''
    This class should be subclassed.
    
    Usage:
    mainGui = GuiBase(title="Test") # or subclass of GuiBase
    mainGui.mainloop()
    mainGui.destroy()
    '''
    def __init__ (self, title="GUI"):
        self.top = tkinter.Tk()
        self.top.title(title)
        self.tabs = []
    
    def showTab (self, tabid):
        for fr in self.tabs:
            fr.grid_remove ()
        idx = int (tabid)
        self.tabs[idx].grid (row=0, column=0, sticky='NEWS')

        self.top.grid_columnconfigure (0, weight=1)
        self.top.grid_rowconfigure (0, weight=1)

    def methodFactory (self, meth, data):
        def f1 ():
            meth (data)
        return f1
    
    """
    Methods to load GUI description
    """
    def loadFrame(self, gnode, xnode):
        for e in xnode.childNodes:
            if e.nodeType == 1:
                newNode = GuiNode (e.tagName, e.attributes)
                if e.tagName == "Frame":
                    self.loadFrame(newNode, e)
                gnode.addNode (newNode)
                
    def loadTabs(self, root):
        tabDescs = []
        for e in root.childNodes:
            if e.nodeType == 1 and e.tagName == "Tab":
                gnode = GuiNode ("Tab", e.attributes)
                self.loadFrame (gnode, e)
                tabDescs.append (gnode)
        self.tabDescs = tabDescs
    
    def buildGui(self):
        for t in self.tabDescs:
            tab = FrameBase(self.top)
            for n in t.childNodes:
                tab.addNode (n)
            self.tabs.append (tab)
        
    def readDesc(self, xmlFile):
        dom = parse(xmlFile)
        self.loadTabs (dom.documentElement)
        # debug
        # self.showTabs()
        
        # Now we can build the GUI
        self.buildGui()
        self.showTab(0)
    
    def showTabs(self):
        for t in self.tabDescs:
            t.show()
    
    """
    Methods to build GUI
    """
    def addCascadeMenu (self, menu, mtree):
        '''
        Recursively adds new menu items.
        '''
        for entry in mtree:
            if len (entry) == 2:
                name, cont = entry
                newMenu = tkinter.Menu (menu, tearoff=0)
                menu.add_cascade (label=name, menu=newMenu)
                for entry1 in cont:
                    if len (entry1) == 2:
                        m1, callback = entry1
                        self.addCascadeMenu (newMenu, ((m1, callback),))
                    elif len (entry1) == 3:
                        m1, callback, data = entry1
                        newMenu.add_command (label=m1, command=self.methodFactory (callback, data))
            elif len (entry) == 3:
                name, cont, data = entry
                menu.add_command (label=name, command=self.methodFactory (cont, data))
                
    def addMenus (self, mtree):
        '''
        Creates a new menu and binds the menu to the top level window.
        Adds new menu items using the given description in mtree.
        '''
        menu = tkinter.Menu (self.top, tearoff=0)
        self.top.config (menu=menu)
        self.addCascadeMenu (menu, mtree)

    def getMenuDesc (self):
        return (
                ("File", (("Exit", self.quit, "ExitData"),)),
            )
    
    def quit (self, data=None):
        sys.exit(0)
        
    def mainloop (self):
        self.top.mainloop()

    def destroy (self, *args):
        self.top.destroy()

if __name__ == "__main__":
    gui = GuiBase ()
    gui.addMenus(gui.getMenuDesc())
    gui.readDesc("guidesc.xml")
    gui.mainloop()
