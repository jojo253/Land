import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

#  width and height of the map
W = H = 100
# Elasticity Coefficient
E = 0
# Gravitation Coefficient
G = 10**-4
# Drag Coefficient
C = 0.1
# radius of a circle
R = 0.5
# init the map info
N = 100
xys = W * np.random.rand(N, 2)
vxys = np.zeros((N, 2))
axys = np.zeros((N, 2))


def distence(pos1, pos2):
    dpos = getdpos(pos1, pos2)
    return np.dot(dpos, dpos)**0.5


#  each boundary of the map is connected
def sgn(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def getdpos(pos1, pos2):
    dpos = pos2 - pos1
    dpos[0] -= (abs(dpos[0]) > 0.5) * sgn(dpos[0])
    dpos[1] -= (abs(dpos[1]) > 0.5) * sgn(dpos[1])
    return dpos


def checkCollision():
    '''
    if distence(pos1+v1, pos2+v2) < 2 * r:
        it has collision with self
        self.v = ((1-e)*self.v + (1+e)*other.v)/2
        other.v = ((1+e)*self.v + (1-e)*other.v)/2
    '''
    global xys
    global vxys
    for i in range(N):
        for j in range(i, N):
            if distence(xys[i], xys[j]) < 2 * R:
                vxys[i], vxys[j] = ((1 - E) * vxys[i] +
                                    (1 + E) * vxys[j]) / 2, (
                                        (1 + E) * vxys[i] +
                                        (1 - E) * vxys[j]) / 2


def setAttraction():
    '''
    it has attraction with self
    self.a = sum of (dx/d**3, dy/d**3)
    '''
    global xys
    global axys
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            axys[i] += G * getdpos(xys[i], xys[j]) / distence(xys[i],
                                                              xys[j])**3


def setFriction():
    global vxys
    vxys -= C * vxys**2


def setSpdPos():
    '''
    self.v+ = self.a
    self.x, self.y+ = self.v
    '''
    global xys
    global vxys
    global axys
    vxys += axys
    xys += vxys

    for i in range(N):
        while xys[i, 0] < 0:
            xys[i, 0] += W
        while xys[i, 0] > W:
            xys[i, 0] -= W
        while xys[i, 1] < 0:
            xys[i, 1] += H
        while xys[i, 1] > H:
            xys[i, 1] -= H


def show_animation():
    fig, ax = plt.subplots()

    def init():
        global xys, sct
        sct = ax.scatter(*xys.T, c='black')
        return sct,

    def update(*args):
        global xys, sct
        checkCollision()
        setAttraction()
        setFriction()
        setSpdPos()

        plt.cla()
        sct = ax.scatter(*xys.T, c='black')
        return sct,

    ani = animation.FuncAnimation(fig, update, init_func=init, interval=60)
    plt.show()


if __name__ == "__main__":
    show_animation()
