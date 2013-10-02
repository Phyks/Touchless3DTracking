#!/usr/bin/env python

import pyglet
import pyglet.gl as gl

window = pyglet.window.Window()


@window.event
def on_draw():
    # Reset
    # =====
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    # Camera view
    # ===========
    gl.gluPerspective(70, window.width / window.height, 1, 1000)

    gl.gluLookAt(2, 1, 1, 0, 0, 0, 0, 0, 1)

    # Draw the cube
    # =============
    gl.glBegin(gl.GL_QUADS)

    # Left face
    gl.glColor3f(1.0, 0, 0)
    gl.glVertex3f(1, -1, -1)
    gl.glVertex3f(1, -1, 1)
    gl.glVertex3f(-1, -1, 1)
    gl.glVertex3f(-1, -1, -1)

    # Right face
    gl.glColor3f(0, 1.0, 0)
    gl.glVertex3f(-1, -1, 1)
    gl.glVertex3f(-1, 1, 1)
    gl.glVertex3f(-1, 1, -1)
    gl.glVertex3f(-1, -1, -1)

    #Bottom face
    gl.glColor3f(0, 0, 1.0)
    gl.glVertex3f(1, -1, -1)
    gl.glVertex3f(-1, -1, -1)
    gl.glVertex3f(-1, 1, -1)
    gl.glVertex3f(1, 1, -1)

    gl.glEnd()

    gl.glColor3f(0, 0, 0)
    pointer = gl.gluNewQuadric()
    gl.gluSphere(pointer, 0.1, 20, 20)

pyglet.app.run()
