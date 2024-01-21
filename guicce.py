#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                     {{{ GUICCE }}}                         +
  A simple GUI for running C programs with gcc on MacOS.    +
                 Kaycee Ingram <kazewaze>                   +
                      - 1/20/2024 -                         +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

import wx
import wx.lib.buttons as buttons
import subprocess
import tempfile

script = 'guicce'           # Shell Script to run gcc on .c file.
programs_dir = "C_Programs" # Name of Root Dir Folder for C Programs.
c_file = ''                 # Selected .c file for gcc to run.

# I Feel like the Function Name does the job... yeah.
def get_terminal_ouput(script, c_file):
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen([("./" + script + ".sh"), ("./%s/%s/%s" % (programs_dir, c_file.capitalize(), c_file))], stdout=tempf)
        proc.wait()
        tempf.seek(0)
        output = tempf.read().decode().split('\n')[0]

        return output

# Main Window Class.
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        # Create Main Window/Frame.
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, (1000, 800), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | 0 | 0 | wx.MINIMIZE_BOX)

        MenuBar = wx.MenuBar()
        AboutMenu = wx.Menu()

        item = AboutMenu.Append(wx.ID_HELP, "GUICCE",
                                "Information about this program.")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)

        MenuBar.Append(AboutMenu, "About")

        self.SetMenuBar(MenuBar)

        #----------------------------------
        # Create Main Window's UI Elements:
        #----------------------------------
        # Create Main Panel within the Window.
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.panel.SetBackgroundColour(wx.Colour(255, 255,255))

        # Logo Image.
        self.picture = wx.StaticBitmap(self.panel, size=(200,300), pos=(350,-110))
        self.picture.SetBitmap(wx.Bitmap('./assets/GUICCE.png'))

        # UI Element Fonts.
        quote_font = wx.Font(30, family=wx.FONTFAMILY_DECORATIVE, style=0, weight=500, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        result_font = wx.Font(45, family=wx.FONTFAMILY_DEFAULT, style=0, weight=400, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        button_font = wx.Font(20, family=wx.FONTFAMILY_DEFAULT, style=0, weight=700, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        lblname_font = wx.Font(30, family=wx.FONTFAMILY_DECORATIVE, style=0, weight=500, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)
        editname_font = wx.Font(25, family=wx.FONTFAMILY_DEFAULT, style=0, weight=400, underline=False, faceName="", encoding=wx.FONTENCODING_DEFAULT)

        # Create Terminal Output Label.
        self.quote = wx.StaticText(self.panel, label="Program Output", size=(50, 25), pos=(390, 250), style=wx.ALIGN_CENTER)
        self.quote.SetFont(quote_font)

        # Create Terminal Output Area (blank until file runs).
        self.result = wx.StaticText(self.panel, label="", size=(950, 455), pos=(25, 295), style=wx.ALIGN_CENTER, name ="Output")
        self.result.SetFont(result_font)
        # Set Terminal Output Text and Terminal Background Color.
        self.result.SetForegroundColour((252, 0, 6, 255))
        self.result.SetBackgroundColour((222, 224, 233, 255))

        # Create Run Button.
        self.button = buttons.GenButton(self.panel, label="Run", size=(135, 35), pos=(435, 190))
        self.button.SetFont(button_font)
        # Set Button Text and Background Color.
        self.button.SetForegroundColour((0, 0, 0, 255))
        self.button.SetBackgroundColour((222, 224, 233, 255))

        # Create File Name Input Label.
        self.lblname = wx.StaticText(self.panel, label="File Name", size=(25, 25), pos=(433, 95), style=wx.ALIGN_CENTER)
        self.lblname.SetFont(lblname_font)

        # Create File Name Input.
        self.editname = wx.TextCtrl(self.panel, size=(225, 30), pos=(390, 130))
        self.editname.SetFont(editname_font)
        # Set File Name Input Text and Background Color.
        self.editname.SetForegroundColour((0, 0, 0, 255))
        self.editname.SetBackgroundColour((222, 224, 233, 255))

        # Set Sizer for the Frame.
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)

        # Set Simple Sizer for a Nice Border.
        self.sizer = wx.GridBagSizer(5, 5)
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        #----------------------------------
        # Set Event Handlers (Button Pressed).
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        #----------------------------------

    # Event for "Run" Button Press (runs .c file).
    def OnButton(self, e):
        # Only name of file needed, GUICCEE will add .c for you.
        c_file = str(self.editname.GetValue()).strip()
        output = get_terminal_ouput(script, c_file)
        self.result.SetLabel(output)

    # Event for "About" Button Press (In the menu at the top).
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A simple GUI for running\n"
                                     "C programs with gcc on MacOS.\n"
                                     "Written by Kaycee Ingram <kazewaze>.\n",
                                "GUICCE", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

# Run GUI Program.
app = wx.App()
frame = MyFrame(None, '') # No Title needed since we use the Logo Image.
frame.Show()
app.MainLoop()