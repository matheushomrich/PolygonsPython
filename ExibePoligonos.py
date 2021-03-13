# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe um polígono em OpenGL
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *

# ***********************************************************************************
Mapa = Polygon()
ConvexHull = Polygon()

# Limites da Janela de Seleção
Min = Point()
Max = Point()

# ***********************************************************************************
def reshape(w,h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Seleção, com 10% das dimensões do polígono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

# ***********************************************************************************
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glColor3f(1.0, 1.0, 0.0)
    Mapa.desenhaPoligono()
    #Mapa.desenhaVertices()
    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    #print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        sys.exit()
    if args[0] == ESCAPE:
        sys.exit()
    if args[0] == b'p':
        Mapa.imprimeVertices()
    if args[0] == b'a':
        LePontosDeArquivo("EstadoRS.txt")

# ***********************************************************************************
# LePontosDeArquivo(Nome):
#  Realiza a leitura de uam arquivo com as coordenadas do polígono
# ***********************************************************************************
def LePontosDeArquivo(Nome):
    global Min, Max  # Variáveis usadas para definir os limites da Window
    
    Pt = Point()
    infile = open(Nome)
    line = infile.readline()
    number = int(line)
    for line in infile:
        words = line.split() # Separa as palavras na linha
        x = float (words[0])
        y = float (words[1])
        Mapa.insereVertice(x,y,0)
        #Mapa.insereVertice(*map(float,line.split))
    infile.close()
    Min, Max = Mapa.getLimits()
    #print ("Após leitura do arquivo:")
    #Min.imprime()
    #Max.imprime()

# ***********************************************************************************
# Trabalho 1
# ***********************************************************************************

def  hasIntersection(p1: Point, p2: Point, p3: Point, p4: Point):
    det = (p4.x - p3.x) * (p2.y - p1.y) - (p4.y - p3.y) * (p2.x -p1.x)

    #no intersection
    if (det == 0.0):
        return False 

    s = ((p4.x - p3.x) * (p3.y - p1.y) - (p4.y - p3.y) * (p3.x - p1.x))/ det 
    t = ((p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x))/ det 

    #has intersection
    if((s > 0 and s < 1) and (t > 0 and t < 1) ):
        return True  


def intersections(polygon1: Polygon, polygon2: Polygon):
    intersections = []
    c = 0
    for i in range(0, len(polygon1.Vertices)):
        for j in range(0, len(polygon2.Vertices)):
            if(hasIntersection(i, i+1, j, j+1)):        #verifica intersecao com todas arestas exceto ultimoponto - primeiroponto do poligono2
                intersections[c] = (i, i+1, j, j+1)
                c+=1
        if(hasIntersection(i, i+1, polygon2.Vertices[len(polygon2.Vertices)], polygon2.Vertices[0])):        # verifica apenas ultimoponto - primeiroponto do poligono2
                intersections[c] = (i, i+1, polygon2.Vertices[len(polygon2.Vertices)], polygon2.Vertices[0])
                c+=1
    i1 = polygon1.Vertices[len(polygon1.Vertices)]
    i2 = polygon1.Vertices[0]
    for j in range(0, len(polygon2.Vertices)):
            if(hasIntersection(i2, i1, j, j+1)):        #verifica intersecao com todas arestas exceto ultimoponto - primeiroponto do poligono2
                intersections[c] = (i2, i1, j, j+1)
                c+=1
    if(hasIntersection(i2, i1, polygon2.Vertices[len(polygon2.Vertices)], polygon2.Vertices[0])):        # verifica apenas ultimoponto - primeiroponto do poligono2
                intersections[c] = (i2, i1, polygon2.Vertices[len(polygon2.Vertices)], polygon2.Vertices[0])
                c+=1
    return intersections

def intersectionPoint(a1: Point, a2: Point, b1: Point, b2: Point):

    xdiff = (a1.x - a2.x, b1.x - b2.x)
    ydiff = (a1.y - a2.y, b1.y - b2.y)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    
    d = (a1.x * a2.y - a1.y * a2.x, b1.x * b2.y - b1.y * b2.x)
    
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return x, y


def uniao(polygon1: Polygon, polygon2: Polygon):
    intersectionsList = intersections(polygon1, polygon2)
    if(len(intersectionsList) > 0):
        for e in intersectionsList:
            a = intersectionPoint(e[0], e[1],e [2], e[3])
    else:
        print("Union can't be made, there are no intersections between the polygons in the parameters")

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

LePontosDeArquivo("TesteT1.txt")
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Exibe Polignos")
glutDisplayFunc(display)
#glutIdleFunc(showScreen)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMainLoop()
