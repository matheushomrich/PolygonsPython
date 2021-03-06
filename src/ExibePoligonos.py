# ***********************************************************************************
#   Authors: Matheus Homrich and Thiago Mello
#   GitHub: https://github.com/matheushomrich/PolygonsPython
# ***********************************************************************************

import os
import os.path
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *

# ***********************************************************************************
Mapa = Polygon()

A = Polygon()
B = Polygon()
Uniao = Polygon()
Intersecao = Polygon()
Diferenca = Polygon()

# Limites lógicos da área de desenho
Min = Point()
Max = Point()


Ponto = Point()
Meio = Point()
Terco = Point()
Largura = Point()

# ***********************************************************************************


def ProdEscalar(v1, v2):
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z

# ***********************************************************************************


def ProdVetorial(v1, v2, vresult):
    vresult.x = v1.y * v2.z - (v1.z * v2.y)
    vresult.y = v1.z * v2.x - (v1.x * v2.z)
    vresult.z = v1.x * v2.y - (v1.y * v2.x)

# ***********************************************************************************


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Seleção, com 10% das dimensões do polígono
    BordaX = abs(Max.x-Min.x) * 0.1
    BordaY = abs(Max.y-Min.y) * 0.1
    #glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def DesenhaEixos():
    glBegin(GL_LINES)
    # eixo horizontal
    glVertex2f(Min.x, Meio.y)
    glVertex2f(Max.x, Meio.y)
    #  eixo vertical 1
    glVertex2f(Min.x + Terco.x, Min.y)
    glVertex2f(Min.x + Terco.x, Max.y)
    #  eixo vertical 2
    glVertex2f(Min.x + 2*Terco.x, Min.y)
    glVertex2f(Min.x + 2*Terco.x, Max.y)
    glEnd()

# ***********************************************************************************


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1)
    DesenhaEixos()

    glPushMatrix()
    glTranslatef(0, Meio.y, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1, 1, 0)  # R, G, B  [0..1]
    A.desenhaPoligono()
    glColor3f(1.0, 0.0, 0.0)
    B.desenhaPoligono()
    glPopMatrix()

    # Desenha o polígono A no meio, acima
    glPushMatrix()
    glTranslatef(Terco.x, Meio.y, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1, 1, 0)  # R, G, B  [0..1]
    A.desenhaPoligono()
    glPopMatrix()

    # Desenha o polígono B no canto superior direito
    glPushMatrix()
    glTranslatef(Terco.x*2, Meio.y, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1, 0, 0)  # R, G, B  [0..1]
    Uniao = uniao(A, B)
    Uniao.desenhaPoligono()
    glPopMatrix()
    createFilePolygon(Uniao, "Uniao", False)


    # Desenha o polígono A no canto inferior esquerdo
    glPushMatrix()
    glTranslatef(0, 0, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1, 1, 0)  # R, G, B  [0..1]
    Intersecao = interseccao(A, B)
    Intersecao.desenhaPoligono()
    glPopMatrix()
    createFilePolygon(Intersecao, "Interseccao", False)

    # Desenha o polígono B no meio, abaixo
    glPushMatrix()
    glTranslatef(Terco.x, 0, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1, 0, 0)  # R, G, B  [0..1]
    Diferencaa = diferenca(A, B)
    Diferencaa.desenhaPoligono()
    glPopMatrix()
    createFilePolygon(Diferencaa, "Diferenca", False)

    # Desenha o polígono B no meio, abaixo
    glPushMatrix()
    glTranslatef(Terco.x*2, 0, 0)
    glScalef(0.33, 0.5, 1)
    glLineWidth(2)
    glColor3f(1, 0, 0)  # R, G, B  [0..1]
    Diferencab = diferenca(B, A)
    Diferencab.desenhaPoligono()
    glPopMatrix()
    createFilePolygon(Diferencab, "Diferenca", True)
    glutSwapBuffers()


# ***********************************************************************************
# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'


def keyboard(*args):
    #print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
    if args[0] == b'p':
        Mapa.imprimeVertices()
    if args[0] == b'a':
        LePontosDeArquivo()
# Força o redesenho da tela
    glutPostRedisplay()


# ***********************************************************************************
# LePontosDeArquivo(Nome):
#  Realiza a leitura de uam arquivo com as coordenadas do polígono
# ***********************************************************************************
def LePontosDeArquivo(Nome, P):

    Pt = Point()
    infile = open(Nome)
    line = infile.readline()
    number = int(line)
    for line in infile:
        words = line.split()  # Separa as palavras na linha
        x = float(words[0])
        y = float(words[1])
        P.insereVertice(x, y, 0)
        # Mapa.insereVertice(*map(float,line.split))
    infile.close()
    #print ("Após leitura do arquivo:")
    # Min.imprime()
    # Max.imprime()


def ObtemMaximo(P1, P2):
    Max = copy.deepcopy(P1)

    if (P2.x > Max.x):
        Max.x = P2.x

    if (P2.y > Max.y):
        Max.y = P2.y

    if (P2.z > Max.z):
        Max.z = P2.z

    return Max


def ObtemMinimo(P1, P2):
    Min = copy.deepcopy(P1)

    if (P2.x < Min.x):
        Min.x = P2.x

    if (P2.y < Min.y):
        Min.y = P2.y

    if (P2.z < Min.z):
        Min.z = P2.z

    return Min


def init():
    # Variáveis usadas para definir os limites da Window
    global Min, Max, Meio, Terco, Largura, arquivoUm, arquivoDois

    arquivoUm = "Objeto1"
    arquivoDois = "Objeto2"

    entradaAquivoUm = "txts/" + arquivoUm + ".txt" 
    entradaAquivoDois = "txts/" + arquivoDois + ".txt" 

    LePontosDeArquivo(entradaAquivoUm, A)
    Min, Max = A.getLimits()
    LePontosDeArquivo(entradaAquivoDois, B)
    MinAux, MaxAux = B.getLimits()
    # Atualiza os limites globais após cada leitura
    Min = ObtemMinimo(Min, MinAux)
    Max = ObtemMaximo(Max, MaxAux)

    # Ajusta a largura da janela lógica em função do tamanho dos polígonos
    Largura.x = Max.x-Min.x
    Largura.y = Max.y-Min.y

    # Calcula 1/3 da largura da janela
    Terco = Largura
    fator = 1.0/3.0
    Terco.multiplica(fator, fator, fator)

    # Calcula 1/2 da largura da janela
    Meio.x = (Max.x + Min.x)/2
    Meio.y = (Max.y + Min.y)/2
    Meio.z = (Max.z + Min.z)/2

    V1 = Point(1, 0, 0)
    V2 = Point(0, 1, 0)
    V3 = Point()

    ProdVetorial(V1, V2, V3)
    print("Produto Vetorial: ")
    V3.imprime()


# ***********************************************************************************
# Main Program
# ***********************************************************************************

s, t = -1, -1


def hasIntersection(p1, p2, p3, p4):
    ret = False
    global s, t
    s, t = -1, -1
    ret = intersec2d(p1,  p2,  p3,  p4)
    if (not ret):
        return False
    if (s >= 0.0 and s <= 1.0 and t >= 0.0 and t <= 1.0):
        return True
    else:
        return False


def intersec2d(p1, p2, p3, p4):
    det = 0.0

    det = (p4.x - p3.x) * (p2.y - p1.y) - (p4.y - p3.y) * (p2.x - p1.x)

    if (det == 0.0):
        return False  # n�o h� intersec��o

    global s, t
    s = ((p4.x - p3.x) * (p3.y - p1.y) - (p4.y - p3.y) * (p3.x - p1.x)) / det
    t = ((p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)) / det

    return True  # h� intersec��o

# ***********************************************************************************
# Operations
# ***********************************************************************************

def intersectionPoint(a1: Point, a2: Point, b1: Point, b2: Point):

    xdiff = (a1.x - a2.x, b1.x - b2.x)
    ydiff = (a1.y - a2.y, b1.y - b2.y)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)

    d = (a1.x * a2.y - a1.y * a2.x, b1.x * b2.y - b1.y * b2.x)

    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    intersecP = Point()
    intersecP.set(x, y, 0)
    return intersecP


def intersections(polygon1: Polygon, polygon2: Polygon):
    intersectionsL = []
    c = 0
    for i in range(0, len(polygon1.Vertices) - 2):
        for j in range(0, len(polygon2.Vertices) - 2):
            # verifica intersecao com todas arestas exceto ultimoponto - primeiroponto do poligono2
            if(hasIntersection(polygon1.Vertices[i], polygon1.Vertices[i + 1], polygon2.Vertices[j], polygon2.Vertices[j + 1])):
                intersectionsL[c] = (polygon1.Vertices[i], polygon1.Vertices[i + 1],
                                     polygon2.Vertices[j], polygon2.Vertices[j + 1])
                c += 1
        # verifica apenas ultimoponto - primeiroponto do poligono2
        if(hasIntersection(polygon1.Vertices[i], polygon1.Vertices[i + 1], polygon2.Vertices[len(polygon2.Vertices) - 1], polygon2.Vertices[0])):
            intersectionsL[c] = (polygon1.Vertices[i], polygon1.Vertices[i + 1],
                                 polygon2.Vertices[len(polygon2.Vertices) - 1], polygon2.Vertices[0])
            c += 1
    i1 = polygon1.Vertices[len(polygon1.Vertices) - 1]
    i2 = polygon1.Vertices[0]
    for j in range(0, len(polygon2.Vertices) - 2):
        # verifica intersecao com todas arestas exceto ultimoponto - primeiroponto do poligono2
        if(hasIntersection(i2, i1, polygon2.Vertices[j], polygon2.Vertices[j + 1])):
            intersectionsL[c] = (
                i2, i1, polygon2.Vertices[j], polygon2.Vertices[j + 1])
            c += 1
    # verifica apenas ultimoponto - primeiroponto do poligono2
    if(hasIntersection(i2, i1, polygon2.Vertices[len(polygon2.Vertices) - 1], polygon2.Vertices[0])):
        intersectionsL[c] = (i2, i1, polygon2.Vertices[len(
            polygon2.Vertices) - 1], polygon2.Vertices[0])
        c += 1
    return intersectionsL


isOut = True
vAuxAdd = False

def auxArestas(aresta, c, d, polygon):
    global isOut
    auxArestasV = []
    global vAuxAdd
    vAuxAdd = False
    for j in range(0, len(polygon.Vertices) - 1):
        ca = polygon.Vertices[j]
        da = polygon.Vertices[j+1]
        if((not (ca == c and da == d)) and hasIntersection(aresta[0], aresta[1], ca, da)):
            ip = intersectionPoint(aresta[0], aresta[1], ca, da)
            auxArestasV.append((aresta[0], ip, isOut))
            isOut = not isOut
            auxArestasVetor = auxArestas(
                (ip, aresta[1], isOut), ca, da, polygon)
            if(vAuxAdd):  # talvez tenha q fazer for
                for i in auxArestasVetor:
                    auxArestasV.append(i)
            else:
                auxArestasV.append((ip, aresta[1], isOut))
            vAuxAdd = True

    ca = polygon.Vertices[len(polygon.Vertices)-1]
    da = polygon.Vertices[0]
    if((not (ca == c and da == d)) and hasIntersection(aresta[0], aresta[1], ca, da)):
        ip = intersectionPoint(aresta[0], aresta[1], ca, da)
        auxArestasV.append((aresta[0], ip, isOut))
        isOut = not isOut
        auxArestasVetor = auxArestas((ip, aresta[1], isOut), ca, da, polygon)
        if(vAuxAdd):  # talvez tenha q fazer for
            for i in auxArestasVetor:
                auxArestasV.append(i)
        else:
            auxArestasV.append((ip, aresta[1], isOut))
        vAuxAdd = True
    return auxArestasV


def isInside(poly: Polygon, point: Point):
    i = 0
    j = len(poly.Vertices) - 1
    inside = False
    while i < len(poly.Vertices):
        if(((poly.Vertices[i].y > point.y) != (poly.Vertices[j].y > point.y))
           and (point.x < (poly.Vertices[j].x - poly.Vertices[i].x) * (point.y - poly.Vertices[i].y) / (poly.Vertices[j].y-poly.Vertices[i].y) + poly.Vertices[i].x)):
            inside = not inside
        j = i
        i = i + 1

    return inside


def classificaArestas(polygon1: Polygon, polygon2: Polygon):
    arestas = []
    global vAuxAdd
    global isOut
    
    isOut = not isInside(polygon2, polygon1.Vertices[0])  # arestas FORA = True
    
    for i in range(0, len(polygon1.Vertices) - 1):
        a = polygon1.Vertices[i]
        b = polygon1.Vertices[i + 1]
        add = True
        for j in range(0, len(polygon2.Vertices) - 1):
            c = polygon2.Vertices[j]
            d = polygon2.Vertices[j + 1]
            if(hasIntersection(a, b, c, d)):
                if(add):
                    ip = intersectionPoint(a, b, c, d)
                    arestas.append((a, ip, isOut))
                    isOut = not isOut
                    auxArestasVetor = auxArestas(
                        (ip, b, isOut), c, d, polygon2)
                    if(vAuxAdd):  # talvez tenha q fazer for
                        for i in auxArestasVetor:
                            arestas.append(i)
                    else:
                        arestas.append((ip, b, isOut))
                    add = False
        
        c = polygon2.Vertices[len(polygon2.Vertices) - 1]
        d = polygon2.Vertices[0]
        
        if(hasIntersection(a, b, c, d)):
            if(add):
                ip = intersectionPoint(a, b, c, d)
                arestas.append((a, ip, isOut))
                isOut = not isOut
                auxArestasVetor = auxArestas((ip, b, isOut), c, d, polygon2)
                if(vAuxAdd):  # talvez tenha q fazer for
                    for i in auxArestasVetor:
                        arestas.append(i)
                else:
                    arestas.append((ip, b, isOut))
                add = False
        if(add):
            arestas.append((a, b, isOut))
    
    a = polygon1.Vertices[len(polygon1.Vertices) - 1]
    b = polygon1.Vertices[0]
    add = True
    
    for j in range(0, len(polygon2.Vertices) - 1):
        c = polygon2.Vertices[j]
        d = polygon2.Vertices[j+1]
        
        if(hasIntersection(a, b, c, d)):
            if(add):
                ip = intersectionPoint(a, b, c, d)
                arestas.append((a, ip, isOut))
                isOut = not isOut
                auxArestasVetor = auxArestas((a, ip, isOut), c, d, polygon2)
                if(vAuxAdd):  # talvez tenha q fazer for #################################### AQUI
                    for i in auxArestasVetor:
                        arestas.append(i)
                else:
                    arestas.append((ip, b, isOut))
                add = False
    
    c = polygon2.Vertices[len(polygon2.Vertices) - 1]
    d = polygon2.Vertices[0]
    
    if(hasIntersection(a, b, c, d)):
        if(add):
            ip = intersectionPoint(a, b, c, d)
            arestas.append((ip, b, isOut))
            isOut = not isOut
            auxArestasVetor = auxArestas((a, ip, isOut), c, d, polygon2)
            if(vAuxAdd):  # talvez tenha q fazer for
                for i in auxArestasVetor:
                    arestas.append(i)
            else:
                arestas.append((ip, b, isOut))
            add = False
    if(add):
        arestas.append((a, b, isOut))
    
    return arestas


def uniao(polygon1: Polygon, polygon2: Polygon):
    arestas1 = classificaArestas(polygon1, polygon2)
    arestas2 = classificaArestas(polygon2, polygon1)

    isUniao = False

    for i in range(0, len(arestas1)):
        if arestas1[i][2] == False:
            isUniao = True
            break

    if not isUniao:
        print("Nao ha uniao entre os poligonos passados nos parametros")
        return polygon1

    uniaoAux = []
    for i in range(0, len(arestas1)):
        if arestas1[i][2]:
            uniaoAux.append(arestas1[i])
    for i in range(0, len(arestas2)):
        if arestas2[i][2]:
            uniaoAux.append(arestas2[i])

    uniaoFinal = Polygon()
    pInit = uniaoAux[0][0]
    pFinal = uniaoAux[0][1]
    uniaoFinal.insereVertice(pInit.x, pInit.y, pInit.z)
    uniaoFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
    c = 1

    while not pInit.isEqual(pFinal):
        if((uniaoAux[c][0].x == pFinal.x) and (uniaoAux[c][0].y == pFinal.y)):
            pFinal = uniaoAux[c][1]
            if not pInit.isEqual(pFinal):
                uniaoFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
        c += 1
        if c == len(uniaoAux):
            c = 1

    return uniaoFinal


def interseccao(polygon1: Polygon, polygon2: Polygon):
    arestas1 = classificaArestas(polygon1, polygon2)
    arestas2 = classificaArestas(polygon2, polygon1)

    isUniao = False

    for i in range(0, len(arestas1)):
        if arestas1[i][2] == False:
            isUniao = True
            break

    if not isUniao:
        print("Nao ha interseccao entre os poligonos passados nos parametros")
        return polygon1

    intersectaux = []
    for i in range(0, len(arestas1)):
        if arestas1[i][2] == False:
            intersectaux.append(arestas1[i])
    for i in range(0, len(arestas2)):
        if arestas2[i][2] == False:
            intersectaux.append(arestas2[i])

    intersectFinal = Polygon()
    pInit = intersectaux[0][0]
    pFinal = intersectaux[0][1]
    intersectFinal.insereVertice(pInit.x, pInit.y, pInit.z)
    intersectFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
    c = 1
    while not pInit.isEqual(pFinal):
        if((intersectaux[c][0].x == pFinal.x) and (intersectaux[c][0].y == pFinal.y)):
            pFinal = intersectaux[c][1]
            if not pInit.isEqual(pFinal):
                intersectFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
        c += 1
        if c == len(intersectaux):
            c = 1

    return intersectFinal


def diferenca(polygon1: Polygon, polygon2: Polygon):
    arestas1 = classificaArestas(polygon1, polygon2)
    arestas2 = classificaArestas(polygon2, polygon1)

    isUniao = False

    for i in range(0, len(arestas1)):
        if arestas1[i][2] == False:
            isUniao = True
            break

    if not isUniao:
        print("Nao ha diferenca entre os poligonos passados nos parametros")
        return polygon1

    diffAux = []
    for i in range(0, len(arestas1)):
        if arestas1[i][2]:
            diffAux.append(arestas1[i])
    for i in range(0, len(arestas2)):
        if not arestas2[i][2]:
            diffAux.append(arestas2[i])

    diffFinal = Polygon()
    pInit = diffAux[0][0]
    pFinal = diffAux[0][1]
    diffFinal.insereVertice(pInit.x, pInit.y, pInit.z)
    diffFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
    c = 1
    c2 = 0
    test = False

    sizeAux = len(diffAux)

    while (sizeAux != len(diffFinal.Vertices)):
        if((diffAux[c][0].x == pFinal.x) and (diffAux[c][0].y == pFinal.y)):
            pFinal = diffAux[c][1]
            if not pInit.isEqual(pFinal):
                diffFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
                diffAux.pop(c)
        ##c += 1

        if test:
            if((diffAux[c][1].x == pFinal.x) and (diffAux[c][1].y == pFinal.y)):
                pFinal = diffAux[c][0]
                if not pInit.isEqual(pFinal):
                    diffFinal.insereVertice(pFinal.x, pFinal.y, pFinal.z)
                    diffAux.pop(c)

        c += 1
        if c >= len(diffAux):
            c = 1
            c2 += 1
            if c2 == 2:
                test = not test

    return diffFinal


def createFilePolygon(polygon1: Polygon, fileName, diffBA):
    write =  ""
    cont = 0
    while cont < polygon1.getNVertices():
        write += "\n"
        write += str(int(polygon1.Vertices[cont].x)) + " " + str(int(polygon1.Vertices[cont].y))
        cont += 1  
    
    if diffBA:
        filename = arquivoDois + fileName + arquivoUm
    else:
        filename = arquivoUm + fileName + arquivoDois

    ##filename = filename 
    filepath = "results/" + filename + ".txt"

    if os.path.isfile(filepath):
        os.remove(filepath)
       
    f = open(filepath, "x")
    f.write(str(cont))
    f.write(write)
    f.close()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************


init()
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Exibe Polignos")
glutDisplayFunc(display)
# glutIdleFunc(showScreen)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)


try:
    glutMainLoop()
except SystemExit:
    pass
