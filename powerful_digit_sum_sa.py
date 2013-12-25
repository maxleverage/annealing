#!/usr/bin/env python

import math as m
import numpy as np
import time

""" Digit Sum """

def digit_sum(number):
	s = 0
	while number:
		s += number % 10
		number /= 10
	return s 

""" Energy Function """

def compute_energy(base, exponent):
	return -(digit_sum(base ** exponent))

""" Simulated Annealing """

def simulated_annealing(start_temp, cooling_rate, max_base, max_exponent, max_iter):
	start_time = time.time()
	initial_base, initial_exponent = np.random.randint(1, max_base + 1), np.random.randint(1, max_exponent + 1)
	initial_energy = compute_energy(initial_base, initial_exponent)
	iter = 0
	while iter < max_iter:
		new_base, new_exponent = np.random.randint(1, max_base + 1), np.random.randint(1, max_exponent + 1)
		new_energy = compute_energy(new_base, new_exponent)
		if new_energy < initial_energy:
			initial_energy = new_energy
			start_temp *= (1 - cooling_rate)
		elif new_energy == initial_energy:
			start_temp *= (1 - cooling_rate / 5)
		elif new_energy > initial_energy:
			if np.exp((initial_energy - new_energy) / start_temp) > np.random.random():
				initial_energy = new_energy
				start_temp *= (1 - cooling_rate)
			else:
				start_temp *= (1 - cooling_rate / 5)
		iter += 1
	return -(initial_energy)

start_time = time.time()
result = []
counter = 0
while counter < 5:
	result.append(simulated_annealing(200, 0.03, 100, 100, 3000))
	counter += 1

finish_time = time.time() - start_time

print finish_time, max(result)