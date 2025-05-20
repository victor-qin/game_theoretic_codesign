'''
Given data on the Pareto front and a Nash equilibrium point, this script generates a scatter plot.
'''

from decimal import Decimal
import numpy as np
import matplotlib.pyplot as plt

# Reconstruct data as a list of tuples
data = [
(Decimal('0.078125000'), Decimal('0.921875000')), (Decimal('0.296875000'),
    Decimal('0.703125000')), (Decimal('0.382812500'), Decimal('0.617187500')), (Decimal('0.515625000'),
    Decimal('0.484375000')), (Decimal('0.601562500'), Decimal('0.398437500')), (Decimal('0.734375000'),
    Decimal('0.265625000')), (Decimal('0.023437500'), Decimal('0.976562500')), (Decimal('0.109375000'),
    Decimal('0.890625000')), (Decimal('0.195312500'), Decimal('0.804687500')), (Decimal('0.328125000'),
    Decimal('0.671875000')), (Decimal('0.414062500'), Decimal('0.585937500')), (Decimal('0.593750000'),
    Decimal('0.406250000')), (Decimal('0.726562500'), Decimal('0.273437500')), (Decimal('0.812500000'),
    Decimal('0.187500000')), (Decimal('0.007812500'), Decimal('0.992187500')), (Decimal('0.187500000'),
    Decimal('0.812500000')), (Decimal('0.320312500'), Decimal('0.679687500')), (Decimal('0.406250000'),
    Decimal('0.593750000')), (Decimal('0.539062500'), Decimal('0.460937500')), (Decimal('0.625000000'),
    Decimal('0.375000000')), (Decimal('0.843750000'), Decimal('0.156250000')), (Decimal('0.132812500'),
    Decimal('0.867187500')), (Decimal('0.218750000'), Decimal('0.781250000')), (Decimal('0.351562500'),
    Decimal('0.648437500')), (Decimal('0.437500000'), Decimal('0.562500000')), (Decimal('0.523437500'),
    Decimal('0.476562500')), (Decimal('0.656250000'), Decimal('0.343750000')), (Decimal('0.875000000'),
    Decimal('0.125000000')), (Decimal('0.031250000'), Decimal('0.968750000')), (Decimal('0.164062500'),
    Decimal('0.835937500')), (Decimal('0.250000000'), Decimal('0.750000000')), (Decimal('0.468750000'),
    Decimal('0.531250000')), (Decimal('0.687500000'), Decimal('0.312500000')), (Decimal('0.953125000'),
    Decimal('0.046875000')), (Decimal('0.062500000'), Decimal('0.937500000')), (Decimal('0.148437500'),
    Decimal('0.851562500')), (Decimal('0.281250000'), Decimal('0.718750000')), (Decimal('0.546875000'),
    Decimal('0.453125000')), (Decimal('0.765625000'), Decimal('0.234375000')), (Decimal('0.851562500'),
    Decimal('0.148437500')), (Decimal('0.984375000'), Decimal('0.015625000')), (Decimal('0.140625000'),
    Decimal('0.859375000')), (Decimal('0.273437500'), Decimal('0.726562500')), (Decimal('0.359375000'),
    Decimal('0.640625000')), (Decimal('0.578125000'), Decimal('0.421875000')), (Decimal('0.664062500'),
    Decimal('0.335937500')), (Decimal('0.796875000'), Decimal('0.203125000')), (Decimal('0.882812500'),
    Decimal('0.117187500')), (Decimal('0.171875000'), Decimal('0.828125000')), (Decimal('0.390625000'),
    Decimal('0.609375000')), (Decimal('0.476562500'), Decimal('0.523437500')), (Decimal('0.609375000'),
    Decimal('0.390625000')), (Decimal('0.695312500'), Decimal('0.304687500')), (Decimal('0.828125000'),
    Decimal('0.171875000')), (Decimal('0.914062500'), Decimal('0.085937500')), (Decimal('0.203125000'),
    Decimal('0.796875000')), (Decimal('0.289062500'), Decimal('0.710937500')), (Decimal('0.421875000'),
    Decimal('0.578125000')), (Decimal('0.507812500'), Decimal('0.492187500')), (Decimal('1.000000000'),
    Decimal('0E-9')), (Decimal('0.640625000'), Decimal('0.359375000')), (Decimal('0.820312500'),
    Decimal('0.179687500')), (Decimal('0.906250000'), Decimal('0.093750000')), (Decimal('0.015625000'),
    Decimal('0.984375000')), (Decimal('0.101562500'), Decimal('0.898437500')), (Decimal('0.234375000'),
    Decimal('0.765625000')), (Decimal('0.500000000'), Decimal('0.500000000')), (Decimal('0.632812500'),
    Decimal('0.367187500')), (Decimal('0.718750000'), Decimal('0.281250000')), (Decimal('0.937500000'),
    Decimal('0.062500000')), (Decimal('0.093750000'), Decimal('0.906250000')), (Decimal('0.226562500'),
    Decimal('0.773437500')), (Decimal('0.312500000'), Decimal('0.687500000')), (Decimal('0.445312500'),
    Decimal('0.554687500')), (Decimal('0.531250000'), Decimal('0.468750000')), (Decimal('0.750000000'),
    Decimal('0.250000000')), (Decimal('0.968750000'), Decimal('0.031250000')), (Decimal('0.039062500'),
    Decimal('0.960937500')), (Decimal('0.125000000'), Decimal('0.875000000')), (Decimal('0.257812500'),
    Decimal('0.742187500')), (Decimal('0.343750000'), Decimal('0.656250000')), (Decimal('0.562500000'),
    Decimal('0.437500000')), (Decimal('0.781250000'), Decimal('0.218750000')), (Decimal('0.070312500'),
    Decimal('0.929687500')), (Decimal('0.156250000'), Decimal('0.843750000')), (Decimal('0.375000000'),
    Decimal('0.625000000')), (Decimal('0.773437500'), Decimal('0.226562500')), (Decimal('0.859375000'),
    Decimal('0.140625000')), (Decimal('0.945312500'), Decimal('0.054687500')), (Decimal('0E-9'),
    Decimal('1.000000000')), (Decimal('0.453125000'), Decimal('0.546875000')), (Decimal('0.671875000'),
    Decimal('0.328125000')), (Decimal('0.757812500'), Decimal('0.242187500')), (Decimal('0.890625000'),
    Decimal('0.109375000')), (Decimal('0.976562500'), Decimal('0.023437500')), (Decimal('0.046875000'),
    Decimal('0.953125000')), (Decimal('0.265625000'), Decimal('0.734375000')), (Decimal('0.484375000'),
    Decimal('0.515625000')), (Decimal('0.570312500'), Decimal('0.429687500')), (Decimal('0.703125000'),
    Decimal('0.296875000')), (Decimal('0.789062500'), Decimal('0.210937500')), (Decimal('0.921875000'),
    Decimal('0.078125000')),

]

nash = (Decimal('0.3359375'), Decimal('0.328125'))
# Convert to floats
xs = [float(x) for x, y in data]
ys = [float(y) for x, y in data]

# Plot
plt.figure(figsize=(6,6))
plt.scatter(xs, ys, s=10, label='Pareto Front')
plt.scatter(float(nash[0]), float(nash[1]), color='red', s=100, label='Nash Equilibrium')
x_line = np.linspace(min(xs), 0.5, 100)
y_line = 0.5 - x_line
plt.plot(x_line, y_line, color='green', label='Social Welfare Optimal Line')
plt.xlabel('x1')
plt.ylabel('x2')
plt.title('Scatter Plot of Provided Dataset')
plt.axis('equal')
plt.legend()
plt.show()