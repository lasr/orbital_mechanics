"""Created on Wed Sep 10 2015 11:06.

@author: Nathan Budd
"""
from .model_abstract import ModelAbstract
from .perturb_zero import PerturbZero


class SystemDynamics(ModelAbstract):
    """Combines a plant model, control, and perturbations.

    Instance Members
    -------
    plant : ModelAbstract subclass
    Represents the simple, unperturbed system dynamics.

    control : ModelAbstract subclass
    Represents the system control.

    preturbations : list of ModelAbstract subclasses
    Represent perturbations acting on the system.
    """

    def __init__(self, plant, control=PerturbZero(),
                 perturbations=[PerturbZero()]):
        """."""
        self.plant = plant
        self.control = control
        self.perturbations = perturbations
        super().__init__()

    def __call__(self, T, X):
        """Evaluate the full system dynamics.

        Input
        -----
        T : np.array
        An mx1 column array of times.

        X : np.array
        An mxn array of states.

        Output
        ------
        Xdot : np.array
        An mxn array of state derivatives
        """
        Xdot = self.plant(T, X) + self.control(T, X)
        for perturb in self.perturbations:
            Xdot = Xdot + perturb(T, X)

        self.Xdot = Xdot
        return Xdot

    def __repr__(self):
        """Printable represenation of the object."""
        return 'SystemDynamics({}, {}, {})'.format(
            self.plant, self.control, self.perturbations)

    def __str__(self):
        """Human readable represenation of the object."""
        output = 'SystemDynamics'
        output += '(plant={}, control={}, perturbations={})'.format(
            self.plant, self.control, self.perturbations)
        return output
