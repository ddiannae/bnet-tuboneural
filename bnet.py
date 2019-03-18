#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import PyBoolNet


def createGraphs(primes):
	PyBoolNet.InteractionGraphs.create_image(primes, "graph.pdf")
	igraph = PyBoolNet.InteractionGraphs.primes2igraph(primes)

	for x in igraph.nodes():
		if "GF" in x:
			igraph.node[x]["shape"] = "square"
			igraph.node[x]["fillcolor"] = "lightblue"

	PyBoolNet.InteractionGraphs.add_style_inputs(igraph)
	PyBoolNet.InteractionGraphs.add_style_constants(igraph)
	PyBoolNet.InteractionGraphs.igraph2image(igraph, "interGraph.pdf")

	state = PyBoolNet.StateTransitionGraphs.random_state(primes)
	local_igraph = PyBoolNet.InteractionGraphs.local_igraph_of_state(primes, state)
	PyBoolNet.InteractionGraphs.add_style_interactionsigns(local_igraph)
	PyBoolNet.InteractionGraphs.igraph2image(local_igraph, "localInterGraph.pdf")

def getAttractors(primes):
	stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
	steady, cyclic = PyBoolNet.Attractors.compute_attractors_tarjan(stg)
	print(steady)
	print(cyclic)

	# random walk attractor detection
	state = PyBoolNet.Attractors.find_attractor_state_by_randomwalk_and_ctl(primes, "asynchronous")
	print(state)

	# model checking based attractor detection
	attrs = PyBoolNet.Attractors.compute_json(primes, "asynchronous", FnameJson="attrs.json")
	print(attrs["is_complete"])
	for x in attrs["attractors"]:
		print(x["is_steady"])
		print(x["state"]["str"])


def enumerateInputs(primes):
	for x in PyBoolNet.PrimeImplicants.input_combinations(primes):
		print(x)

if __name__=="__main__":

	# basic drawing

	primes = PyBoolNet.FileExchange.bnet2primes("reglas.bnet")
	createGraphs(primes)

