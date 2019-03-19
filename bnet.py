#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import PyBoolNet
import matplotlib.pyplot as plt
import numpy as np


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
    # stg = PyBoolNet.StateTransitionGraphs.primes2stg(primes, "asynchronous")
    # steady, cyclic = PyBoolNet.Attractors.compute_attractors_tarjan(stg)
    # print(steady)
    # print(cyclic)

    # # random walk attractor detection
    # state = PyBoolNet.Attractors.find_attractor_state_by_randomwalk_and_ctl(primes, "asynchronous")
    # print(state)

    # model checking based attractor detection
    attrs = PyBoolNet.Attractors.compute_json(primes, "asynchronous", FnameJson="attrs.json")
    print(attrs["is_complete"])
    for x in attrs["attractors"]:
        print(x["is_steady"])
        print(x["state"]["str"])

def createAttractorsHeatmap(attractorsFile):
    with open(attractorsFile, 'r') as f:
        attrs = json.load(f)
    A = [[int(a) for a in list(x["state"]["str"])] for x in attrs["attractors"]]
    names = sorted([x for x in attrs["primes"]])
    print(names)

    fig, ax = plt.subplots()
    im = plt.imshow(A, extent=[0,len(names),0,1], aspect=len(names))
    #ax.tick_params(top=True, bottom=False,
    #               labeltop=True, labelbottom=False)

    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(range(len(names)), minor = False)
    ax.set_xticks(np.arange(0.5, len(names)+0.5, 1), minor = True)
    ax.set_xticklabels(names, rotation = 90, fontsize = 10, minor = True )
    plt.setp(ax.get_xmajorticklabels(), visible=False)
    plt.yticks([])
    ax.grid(which="major", color="w", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    fig.tight_layout()
    plt.show()

def enumerateInputs(primes):
    for x in PyBoolNet.PrimeImplicants.input_combinations(primes):
        print(x)

if __name__=="__main__":

    primes = PyBoolNet.FileExchange.bnet2primes("reglas.bnet")
    createAttractorsHeatmap("attrs-synchronous.json")
