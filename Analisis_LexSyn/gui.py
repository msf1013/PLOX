import Tkinter
import tkFileDialog
import tkFont
import os.path
import copy
import parser3

class PloxStudio(Tkinter.Tk):
     # Constructor que mantiene un tracking del contenedor padre
     def __init__(self, parent):
          Tkinter.Tk.__init__(self, parent)
          self.parent = parent
          self.initialize()

     # Inicializador que crea todos los elementos GUI
     def initialize(self):
          # Se crea el manejador de layout como tabla
          self.grid()

          # Se cambia el color de background de la GUI
          self.configure(bg = '#1E1E1E')

          # Se hace que el tamano de la ventana no se pueda cambiar
          self.resizable(width=False, height=False)

          # Se establece el tamano y posicion de la ventana
          x = (self.winfo_screenwidth() / 2) - 550
          self.geometry('%dx%d+%d+%d' % (1100, 680, x, 10))

          # Se especifica archivo trabajando original como nada
          self.fileName = ''

          # Se establecen fonts a usar
          buttonFont = tkFont.Font(family = 'Helvetica', size = 11, weight = 'bold')
          entryFont = tkFont.Font(family = 'Helvetica', size = 12)

          # Se crea browser para abrir un archivo
          self.browsePathText = Tkinter.StringVar()
          self.browsePath = Tkinter.Entry(self, state = 'disabled', font = entryFont, textvariable = self.browsePathText, width = 60)
          self.browsePath.grid(row = 0, column = 0, padx = (80, 0), pady = 30, columnspan = 2)
          self.browseFile = Tkinter.Button(self, text = 'Open File', font = buttonFont, command=self.browseFileFromDirectory, bg = '#6584FF', fg = '#F6F6F6')
          self.browseFile.grid(row = 0, column = 2, sticky = 'W')

          # Se crea un textfield para input
          self.input = Tkinter.Text(self, width = 130, height = 20, highlightbackground = '#F6F6F6', highlightthickness = 2, bg = '#1E1E1E', fg = '#F6F6F6')
          self.input.grid(row = 1, column = 0, padx = 25, pady = (10,10), columnspan = 3)

          # Se crea browser para guardar archivo
          self.saveFile = Tkinter.Button(self, text = 'Save File', font = buttonFont, command=self.saveFileIntoDirectory, bg = '#6584FF', fg = '#F6F6F6', width = 10)
          self.saveFile.grid(row = 2, column = 0, pady = 10, padx = (450, 0))

          # Se crean botones para compilar y ejecutar archivo
          self.compileButton = Tkinter.Button(self, text = 'Compile', font = buttonFont, command=self.compileFile, bg = '#6584FF', fg = '#F6F6F6', width = 10)
          self.compileButton.grid(row = 3, column = 0, padx = (330, 40), pady = 10)
          self.executeButton = Tkinter.Button(self, text = 'Execute', font = buttonFont, command=self.executeFile, bg = '#6584FF', fg = '#F6F6F6', width = 10)
          self.executeButton.grid(row = 3, column = 0, padx = (0, 0), sticky = 'E')

          
     # Accion para abrir un archivo de un directorio
     def browseFileFromDirectory(self):
          # Se obtiene el nombre del archivo
          self.browsePathText.set(tkFileDialog.askopenfilename(defaultextension='.ch', filetypes=[('Plox source file','*.ch'), ('All files','*.*')]))

          # Se lee el archivo especificado
          fileName = self.browsePathText.get()
          if(os.path.isfile(fileName)):
                  f = open(fileName, 'r')
                  fileText = f.read()
                  self.input.delete(1.0, 'end')
                  self.input.insert('end', fileText)

     # Accion para abrir un archivo de un directorio
     def saveFileIntoDirectory(self):
          # Se obtiene el path del archivo
          File = tkFileDialog.asksaveasfile(defaultextension='.ch', filetypes=[('Plox source file','*.ch'), ('All files','*.*')])

          # Se graba en el archivo especificado
          if(File is None):
                  return
          textToSave = str(self.input.get(1.0, 'end'))
          File.write(textToSave)
          self.fileName = fileName = File.name
          File.close()

     # Accion para compilar un archivo de un directorio
     def compileFile(self):
          # Se compila archivo
          parser3.parseFile(self.fileName)

     # Accion para ejecutar un archivo de un directorio
     def executeFile(self):
          # Se ejecuta archivo
          import virtualMachine2

# Main que se ejecuta cuando se corre el programa
if __name__ == "__main__":
     # La aplicacion GUI se inicia con titulo "Plox Studio" 
     plox = PloxStudio(None)
     plox.title('Plox Studio')

     # Se cicla el programa indefinidamente en espera de eventos
     plox.mainloop()
