from numba import jit, b1, float32, int32
import numpy as np
from numba.experimental import jitclass
from .observer import *
from .propagator import *
from .particle_state import *



particle_spec = [
    ('observer', Observer.class_type.instance_type),
    ('propagator', Propagator.class_type.instance_type),
    ('ps', ParticleState.class_type.instance_type),
]

@jitclass(particle_spec)
class Particle():
    def __init__(self, particle_id, energy, pos, phi, pitch_angle, dimensions):
        self.ps = ParticleState(particle_id, energy, pos, phi, pitch_angle, dimensions)
        
        
    def simulate(self, observer, propagator):
        simulation_data = []

        self.ps.init_position()
        for step in range(0, propagator.nr_steps+1): 
            self.start_step(propagator, step)
            self.ps.pos_prev =  np.array([self.ps.pos[0], self.ps.pos[1], self.ps.pos[2]], dtype=np.float32)
            for substep in range(self.ps.dimensions):
                self.propagate_substep(propagator, substep)
                observation = observer.observe(self.ps)
                if observation is not None:
                    simulation_data.append(observation)

                    
        return simulation_data


    def start_step(self, propagator, step):
        self.ps.step = step
        self.ps.pos_prev = self.ps.pos
        self.ps = propagator.set_gyroradius(self.ps)
        self.ps.direction = propagator.change_direction(self.ps.direction)
        self.ps.pitch_angle = propagator.change_pitch_angle(self.ps.pitch_angle)


    def propagate_substep(self, propagator, substep):
        self.ps.substep = substep
        self.ps = propagator.move_substep(self.ps)