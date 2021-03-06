'''
UK scenarios
'''

import sciris as sc
import numpy as np
import covasim as cv
import pylab as pl

# Check version
cv.check_version('1.3.3', die=True)
cv.git_info('covasim_version.json')

do_plot = 1
do_save = 1
do_show = 1
verbose = 1
seed    = 1

version   = 'v1'
date      = '2020may26'
folder    = f'results_FINAL_{date}'
file_path = f'{folder}/phase_{version}' # Completed below
data_path = 'UK_Covid_cases_may21.xlsx'
pop_path  = f'{file_path}.pop'
fig_path  = f'{file_path}.png'
#ig_paths = [f'results/testing_scen_{i}.png' for i in range(3)]


start_day = '2020-01-21'
end_day   = '2021-05-31'

# Set the parameters
#quar_eff = 0.8
#quar_effs = {k:quar_eff for k in 'hwsc'}
total_pop = 67.86e6 # UK population size
pop_size = 100e3 # Actual simulated population
ratio = int(total_pop/pop_size)
pop_scale = ratio
pop_type = 'hybrid'
#100% transmissibility of kids also ps=0.0135 for May and June
pop_infected = 4000
#beta=0.00485
beta = 0.00825
cons = {'h':3.0, 's':20, 'w':20, 'c':20}
#50% transmissibility of kids also ps=0.1 for May and June
#pop_infected = 5000
#beta = 0.00525
#cons = {'h':3.0, 's':20, 'w':20, 'c':20}

pars = sc.objdict(
    pop_size     = pop_size,
    pop_infected = pop_infected,
    pop_scale    = pop_scale,
    pop_type     = pop_type,
    start_day    = start_day,
    end_day      = end_day,
    asymp_factor = 1.0,
    beta         = beta,
    contacts     = cons,
    rescale      = True,
)

# Create the baseline simulation
sim = cv.Sim(pars=pars, datafile=data_path, popfile=pop_path, location='uk')


# Interventions

#opening and closing schools intervention changing the h,s,w,c values and ti_start to
#account for changes in Table 1 in the ms
#baseline scenario

# Create the baseline simulation

#interventions = []
#intervention of some testing (tc) starts on 16th March and we run until 1st April when it increases
tc_day = sim.day('2020-03-16')
#intervention of some testing (te) starts on 1st April and we run until 1st May when it increases
te_day = sim.day('2020-04-01')
#intervention of increased testing (tt) starts on 1st May
tt_day = sim.day('2020-05-01')
#intervention of tracing and enhanced testing (tti) starts on 1st June
tti_day= sim.day('2020-06-01')
#schools interventions (ti) start
ti_day   = sim.day('2021-04-17')
#change parameters here for difefrent schools opening strategies with society opening
#June opening with society opening
beta_days      = ['2020-02-14', '2020-03-16', '2020-03-23', '2020-04-30', '2020-05-15', '2020-06-08', '2020-07-01', '2020-07-22', '2020-09-02', '2020-10-28', '2020-11-01', '2020-12-23', '2021-01-03', '2021-02-17', '2021-02-21', '2021-04-06', ti_day]
h_beta_changes = [1.00, 1.00, 1.29, 1.29, 1.29, 1.00, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00]
s_beta_changes = [1.00, 0.90, 0.02, 0.02, 0.02, 0.80, 0.80, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 1.00]
w_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.70, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70]
c_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.80, 0.80, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90]

#September opening with society opening
#h_beta_changes = [1.00, 1.00, 1.29, 1.29, 1.29, 1.29, 1.29, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00]
#s_beta_changes = [1.00, 0.90, 0.02, 0.02, 0.02, 0.02, 0.02, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 1.00]
#w_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.20, 0.30, 0.30, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70]
#c_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.20, 0.30, 0.30, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90]
#
#Phased opening with society opening
#h_beta_changes = [1.00, 1.00, 1.29, 1.29, 1.29, 1.00, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00]
#s_beta_changes = [1.00, 0.90, 0.02, 0.02, 0.02, 0.25, 0.70, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 1.00]
#w_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.40, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70]
#c_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.40, 0.70, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90]

#Phased-delayed opening with society opening
#h_beta_changes = [1.00, 1.00, 1.29, 1.29, 1.29, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00, 1.29, 1.00]
#s_beta_changes = [1.00, 0.90, 0.02, 0.02, 0.02, 0.02, 0.70, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 0.90, 0.00, 1.00]
#w_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.20, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70, 0.50, 0.70]
#c_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.20, 0.20, 0.70, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90, 0.50, 0.90]


h_beta = cv.change_beta(days=beta_days, changes=h_beta_changes, layers='h')
s_beta = cv.change_beta(days=beta_days, changes=s_beta_changes, layers='s')
w_beta = cv.change_beta(days=beta_days, changes=w_beta_changes, layers='w')
c_beta = cv.change_beta(days=beta_days, changes=c_beta_changes, layers='c')

#next two lines to save the intervention
interventions = [h_beta, w_beta, s_beta, c_beta]
sim.update_pars(interventions=interventions)

#Testing and Isolation interventions until 1st June
#s_prob=% of sympomatic that are tested only as part of TI strategies; we fit s_prob_may to data
s_prob_march = 0.007
s_prob_april = 0.009
s_prob_may = 0.0135
a_prob = 0.0
#a_prob_june =0.0135
q_prob = 0.0
t_delay = 1.0

iso_vals = [{k:0.1 for k in 'hswc'}]

interventions += [
    
     cv.test_prob(symp_prob=s_prob_march, asymp_prob=0.00030, symp_quar_prob=q_prob, asymp_quar_prob=q_prob, start_day=tc_day, end_day=te_day-1, test_delay=t_delay),
     cv.test_prob(symp_prob=s_prob_april, asymp_prob=0.00050, symp_quar_prob=q_prob, asymp_quar_prob=q_prob, start_day=te_day, end_day=tt_day-1, test_delay=t_delay),
     cv.test_prob(symp_prob=s_prob_may,   asymp_prob=0.00075, symp_quar_prob=q_prob, asymp_quar_prob=q_prob, start_day=tt_day, end_day=tti_day-1, test_delay=t_delay),
     cv.dynamic_pars({'iso_factor': {'days': te_day, 'vals': iso_vals}}),
   ]

sim.update_pars(interventions=interventions)
for intervention in sim['interventions']:
    intervention.do_plot = False


# Tracing and enhanced testing strategy of symptimatics from 1st June
#testing in June
s_prob_june_2 = 0.0135
a_prob_june_2 = 0.0007
q_prob_june = 0.0
t_delay = 1.0

#tracing in june
t_eff_june = 0.0
t_probs_june = {k:t_eff_june for k in 'hwsc'}
trace_d = {'h':0, 's':1, 'w':1, 'c':2}
ttq_june_2 = cv.contact_tracing(trace_probs=t_probs_june, trace_time=trace_d, start_day=tti_day)

#testing and isolation intervention
interventions += [
     cv.test_prob(symp_prob=s_prob_june_2,
                         asymp_prob=0.0007, symp_quar_prob=q_prob_june, asymp_quar_prob=q_prob_june,
                           start_day=tti_day, test_delay=t_delay),
     cv.contact_tracing(trace_probs=t_probs_june, trace_time=trace_d, start_day=tti_day),
     cv.dynamic_pars({'iso_factor': {'days': tti_day, 'vals': iso_vals}})
  ]

sim.update_pars(interventions=interventions)
for intervention in sim['interventions']:
    intervention.do_plot = False


# Changing kids' transmissability
sim.initialize() # Create the population
reduce_kids = True #set tgis to True to change the transmissibility numbers below
if reduce_kids:
    print('Reducing transmission among kids')
    children = sim.people.age<18 # Find people who are children
    child_inds = sc.findinds(children) # Turn the boolean array into a list of indices
    for lkey in sim.people.layer_keys(): # Loop over each layer
        child_contacts = np.isin(sim.people.contacts[lkey]['p1'], child_inds) # Find contacts where the source is a child
        child_contact_inds = sc.findinds(child_contacts) # Convert to indices
        sim.people.contacts[lkey]['beta'][child_contact_inds] = 1.0 # MODIFY TRANSMISSION
        #sim.people.contacts[lkey]['beta'][:] = 0.0 # MODIFY TRANSMISSION


if __name__ == '__main__':

    NOISE = 0.00

    msim = cv.MultiSim(base_sim=sim) # Create using your existing sim as the base
    msim.run(reseed=True, noise=NOISE, n_runs=8, keep_people=True) # Run with uncertainty

    # Recalculate R_eff with a larger window
    for sim in msim.sims:
        sim.compute_r_eff(smoothing=10)

    msim.reduce() # "Reduce" the sims into the statistical representation

    results = msim.results # Use this instead of sim.results
    
    #to produce mean cumulative infections and deaths for barchart figure
    #msim.results['cum_deaths'].values.mean()
    #msim.results['cum_infectious'].values.mean()


    # Save the key figures

    plot_customizations = dict(
        interval   = 90, # Number of days between tick marks
        dateformat = '%Y/%m', # Date format for ticks
        fig_args   = {'figsize':(14,8)}, # Size of the figure (x and y)
        axis_args  = {'left':0.15}, # Space on left side of plot
        )

    msim.plot_result('r_eff', **plot_customizations)
    # pl.xlim([10, 496]) # Trim off the beginning and end which are noisy
    pl.axhline(1.0, linestyle='--', c=[0.8,0.4,0.4], alpha=0.8, lw=4) # Add a line for the R_eff = 1 cutoff
    pl.title('')
    pl.savefig('R_eff.png')

    msim.plot_result('cum_deaths', **plot_customizations)
    pl.title('')
    pl.savefig('Deaths.png')

    msim.plot_result('new_infections', **plot_customizations)
    pl.title('')
    pl.savefig('Infections.png')

    msim.plot_result('cum_diagnoses', **plot_customizations)
    pl.title('')
    pl.savefig('Diagnoses.png')

    msim.plot_result('new_tests', **plot_customizations)
    pl.savefig('Test.png')
    


    #if do_plot:
     #   to_plot = cv.get_sim_plots()
      #  to_plot['Health outcomes'].remove('cum_severe')
       # fig = msim.plot(to_plot=to_plot, do_save=do_save, do_show=do_show, fig_path=fig_path, interval=60)


    # if do_save:
    #     msim.save(f'{file_path}.sim', keep_people=True)

    # if do_plot:
    #     for reskey in ['new_infections', 'cum_deaths']:
    #         fig = msim.plot(to_plot=[reskey], fig_args={'figsize':(12,7)}, do_save=do_save, fig_path=fig_path, interval=60)
    #         pl.title('')

    #to_plot = cv.get_sim_plots()
    #to_plot['Health outcomes'].remove('cum_severe')
    #sim.plot(to_plot=to_plot)

   # if do_plot:
        #to_plot = cv.get_sim_plots()
        #to_plot['Health outcomes'].remove('cum_severe')
        #sim.plot(to_plot=to_plot)
    #    fig = msim.plot(to_plot=to_plot,do_save=do_save, do_show=do_show, fig_path=fig_path, interval=60)
