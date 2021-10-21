# -*- coding: utf-8 -*-

import numpy as np
def basketing_special(y,x_start,num_of_dots,ratio=0.5):
  '''
  "num_of_dots" is total number of baskets
  x_start is minimum of our distribution
  y is the probability array and its length is equeal to the number of points in distribution (x_start+i,y[i])
  example:
    pa = np.load(path+'N4000/N4000 j1.5 d1.5 g7.0 w1.0 base0 PA_Hei_pos.npy')
    y = pa[1:]
    x_start = pa[0]
    
  returned x and z are new array of positions
  each x element is the beginning of basket and each z value is the number(or probability if "y" has been normalized) of that basket
  all arrays are numpy.ndarray type
  '''
  if len(y)<=num_of_dots:
    return np.arange(x_start,x_start+len(y)),y
  if ratio>1 or ratio<0:
    ratio = 0.5
  bin_start_value = int(((x_start)**(ratio)*(len(y)+x_start)**(1-ratio)))
  bin_start_index = bin_start_value - x_start
  if bin_start_index >= num_of_dots:
    num_of_dots = num_of_dots+bin_start_index
  new_bins = np.unique(np.sort(np.logspace(np.log10(bin_start_value),np.log10(len(y)+x_start+1),num_of_dots-bin_start_index).astype(int)))
  num_of_dots = len(new_bins)+bin_start_index  
  z = np.empty(num_of_dots)
  x = np.empty(num_of_dots,dtype=int)
  z[:bin_start_index] = y[:bin_start_index]
  x[:bin_start_index] = np.arange(x_start,bin_start_value)
  x[bin_start_index:] = new_bins
  bins2 = np.roll(new_bins,-1)
  dbins = bins2 - new_bins
  for i,j in enumerate(range(bin_start_index,num_of_dots)):
    z[j] = y[new_bins[i]-x_start:bins2[i]-x_start].sum()/dbins[i]
  return x,z