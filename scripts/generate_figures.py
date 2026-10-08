# Reproduction of the 16 descriptive figures.
# Run from repository root: python scripts/generate_figures.py
from pathlib import Path
import pandas as pd, numpy as np, matplotlib.pyplot as plt
d=pd.read_csv('data/M24_AB_2000_ANALYTICAL_GRID.csv',keep_default_na=False)
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
FIG_DIR=Path('figures');FIG_DIR.mkdir(exist_ok=True)
MODELS=['Gemini','Qwen','GPT-OSS-20B','GPT-OSS-120B']
COLORS={'Gemini':'#164B6B','Qwen':'#A94D16','GPT-OSS-20B':'#176A58','GPT-OSS-120B':'#583875'}
CONDS=['baseline','paraphrase','formatting','instruction_position','irrelevant_context']
D=d.copy();D['end_to_end_success']=pd.to_numeric(D['end_to_end_success']).astype(int)
for col in ['acquired','parsed','response_length_words','prompt_length_words']:
 D[col]=pd.to_numeric(D[col],errors='coerce').fillna(0)
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.bbox':'tight','figure.dpi':120})
FIG_NAMES=[]
def save(name,fig):
 fig.savefig(FIG_DIR/(name+'.png'),dpi=210,facecolor='white')
 fig.savefig(FIG_DIR/(name+'.svg'),facecolor='white')
 plt.close(fig);FIG_NAMES.append(name)
def bar_model(tab,name,ylabel='Accuracy (%)',ylim=None):
 fig,ax=plt.subplots(figsize=(8.2,4.5));xx=np.arange(len(tab.index));wid=.18
 for j,m in enumerate(MODELS):
  if m in tab.columns:ax.bar(xx+(j-1.5)*wid,tab[m].values,width=wid,label=m,color=COLORS[m],edgecolor='white')
 ax.set_xticks(xx,tab.index,rotation=12);ax.set_ylabel(ylabel)
 if ylim:ax.set_ylim(*ylim)
 ax.grid(axis='y',alpha=.18);ax.set_axisbelow(True);ax.legend(ncol=2,fontsize=8)
 fig.tight_layout();save(name,fig)
for b in ['A','B']:
 tab=(D[D.block==b].groupby(['condition','model_tag']).end_to_end_success.mean().unstack().reindex(CONDS)*100)
 bar_model(tab,'Fig_Block'+b+'_Accuracy')
fig,ax=plt.subplots(figsize=(8,4.3))
acc=D.groupby(['block','model_tag']).end_to_end_success.mean().unstack().loc[['A','B']]*100
xx=np.arange(2)
for j,m in enumerate(MODELS):ax.bar(xx+(j-1.5)*.19,acc[m],width=.19,color=COLORS[m],label=m)
ax.set_xticks(xx,['Block A','Block B']);ax.set_ylabel('End-to-end accuracy (%)');ax.set_ylim(0,105);ax.legend(ncol=2,fontsize=8);ax.grid(axis='y',alpha=.2);fig.tight_layout();save('Fig_Block_Comparison',fig)
bench=(D.groupby(['benchmark','model_tag']).end_to_end_success.mean().unstack()*100)
bar_model(bench,'Fig_Benchmark_Comparison')
fig,ax=plt.subplots(figsize=(8.2,4.2));statuses=D.groupby('model_tag')[['acquired','parsed','end_to_end_success']].sum().reindex(MODELS)
for j,k in enumerate(statuses.columns):ax.bar(np.arange(4)+(j-1)*.23,statuses[k],width=.23,label=k.replace('_',' '))
ax.set_xticks(range(4),MODELS);ax.set_ylabel('Observations / 500 intended');ax.legend();fig.tight_layout();save('Fig_Completeness',fig)
# preserve Colab-style line trajectories, not histograms, computed from same data
for b in ['A','B']:
 tab=D[D.block==b].groupby(['condition','model_tag']).end_to_end_success.mean().unstack().reindex(CONDS)*100
 fig,ax=plt.subplots(figsize=(9.2,4.8))
 for m in MODELS:ax.plot(range(5),tab[m].values,marker='o',lw=2.0,label=m,color=COLORS[m])
 ax.set_xticks(range(5),CONDS,rotation=14,ha='right');ax.set_ylabel('End-to-end accuracy (%)');ax.grid(axis='y',alpha=.22)
 ax.legend(ncol=2,fontsize=9);fig.tight_layout();save('Fig_Leaderboard_Trajectories_'+b,fig)
for b in ['A','B']:
 for bench in ['All','ARC_Challenge','GSM8K']:
  sub=D[D.block==b]
  if bench!='All':sub=sub[sub.benchmark.str.replace('-','_',regex=False).str.replace(' ','_',regex=False).eq(bench)]
  tab=sub.groupby(['model_tag','condition']).end_to_end_success.mean().unstack().reindex(index=MODELS,columns=CONDS)*100
  fig,ax=plt.subplots(figsize=(8.5,3.9));im=ax.imshow(tab.to_numpy(),vmin=0,vmax=100,cmap='YlGnBu',aspect='auto')
  ax.set_yticks(range(4),MODELS);ax.set_xticks(range(5),CONDS,rotation=20,ha='right')
  for i in range(4):
   for j in range(5):
    v=tab.iloc[i,j];ax.text(j,i,'—' if pd.isna(v) else f'{v:.0f}',ha='center',va='center',fontsize=9,color='white' if v>72 else 'black')
  fig.colorbar(im,ax=ax,label='Accuracy (%)');fig.tight_layout();save('Fig_Heatmap_'+b+'_'+bench,fig)
# Paired baseline effects; denominator: question-paired model x block
q=D.pivot_table(index=['block','model_tag','question_id'],columns='condition',values='end_to_end_success',aggfunc='first').reindex(columns=CONDS)
deltas=q[CONDS[1:]].sub(q['baseline'],axis=0).groupby(level='model_tag').mean().reindex(MODELS)*100
bar_model(deltas.T,'Fig_Paired_Baseline_Deltas',ylabel='Paired change (percentage points)')
trans=[]
for c in CONDS[1:]:
 t=q[['baseline',c]].dropna();trans.append([int(((t.baseline==1)&(t[c]==1)).sum()),int(((t.baseline==1)&(t[c]==0)).sum()),int(((t.baseline==0)&(t[c]==1)).sum()),int(((t.baseline==0)&(t[c]==0)).sum())])
fig,ax=plt.subplots(figsize=(8,4.5));arr=np.array(trans);bottom=np.zeros(4)
for j,label in enumerate(['Correct → correct','Correct → incorrect','Incorrect → correct','Incorrect → incorrect']):
 ax.bar(np.arange(4),arr[:,j],bottom=bottom,label=label);bottom+=arr[:,j]
ax.set_xticks(range(4),CONDS[1:],rotation=15,ha='right');ax.set_ylabel('Paired observations');ax.legend(fontsize=8);fig.tight_layout();save('Fig_Paired_Transitions',fig)
# Question-level paired bootstrap, reproducible seed
rng=np.random.default_rng(2409);ci=[]
for m in MODELS:
 s=q.xs(m,level='model_tag');base=s['baseline'].to_numpy()
 for c in CONDS[1:]:
  dif=(s[c].to_numpy()-base);dif=dif[np.isfinite(dif)]
  bs=np.mean(dif[rng.integers(0,len(dif),size=(1000,len(dif)))],axis=1)*100
  ci.append((m,c,float(np.mean(dif)*100),float(np.quantile(bs,.025)),float(np.quantile(bs,.975))))
CI=pd.DataFrame(ci,columns=['model','condition','delta_pp','ci_low_pp','ci_high_pp']);CI.to_csv('data/M24_Paired_Bootstrap_CI.csv',index=False)
fig,ax=plt.subplots(figsize=(9.2,5));yy=np.arange(len(CI))
for m in MODELS:
 sub=CI[CI.model==m];inds=sub.index.to_numpy();ax.errorbar(sub.delta_pp,inds,xerr=[sub.delta_pp-sub.ci_low_pp,sub.ci_high_pp-sub.delta_pp],fmt='o',capsize=2,color=COLORS[m],label=m)
ax.axvline(0,color='#555',ls='--',lw=1);ax.set_yticks(yy,[f'{r.model}: {r.condition}' for r in CI.itertuples()],fontsize=7);ax.set_xlabel('Paired accuracy change (percentage points)');ax.legend(ncol=2,fontsize=8);fig.tight_layout();save('Fig_Paired_Bootstrap_CI',fig)
# response length: revised two panels with disjoint bin edges
fig,(a1,a2)=plt.subplots(1,2,figsize=(12.6,5.1),gridspec_kw={'width_ratios':[1.35,1]})
hatches=['///','\\\\','xx','..'];maxlen=int(D.response_length_words.max());tailend=max(1000,int(np.ceil(maxlen/100)*100))
for m,h in zip(MODELS,hatches):
 vals=D[D.model_tag==m].response_length_words.to_numpy()
 for ax,edges in [(a1,np.arange(0,251,25)),(a2,np.arange(250,tailend+101,100))]:
  counts,_=np.histogram(vals,bins=edges);ax.stairs(counts,edges,color=COLORS[m],linewidth=1.7)
  ax.stairs(counts,edges,color=COLORS[m],linewidth=.6,fill=True,hatch=h,alpha=.12)
for ax in [a1,a2]:ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
a1.set_xlim(0,250);a2.set_xlim(250,tailend)
a1.set_xlabel('Response length (words)');a2.set_xlabel('Response length (words)');a1.set_ylabel('Responses per 25-word bin');a2.set_ylabel('Responses per 100-word bin')
a1.set_title('(a) Short responses',loc='left');a2.set_title('(b) Long-response tail',loc='left')
fig.legend([Patch(facecolor=COLORS[m],hatch=h,edgecolor=COLORS[m]) for m,h in zip(MODELS,hatches)],MODELS,ncol=4,loc='upper center',bbox_to_anchor=(.5,1.02),frameon=False)
fig.tight_layout(rect=[0,0,1,.91]);save('Fig_Response_Length',fig)
# predictive-model and importance plots are generated in subsequent ML cell
print('Descriptive figures generated:',len(FIG_NAMES))

