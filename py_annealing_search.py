#!/usr/bin/env python

import math as m
import random
import numpy as np 
import time

""" Triples search """
""" Search for integer p less than max_p which generates the longest set of Pythagorean triples """

def triples_seq_search(max_p):
	start = time.time()
	perimeter_range = range(2,max_p,2)
	optimal_counter = 0
	result = 0
	for p in perimeter_range:
		counter = 0
		for a in range(1,int(m.ceil(p/3))):
			if p * (p - 2 * a) % (2 * (p-a)) == 0:
				counter += 1
		if counter > optimal_counter:
			optimal_counter = counter
			result = p
	return result, time.time() - start

""" Compute energy of solution """

def compute_energy(perimeter):
	""" Takes solution index and computes the energy associated at that index """
	initial_energy = 0
	for a in range(1, int(m.ceil(float(perimeter)/3))):
		if perimeter * (perimeter - 2 * a) % (2 * (perimeter - a)) == 0:
			initial_energy -= 1
	return float(initial_energy)

""" Vectorised implementation of pythagorean triples counter. Wins for large values of perimeter """

def compute_energy_vec(perimeter):
	""" Vectorised implementation of computing the energy of a state """
	a_val = np.array(range(1,int(float(perimeter)/3)))
	result = perimeter * (perimeter - 2.0 * a_val) % (2.0 * (perimeter - a_val))
	return float(-len(np.where(result==0)[0]))

""" Annealing search """
print "Running simulated annealing"

def annealing_search(start_temp, cooling_rate, max_p, max_iter):
	start = time.time()
	perimeter_range = range(2, max_p, 2)
	initial_state = np.random.randint(0,len(perimeter_range))
	initial_energy = compute_energy_vec(perimeter_range[initial_state])
	iter = 0
	while iter < max_iter:
		new_state = np.random.randint(0, len(perimeter_range)) 	
		new_energy = compute_energy_vec(perimeter_range[new_state])
		if new_energy < initial_energy:
			initial_energy = new_energy
			initial_state = new_state
			start_temp *= 1 - cooling_rate
		elif new_energy == initial_energy:
			start_temp = start_temp * (1- cooling_rate/5)
		elif np.exp((initial_energy - new_energy)/start_temp) > np.random.random():
			initial_energy = new_energy
			initial_state = new_state
			start_temp *= 1 - cooling_rate
		else:
			start_temp = start_temp * (1 - cooling_rate/5)
		iter += 1
	return (initial_state+1)*2, time.time() - start

""" Raw Inputs """

start_temp = float(raw_input('Enter start temperature: '))
cooling_rate = float(raw_input('Enter cooling rate: '))
max_p = int(raw_input('Enter maximum perimeter: '))
max_iter = int(raw_input('Enter maximum iteration: '))
counter_limit = int(raw_input('Enter SA runs: '))

""" Annealing iterations """
counter = 0
while counter < counter_limit:
	print annealing_search(start_temp, cooling_rate, max_p, max_iter)
	counter += 1



