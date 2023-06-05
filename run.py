# Initialize graph and drawing
# imports
import random
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
from itertools import permutations

Acolor = '<span^^^class="A">'
Bcolor = '<span^^^class="B">'

f = open('description.json')
description = json.load(f)
f.close()

E = [
    (1,2,6),
    (1,3,6),
    (2,3,5),
    (2,5,2),
    (2,4,4),
    (3,5,9),
    (4,5,8), 
    (4,6,4),
    (4,7,7),
    (5,7,7),
    (6,7,11),
    (6,8,7),
    (7,8,4),
    (9,3,5),
    (9,5,9)]
lenv=9
#V = [i+1 for i in range(lenv)]

Vlocations = {
    1:(0,1),
    2:(1,0),
    3:(1,2),
    4:(2,0),
    5:(2,2),
    6:(3,0),
    7:(3,2),
    8:(4,1),
    9:(2,3)}

def getElocations(Vlocations, E, color='b'):
  Elocations=[]
  weights=[]
  mids=[]
  for (i, j, w) in E:
    weights.append(w)
    x1, y1 = Vlocations[i]
    x2, y2 = Vlocations[j]
    Elocations.append((x1,x2))
    Elocations.append((y1,y2))
    Elocations.append(color)
    mids.append(((x1+x2)/2,(y1+y2)/2))
  return Elocations, weights,mids

def printEdge(Vlocations, E, color='b'):
  edges, weights, mids = getElocations(Vlocations, E, color)
  for xy, w in zip(mids, weights):
    plt.annotate(str(w), xy, fontsize=22,bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.3))
  plt.plot(*edges, linewidth=5,color='gray')


def printVertex(Vlocations, color='#e8eaed'):
  VXs, VYs =[], []
  for v, xy in Vlocations.items():
    plt.annotate(str(v), xy, ha='center',fontsize=22,  zorder=20)
    VXs.append(xy[0])
    VYs.append(xy[1])
  plt.scatter(VXs, VYs, s=1200, c=color, zorder=10)

# Run algo
def adjacency(V, E):
  adj = [[0 for _ in range(len(V))] for __ in range(len(V))]
  for (i,j,w) in E:
    i=i-1
    j=j-1
    adj[i][j]=adj[j][i]=w
  return adj

def weightsum(S, v_, adj):
  v_1 = v_-1
  su=0
  for v in S:
    v1=v-1
    su+=adj[v1][v_1]
  return su

def diff(B, A, v, adj):
  return  weightsum(B, v, adj)- weightsum(A, v, adj)
    
## find connecting edges
def cuts(AVlocations, BVlocations, V, E):
  adj = adjacency(V,E)
  cut=[]
  sumweights=0
  for Av, Axy in AVlocations.items():
    for Bv, Bxy in BVlocations.items():
      weight=adj[Av-1][Bv-1]
      if weight > 0:
        sumweights+=weight
        edgeX = (Axy[0], Bxy[0])
        edgeY = (Axy[1], Bxy[1])
        cut.append(edgeX)
        cut.append(edgeY)
        cut.append('cyan')
  return cut,sumweights

def algo(V, E):
  adj = adjacency(V, E)
  A = []
  B = []
  for v in V:
    dif=diff(B, A, v, adj)
    if dif > 0:
      A.append(v)
    else:
      B.append(v)
  return A, B

def sumWeightSet(A, V, E):
  adj = adjacency(V,E)
  weights=0
  for v1 in A:
    for v2 in A:
      weights += adj[v1-1][v2-1]
  return weights//2


def getVlocations(V, Vlocations):
  subset={}
  for v in V:
    subset[v] = Vlocations[v]
  return subset


def algo(V, E):
  adj = adjacency(V, E)
  A = []
  B = []
  for v in V:
    dif=diff(B, A, v, adj)
    if dif > 0:
      A.append(v)
    else:
      B.append(v)
  return A, B

def vis(A):
  if len(A)==0:
    return "$\{ \}$"
  s = "$\{$"
  for a in A:
    s += f"${str(a)}$  "
  return s[:-1] + "$\}$"

def align(v):
  if len(str(v)) == 1:
    return " " + str(v) + " "  
  if len(str(v)) == 2:
    return " " + str(v)
  else: return str(v)

def printStart(V, E):
    ## Images
    plt.figure(figsize=(18,10))
    printEdge(Vlocations, E)
    printVertex(Vlocations)
    plt.axis('off')
    imgpath = "static/maxcutimgs/start.png"
    plt.savefig(imgpath)
    plt.close('all') 
    
    # ## Annotations   
    # plt.figure(figsize=(18,5))
    # plt.plot([-2.0, 1.7], [-2.0, 1.7], color="white", alpha=0.0)
    # plt.text(-1.1,1.2, f"Before scanning vertices, A and B are empty", fontsize=15, color='darkred', ha='left', va='bottom',family='monospace')
    # plt.text(-1.0, -0.25, f"A: {vis([])}",ha='left', va='bottom',fontsize=15,bbox=dict(boxstyle='round,pad=0.2', fc='magenta', alpha=0.4) )
    # plt.text(-1.0, -0.75, f"B: {vis([])}",ha='left', va='bottom',fontsize=15,bbox=dict(boxstyle='round,pad=0.2', fc='lightgreen', alpha=0.4) )
    annopath = "static/maxcutimgs/start_annotation.png"
    # plt.axis('off')
    # plt.savefig(annopath)
    # plt.close('all') 
    
    text = f"<br>Before scanning vertices, A and B are empty"
    return imgpath, annopath, text
    
def printSteps(V, E):    
    listOfDic = []
    adj = adjacency(V, E)
    A = []
    B = []
    for id, v in enumerate(V):
        vStr = f"Current v: {v}"
        sumA = weightsum(A, v, adj)
        sumB = weightsum(B, v, adj)
        dif=diff(B, A, v, adj)
        if dif > 0:
            A.append(v)
            compStr = f"Decision condition: $\sum w(B,{v}) \geqslant \sum w(A, {v})$<br>Decision condition:     ${sumB}$              $>$              ${sumA}$<br>Adding ${align(v)}$ to $A$<br>Updated "
            visStr = f"{Acolor}$A$:  {vis(A)}</span>"
            fc='magenta'
        else:
            B.append(v)
            compStr = f"Decision condition: $\sum w(B,{v}) \leqslant \sum w(A, {v})$<br>Decision condition:     ${sumB}$              $\leqslant$              ${sumA}$<br>Adding ${align(v)}$ to $B$<br>Updated "      
            visStr = f"{Bcolor}B:  {vis(B)}</span>"
            fc='lightgreen'
        AVlocations = getVlocations(A, Vlocations)
        BVlocations = getVlocations(B, Vlocations)
        AAweights=sumWeightSet(A,V, E)
        BBweights=sumWeightSet(B,V, E)
        cut, ABweights=cuts(AVlocations, BVlocations, V, E)
        totalweights=sum(sum(adjacency(V,E),[])) //2
        ABinvariantStr = f"Loop invariant holds: $\sum w(A,B)\geqslant \sum w(A,A) + \sum w(B,B)$<br>Loop invariant holds:   ${align(ABweights)}$                  $\geqslant$                   ${align(AAweights)}$  $+$   ${align(BBweights)}$" 
        
        ## Image
        plt.figure(figsize=(18,10))
        printEdge(Vlocations, E)
        plt.plot(*cut, linewidth=7)
        
        printVertex(Vlocations)
        printVertex(AVlocations,color='magenta')
        printVertex(BVlocations,color='lightgreen')
        
        plt.plot(Vlocations[v][0], Vlocations[v][1], 'o', ms=19* 2, mec='darkorange', mfc='none', mew=17, zorder=1)
        plt.axis('off')
        imgpath = f"static/maxcutimgs/{id}.png"
        plt.savefig(imgpath)
        plt.close('all') 
        
        # ## Annotations
        # plt.figure(figsize=(18,4))
        # plt.plot([0.5, -1.5, 2.5], [0.5, -1.5,2.5], color="white", alpha=0.0)
        # # A: {}
        # plt.text(-1.2, 1.00, f"A: {vis(A)}",ha='left', va='bottom',fontsize=15,bbox=dict(boxstyle='round,pad=0.2', fc='magenta', alpha=0.4) )
        # # B: {}
        # plt.text(-1.2, 0.50, f"B: {vis(B)}",ha='left', va='bottom',fontsize=15,bbox=dict(boxstyle='round,pad=0.2', fc='lightgreen', alpha=0.4) )
        # # Current v : Decision condition * 2
        # plt.text(-1.25, -1.5, f"{vStr}<br><br><br><br><br>{compStr}<br>", fontsize=15, color='darkred', ha='left', va='bottom',family='monospace')
        # # Adding .. to ...
        # plt.text(-0.90,-1.26, f"{visStr}",ha='left', va='bottom',fontsize=15,bbox=dict(boxstyle='round,pad=0.2', fc=fc, alpha=0.4) )
        # # Loop invaraint holds 
        # plt.text(-1.25,-2, f"<br>{ABinvariantStr}", fontsize=15, color='darkred', ha='left', va='bottom',family='monospace')
        annopath = f"static/maxcutimgs/{id}_annotation.png"
        # plt.axis('off')
        # plt.savefig(annopath)
        # plt.close('all') 
        
        text = f"<br>Current v: ${v}$<br>{Acolor}$A$: {vis(A)}</span><br>{Bcolor}$B$: {vis(B)}</span><br>{compStr}{visStr}<br>{ABinvariantStr}<br>"
        listOfDic.append(
          {"img": imgpath, "annotation": annopath, "description":f"{description[str(v)]}<hr>{text}".replace(" ","&nbsp").replace("^^^", " ")}) 
           
    return listOfDic

def printEnd(V, E):
    A, B = algo(V, E)
    AVlocations = getVlocations(A, Vlocations)
    BVlocations = getVlocations(B, Vlocations)
    cut, ABweights=cuts(AVlocations, BVlocations, V, E)
    totalweights=sum(sum(adjacency(V,E),[])) //2
    ratio=ABweights/totalweights
    AAweights=sumWeightSet(A,V, E)
    BBweights=sumWeightSet(B,V, E)
    
    # ## Image
    # plt.figure(figsize=(18,10))
    # printEdge(Vlocations, E)
    # plt.plot(*cut, linewidth=7)
    # printVertex(AVlocations,color='magenta')
    # printVertex(BVlocations,color='lightgreen')
    # plt.axis('off')
    imgpath=f"static/maxcutimgs/end.png"
    # plt.savefig(imgpath)
    # plt.close('all') 
    
    # ## Annotations
    # plt.figure(figsize=(18,5))    
    # plt.text(-0.2, -0.2, f"CutWeights/TotalWeights: {ABweights}/{totalweights}<br>ratio={ratio:.2f} >= 0.5", fontsize=15, color='darkred', ha='left', va='bottom',family='monospace')
    # plt.plot([-0.5, 0.5], [-0.5, 0.5], color="white", alpha=0.0)
    annopath = "static/maxcutimgs/end_annotation.png"
    # plt.axis('off')
    # plt.savefig(annopath)
    # plt.close('all') 
    
    text = f"<br>Total Cut Weights: ${ABweights}/{totalweights}$<br>$\operatorname{ratio}={ratio:.2f} \geqslant 0.5$"
    return imgpath, annopath, text

## Entry
def printAlgo(V, E):
    imgpathS, annopathS, textS = printStart(V, E)
    listOfDic = printSteps(V, E)
    imgpathE, annopathE, textE = printEnd(V, E)
    slides = [{"img": imgpathS, 
               "annotation": annopathS,
               "desctiption": f"{description['start']}<hr>{textS.replace(' ', '&nbsp;').replace('^^^', ' ')}"}] \
      + listOfDic \
      + [{"img": imgpathE, 
          "annotation": annopathE, 
          "description": f'{description["end"]}<hr>{textE.replace(" ", "&nbsp;").replace("^^^", " ")}'}]
    return slides

def printHtml():
    return printAlgo([2,6,3,7,1,8,4,5,9],E)