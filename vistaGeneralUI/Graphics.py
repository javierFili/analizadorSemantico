from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.graphics import Line
from structure.exceptions.EvalException import EvalException
from structure.exceptions.NodeException import NodeException
from structure.exceptions.ParseException import ParseException
from structure.exceptions.TokenizeException import TokenizeException
from structure.tree.Tree import Tree
from kivy.uix.button import Button


def creacion(self, funcion_matematica):
  try:
    self.canvas.clear()
    tree = Tree()
    tree.parse(funcion_matematica)
    print(tree.evaluate())
    x = 300
    y = 100
    self.result_text = Label(text="Resultado:", size_hint=(None, None), pos=(x, y), size=(30, 30), halign='center',
                             valign='middle')
    self.add_widget(self.result_text)
    self.result = Label(text=str(tree.evaluate()), size_hint=(None, None), pos=(x, y - 40), size=(30, 30),
                        halign='center', valign='middle')
    self.add_widget(self.result)
    self.result_jerarquia = Label(text=str(tree.root), size_hint=(None, None), pos=(x, y - 80), size=(30, 30),
                                  halign='center', valign='middle')
    self.add_widget(self.result_jerarquia)
    arbol = tree.viewTreeUI()
    for posiciones_valores in zip(arbol):
      Color(0, 0,1 )
      x = posiciones_valores[0][0][0]
      y = posiciones_valores[0][0][1]
      x1 = posiciones_valores[0][2][0]
      y1 = posiciones_valores[0][2][1]
      texto = posiciones_valores[0][1]
      Line(points=[x, y, x1, y1], width=2)
      Ellipse(pos=(x, y), size=(30, 30))
      text_label = Label(text=texto, size_hint=(None, None), pos=(x, y), size=(30, 30), halign='center',
                         valign='middle')
      self.add_widget(text_label)
  except (EvalException):

    self.result_text = Label(text="Existio un error al momento de evaluar", size_hint=(None, None), pos=(300, 300),
                             size=(30, 30),
                             halign='center', valign='middle')
    self.add_widget(self.result_text)

  except  (NodeException):
    self.result_text = Label(text="Existio un error en uno de los signos", size_hint=(None, None),
                             pos=(300, 300),
                             size=(30, 30),
                             halign='center', valign='middle')
    self.add_widget(self.result_text)
  except  ParseException:
    self.result_text = Label(text="Existio un error al momento de realizar la jerarquizacion", size_hint=(None, None),
                             pos=(300, 300),
                             size=(30, 30),
                             halign='center', valign='middle')
    self.add_widget(self.result_text)
  except TokenizeException:
    self.result_text = Label(text="Existio un error al momento de realizar los tokens", size_hint=(None, None),
                             pos=(300, 300),
                             size=(30, 30),
                             halign='center', valign='middle')
    self.add_widget(self.result_text)


class MyWidget(Widget):
  def __init__(self, funcion, **kwargs):
    super(MyWidget, self, ).__init__(**kwargs)
    with self.canvas:
      # self.canvas.draw("Hola Mundo!", (20, 40), font_size=24)
      creacion(self, funcion)

  def update_circle(self, funcion):
    with self.canvas:
      creacion(self, funcion)


class MyApp(App):
  def build(self):
    self.layout = BoxLayout(orientation='vertical', size_hint=(None, None))
    # Parte superior: Entrada de texto
    self.text_input = TextInput(text='3+23*4-3-7-8+8', multiline=False)
    self.layout.add_widget(self.text_input)
    # Parte inferior: SVG o Canvas con una circunferencia
    self.my_widget = MyWidget(self.text_input.text)
    self.layout.add_widget(self.my_widget)
    # Vincular la actualización de la circunferencia al cambio de texto
    button = Button(text='Obtener Texto', on_press=self.on_button_press)
    self.layout.add_widget(button)
    return self.layout

  def on_button_press(self, instance):
    # Obtener el TextInput por su ID
    texto_ingresado = self.text_input.text
    self.layout.remove_widget(self.my_widget)
    self.my_widget = MyWidget(texto_ingresado)
    self.layout.add_widget(self.my_widget)
