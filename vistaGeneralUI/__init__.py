from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color
from kivy.graphics import Line
import estructura.ConstructorArbol as constructor


# maximo de numeros en la operacion 7.+6 => 13 caracteres.
# 3*2+2+2*3-2/2   =>5 ...2*6+1-2*3/1+3+2+3
#
#

def creacion(self):
  funcion_matematica = "4*3*4-3*4+4+3*4+5*3"
  funcion_matematica = funcion_matematica.replace(" ", "")
  expresion_jerarquizada = constructor.jerarquizar_operaciones(funcion_matematica)
  arbol = constructor.constructor_de_Arbol(expresion_jerarquizada)
  for posiciones_valores in zip(arbol):
    Color(1, 0, 0)
    x = posiciones_valores[0][0][0]
    y = posiciones_valores[0][0][1]
    x1 = posiciones_valores[0][2][0]
    y1 = posiciones_valores[0][2][1]
    texto = posiciones_valores[0][1]
    Line(points=[x, y, x1, y1], width=2)
    self.circle = Ellipse(pos=(x, y), size=(30, 30))
    self.text_label = Label(text=(texto), pos=(x, y), size=(30, 30), halign='center', valign='middle')


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
    self.text_input = TextInput(text='', multiline=False)
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
    try:
      # Intenta convertir el texto a un número para usar como radio
      radius = float(value)
      self.my_widget.update_circle(radius)
      self.result_label.text = f'Resultado: {radius}'
    except ValueError:
      self.result_label.text = 'Error: Ingrese un número válido'

  def tree_visualizer(self):
    constructor.obtener_elemento()


if __name__ == '__main__':
  MyApp().run()
