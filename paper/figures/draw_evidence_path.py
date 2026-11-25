from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
out=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','pdf.fonttype':42})
fig,ax=plt.subplots(figsize=(7.1,2.25))
fig.subplots_adjust(left=.01,right=.99,bottom=.02,top=.98)
ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
xs=[.10,.36,.64,.90]
nodes={
'score':(xs[0],.85,'Evaluation score'),
'run':(xs[1],.85,'Evaluation run'),
'release':(xs[2],.85,'Model release'),
'checkpoint':(xs[3],.85,'Checkpoint'),
'decision':(xs[0],.47,'Use decision'),
'job':(xs[1],.47,'Local contribution'),
'update':(xs[2],.47,'Update artifact'),
'round':(xs[3],.47,'Training round'),
'policy':(xs[0],.10,'Policy version'),
'data':(xs[1],.10,'Dataset snapshot')}
w=.18;h=.14
for key,(x,y,label) in nodes.items():
    external=key in {'checkpoint','update','policy','data'}
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.004,rounding_size=0.012',facecolor='#f0f0f0' if external else '#e5eef5',edgecolor='#253b50',linewidth=.8))
    ax.text(x,y,label,ha='center',va='center',fontsize=7.5)
def link(a,b,label,vertical=False,offset=.11):
    x1,y1,_=nodes[a];x2,y2,_=nodes[b]
    if vertical:
        sign=1 if y2>y1 else -1
        start=(x1,y1+sign*h/2);end=(x2,y2-sign*h/2)
        tx=x1+.018;ty=(y1+y2)/2;ha='left'
        if x1 > .8:
            tx=x1-.018;ha='right'
    else:
        sign=1 if x2>x1 else -1
        start=(x1+sign*w/2,y1);end=(x2-sign*w/2,y2)
        tx=(x1+x2)/2;ty=y1+offset;ha='center'
    ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=9,linewidth=.8,color='#1c2734'))
    ax.text(tx,ty,label,ha=ha,va='center',fontsize=6.1,color='#263846')
link('score','run','prov:wasGeneratedBy')
link('run','release','edso:evaluatedRelease')
link('release','checkpoint','prov:wasDerivedFrom')
link('checkpoint','round','prov:\nwasGeneratedBy',True)
link('round','update','edso:update')
link('update','job','prov:wasGeneratedBy')
link('job','decision','edso:decisionRecord')
link('decision','policy','edso:policyVersion',True)
link('job','data','edso:inputSnapshot',True)
ax.text(.64,.13,'Blue: EDSO classes\nGray: reused artifact / policy types',ha='left',va='center',fontsize=7,color='#334455',linespacing=1.5)
fig.savefig(out/'evidence_path.pdf')
fig.savefig(out/'evidence_path.png',dpi=180)
