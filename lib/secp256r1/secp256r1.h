#ifndef __SECP2561R1_H__
#define __SECP2561R1_H__
#include <ecc.h>
void get_curve_param(curve_params_t *para);
NN_UINT omega_mul(NN_DIGIT *a, NN_DIGIT *b, NN_DIGIT *omega, NN_UINT digits);
#endif