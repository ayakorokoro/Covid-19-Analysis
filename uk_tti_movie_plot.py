import numpy as np
import pylab   as pl
import sciris  as sc
import covasim as cv
import datetime as dt
import matplotlib.ticker as ticker


fn = 'uk-tti-movie.msim'
nsims   = 201
seeds   = 10
plot_diagnostic = False
plot_movie = True
n_total = nsims*seeds

T = sc.tic()

msim = cv.load(fn)
s0 = msim.sims[0]

results = np.zeros((nsims, seeds, s0.npts))
count = -1
for i in range(nsims):
    for j in range(seeds):
        count += 1
        vals = msim.sims[count].results['new_infections'].values
        results[i,j,:] = vals

print('Plotting...')
if plot_diagnostic:
    fig = pl.figure(figsize=(26,18))
    for i in range(nsims):
        pl.subplot(nsims//2, 2, i+1)
        data = results[i,:,:]
        for j in range(seeds):
            pl.plot(s0.tvec, results[i,j,:])

xlims = [s0.tvec[0], s0.tvec[-1]]
ylims = [0, results.max()]

dur = 10 # Duration of symptoms
mintest = 0.0
maxtest = 0.2
test_vals = np.linspace(mintest, maxtest, nsims) # TODO: remove duplication
test_pct = (1-(1-test_vals)**dur)*100

# Trim indices
low_inds = sc.findinds(test_pct<=4)
med_inds = sc.findinds(np.logical_and(test_pct>4, test_pct<=20))
high_inds = sc.findinds(test_pct>20)
inds = low_inds[::1].tolist() + med_inds[::2].tolist() + high_inds[::10].tolist()

# Actually plot
if plot_movie:
    fig = pl.figure(figsize=(10,8)) # Create a new figure
    frames = [] # Initialize the frames
    count = 0
    for i in range(nsims): # Loop over the frames
        print(f'Plotting {i}, testing = {test_pct[i]}%...')
        if i not in inds:
            print('  ...skipping')
        else:
            count += 1
            handles = []
            l2 = 'Mean of individual runs' if i==0 else None
            plt = pl.plot(s0.tvec, results[i,:,:].mean(axis=0), lw=2, c='k', label=l2, zorder=10)
            handles.append(plt[0])
            for j in range(seeds):
                l1 = 'Individual runs' if i==0 and j==0 else None
                plt = pl.plot(s0.tvec, results[i,j,:], alpha=0.3, label=l1)
                handles.append(plt[0]) # 0 since returns a list...why
            pl.xlim(xlims) # Set x-axis limits
            pl.ylim(ylims) # Set y-axis limits
            kwargs = {'transform':pl.gca().transAxes, 'horizontalalignment':'center'} # Set the "title" properties
            title = pl.text(0.5, 1.05, f'Symptomatic testing rate after August 1st: {test_pct[i]:0.1f}%', **kwargs) # Unfortunately pl.title() can't be dynamically updated
            handles.append(title)
            pl.xlabel('Date')
            pl.ylabel('New infections')
            pl.legend()
            sc.commaticks()

            # Set the x-axis intervals
            @ticker.FuncFormatter
            def date_formatter(x, pos):
                return (s0['start_day'] + dt.timedelta(days=int(x))).strftime('%Y-%b')
            interval = 91.5
            ax = pl.gca()
            ax.set_xticks(pl.arange(xlims[0], xlims[1], interval))
            ax.xaxis.set_major_formatter(date_formatter)

            frames.append(handles) # Store updated artists
    print(f'Saving {count} frames...')
    sc.savemovie(frames, 'uk_tti_movie.mp4', fps=3, quality='high') # Save movie as a high-quality mp4



print('Done.')
sc.toc(T)