from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    
    goal_tree = OR(hypothesis)
    
    for rule in rules:
        consequence_pattern = rule.consequent()[0]
        bindings = match(consequence_pattern,hypothesis)
        
        if bindings == None:
            #print 'no rule was found'
            continue
        else:
            
            if isinstance(rule.antecedent(),AND):
                subtree = AND()
            else:
                subtree = OR()
            
            if isinstance(rule.antecedent(),(OR,AND)):
                for antecedent in rule.antecedent():
                    new_hypo = populate(antecedent,bindings)
                    subtree.append(backchain_to_goal_tree(rules,new_hypo))
                    goal_tree.append(subtree)
            else:
                new_hypo = populate(rule.antecedent(),bindings)
                subtree.append(backchain_to_goal_tree(rules,new_hypo))
                goal_tree.append(subtree)
                        
    return simplify(goal_tree) 
# Here's an example of running the backward chainer - uncomment
# it to see it work:

