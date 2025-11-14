from control import feedback, step_response, forced_response, series

def closed_loop(regler, strecke):
    return feedback(series(regler.tf(), strecke.tf()), 1)

def simulate_step(system):
    return step_response(system)

def simulate_signal(system, t, u):
    return forced_response(system, t, u)

