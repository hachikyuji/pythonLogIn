import tkinter as tk
from tkinter import*
from PIL import Image, ImageTk
from tkinter import font

class TextLineNumbers(tk.Canvas):
    def __init__(selfnit__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        # Attach the Text widget to the line numbers canvas
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        # Clear existing line numbers
        self.delete("all")

        # Get the index of the first visible line in the Text widget
        i = self.textwidget.index("@0,0")

        while True:
            # Get information about the display line
            dline = self.textwidget.dlineinfo(i)
            if dline is None: break

            # Extract the y-coordinate and line number
            y = dline[1]
            linenum = str(i).split(".")[0]
            # Create a text element for the line number
            self.create_text(2, y, anchor="nw", text=linenum)
            # Move to the next line
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result
class LeftPanel(tk.Frame): #buttons
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="brown", width=200, **kwargs)
        # Load and set background image
        self.background_image = Image.open("1426487.jpg")
        self.background_image = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Change font for buttons
        button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Button for running lexical analysis
        self.lexical_button = tk.Button(self, text="Run Lexical", command=master.run_lexical, font=button_font, bg="indigo", fg="white")
        self.lexical_button.pack(pady=10, fill=tk.X)
        # Button for running syntax analysis
        self.syntax_button = tk.Button(self, text="Run Syntax", command=master.run_syntax, font=button_font, bg="indigo", fg="white")
        self.syntax_button.pack(pady=10, fill=tk.X)
        # Button for running semantic analysis
        self.semantic_button = tk.Button(self, text="Run Semantic", command=master.run_semantic, font=button_font, bg="indigo", fg="white")
        self.semantic_button.pack(pady=10, fill=tk.X)
        # Button for screen clearing
        self.clr_button = tk.Button(self, text="Clear Panels", command=master.run_clr, font=button_font, bg="deeppink4", fg="white")
        self.clr_button.pack(pady=10, fill=tk.X)

class TopPanel(tk.Frame): #user input
    def __init__(self, master, **kwargs):
        super().__init__(master, bg="black", height=150, **kwargs)

        #Change font for top panel
        topPanel_font = font.Font(family="Courier", size=12)
        #Change font for top panel-title
        topPanelTitle_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Label for the input section
        self.input_label = tk.Label(self, text="Input", fg="white", bg="black", font=topPanelTitle_font)
        self.input_label.pack(side=tk.TOP, fill=tk.X)

        # Text widget for user input
        self.input_text = CustomText(self)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=self.vsb.set)
        self.input_text.tag_configure("font", font=topPanel_font)
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.input_text)
        self.input_text.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        self.vsb = tk.Label(self, fg="white", bg="black")
        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.input_text.pack(side="right", fill="both", expand=True)

        self.input_text.bind("<<Change>>", self._on_change)
        self.input_text.bind("<Configure>", self._on_change)

    def _on_change(self, event):
        self.linenumbers.redraw()

class MiddlePanel(tk.Frame):  # the one on the right most 'lexeme token' = Token
    def __init__(self, master, **kwargs):
        # Change font for middle panel
        middlePanel_font = font.Font(family="Courier", size=12)
        #Change font for middle panel-title
        middlePanelTitle_font = font.Font(family="Helvetica", size=12, weight="bold")

        super().__init__(master, bg="darkslategray", **kwargs)
        self.token_label = tk.Label(self, text="Lexeme Token", fg="white", bg="black", font=middlePanelTitle_font)
        self.token_label.pack(side=tk.TOP, fill=tk.X)

        # Create a canvas and a scrollbar for the middle panel
        self.canvas = tk.Canvas(self, bg="darkslateblue")
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the token display label
        self.frame = tk.Frame(self.canvas, bg="darkslategray")
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Label for displaying tokens
        self.token_display = tk.Label(self.frame, text="Token displayed here", bg="darkslateblue", fg="white",
                                      justify=tk.LEFT, wraplength=340, anchor=tk.NW, font=middlePanel_font)
        self.token_display.pack(fill=tk.BOTH, expand=True)

        # Bind the canvas scrolling to the frame
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


class BottomPanel(tk.Frame): #Results (errors0
    def __init__(self, master, **kwargs):
        # Change font for bottom panel
        bottomPanel_font = font.Font(family="Courier", size=12)
        #Change font for bottom panel-title
        bottomPanel_fontPanelTitle_font = font.Font(family="Helvetica", size=12, weight="bold")

        super().__init__(master, bg="white", **kwargs)
        self.results_label = tk.Label(self, text="Results", fg="white", bg="black", font=bottomPanel_fontPanelTitle_font)
        self.results_label.pack(side=tk.TOP, fill=tk.X)

        # Create a canvas and a scrollbar for the bottom panel
        self.canvas = tk.Canvas(self, bg="black")
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the results display label
        self.frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Label for displaying analysis results
        self.results_display = tk.Label(self.frame, text="Result checking here", bg="black", fg="white",
                                        justify=tk.LEFT, wraplength=700, anchor=tk.NW, font=bottomPanel_font)
        self.results_display.pack(fill=tk.BOTH, expand=True)

        # Bind the canvas scrolling to the frame
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))


class TextAnalyzerApp(tk.Tk): #main/main window
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Text Analyzer")  # Title of window here
        self.geometry("1200x800")  # Set the preferred default window size

        # Initialize the left panel
        self.left_panel = LeftPanel(self)
        self.left_panel.grid(row=0, column=0, rowspan=3, sticky="ns")

        # Initialize the top panel
        self.top_panel = TopPanel(self)
        self.top_panel.grid(row=0, column=1, columnspan=1, sticky="news")

        # Initialize the middle panel (moved to the right-most side)
        self.middle_panel = MiddlePanel(self)
        self.middle_panel.grid(row=0, column=2, rowspan=3, sticky="nsew")

        # Initialize the bottom panel
        self.bottom_panel = BottomPanel(self)
        self.bottom_panel.grid(row=1, column=1, columnspan=1, sticky="nsew")

        # Set row and column weights to make the panels resize properly
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=4)  # Increase weight for the row containing the bottom panel
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def run_lexical(self):  # button action
        # Get user input from the top panel
        input_text = self.top_panel.input_text.get("1.0", tk.END).strip()

        # Split the input into lines
        lines = input_text.split("\n")

        # Initialize an empty result string
        result = ""
        result1 = ""

        # Loop through each line, get the line number, and append it to the result string
        for i, line in enumerate(lines, start=1):
            result += f"Tokens for line {i}: '{line}' displayed here\n"

        # Display the result in the middle panel
        self.middle_panel.token_display.config(text=result)

        # Loop through each line, get the line number, and append it to the result string
        for i, line in enumerate(lines, start=1):
            result1 += f"Lexical: Result/Error for line {i}: '{line}' displayed here\n"

        # Placeholder action for result checking (display in result panel), replace with actual logic
        self.bottom_panel.results_display.config(text=result1)

    def run_syntax(self):  # button action
        # Get user input from the top panel
        input_text = self.top_panel.input_text.get("1.0", tk.END).strip()

        # Placeholder action for token panel, when syntax button is clicked
        result = f"N/A"
        self.middle_panel.token_display.config(text=result)

        # Placeholder action for syntax analysis (disp in result panel), replace with actual logic
        result = f"Syntax result for '{input_text}' checking here"
        self.bottom_panel.results_display.config(text=result)

    def run_semantic(self):  # button action
        # Get user input from the top panel
        input_text = self.top_panel.input_text.get("1.0", tk.END).strip()

        # Placeholder action for token panel, when semantic button is clicked
        result = f"N/A"
        self.middle_panel.token_display.config(text=result)

        # Placeholder action for semantic analysis (disp in result panel), replace with actual logic
        result = f"Semantic result for '{input_text}' checking here"
        self.bottom_panel.results_display.config(text=result)

    def run_clr(self):  # button action
        # Clear the contents of the Text widget in the top panel
        self.top_panel.input_text.delete("1.0", tk.END)

        # Clear the contents of the Label widget in the middle panel
        self.middle_panel.token_display.config(text="")

        # Clear the contents of the Label widget in the bottom panel
        self.bottom_panel.results_display.config(text="")


if __name__ == "__main__":
    app = TextAnalyzerApp()
    app.mainloop()