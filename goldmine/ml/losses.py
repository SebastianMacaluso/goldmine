import logging
import torch
from torch.nn.modules.loss import BCELoss, MSELoss
import numpy as np


def negative_log_likelihood(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true):
    return -torch.mean(log_p_pred)


def score_mse(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true):
    return MSELoss()(t_pred, t_true)


def ratio_mse_num(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true, log_r_clip=25.):
    r_pred = torch.exp(log_r_pred)
    # r_true = torch.clamp(r_true, np.exp(-log_r_clip), np.exp(log_r_clip))
    # r_pred = torch.exp(torch.clamp(log_r_pred, -log_r_clip, log_r_clip))

    return MSELoss()((1. - y_true) * (1. / r_pred), (1. - y_true) * (1. / r_true))


def ratio_mse_den(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true, log_r_clip=25.):
    r_pred = torch.exp(log_r_pred)
    # r_true = torch.clamp(r_true, np.exp(-log_r_clip), np.exp(log_r_clip))
    # r_pred = torch.exp(torch.clamp(log_r_pred, -log_r_clip, log_r_clip))

    return MSELoss()(y_true * r_pred, y_true * r_true)


def ratio_mse(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true, log_r_clip=25.):
    return (ratio_mse_num(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true, log_r_clip)
            + ratio_mse_den(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true, log_r_clip))


def standard_cross_entropy(log_p_pred, log_r_pred, t_pred, y_true, r_true, t_true, log_r_clip=25.):
    r_pred = torch.exp(log_r_pred)
    # r_pred = torch.exp(torch.clamp(log_r_pred, -log_r_clip, log_r_clip))
    s_hat = 1. / (1. + r_pred)

    return BCELoss()(s_hat, y_true)
