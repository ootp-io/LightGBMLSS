from torch.distributions import Beta as Beta_Torch
from .distribution_utils import DistributionClass
from ..utils import *


class Beta(DistributionClass):
    """
    Beta distribution class.

    Distributional Parameters
    -------------------------
    concentration1: torch.Tensor
        1st concentration parameter of the distribution (often referred to as alpha).
    concentration0: torch.Tensor
        2nd concentration parameter of the distribution (often referred to as beta).

    Source
    -------------------------
    https://pytorch.org/docs/stable/distributions.html#beta

    Parameters
    -------------------------
    stabilization: str
        Stabilization method for the Gradient and Hessian. Options are "None", "MAD", "L2".
    response_fn: str
        Response function for transforming the distributional parameters to the correct support. Options are
        "exp" (exponential) or "softplus" (softplus).
    loss_fn: str
        Loss function. Options are "nll" (negative log-likelihood) or "crps" (continuous ranked probability score).
        Note that if "crps" is used, the Hessian is set to 1, as the current CRPS version is not twice differentiable.
        Hence, using the CRPS disregards any variation in the curvature of the loss function.
    """
    def __init__(self,
                 stabilization: str = "None",
                 response_fn: str = "exp",
                 loss_fn: str = "nll"
                 ):
        # Specify Response Functions
        if response_fn == "exp":
            response_fn = exp_fn
        elif response_fn == "softplus":
            response_fn = softplus_fn
        else:
            raise ValueError("Invalid response function. Please choose from 'exp' or 'softplus'.")

        # Set the parameters specific to the distribution
        distribution = Beta_Torch
        param_dict = {"concentration1": response_fn, "concentration0": response_fn}
        torch.distributions.Distribution.set_default_validate_args(False)

        # Specify Distribution Class
        super().__init__(distribution=distribution,
                         univariate=True,
                         discrete=False,
                         n_dist_param=len(param_dict),
                         stabilization=stabilization,
                         param_dict=param_dict,
                         distribution_arg_names=list(param_dict.keys()),
                         loss_fn=loss_fn
                         )
