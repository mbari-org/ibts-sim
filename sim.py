import time
import numpy as np
from components import ParticleField
import matplotlib.pyplot as plt

# Create a background particle field
bg_field = ParticleField([0,0,0],[10,10,10],1, 1,-1.5)

# Create a copepod patch field at 10 m depth with 1 km extent in xy, 1 km in x
copepod_field = ParticleField([1,0,.02],[.5,.5,.003],10, 1,-1.5)

auv_start = np.array([0,0,0])
auv_speed = .001 # km/s
auv_angle = 20 # deg
auv_max_depth = .06 # km
auv_min_depth = .002 # km
duration = 3600 # s
time_step = 1 # s

elapsed_time = 0
auv_location = auv_start

data_index = 0
data = np.zeros((int(duration/time_step), 4))

while elapsed_time < duration:
    
    bg_counts = bg_field.sample(auv_location, 1, 1, -1.5)
    copepod_counts = copepod_field.sample(auv_location, 1, 1, -1.5)
    #print([auv_location, auv_angle, elapsed_time, bg_counts, copepod_counts])
    
    data[data_index,0] = auv_location[0]
    data[data_index,1] = auv_location[2]
    data[data_index,2] = bg_counts
    data[data_index,3] = copepod_counts
    data_index += 1
    
    # Move AUV
    auv_location = auv_location + [time_step*auv_speed*np.cos(auv_angle*np.pi/180), 0, time_step*auv_speed*np.sin(auv_angle*np.pi/180)]
    elapsed_time += time_step
    
    # depth limit
    if auv_location[2] >= auv_max_depth:
        auv_angle = -1* abs(auv_angle) 
    if auv_location[2] <= auv_min_depth:
        auv_angle = abs(auv_angle) 


# Plot counts vs depth and time
fig, ax = plt.subplots()
for i in range(0,data.shape[0]):
    ax.plot(1000*data[i,0], 1000*data[i,1], c='red', marker='o', alpha=data[i,3]/10.0)

ax.set_ylim(100, 0)
ax.grid(True)
ax.set_xlabel('Horizontal Distance (m)')
ax.set_ylabel('Depth (m)')
plt.show()