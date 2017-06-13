import kivy
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Ellipse, Rectangle, Line
from kivy.properties import NumericProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import Label as CoreLabel
from kivy.uix.widget import Widget

kivy.require('1.10.0')

class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class LineNumbersSection(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, 0.3)

        with self.canvas.before:
            Color(1, 1, 1, 1)
            # self.rect = Rectangle(size=self.size, pos=self.pos)


class HexEdit(FocusBehavior, Widget):
    font_size = NumericProperty('15sp')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.text = []

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            Color(0, 0, 0, 1)
            #self.line = Line(points=[100, 0, 100, self.rect.size[1]], width=1)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _create_line_label(self, text):
        label = CoreLabel(text=text)
        label.refresh()
        texture = label.texture
        return texture

    def _update_rect(self, instance, value=None):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        # line_points = self.line.points[:]
        # line_points[3] = instance.size[1]
        # self.line.points = line_points

    def _update_canvas(self):
        self.canvas.clear()
        self.canvas.add(Color(0, 0, 0, 1))

        for (texture, pos) in self.text:
            self.canvas.add(
                Rectangle(size=texture.size, pos=pos, texture=texture))


    def on_touch_down(self, touch):
        if self.disabled:
            return

        touch_pos = touch.pos

        if not self.collide_point(*touch_pos):
            return False

        texture = self._create_line_label('width: {}, height: {}'.format(self.width, self.height))
        self.text.append((texture, touch_pos))
        self._update_canvas()


class RawdiskApp(App):
    def build(self):
        parent = RootWidget()
        line_numbers = LineNumbersSection()
        hex_edit = HexEdit()
        parent.add_widget(line_numbers)
        parent.add_widget(hex_edit)
        return parent

if __name__ == '__main__':
    RawdiskApp().run()
