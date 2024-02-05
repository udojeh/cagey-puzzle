# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    
    # determine a set of constraints to check
    cons = []
    if newVar is not None:
        cons = csp.get_cons_with_var(newVar)
    else:
        cons = csp.get_all_cons()
    # keeps track of (var, val) tuples that were pruned
    pruned = []
    for c in cons:
        for var in c.get_scope():
            # prune variables that do not satisfy constraints
            for val in var.cur_domain():
                if c.check_var_val(var, val):
                    pass
                else:
                    var.prune_value(val)
                    pruned.append((var, val))
            # check if dead end -- could not assign a value to variable
            if not var.cur_domain():
                return False, pruned

    return True, pruned

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    # initialize queue with constraints
    con_queue = []
    if newVar is None:
        con_queue = csp.get_all_cons()
    else:
        con_queue = csp.get_cons_with_var(newVar)

    pruned = []
    while con_queue:
        con = con_queue.pop(0)
        for var in con.get_scope():
            # prune variables that do not satisfy constraints
            for val in var.cur_domain():
                if con.check_var_val(var, val):
                    pass
                else:
                    var.prune_value(val)
                    pruned.append((var, val))
                    # add possibly impacted constraints back to queue
                    for neighbor_con in csp.get_cons_with_var(var):
                        if neighbor_con not in con_queue:
                            con_queue.append(neighbor_con)
            # check if dead end -- could not assign a value to variable
            if not var.cur_domain():
                return False, pruned
    
    return True, pruned