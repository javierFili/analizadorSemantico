from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.graphics import Line
from structure.tree.Tree import Tree
from kivy.uix.button import Button
from kivy.core.window import Window


def creacion(self, funcion_matematica):
  # funcion_matematica = '3+23*4-2+3-7-8+8'  # (1*2*3)-(4*5)+6+7
  self.canvas.clear()
  tree = Tree()
  tree.parse(funcion_matematica)
  print(tree.evaluate())
  arbol = tree.viewTreeUI()
  for posiciones_valores in zip(arbol):
    Color(1, 0, 0)
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


class MyWidget(Widget):
  def __init__(self, funcion, **kwargs):
    super(MyWidget, self,).__init__(**kwargs)
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
    self.text_input = TextInput(text='3+23*4-2+3-7-8+8', multiline=False)
    self.layout.add_widget(self.text_input)
    # Parte media: Resultado
    self.result_label = Label(text='Resultado:')
    self.layout.add_widget(self.result_label)
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
    # self.my_widget.update_circle(texto_ingresado)

  def tree_visualizer(self):
    pass


if __name__ == '__main__':
  MyApp().run()
