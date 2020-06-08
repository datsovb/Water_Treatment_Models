# -*- coding: utf-8 -*-
"""
Created on Wed May 20 08:10:32 2020

@author: BDATSOV
"""

###### 



import pandas as pd
import numpy as np
import sys
   
def conv_units(u_in, u_out, u_list, u_coef, label, caller):
    
    if u_in in u_list:
        u_in_pos = u_list.index(u_in)
    else:

        print('WARRNING: ' + caller + ' is not in porper units!')
        print('Acceptable units for ' + label + ' are: ', *u_list, sep='\n')
        
        pos_assigned = True
        while pos_assigned:
            try:
                u_in = str(input('Please eneter the correct units here:'))
                if u_in in u_list:
                    u_in_pos = u_list.index(u_in)
                    pos_assigned = False
                    break
            except ValueError:
                print('Entered units are not accepted.')
                
    if u_out in u_list:
        u_out_pos = u_list.index(u_out)
    else:
        print(u_out + ' are not acceptable units.')
        print('Enter units in one of the following units list:', *u_list, sep='\n')
        u_out_pos = False
        sys.exit()
    
    base_vector = np.array(u_coef)
    base_data = np.array([base_vector]*len(base_vector))
    l_factor = base_data/base_vector[:,None]
    factor = l_factor[u_in_pos,u_out_pos]    
    
    return factor, u_in, u_out



def conv_length(u_in, u_out, label, caller):
    units = ['m','cm','mm','ft','in', 'um']
    coefs = [1.,100.,1000.,3.2808,39.3701, 1.0e6]
    cv, u_in, u_out = conv_units(u_in,u_out, units, coefs, label, caller)
    
    return cv, u_in, u_out


def conv_volume(u_in, u_out, label, caller):
    units = ['m3','cm3','ml','L','mm3','gal','ft3','in3','cuf']
    coefs = [1., 1.0e6, 1.0e6, 1.0e3, 1.0e9, 264.172, 35.3147, 61023.801579099, 35.3147]
    cv, u_in, u_out = conv_units(u_in,u_out, units, coefs, label, caller)
    
    return cv, u_in, u_out


def conv_time(u_in, u_out, label, caller):
    units = ['days','hours','min','sec','m','s','h','d', 'hr', 'day', 'hour']
    coefs = [1. , 24., 24.*60., 24*60*60, 24.*60., 24*60*60, 24., 1., 24., 1., 24.]
    cv, u_in, u_out = conv_units(u_in,u_out, units, coefs, label, caller)
    
    return cv, u_in, u_out


def conv_vol_per_time(u_in, u_out, label, caller):
    vars_lst = [u_in, u_out]
    vol = []
    time = []
    for var in vars_lst:
        if '/' in var:
            vol.append(var.split('/')[0])
            time.append(var.split('/')[1])
        elif 'gpm' in var:
            vol.append('gal')
            time.append('min')
        else:
            print('else')
    v_f, u_in_v, u_out_v = conv_volume(vol[0],vol[1], label, caller)
    t_f, u_in_t, u_out_t = conv_time(time[0], time[1], label, caller)
    
    if u_in_v == 'gal':
        u_in_v = 'g'
        u_in = u_in_v + 'p' + u_in_t
    else:
        u_in = u_in_v + '/' + u_in_t        
    
    cv = v_f/t_f, u_in, u_out
    
    return cv


def conv_vel(u_in, u_out, label, caller):
    vars_lst = [u_in, u_out]
    lenght = []
    time = []
    for var in vars_lst:
        if '/' in var:
            lenght.append(var.split('/')[0])
            time.append(var.split('/')[1])
        elif 'gpm' in var:
            lenght.append('gal')
            time.append('min')
        else:
            print('else')
    l_f, u_in_l, u_out_l = conv_length(lenght[0],lenght[1], label, caller)
    t_f, u_in_t, u_out_t = conv_time(time[0], time[1], label, caller)
    
    u_in = u_in_l + '/' + u_in_t
    
    cv = l_f/t_f
    
    return cv, u_in, u_out

def conv_dens(u_in, u_out, label, caller):
    vars_lst = [u_in, u_out]
    wght = []
    vol = []
    for var in vars_lst:
        if '/' in var:
            wght.append(var.split('/')[0])
            vol.append(var.split('/')[1])
        elif 'gpm' in var:
            wght.append('gal')
            vol.append('min')
        else:
            print('else')
    w_f, u_in_w, u_out_w = conv_weight(wght[0],wght[1], label, caller)
    v_f, u_in_v, u_out_v = conv_volume(vol[0], vol[1], label, caller)
    
    if u_in_v == 'gal':
        u_in_v = 'g'
        u_in = u_in_w + 'p' + u_in_v
    else:
        u_in = u_in_w + '/' + u_in_v
    
    cv = w_f/v_f
    
    return cv, u_in, u_out

def conv_area(u_in, u_out, label, caller):
    units = ['m2', 'cm2', 'mm2', 'ft2', 'in2']
    coefs = [1., 10000., 1000000., 1550.0031, 10.7639]
    cv, u_in, u_out = conv_units(u_in, u_out, units, coefs, label, caller)
    
    return cv, u_in, u_out
    

def conv_area_per_time(u_in, u_out, label, caller):
    vars_lst = [u_in, u_out]
    area = []
    time = []
    for var in vars_lst:
        if '/' in var:
#            print(var.split('/'))
            area.append(var.split('/')[0])
            time.append(var.split('/')[1])
        elif 'gpm' in var:
            area.append('gal')
            time.append('min')
        else:
            print('else')
    l_f, u_in_l, u_out_l = conv_area(area[0],area[1], label, caller)
    t_f, u_in_t, u_out_t = conv_time(time[0], time[1], label, caller)
    
    u_in = u_in_l + '/' + u_in_t
    
    cv = l_f/t_f
    
    return cv, u_in, u_out
    
    
    
def conv_fr_to_vel(u_in, u_out, diam, diam_u, label, caller):

    if '/' in u_out:
        l_out, time_out = u_out.split('/')
    else:
        l_out = 'gal'
        time_out = 'min'
        
    tmp_vol_u = diam_u + '3' + '/' + time_out       # create diam_u per time_out
    vol_to_d, u_in_vd, u_out_vd = conv_vol_per_time(u_in, tmp_vol_u, label, caller)  #conv vol units to diam units
    tmp_cv, u_in_tmp, u_out_tmp = conv_length(diam_u, l_out, label, caller)           # conv linear units to cm
    cv = vol_to_d*tmp_cv/(np.pi*diam**2/4)
    u_in = u_in_vd + '/' + u_out_vd
    
    return cv, u_in, u_out


def conv_conc(u_in, u_out, MW, val, label, caller):
    units = ['meq', 'mg', 'ug', 'ng', 'mgN', 'mgC']
    coefs = [1, MW*val, 1000.*MW*val, 1.0e6*MW*val, 14.001*val, 12.011*val]
    cv, u_in, u_out = conv_units(u_in, u_out, units, coefs, label, caller)
    return cv, u_in, u_out


def conv_database(data_in, u_in, u_out, conv_fn, MW, val):
    
    for u in u_in.keys():
#        tmp_conv_fn = conv_fn[u]
        cf, u_in[u], u_out[u] = conv_fn(u_in[u], u_out[u], MW[u], val[u], u, u)
        data_in[u] *= cf
        
    return data_in, u_in, u_out


def conv_params(data_in, u_in, u_out, conv_fn):    
    for u in u_in.keys():
        tmp_conv_fn = conv_fn[u]
        cf, u_in[u], u_out[u] = tmp_conv_fn(u_in[u], u_out[u], u, u)
        data_in.loc[u, 'value'] *= cf
        data_in.loc[u, 'units'] = u_out[u]        
        
    return data_in

def conv_weight(u_in, u_out, label, caller):
    units = ['kg', 'g', 'mg', 'ug', 'ng', 'lbs', 'lb', 'lbm', 'oz']
    coefs = [1., 1000., 1.0e6, 1.0e9, 1.0e12, 2.2046226218, 2.2046226218, 2.2046226218, 35.27396195]
    cv, u_in, u_out = conv_units(u_in, u_out, units, coefs, label, caller)
    return cv, u_in, u_out

def conv_capacity(u_in, u_out, label, caller):
    vars_lst = [u_in, u_out]
    conc = []
    wght = []
    for var in vars_lst:
        if '/' in var:
#            print(var.split('/'))
            conc.append(var.split('/')[0])
            wght.append(var.split('/')[1])
        elif 'gpm' in var:
            conc.append('gal')
            wght.append('min')
        else:
            print('else')
    c_f, u_in_c, u_out_c = conv_conc(conc[0],conc[1], label, caller)
    w_f, u_in_w, u_out_w = conv_weight(wght[0], wght[1], label, caller)
    
    cv = c_f/w_f
    u_in = u_in_c + '/' + u_in_w
    
    return cv, u_in, u_out


def conv_params_data(data):
    params_Dct = data.to_dict('index')
    
    u_in = {}
    
    u_out = {'time':'s', 'RHOP':'g/ml', 'rb':'cm', 'kL':'cm/s', \
             'Ds':'cm2/s', 'v':'cm/s', 'Qm':'meq/g', 'L':'cm', \
             'flrt':'cm3/s', 'diam':'cm'}
    
    u_fn = {'time':conv_time, 'RHOP':conv_dens, 'rb':conv_length, 'kL':conv_vel, \
             'Ds':conv_area_per_time, 'v':conv_vel, 'Qm':conv_capacity , \
             'flrt':conv_vol_per_time, 'L':conv_length, 'diam':conv_length}
    
    params_pop = ['Qm', 'EBED', 'nz', 'nr']
    
    
    for p in params_Dct.keys():
        if p not in params_pop:
            u_in[p] = params_Dct[p]['units']
            u_out[p] = u_out[p]
            u_fn[p] = u_fn[p]

    
    params_out = conv_params(data, u_in, u_out, u_fn)
    
    if 'v' not in params_out.index:
        flrt_f, u_in_fr, u_out_fr = conv_fr_to_vel(data.loc['flrt','units'], 'cm/s', \
                                data.loc['diam','value'], \
                                data.loc['diam','units'], '', '')    
    
        flrt_cv = params_out.loc['flrt','value']*flrt_f
        
        v_row = pd.DataFrame([[flrt_cv, 'cm/s']], columns = ['value', 'units'], \
                             index = ['v'])
        
        params_out = params_out.append(v_row)
    else:
        params_out = params_out
        if 'flrt' in params_out.index:
            print('The linear velocity has been used instead of the flow rate.')
    
    return params_out
