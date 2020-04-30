'''
UK scenarios
'''

import sciris as sc
import numpy as np
import covasim as cv

# Check version
cv.check_version('0.29.5')
cv.git_info('covasim_version.json')

do_plot = 1
do_save = 1
do_show = 0
verbose = 1
seed    = 1

version   = 'v1'
date      = '2020apr20'
folder    = f'results_{date}'
file_path = f'{folder}/phase_{version}' # Completed below
data_path = 'UK_Covid_19_cases_apr30.xlsx'
pop_path  = f'{file_path}.pop'
fig_path  = f'{file_path}.png'

start_day = sc.readdate('2020-01-21')
end_day   = sc.readdate('2021-05-01')
n_days    = (end_day -start_day).days

#ttq_date = sc.readdate('2020-06-01')
#ttq_day = (ttq_date - start_day).days


# Set the parameters
quar_eff = 0.0
quar_effs = {k:quar_eff for k in 'hwsc'}
total_pop = 66.65e6 # UK population size
pop_size = 100e3 # Actual simulated population
ratio = int(total_pop/pop_size)
pop_scale = ratio
pop_infected = 5000
pop_type = 'hybrid'
beta = 0.0068
#beta = 0.0068 to fit deaths until 27th April
#ttq_day = 134
#ttq_day = 20
cons = {'h':3.0, 's':20, 'w':20, 'c':20}

pars = sc.objdict(
    pop_size     = pop_size,
    pop_infected = pop_infected//pop_scale,
    pop_scale    = pop_scale,
    pop_type     = pop_type,
    start_day    = start_day,
    n_days       = n_days,
    asymp_factor = 0.6,
    beta         = beta,
    contacts     = cons,
)

# Create the simulation
sim = cv.Sim(pars=pars, datafile=data_path, popfile=pop_path)

# Interventions

#opening and closing schools intervention changing the h,s,w,c values and ti_start to 
#account for changes in Table 1 in the ms
interventions = []

ti_start = '2020-06-01'
ti_day   = (sc.readdate(ti_start)-start_day).days
beta_days      = ['2020-02-14', '2020-03-16', '2020-03-23', '2020-03-30', ti_start]
beta_days      = [(sc.readdate(day)-start_day).days for day in beta_days]
h_beta_changes = [1.00, 1.00, 1.29, 1.29, 1.00]
s_beta_changes = [1.00, 0.90, 0.10, 0.10, 0.90]
w_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.80]
c_beta_changes = [0.90, 0.80, 0.20, 0.20, 0.80]

h_beta = cv.change_beta(days=beta_days, changes=h_beta_changes, layers='h')
s_beta = cv.change_beta(days=beta_days, changes=s_beta_changes, layers='s')
w_beta = cv.change_beta(days=beta_days, changes=w_beta_changes, layers='w')
c_beta = cv.change_beta(days=beta_days, changes=c_beta_changes, layers='c')

#these two lines are switched on to run the intervention
interventions = [h_beta, w_beta, s_beta, c_beta]
sim.update_pars(interventions=interventions)

#Testing interventions

#this is not run but I start testing strategies from line 108
#sympt_test = 40.0
#daily_tests = sim.data['new_tests']//ratio
#symp_p  = 0.20
#asymp_p = 0.005
#test_t  = 1
#trace_p = {'h':1.0, 's':1.0, 'w':1.0, 'c':2.0} 
#trace_t = {'h':1, 's':1, 'w':1, 'c':1}
#trace_d = {'h':0, 's':1, 'w':1, 'c':2
#interventions += [
#     cv.test_num(daily_tests=daily_tests, sympt_test=sympt_test),
#     cv.test_prob(start_day=ti_day, symp_prob=symp_p, asymp_prob=asymp_p, test_delay=trace_d),
#     cv.contact_tracing(start_day=ti_day, trace_probs=trace_p, trace_time=trace_t),
#]


# testing to drive suppression
#I change parameters s_prob=% of sympomatic that are tested only as part of TTI strategies
s_prob = 0.8 
a_prob = 0.005
q_prob = 0.0
t_delay = 1.0
extra_tests= cv.test_prob(symp_prob=s_prob,
                            asymp_prob=a_prob, symp_quar_prob=q_prob, asymp_quar_prob=q_prob,
                            start_day=ti_day, test_delay=t_delay)
#immediate isolation
#on day ti_day people with contacts and diagnosed are not likely to transmit a sare immediately isolated
d_eff = 0.0
isolation = cv.dynamic_pars({'diag_factor': {'days': ti_day, 'vals': d_eff}})


#the next line 122 is to model the scenarios of reduced probability of transmission for the 
#phased school openings so that beta is reduced by 10% 
#from ti_day which is when sschools reopen fr a week
reduced transmision = cv.dynamic_pars({'beta':{'days':[t_day, ti_day+7], 'vals':[0.0068, 0.0056]}})

# immediate home quarantine
t_eff = 1.0
t_time = 0
ttq_day = ti_day
t_probs = {k:t_eff for k in 'hwsc'}
t_times = {k:t_time for k in 'hwsc'}
ttq = cv.contact_tracing(trace_probs=t_probs, trace_time=t_times, start_day=ti_day)
interventions += [
     h_beta, w_beta, s_beta, c_beta,     
     cv.test_prob(symp_prob=s_prob,
                            asymp_prob=a_prob, symp_quar_prob=q_prob, asymp_quar_prob=q_prob,
                            start_day=ti_day, test_delay=t_delay),
     cv.dynamic_pars({'beta': {'days': [ti_day, ti_day+7], 'vals': [0.0068,0.00612]}}),
     cv.dynamic_pars({'diag_factor': {'days': ti_day, 'vals': d_eff}}),
     cv.contact_tracing(trace_probs=t_probs, trace_time=t_times, start_day=ti_day)
    ]
#the next lines (137-138) are commented out when I run schools opening only without TTI
# and not when I run schools opening+TTI
pars['interventions'] = [extra_tests, isolation, ttq]
sim.update_pars(interventions=interventions)


# Changing kids' transmissability
#I set True and change the number to alter kids transmissibility
sim.initialize() # Create the population
reduce_kids = True #set tgis to True to change the transmissibility numbers below
if reduce_kids:
    print('Reducing transmission among kids')
    children = sim.people.age<18 # Find people who are children
    child_inds = sc.findinds(children) # Turn the boolean array into a list of indices
    for lkey in sim.people.layer_keys(): # Loop over each layer
        child_contacts = np.isin(sim.people.contacts[lkey]['p1'], child_inds) # Find contacts where the source is a child
        child_contact_inds = sc.findinds(child_contacts) # Convert to indices
        sim.people.contacts[lkey]['beta'][child_contact_inds] = 1.00# MODIFY TRANSMISSION
        # sim.people.contacts[lkey]['beta'][:] = 0.0 # MODIFY TRANSMISSION
  
#plotting R0 for each scenario: 
#PLEASE ADD to plot the R0 distribution



if __name__ == '__main__':
    sim.run()

    if do_save:
        sim.save(f'{file_path}.sim', keep_people=True)

    if do_plot:
        fig = sim.plot(do_save=do_save, do_show=do_show, fig_path=fig_path, interval=60)