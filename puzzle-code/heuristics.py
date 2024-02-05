# =============================
# Student Names: Hunter Coker, Brandon Liang, Udo Ojeh
# Group ID: Group 22
# Date: February 2nd, 2024
# =============================
# CISC 352 - W23
# heuristics.py
# desc: Contains 2 different heuristic implementations that return variables.
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''

    vars = csp.get_all_vars()
    max = (None, -1)
    for var in vars:
        var_degree = 0
        constraints = csp.get_cons_with_var(var)
        if (not constraints) and (not var.is_assigned()):
            var_degree += 1
        else:
            for c in constraints:
                var_degree += c.get_n_unasgn()
        if var_degree > max[1]:
            max = (var, var_degree)

    return max[0]

def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''

    vars = csp.get_all_vars()
    min = (vars[0], vars[0].cur_domain_size())
    for var in vars[1:]:
        var_domain_size = var.cur_domain_size()
        if var_domain_size < min[1]:
            min = (var, var_domain_size)

    return min[0]
