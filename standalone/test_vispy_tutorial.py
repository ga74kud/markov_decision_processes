import numpy as np
from vispy import app, gloo
import time


N=3000
data = np.zeros(N, [('a_lifetime', np.float32),
                    ('a_vec', np.float32, 2)])
vertex = """
uniform float u_time;
attribute vec2 a_vec;
attribute float a_lifetime;
void main () {
    if (u_time <= a_lifetime)
    {
        gl_Position = vec4(a_vec, 0.0, 1.0);
    }
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""
class Canvas(app.Canvas):

    def __init__(self):
        app.Canvas.__init__(self, keys='interactive', size=(800, 600))

        self._program = gloo.Program(vertex, fragment)
        self._program.bind(gloo.VertexBuffer(data))

        self._new_draw()

        gloo.set_state(blend=True, clear_color='black',
                       blend_func=('src_alpha', 'one'))

        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])

        self._timer = app.Timer('auto', connect=self.update, start=True)

        self.show()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)

    def compute_circle(self, N):
        vec=np.array([(np.sin((2*i*np.pi)/N), np.cos((2*i*np.pi)/N))  for i in range(0, N)])
        return vec

        #gloo.clear((1, 1, 1, 1))
    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.size)

    def on_draw(self, event):
        gloo.clear()
        self._program['u_time'] = time.time() - self._starttime
        self._program.draw('lines')

        # New explosion?
        if time.time() - self._starttime > 1.5:
            self._new_draw()
    def _new_draw(self):
        vec = self.compute_circle(N)
        lifetime=np.random.normal(2.0, 0.5, (N,))
        data['a_lifetime'] = lifetime
        data['a_vec'] = vec
        self._starttime = time.time()






if __name__ == '__main__':
    c = Canvas()
    app.run()