#!/usr/bin/env python3
"""Reproducible M24 response-length distributions; no external data fetch."""
import argparse, csv
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

MODELS=['Gemini','Qwen','GPT-OSS-20B','GPT-OSS-120B']
COLORS=['#164B6B','#A94D16','#176A58','#583875']
HATCHES=['///','\\\\','xx','..']

def read_data(path):
    out={m:[] for m in MODELS}
    with open(path,encoding='utf-8-sig',newline='') as fh:
        for r in csv.DictReader(fh):
            if r['block'] not in ('A','B'):continue
            m=r['model_tag']
            if m not in out:raise ValueError(f'Unexpected model: {m}')
            value=r['response_length_words']
            if value=='':
                raise ValueError(f'Missing response_length_words for {r["observation_id"]}')
            out[m].append(int(float(value)))
    return {k:np.asarray(v,dtype=int) for k,v in out.items()}

def make_plot(data,outdir,short_max=250,short_bin=25,tail_bin=100):
    fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12.6,5.1),gridspec_kw={'width_ratios':[1.35,1]},sharey=False)
    # Non-overlapping horizontal intervals; zeros included in first bin.
    short_edges=np.arange(0,short_max+short_bin,short_bin)
    maximum=max(int(v.max()) for v in data.values())
    tail_end=max(1000, int(np.ceil(maximum/tail_bin)*tail_bin))
    tail_edges=np.arange(short_max,tail_end+tail_bin,tail_bin)
    for m,c,h in zip(MODELS,COLORS,HATCHES):
        vals=data[m]
        for ax,edges in ((ax1,short_edges),(ax2,tail_edges)):
            counts,_=np.histogram(vals,bins=edges)
            ax.stairs(counts,edges,color=c,linewidth=1.7,fill=False,zorder=3)
            # Transparent hatched fill keeps all four series visible.
            ax.stairs(counts,edges,color=c,linewidth=.75,fill=True,hatch=h,alpha=.13,zorder=2)
    for ax in (ax1,ax2):
        ax.grid(axis='y',color='#D7DEE5',linewidth=.8)
        ax.set_axisbelow(True)
        ax.spines[['top','right']].set_visible(False)
        ax.tick_params(labelsize=10)
        ax.set_ylim(bottom=0)
    ax1.set_xlim(0,short_max)
    ax2.set_xlim(short_max,tail_end)
    ax1.set_xlabel('Response length (words)',fontsize=11)
    ax2.set_xlabel('Response length (words)',fontsize=11)
    ax1.set_ylabel(f'Responses per {short_bin}-word bin',fontsize=11)
    ax2.set_ylabel(f'Responses per {tail_bin}-word bin',fontsize=11)
    ax1.set_title('(a) Short responses',fontsize=12,fontweight='bold',loc='left')
    ax2.set_title('(b) Long-response tail',fontsize=12,fontweight='bold',loc='left')
    handles=[Patch(facecolor=c,edgecolor=c,hatch=h,alpha=.65,label=m) for m,c,h in zip(MODELS,COLORS,HATCHES)]
    fig.legend(handles=handles,ncol=4,loc='upper center',bbox_to_anchor=(.5,.99),frameon=False,fontsize=10)
    fig.subplots_adjust(left=.075,right=.985,bottom=.15,top=.83,wspace=.25)
    for ext in ('png','pdf','svg'):
        fig.savefig(outdir/f'Fig_Response_Length_Revised.{ext}',dpi=300,facecolor='white')
    plt.close(fig)
    return short_edges,tail_edges

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--data',default='M24_AB_2000_ANALYTICAL_GRID.csv')
    p.add_argument('--out',default='.')
    p.add_argument('--short-max',type=int,default=250)
    p.add_argument('--short-bin',type=int,default=25)
    p.add_argument('--tail-bin',type=int,default=100)
    args=p.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    data=read_data(args.data)
    make_plot(data,out,args.short_max,args.short_bin,args.tail_bin)
    with open(out/'response_length_summary.csv','w',newline='') as f:
        w=csv.writer(f);w.writerow(['model','n','zero_length','positive','median_words','p90_words','max_words','count_ge_250'])
        for m,a in data.items():w.writerow([m,len(a),int((a==0).sum()),int((a>0).sum()),float(np.median(a)),float(np.percentile(a,90)),int(a.max()),int((a>=250).sum())])
    for m,a in data.items():print(m,'n=',len(a),'zeros=',int((a==0).sum()),'max=',a.max())
if __name__=='__main__':main()
