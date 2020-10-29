import numpy as np
from vispy import app, gloo
import time
from vispy.util.transforms import translate, rotate

N=400
data = np.zeros(N, [('a_vec', np.float32, 2)])
vertex = """

attribute vec2 a_vec;

uniform mat4 u_model;
uniform float u_size;

varying float v_size;
void main () {
    gl_Position = u_model*vec4(a_vec, 0.0, 1.0);

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

        self.program = gloo.Program(vertex, fragment)
        self.program.bind(gloo.VertexBuffer(data))
        self.theta = -1
        gloo.set_state(blend=True, clear_color='black',
                       blend_func=('src_alpha', 'one'))
        self.translate = 1
        gloo.set_viewport(0, 0, self.physical_size[0], self.physical_size[1])

        self.new_draw()
        self.model = np.eye(4, dtype=np.float32)
        self.program['u_model'] = self.model
        self.timer = app.Timer('auto', connect=self.on_timer, start=True)
        self.show()

    def on_resize(self, event):
        width, height = event.physical_size
        gloo.set_viewport(0, 0, width, height)
    def on_timer(self, event):
        self.theta += 0.001
        self.model = translate((self.theta,0,0))

        self.program['u_model'] = self.model
        self.update()

    def compute_circle(self, N):
        vec=np.array([(np.sin((2*i*np.pi)/N), np.cos((2*i*np.pi)/N))  for i in range(0, N)])
        return vec

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *event.size)

    def on_draw(self, event):
        gloo.clear()
        self.program.draw('lines')


    def new_draw(self):
        vec = self.compute_circle(N)
        data['a_vec'] = vec
        self.starttime = time.time()

if __name__ == '__main__':
    c = Canvas()
    app.run()