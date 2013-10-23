#!/usr/bin/env python

import math as m
import random
import numpy as np 
import time

""" Triples search """
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

""" Simulated Annealing """
""" Acceptance probability function for simulated annealing """

def acceptance_probability(temperature, init_energy, new_energy):
	""" If neighboring energy level is lower, we accept it unconditionally else we compute the transition probability as a function of the initial energy and current temperature"""
	temperature = float(temperature)
	init_energy = float(init_energy)
	new_energy = float(new_energy)
	if new_energy < init_energy:
		return 1
	else:
		return m.exp((init_energy - new_energy) / temperature)

""" Compute energy of solution """

def compute_energy(perimeter):
	""" Takes solution index and computes the energy associated at that index """
	initial_energy = 0
	for a in range(1, int(m.ceil(perimeter/3))):
		if perimeter * (perimeter - 2 * a) % (2 * (perimeter - a)) == 0:
			initial_energy -= 1
	return initial_energy

""" Simulated annealing search for pythagorean triples """

def annealing_search(start_temp, end_temp, cooling_rate, max_p, m_iter):
	start = time.time()
	temperature = start_temp
	""" Search space energy """
	perimeter_range = range(2, max_p, 2)
	initial_solution = random.randint(0, len(perimeter_range)-1)
	initial_energy = compute_energy(perimeter_range[initial_solution])
	best_solution = [initial_solution]
	while temperature > end_temp:
		m_counter = 0
		while m_counter < m_iter:
			new_solution = random.randint(0, len(perimeter_range)-1) 
			new_energy = compute_energy(perimeter_range[new_solution])
			if new_energy < initial_energy:
				initial_energy = new_energy
				initial_solution = new_solution
			elif acceptance_probability(temperature, initial_energy, new_energy) > random.random():
				initial_energy = new_energy
				initial_solution = new_solution
			m_counter += 1		
		temperature *= 1 - cooling_rate
		return perimeter_range[initial_solution]

