from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Line

class LineApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        drawing_area = DrawingArea()
        layout.add_widget(drawing_area)
        return layout

class DrawingArea(Widget):
    def on_touch_down(self, touch):
        with self.canvas:
            # Dibujar una línea desde (100, 100) hasta el lugar donde se tocó la pantalla
            Line(points=[100, 100, touch.x, touch.y], width=2)

if __name__ == '__main__':
    LineApp().run()
