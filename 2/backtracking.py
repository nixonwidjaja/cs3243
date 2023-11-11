'''
This is the code template for Project 2.1.
You may remove or add any additional classes or methods you require.
'''
from __future__ import annotations
from typing import List, Dict, Set, Tuple, Any

class Assignment:
    pass

first = {}
second = {}
chosen = set()

def evaluate(state: dict, constraints: dict) -> bool:
    for i in constraints:
        f = constraints[i]
        a, b = i
        if not f(state[a], state[b]):
            return False
    return True

def prune(state: dict, constraints: dict, i, keys, domains: dict):
    changed = {}
    for j in range(i + 1, len(keys)):
        a, b = keys[i], keys[j]
        if (a, b) in constraints:
            new_domain = []
            f = constraints[(a, b)]
            changed[b] = domains[b]
            for k in domains[b]:
                if f(state[a], k):
                    new_domain.append(k)
            domains[b] = new_domain
        if (b, a) in constraints:
            new_domain = []
            f = constraints[(b, a)]
            changed[b] = domains[b]
            for k in domains[b]:
                if f(k, state[a]):
                    new_domain.append(k)
            domains[b] = new_domain
    return changed

def MRV(domains: dict, keys: list, i):
    unexplored = keys[i:]
    unexplored.sort(key=lambda x: len(domains[x]))
    keys = keys[:i] + unexplored
    return keys

def LCV(domains: dict, key):
    def count_constraint(val):
        count = 0
        if key in first:
            for pair in first[key]:
                if pair in chosen:
                    continue
                f = first[key][pair]
                for other in domains[pair]:
                    if f(val, other):
                        count += 1
        if key in second:
            for pair in second[key]:
                if pair in chosen:
                    continue
                f = second[key][pair]
                for other in domains[pair]:
                    if f(other, val):
                        count += 1
        return count
    values = list(domains[key])
    values.sort(key=lambda x: count_constraint(x), reverse=True)
    return values

def forward_checking(i, domains: dict, keys: list): # true if continue
    for j in range(i, len(keys)):
        if len(domains[keys[j]]) == 0:
            return True
    return False

def revert(domains: dict, changed: dict):
    for i in changed:
        domains[i] = changed[i]

def solve_CSP(d : Dict[str : Any]) -> Dict[str : int]:
    domains: dict = d['domains']
    for i in domains:
        domains[i] = list(set(domains[i]))
    constraints = d['constraints']
    for a, b in constraints:
        if a not in first:
            first[a] = {}
        first[a][b] = constraints[(a, b)]
    for a, b in constraints:
        if b not in second:
            second[b] = {}
        second[b][a] = constraints[(a, b)]
    n = len(domains)
    keys = list(domains.keys())
    state = {}

    def dfs(i, domains: dict, keys: list):
        if i == n:
            return True
        if forward_checking(i, domains, keys):
            return False
        keys = MRV(domains, keys, i)
        key = keys[i]
        chosen.add(key)
        for j in LCV(domains, key):
            state[key] = j
            changed = prune(state, constraints, i, keys, domains)
            if dfs(i + 1, domains, keys):
                return True
            revert(domains, changed)
        return False
    
    res = dfs(0, domains, keys)
    if res:
        return state
    else:
        return None
