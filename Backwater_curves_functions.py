# -*- coding: utf-8 -*-
"""
Backwater curves functions

@author: Tung Dao, Dec 2021
"""
# In[Library]
import numpy as np
from scipy.optimize import fsolve

# In[bed roughness]


def bedRoughness(soil_type, diameter_soil):
    if soil_type == 'sand':
        bed_roughness = 0.1
        return bed_roughness
    elif soil_type == 'clay':
        bed_rougness = 0.05
        return bed_roughness
    elif soil_type == 'narrow_gravel':
        bed_roughness = 2*diameter_soil
        return bed_roughness
    elif soil_type == 'wide_gravel':
        bed_roughness = 6*diameter_soil
        return bed_roughness
    else:
        return 'The soil type is unfamiliar, check the input of the function.'

# In[Chezy - Velocity]


def Chezy(hydraulic_radius, bed_roughness):
    chezys_constant = 18 * np.log10(12 * hydraulic_radius / bed_roughness)
    return chezys_constant


def Velocity(chezys_constant, hydraulic_radius, bed_slope):
    mean_velocity = chezys_constant * np.sqrt(hydraulic_radius*bed_slope)
    return mean_velocity

# In[Equilibrium depth]


def equilibriumDepth(discharge_Q, chezys_constant, river_width, bed_slope):
    equilibrium_depth = (discharge_Q /
                         (chezys_constant * river_width
                          * np.sqrt(bed_slope)))**(2/3)
    return equilibrium_depth


def SolveEquilibriumDepth(h):
    river_width = 240
    bed_slope = 1/10000
    bed_roughness = 0.1
    discharge_Q = 200
    return (10**((discharge_Q/(h**(3/2) * 18))
            / (river_width * np.sqrt(bed_slope)))
            * bed_roughness / 12 - h)


equilibrium_depth = fsolve(SolveEquilibriumDepth, 1)

# In[Backwater curves]


def backwater_curve(wdepth_diff_x0, bed_slope,
                    initial_wdepth, interest_length):
    exponential_part = []
    wdepth_diff_x = []
    water_depth = []
    for i in range(len(interest_length)):
        exponential_part = -3 * bed_slope * interest_length /\
            initial_wdepth
        wdepth_diff_x = wdepth_diff_x0 * np.exp(exponential_part)
    water_depth = wdepth_diff_x + initial_wdepth
    return water_depth

# In[weir height]


def weir_height_calculation(discharge_Q, river_width,
                            initial_wdepth, wdepth_diff_x0):
    gravity = 9.81
    discharge_q = discharge_Q / river_width
    crit_depth = discharge_q / gravity
    weir_height = initial_wdepth + wdepth_diff_x0 - crit_depth
    print(f"For the initial parameters of the weir and the river, such as:\
\n An average width, B = {river_width} (m)\
\n An average discharge, Q = {discharge_Q} (m\N{superscript three}/s) \
\n An initial water depth, h = {initial_wdepth} (m)\
\n A water depth difference at x = 0, z\N{subscript zero} = {wdepth_diff_x0} (m)\
\nThe critical depth will be {crit_depth:.3f} (m).\
\nTherefore, the weir height will be {weir_height:.3f} (m)")
    return weir_height, crit_depth
