from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.graphics import Line
import estructura.ConstructorArbol as constructor
from structure.tree.Tree import Tree


# maximo de numeros en la operacion 7.+6 => 13 caracteres.
# 3*2+2+2*3-2/2   =>5 ...2*6+1-2*3/1+3+2+3
#
#

def creacion(self):
  funcion_matematica = '3+2-3*4-2+3-7-8+8'  # (1*2*3)-(4*5)+6+7
  tree = Tree()
  tree.parse(funcion_matematica)
  print(tree.__str__())
  arbol = tree.viewTreeUI()
  print(arbol)
  for posiciones_valores in zip(arbol):
    Color(1, 0, 0)
    x = posiciones_valores[0][0][0]
    y = posiciones_valores[0][0][1]
    x1 = posiciones_valores[0][2][0]
    y1 = posiciones_valores[0][2][1]
    texto = posiciones_valores[0][1]
    Line(points=[x, y, x1, y1], width=2)
    self.circle = Ellipse(pos=(x, y), size=(30, 30))
    self.text_label = Label(text=texto, size_hint=(None, None), pos=(x, y), size=(30, 30), halign='center',
                            valign='middle')
    self.add_widget(self.text_label)


class MyWidget(Widget):
  def __init__(self, **kwargs):
    super(MyWidget, self).__init__(**kwargs)
    with self.canvas:
      creacion(self)

  def update_circle(self, funcion):
    pass


class MyApp(App):
  def build(self):
    layout = BoxLayout(orientation='vertical', size_hint=(None, None))
    # Parte superior: Entrada de texto
    self.text_input = TextInput(text='3+2-3*4-2+3-7-8+8', multiline=False)
    layout.add_widget(self.text_input)
    # Parte media: Resultado
    self.result_label = Label(text='Resultado:')
    layout.add_widget(self.result_label)
    # Parte inferior: SVG o Canvas con una circunferencia
    self.my_widget = MyWidget()
    layout.add_widget(self.my_widget)
    # Vincular la actualización de la circunferencia al cambio de texto
    self.text_input.bind(text=self.update_circle)

    return layout

  def update_circle(self, instance, value):
    creacion(value)

  def tree_visualizer(self):
    constructor.obtener_elemento()


if __name__ == '__main__':
  MyApp().run()
