from torch.distributions import Weibull as Weibull_Torch
from lightgbmlss.utils import *
from .distribution_utils import DistributionClass


class Weibull(DistributionClass):
    """
    Weibull distribution class.

    Distributional Parameters
    -------------------------
    scale: torch.Tensor
        Scale parameter of distribution (lambda).
    concentration: torch.Tensor
        Concentration parameter of distribution (k/shape).

    Source
    -------------------------
    https://pytorch.org/docs/stable/distributions.html#weibull

     Parameters
    -------------------------
    stabilization: str
        Stabilization method for the Gradient and Hessian. Options are "None", "MAD", "L2".
    response_fn: str
        When a custom objective and metric are provided, LightGBM doesn't know its response and link function. Hence,
        the user is responsible for specifying the transformations. Options are "exp" or "softplus".
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
        distribution = Weibull_Torch
        param_dict = {"scale": response_fn, "concentration": response_fn}

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
