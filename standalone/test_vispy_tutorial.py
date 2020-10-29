import numpy as np
from vispy import app
from vispy import gloo

c = app.Canvas(keys='interactive')

vertex = """
attribute vec2 a_position;
void main (void)
{
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

fragment = """
void main()
{
    gl_FragColor = vec4(0.0, 0.0, 0.0, 1.0);
}
"""

def compute_circle(N):
    X=[np.sin((2*i*np.pi)/N) for i in range(0, N)]
    Y=[np.cos((2*i*np.pi)/N) for i in range(0, N)]
    return X, Y


program = gloo.Program(vertex, fragment)
N=300
X, Y=compute_circle(N)
program['a_position'] = np.c_[X, Y].astype(np.float32)

@c.connect
def on_resize(event):
    gloo.set_viewport(0, 0, *event.size)
@c.connect
def on_draw(event):
    gloo.clear((1,1,1,1))
    program.draw('line_strip')
c.show()
app.run()
