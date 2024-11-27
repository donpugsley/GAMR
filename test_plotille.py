import plotille

import plotille
import numpy as np

X = np.sort(np.random.normal(size=1000))

fig = plotille.Figure()
fig.width = 60
fig.height = 30
fig.set_x_limits(min_=-3, max_=3)
fig.set_y_limits(min_=-1, max_=1)
fig.color_mode = 'byte'
fig.plot([-0.5, 1], [-1, 1], lc=25, label='line')
fig.scatter(X, np.sin(X), lc=100, label='sin')
fig.scatter(X, -np.sin(X)/2, lc=150, label='othersin')
fig.scatter(X, np.cos(X), lc=250, label='cos')
fig.plot(X, (X+2)**2 , lc=200, label='square')
print(fig.show(legend=True))