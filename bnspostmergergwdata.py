#! /usr/bin/env python

"""
Python routines for basic work with data in
https://github.com/bernuzzi/bnspostmergergwdata
"""

import numpy as np
import csv

import pylab
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import matplotlib.cm as cmx
from matplotlib import rc
from matplotlib.gridspec import GridSpec

def csv_dict_reader(filename):
    """
    Read a CSV file using csv.DictReader
    """
    data = [] 
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=',')
        for line in reader:
            data.append(line)
    return data

def convert_float_array(x):
    xx = np.array(x)
    return  xx.astype(np.float)

def plot_fig3_kv(ax, data, key,val, title_str,label_str, cm):
    """ Plot f_2(kappa) for given pair key|val """
    n = len(val)
    for i in range(n):
        f2 = [d['Mf2'] for d in data if d[key]==val[i]]; 
        f2 = 100 * convert_float_array(f2);
        k2 = [d['kappa'] for d in data if d[key]==val[i]]
        this_color = cm(1.*i/n)
        ax.scatter(k2, f2, s=22, c=this_color, marker='o', alpha=0.6, label=label_str[i]) #, edgecolors='None')
    ax.legend(scatterpoints=1, frameon=False, ncol=2, loc=1, title=title_str, prop={'size':6}, labelspacing=0.5,columnspacing=0.5)
    return

if __name__ == "__main__":
    

    """ Example: plot Fig.3 of Bernuzzi+ 2015 """

    # Load data
    data = csv_dict_reader("./gwpmf.csv");    

    # Extract mass, EOS, q, Gammath info
    eos = [d["eos"] for d in data]
    eos = list(set(eos))
    
    q = [d["q"] for d in data]
    q = list(set(q))
    
    gamma = [d["gamma"] for d in data]
    gamma = list(set(gamma))

    mass = [d["mass"] for d in data]
    mass = list(set(mass))
    
    # Sort
    mass = np.sort(mass);
    q = np.sort(q);
    gamma = np.sort(gamma);

    # Figure layout    
    fig_width_pt = 400.0  
    inches_per_pt = 1.0/72.27  # convert pt to inch
    golden_mean = (np.sqrt(5)-1.0)/2.0  # aesthetic ratio
    aratio = golden_mean
    fig_width = fig_width_pt*inches_per_pt  # width in inches
    fig_height = fig_width*aratio  # height in inches
    fig_size = [fig_width,fig_height]    
    fsize = 10; # 16
    params = {'backend': 'pdf',
              'axes.labelsize': fsize,
              'font.size': fsize,
              'legend.fontsize': fsize,
              'xtick.labelsize': fsize,
              'ytick.labelsize': fsize,
              'text.usetex': True,
              'figure.figsize': fig_size,
              'savefig.dpi': 600}
    pylab.rcParams.update(params)
    
    fig = plt.figure()
    gs = GridSpec(2, 2)
    gs.update(left=0.075, right=0.99, 
              top=0.99, bottom=0.105,
              hspace=0, wspace=0 )
    
    ax1 = plt.subplot(gs[0,0])
    ax2 = plt.subplot(gs[0,1])
    ax3 = plt.subplot(gs[1,0])
    ax4 = plt.subplot(gs[1,1])
    
    ax1.axis([30., 500, 2.1, 5.2]);
    ax1.set_ylabel('$Mf_2\ [\\times10^2]$',labelpad=0)
    ax1.axes.get_xaxis().set_ticklabels([])
    
    ax2.axis([30., 500, 2.1, 5.2]);
    ax2.axes.get_xaxis().set_ticklabels([])
    ax2.axes.get_yaxis().set_ticklabels([])
    
    ax3.axis([30., 500, 2.1, 5.4]);
    ax3.xaxis.set_ticks([100,200,300,400])
    ax3.set_ylabel('$Mf_2\ [\\times10^2]$',labelpad=0); 
    ax3.set_xlabel('$\\kappa^T_2$',labelpad=1);

    ax4.axis([30., 500, 2.1, 5.2]);
    ax4.xaxis.set_ticks([100,200,300,400])
    ax4.set_xlabel('$\\kappa^T_2$',labelpad=1);
    ax4.axes.get_yaxis().set_ticklabels([])

    # Labels/legend entries 
    label_str_eos = [0]*len(eos);
    label_str_m = [0]*len(mass);
    label_str_q = [0]*len(q);
    label_str_g = [0]*len(gamma);
    for i in range(len(eos)):
        if eos[i]=='Gamma2':
            label_str_eos[i]='$\\Gamma_2$'
        else:
            label_str_eos[i]=eos[i]
    for i in range(len(mass)):
        label_str_m[i]="%s" % mass[i]
    for i in range(len(q)):
        label_str_q[i]="%s" % q[i]
    for i in range(len(gamma)):
        label_str_g[i]="%s" % gamma[i]
    
    # Panels
    cm = plt.cm.get_cmap('gist_rainbow')
    plot_fig3_kv(ax1, data, "mass",mass, "Binary Mass $M$",label_str_m, cm);
    plot_fig3_kv(ax2, data, "eos",eos, "EOS",label_str_eos, cm);
    plot_fig3_kv(ax3, data, "q",q, "Mass-ratio $q$",label_str_q, cm);
    plot_fig3_kv(ax4, data, "gamma",gamma, "$\\Gamma_{th}$",label_str_g, cm);

    # Save plot 
    plt.savefig('f2kappa.png')  
    
