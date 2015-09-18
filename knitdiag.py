#!/usr/bin/env python

import sys
import math
import cairo

####################################################################
### Draws knitting diagrams (only cable patterns for now) 
###
### Patterns are a simple string of stitches (ex. "k5 rc22 p5") but
### for simplicity their generation is as automated as possible.
### Two examples are given (pattern1 and lattice).
###
### Output is a png file named after the name of the pattern.
### 
### Nx and Ny are the number of columns and lines of the diagram.
###
### bx, byu and byd are the size of the borders (x: horizontal
### borders, yu: upper side, yd: lower side).
###
### repetitions are marked too. Only need to include the first column
### where repaetition starts (nbegin) and the number of stitches
### (nrepeat).
###
### List of pre-programmed stitches (more to come):
###
### k p kn pn tbl rcnn lcnn rpcnm lpcnm
###
### note: k=k1, pn=n-purl-st., rcnn=right-cross with n by n knit st.,
### lpcnm left cross with n knit st. and m purl st.


# purl square colour
GREY_TONE=.7
# number of pixels of each square
DELTA_PIXELS=24
LINEWIDTH=.125*DELTA_PIXELS

# pattern information must be stored here
PREBUILT_PATTERNS=["pattern1","lattice","seedstitch"]
### name of pattern, Nx, Ny, [bx,byu,byd], [nbegin, nrepeat],
### variables string (pattern input)
SEEDSTITCH=("seedstitch",20,20,[1.5,.1,.1],False, "self.nx,self.ny")
PATTERN1=("pattern1",50,41,[1.5,.1,.1],False,"self.ny")
LATTICE=("lattice",20,8,[1,.1,1.3],[7,6],False)
#############################################################
###          PRE-BUILT PATTERNS
#############################################################
def seedstitch(nx, ny): 
    """If nx is even, it draws a seed stitch diagram, otherwise it draws a 1x1 rib diagram."""
    return nx*ny/2*"k p "

def pattern1 (Ny):
    """Nx must be 50!! (Ny = 41, optional)"""
    pattern=""
    pattern+=2*(garter(1,50)+garter(2,50))
    for line in range(Ny-8,0,-1):
        pattern+=garter(line,4)+"p2 "
        pattern+=horseShoe1(line)+"p2 "
        pattern+=cable(line)+"p2 "
        pattern+=diamond12(line)+"p2 "
        pattern+=braid2x3(line)+"p2 "
        pattern+=garter(line,4)
    pattern+=2*(garter(2,50)+garter(1,50))
    return pattern

def lattice():
    """Works with Nx, Ny= 20, 8 only"""
    pattern="p3 k2 lpc22 k2 lpc22 k4 p1 "
    pattern+="p1 k4 p2 k4 p2 k4 p3 "
    pattern+="p1 lc22 p2 lc22 p2 lc22 p3 "
    pattern+="p1 k4 p2 k4 p2 k4 p3 "
    pattern+="p1 k4 rpc22 k2 rpc22 k2 p3 "
    pattern+="p3 k4 p2 k4 p2 k4 p1 "
    pattern+="p3 lc22 p2 lc22 p2 lc22 p1 "
    pattern+="p3 k4 p2 k4 p2 k4 p1 "
    return pattern

def garter (line, n):
    if line % 2 == 1:
        return 'p'+str(n)+' '
    else:
        return 'k'+str(n)+' '

def cable(line, n=2):
    """cable with width 2*n (n=2,3 recommended)."""
    repetition=2*(n+1)
    if line % repetition == 3: 
        return 'rc' + 2*str(n) + ' '
    else: 
        return 'k'+str(2*n) + ' '

def braid2x3(line):
    """braid with 3 2-stitch cables"""
    if line % 4 == 1:
        return "rc22 rc22 "
    elif line % 4 == 3:
        return "k2 lc22 k2 "
    else:
        return "k8 "

def horseShoe1(line):
    """horse shoe pattern with a single cross and 8 stitches of width."""
    if line % 6 == 5:
        return"lc22 rc22 "
    else:
        return "k8 "

def honeycomb(line,n=3):
    """honeycomb pattern with n cells."""
    if line % 8 == 3:
        return n*"lc22 rc22 "
    if line % 8 == 7:
        return n*"rc22 lc22 "
    else:
        return n*"k8 "

def diamond12(line):
    """A seed-stitch diamond pattern of 12 stitches and 20 rows"""
    line=line % 20
    if  line == 1 or line == 3:
        return "p4 k4 p4 "
    elif line == 2: 
        return "p4 rc22 p4 "
    elif line == 4: 
        return "p3 lpc21 rpc21 p3 "
    elif line == 5: 
        return "p3 k2 p1 k3 p3 "
    elif line == 6: 
        return "p2 lpc21 k1 p1 rpc21 p2 "
    elif line == 7: 
        return "p2 k2 k1 p1 k1 p1 k2 p2 "
    elif line == 8: 
        return "p1 lpc21 p1 k1 p1 k1 rpc21 p1 "
    elif line == 9: 
        return "p1 k2 p1 k1 p1 k1 p1 k3 p1 "
    elif line == 10: 
        return "lpc21 k1 p1 k1 p1 k1 p1 rpc21 "
    elif line == 11 or line==13: 
        return "k3 p1 k1 p1 k1 p1 k1 p1 k2 "
    elif line == 12: 
        return "k2 p1 k1 p1 k1 p1 k1 p1 k3 "
    elif line == 14: 
        return "rpc21 k1 p1 k1 p1 k1 p1 lpc21 "
    elif line == 15: 
        return "p1 k2 p1 k1 p1 k1 p1 k3 p1 "
    elif line == 16: 
        return "p1 rpc21 p1 k1 p1 k1 lpc21 p1 "
    elif line == 17: 
        return "p2 k3 p1 k1 p1 k2 p2 "
    elif line == 18: 
        return "p2 rpc21 k1 p1 lpc21 p2 "
    elif line == 19:
        return "p3 k2 p1 k3 p3 "
    elif line == 0:
        return "p3 rpc21 lpc21 p3 "
#############################################################
###          CODE BEGINS HERE
#############################################################
class pattern():
    """This class stores pattern information."""
    def __init__(self, name, nx, ny, borders, repeat=False, varstring=False):
        self.name=name
        self.nx=nx
        self.ny=ny
        self.borders=borders # [bx,byu,byd]
        self.repeat=repeat # False or [nbegin,nrepeat]
        self.varstring=varstring # False or ex. "self.nx, self.ny", etc
        self.patternstring=self.pat_gen()
    def pat_info(self):
        print("pattern name = "+self.name)
        print("Nx, Ny = "+str(self.nx)+', '+str(self.ny))
        print("repeat = "+str(self.repeat))
        print("borders = "+str(self.borders))
        print("variables = "+str(self.varstring))
    def pat_gen(self):
        """generates string of pattern"""
        if self.name in PREBUILT_PATTERNS:
            evalstring= self.name+"("+self.varstring+")" if self.varstring else self.name+"()"
            self.patternstring=eval(evalstring)
            return self.patternstring
        else: return ""

def main():
    pattern=PAT.patternstring
    Nx, Ny = PAT.nx, PAT.ny
    bx, byu, byd = PAT.borders
    # image generation
    WIDTH, HEIGHT = int((Nx+2*bx)*DELTA_PIXELS), int((Ny+byu+byd)*DELTA_PIXELS)
    surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    canvas = cairo.Context (surface)
    # 
    draw_diagram(canvas, pattern, Nx, Ny, bx*DELTA_PIXELS, byu*DELTA_PIXELS)
    # Output to PNG  
    surface.write_to_png (PAT.name+'.png') 

def draw_diagram(canvas, pattern, Nx, Ny, x0, y0):
    # create list from pattern
    pattern=pattern.split()
    # draw pattern
    npos=0
    nelem=0
    for stitch in pattern:
        nelem+=1
        nx=npos % Nx
        ny=npos / Nx
        st,n,m=check_stitch(stitch,nelem)
        if nx+n+m > Nx: print 'ERROR: stitch too long, line %s.' % nelem
        npos+=n+m
        if st=='p':
            for i in range(n):
                purl(canvas, x0+(nx+i)*DELTA_PIXELS, y0+ny*DELTA_PIXELS)
        elif st=='t':
            tbl(canvas,x0+nx*DELTA_PIXELS,y0+ny*DELTA_PIXELS)
        elif st=='rc':
            nrc(canvas,n,x0+nx*DELTA_PIXELS,y0+ny*DELTA_PIXELS)
        elif st=='lc':
            nlc(canvas,n,x0+nx*DELTA_PIXELS,y0+ny*DELTA_PIXELS)
        elif st=='rpc':
            nmrpc(canvas,n,m,x0+nx*DELTA_PIXELS,y0+ny*DELTA_PIXELS)
        elif st=='lpc':
            nmlpc(canvas,n,m,x0+nx*DELTA_PIXELS,y0+ny*DELTA_PIXELS)
    # draw grid and outer rectangle
    grid (canvas,Nx,Ny,x0,y0)
    canvas.set_source_rgb (0,0,0)
    canvas.set_line_width (LINEWIDTH)
    canvas.rectangle (x0, y0, Nx*DELTA_PIXELS, Ny*DELTA_PIXELS)
    canvas.stroke ()
    # draw repetition marks
    if PAT.repeat: 
        mark_repetition(canvas,x0,y0,Ny,PAT.repeat[0],PAT.repeat[1])
    # print row numbers
    row_numbering(canvas, x0, Nx, Ny)

def grid(canvas, Nx, Ny, x0, y0, lwidth=LINEWIDTH/2):
    """Draws a grid with Nx*Ny squares"""
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    for i in range(1,Nx):
        canvas.move_to (x0+i*DELTA_PIXELS, y0)
        canvas.line_to (x0+i*DELTA_PIXELS, y0+Ny*DELTA_PIXELS)
        canvas.stroke ()
    for i in range(1,Ny):
        canvas.move_to (x0, y0+i*DELTA_PIXELS)
        canvas.line_to (x0+Nx*DELTA_PIXELS, y0+i*DELTA_PIXELS)
        canvas.stroke ()

def row_numbering(canvas, bx, Nx, Ny):
    """write number of each row in standard way"""
    canvas.set_source_rgb (0, 0, 0)
    #canvas.select_font_face ("Georgia")
    canvas.set_font_size (DELTA_PIXELS)
    for line in range(1,Ny+1):
        xp=0.1*DELTA_PIXELS if  line % 2 == 0 else 1.1*bx+Nx*DELTA_PIXELS
        canvas.move_to ( xp,(Ny-line+1)*DELTA_PIXELS)
        number = str(line)
        if line <10 and Ny>9: 
            number=' '+number
        canvas.show_text (number)

def mark_repetition(canvas,x0,y0,Ny,nbegin,n,lwidth=LINEWIDTH):
    """Mark repetition of n stitches and starting at position nbegin."""
    canvas.set_source_rgb (.7, 0.1, 0.1)
    canvas.set_line_width (lwidth)
    canvas.move_to (x0+nbegin*DELTA_PIXELS,y0)
    canvas.line_to (x0+nbegin*DELTA_PIXELS,y0+(Ny+1)*DELTA_PIXELS)
    canvas.move_to (x0+(nbegin+n)*DELTA_PIXELS,y0)
    canvas.line_to (x0+(nbegin+n)*DELTA_PIXELS,y0+(Ny+1)*DELTA_PIXELS)
    canvas.stroke ()
    canvas.set_source_rgb (0, 0, 0)
    #canvas.select_font_face ("Georgia")
    canvas.set_font_size (DELTA_PIXELS)
    canvas.move_to (x0+(nbegin+.2)*DELTA_PIXELS,y0+(Ny+1)*DELTA_PIXELS)
    canvas.show_text (str(n)+"-st repeat")

def check_stitch(stitch,nelem):
    s0=stitch[0]
    if s0 !='p' and s0 !='k' and s0 !='t' and s0 !='r' and s0 !='l':
        print 'ERROR: wrong notation (1), line %s.' % nelem
    elif stitch=='tbl':
        return 't', 1, 0
    elif s0=='p' or s0=='k':
        if stitch[1:].isdigit:
            n=1 if stitch[1:] == '' else int(stitch[1:])
            return s0, n, 0
    elif s0=='r' or s0=='l':
        if stitch[1]=='c':
            if len(stitch)==4 and stitch[2:].isdigit:
                if stitch[2] != stitch[3]: 
                    print 'ERROR: wrong notation (2), line %s.' % nelem
                return s0+'c', int(stitch[2]), int(stitch[2])
            else: print 'ERROR: wrong notation (3), line %s.' % nelem
        elif len(stitch)==5 and stitch[1:3]=='pc':
            if stitch[3:].isdigit:
                return s0+'pc', int(stitch[3]), int(stitch[4])
            else: print 'ERROR: wrong notation (4), line %s.' % nelem
        else: print 'ERROR: wrong notation (5), line %s.' % nelem
    else: print 'ERROR: wrong notation (6), line %s.' % nelem
    return '',0,0
#############################################################
###          STITCH SYMBOLS
#############################################################
def purl(canvas,x0,y0,lwidth=LINEWIDTH):
    """A purl stitch: a square with gray background"""
    canvas.set_source_rgb (GREY_TONE, GREY_TONE, GREY_TONE)
    canvas.set_line_width (lwidth)
    canvas.rectangle (x0, y0, DELTA_PIXELS, DELTA_PIXELS)
    canvas.fill ()
    #knit(canvas,x0,y0)

def knit(canvas,x0,y0,lwidth=LINEWIDTH):
    """A knit stitch: a half-square. Not for use."""
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    canvas.move_to (x0, y0+DELTA_PIXELS)
    canvas.line_to (x0+DELTA_PIXELS, y0+DELTA_PIXELS)
    canvas.line_to (x0+DELTA_PIXELS, y0)
    canvas.stroke ()

def tbl(canvas,x0,y0,lwidth=LINEWIDTH):
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    x1, y1 = x0+DELTA_PIXELS/2, y0+3./5*DELTA_PIXELS
    x2, y2 = x0+DELTA_PIXELS, y0
    canvas.move_to(x1,y1)
    canvas.curve_to(x0,y0,x2,y2,x1,y1)
    canvas.rel_line_to (DELTA_PIXELS/4,DELTA_PIXELS/4)
    canvas.move_to(x1,y1)
    canvas.rel_line_to (-DELTA_PIXELS/4,DELTA_PIXELS/4)
    canvas.stroke ()

def nrc(canvas,n,x0,y0,lwidth=LINEWIDTH):
    """A right-cross of n by n stitches"""
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    # rightside lines
    canvas.move_to(x0, y0+DELTA_PIXELS)
    canvas.line_to (x0+n*DELTA_PIXELS, y0)
    canvas.move_to(x0+n*DELTA_PIXELS, y0+DELTA_PIXELS)
    canvas.line_to (x0+2*n*DELTA_PIXELS, y0)
    # wrongside lines
    canvas.move_to(x0, y0)
    canvas.line_to (x0+n*DELTA_PIXELS/2, y0+DELTA_PIXELS/2)
    canvas.move_to(x0+2*n*DELTA_PIXELS, y0+DELTA_PIXELS)
    canvas.line_to (x0+1.5*n*DELTA_PIXELS, y0+DELTA_PIXELS/2)
    #
    canvas.stroke ()

def nlc(canvas,n,x0,y0,lwidth=LINEWIDTH):
    """A left-cross of n by n stitches"""
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    # rightside lines
    canvas.move_to(x0, y0+DELTA_PIXELS)
    canvas.line_to (x0+n*DELTA_PIXELS/2, y0+DELTA_PIXELS/2)
    canvas.move_to(x0+2*n*DELTA_PIXELS, y0)
    canvas.line_to (x0+1.5*n*DELTA_PIXELS, y0+DELTA_PIXELS/2)
    # rightside lines
    canvas.move_to(x0, y0)
    canvas.line_to (x0+n*DELTA_PIXELS, y0+DELTA_PIXELS)
    canvas.move_to(x0+2*n*DELTA_PIXELS, y0+DELTA_PIXELS)
    canvas.line_to (x0+n*DELTA_PIXELS, y0)
    #
    canvas.stroke ()

def nmrpc(canvas,n,m,x0,y0,lwidth=LINEWIDTH):
    """A right-purl-cross of n by m stitches"""
    x1, x2, x3 = x0+n*DELTA_PIXELS, x0+m*DELTA_PIXELS, x0+(n+m)*DELTA_PIXELS
    y1 = y0+DELTA_PIXELS
    grey_corner(canvas,x0,y1,x2,y0,x0,y0,x1,y1,lwidth)
    grey_corner(canvas,x3,y0,x1,y1,x3,y1,x2,y0,lwidth)

def nmlpc(canvas,n,m,x0,y0,lwidth=LINEWIDTH):
    """A left-purl-cross of n by m stitches"""
    x1, x2, x3 = x0+n*DELTA_PIXELS, x0+m*DELTA_PIXELS, x0+(n+m)*DELTA_PIXELS
    y1 = y0+DELTA_PIXELS
    grey_corner(canvas,x0,y0,x2,y1,x0,y1,x1,y0,lwidth)
    grey_corner(canvas,x3,y1,x1,y0,x3,y0,x2,y1,lwidth)

def corner (canvas,x0,y0,x1,y1,x2,y2,x3,y3,lwidth=LINEWIDTH):
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    canvas.move_to(x0,y0)
    canvas.line_to (x1,y1)
    xx, yx = intersection(x0,y0,x1,y1,x2,y2,x3,y3)
    canvas.move_to (x2,y2)
    canvas.line_to (xx,yx)
    canvas.stroke ()

def grey_corner (canvas,x0,y0,x1,y1,x2,y2,x3,y3,lwidth=LINEWIDTH):
    xx, yx = intersection(x0,y0,x1,y1,x2,y2,x3,y3)
    grey_triangle(canvas,xx,yx,x1,y1,x2,y2)
    canvas.set_line_width (lwidth)
    canvas.set_source_rgb (0, 0, 0)
    canvas.move_to(x0,y0)
    canvas.line_to (x1,y1)
    canvas.move_to (x2,y2)
    canvas.line_to (xx,yx)
    canvas.stroke ()

def intersection(x0,y0,x1,y1,x2,y2,x3,y3):
    m1, m2 = (y1-y0)/(x1-x0), (y3-y2)/(x3-x2)
    xx = (y2-y0-m2*x2+m1*x0)/(m1-m2)
    yx = y0+m1*(xx-x0) 
    return xx, yx

def grey_triangle(canvas,x0,y0,x1,y1,x2,y2):
    canvas.set_source_rgb (GREY_TONE, GREY_TONE, GREY_TONE)
    canvas.move_to(x0,y0)
    canvas.line_to (x1,y1)
    canvas.line_to (x2,y2)
    canvas.close_path()
    canvas.fill()
#############################################################
###          END OF STITCH SYMBOLS
#############################################################
def usage():
    print """Usage: knitdiag <name of pattern>

List of available patterns (see prebuilt_patterns.py):"""
    print PREBUILT_PATTERNS


if __name__ == '__main__':
    # define pattern and run main
    if len(sys.argv) >= 2 and sys.argv[1] in PREBUILT_PATTERNS:
        PAT=pattern(*vars() [sys.argv[1].upper()])
        PAT.pat_info()
        main()
        print 'Output: '+PAT.name+'.png'
    else: usage()
