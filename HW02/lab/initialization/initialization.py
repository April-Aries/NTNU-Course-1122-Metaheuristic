import numpy as np
import random

def Rajendran(data, jobs, machine, populationSize):
    
    result = []
    sols = [i for i in range(jobs)]
    time = [sum(x) for x in zip(*data)]

    for num in range(populationSize):

        sol = [x for _,x in sorted(zip(time,sols), reverse = True)]

        # Initialize empty sequences for each machine
        machine_sequences = [[] for _ in range(machine)]
        
        # Initialize lists to keep track of processing times on each machine
        machine_processing_times = [0] * machine
        
        # Sort jobs based on the total processing time across all machines
        sorted_jobs = sol
        
        # Assign jobs to machines based on Rajendran's method
        for job in sorted_jobs:
            # Determine the machine with the minimum total processing time
            min_processing_time_machine = np.argmin(machine_processing_times)
            
            # Insert the job into the sequence of the selected machine
            machine_sequences[min_processing_time_machine].append(job)
            
            # Update the processing time for the selected machine
            machine_processing_times[min_processing_time_machine] += data[min_processing_time_machine][job]
        
        # Combine sequences for each machine to form the individual
        individual = []
        for k in machine_sequences:
            for r in k:
              individual.append(r)
        rand_seed = random.sample(range(0, jobs), 2)
        swap_ele = individual[rand_seed[0]]
        individual[rand_seed[0]] = individual[rand_seed[1]]
        individual[rand_seed[1]] = swap_ele
        
        result.append(individual)
       
    return result
    
def NEH(data, jobs, machine, populationSize):
    
    result = []
    sols = [i for i in range(jobs)]
    time = [sum(x) for x in zip(*data)]

    for num in range(populationSize):

        sorted_jobs = [x for _,x in sorted(zip(time,sols), reverse = True)]

        machine_sequences = [[] for _ in range(machine)]
        
        # Initialize an empty schedule
        schedule = np.zeros((jobs, machine))
        
        # Insert the jobs based on NEH heuristic
        for job_index in sorted_jobs:
            # Calculate the additional makespan when inserting the job on each machine
            additional_makespan = []
            for machine_index in range(machine):
                machine_sequence = machine_sequences[machine_index]
                current_makespan = 0
                if len(machine_sequence) > 0:
                    current_makespan = schedule[machine_sequence[-1]][machine_index]
                new_makespan = current_makespan + data[machine_index][job_index]
                additional_makespan.append(new_makespan)
            # Insert the job on the machine that minimizes the additional makespan
            min_makespan_machine = np.argmin(additional_makespan)
            machine_sequences[min_makespan_machine].append(job_index)
            # Update the schedule
            if len(machine_sequences[min_makespan_machine]) == 1:
                schedule[job_index][min_makespan_machine] = data[min_makespan_machine][job_index]
            else:
                schedule[job_index][min_makespan_machine] = schedule[machine_sequences[min_makespan_machine][-2]][min_makespan_machine] + data[min_makespan_machine][job_index]
        
        # Convert the list of machine sequences to the individual representation
        individual = []
        for k in machine_sequences:
          for r in k:
            individual.append(r)
        
        rand_seed = random.sample(range(0, jobs), 2)
        swap_ele = individual[rand_seed[0]]
        individual[rand_seed[0]] = individual[rand_seed[1]]
        individual[rand_seed[1]] = swap_ele
        
        result.append(individual)
       
    return result
    
def randomInit(data, jobs, machine, populationSize):
    sol = [ [] for i in range(populationSize) ]
    for i in range(populationSize):
        sol[i] = [j for j in range(jobs)]
        random.shuffle(sol[i])
    return sol