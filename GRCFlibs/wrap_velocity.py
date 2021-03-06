#! /usr/bin/env python

from numpy import frombuffer
from pylab import *
from ctypes import CDLL, c_double
from numpy.ctypeslib import ndpointer
from os.path import dirname


lib = CDLL(dirname(__file__)+"/c_velo_lib.so")


def v_disc(dParams, gParams, distances):
    c_v_disc = lib.c_v_disc
    cdistances = (c_double * len(distances))(*distances)
    disc_params = (c_double * 5)(float(dParams["cenSurfBri"]),
                                 float(dParams["expScale"]),
                                 float(dParams["thickness"]),
                                 float(dParams["axisRatio"]),
                                 float(dParams["MLratio"]))
    general_params = (c_double * 4)(float(gParams["hubble"]),
                                    float(gParams["LD"]),
                                    float(gParams["scale"]),
                                    float(gParams["Msun"]))
    vd = (c_double * len(distances))(*distances)
    c_v_disc(disc_params, general_params, cdistances, vd, len(cdistances))
    return 1e4*frombuffer(vd)

def v_bulge(bParams, dParams, gParams, distances):
    c_v_bulge = lib.c_v_bulge
    cdistances = (c_double * len(distances))(*distances)
    bulge_params = (c_double * 5)(float(bParams["effSurfBri"]),
                                  float(bParams["effRadius"]),
                                  float(bParams["sersicIndex"]),
                                  float(bParams["axisRatio"]),
                                  float(bParams["MLratio"]))
    disc_params = (c_double * 2)(float(dParams["thickness"]),
                                 float(dParams["axisRatio"]))
    general_params = (c_double * 4)(float(gParams["hubble"]),
                                    float(gParams["LD"]),
                                    float(gParams["scale"]),
                                    float(gParams["Msun"]))
    vb = (c_double * len(distances))(*distances)
    c_v_bulge(bulge_params, disc_params, general_params, cdistances, vb, len(cdistances))
    return 1e4*frombuffer(vb)

def v_halo(bParams, dParams, hParams, gParams, distances):
    c_v_halo = lib.c_v_halo
    cdistances = (c_double * len(distances))(*distances)
    bulge_params = (c_double * 5)(float(bParams["effSurfBri"]),
                                  float(bParams["effRadius"]),
                                  float(bParams["sersicIndex"]),
                                  float(bParams["axisRatio"]),
                                  float(bParams["MLratio"]))
    disc_params = (c_double * 5)(float(dParams["cenSurfBri"]),
                                 float(dParams["expScale"]),
                                 float(dParams["thickness"]),
                                 float(dParams["axisRatio"]),
                                 float(dParams["MLratio"]))
    if hParams["model"] == "NFW":
        haloType = 1.0
    elif hParams["model"] == "isoterm":
        haloType = 0.0
    elif hParams["model"] == "Burkert":
        haloType = -1.0
    halo_params = (c_double * 4)(haloType,
                                float(hParams["includeAC"]),
                                float(hParams["firstParam"]),
                                float(hParams["secondParam"]))
    general_params = (c_double * 4)(float(gParams["hubble"]),
                                    float(gParams["LD"]),
                                    float(gParams["scale"]),
                                    float(gParams["Msun"]))
    vh = (c_double * len(distances))(*distances)
    c_v_halo(bulge_params, disc_params, halo_params, general_params, cdistances, vh, len(cdistances))
    return 1e4*frombuffer(vh)

