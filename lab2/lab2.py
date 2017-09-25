# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    
    toExplore = list(start)
    explored = set()
    explorededges = list()
    goalFound = start == goal
    
    if (goalFound):
        return start
    
    while len(toExplore) > 0 and not goalFound:
        
        exploring = toExplore[0]
        toExplore.remove(exploring)
        explored.add(exploring)
        
        for node in graph.get_connected_nodes(exploring):
            
            if node == goal:
                goalFound = True
                explorededges.append([exploring,node])        
                break
            
            elif not (node in explored or node in toExplore):
                toExplore.append(node)
                explorededges.append([exploring,node])        
            else:
                continue
            
    #backtracking the path
    endedge = explorededges.pop()
    preNode = endedge[0]
    path = [endedge[0],endedge[1]]
       
    while len(explorededges)>0:
        
        edge = explorededges.pop()
        
        if edge[1] == preNode:
            path = [edge[0]]+ path
            preNode = edge[0]
    
    return path
            
## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    
    pathStack = list()
    explored = set()
    goalFound = start == goal
    
    if goalFound:
        return start
    
    pathStack.append(start)
    
    while len(pathStack) > 0:       
        
        currentNode = pathStack[len(pathStack)-1]
        
        if len(graph.get_connected_nodes(currentNode)) > 0:
            
            counter = 0
            
            for node in graph.get_connected_nodes(currentNode):
                            
                counter += 1
                
                if node == goal:
                    pathStack.append(node)
                    return pathStack
                    
                elif node not in pathStack and node not in explored:
                    pathStack.append(node)                  
                    break
                
                else:
                    
                    if counter == len(graph.get_connected_nodes(currentNode)):
                        explored.add(pathStack.pop())
                        
                    else: 
                        continue
        
        else:
            explored.add(pathStack.pop())
            
    return pathStack


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    
    pathStack = list()
    explored = set()
    goalFound = start == goal
    
    if goalFound:
        return start
    
    pathStack.append(start)
    
    while len(pathStack) > 0:       
        
        currentNode = pathStack[len(pathStack)-1]
        
        if len(graph.get_connected_nodes(currentNode)) > 0:
            
            heurList = list()
            #get heuristic value and sort it
            for node in graph.get_connected_nodes(currentNode):
                heurList.append(graph.get_heuristic(node, goal))
           
            heurList.sort()
            heurList.reverse()
            #find the lowest heuris node
            nodeFound = False
            while len(heurList)>0 and not nodeFound :
                
                target_heur = heurList.pop()
                for node in graph.get_connected_nodes(currentNode):
                    
                    targetFound = target_heur == graph.get_heuristic(node, goal)
                    not_visited = node not in pathStack and node not in explored
                    
                    if targetFound and not_visited:
                        pathStack.append(node)  
                        
                        if node == goal:    
                            return pathStack
                    
                        nodeFound = True
                        break
                        
            if not nodeFound:
                explored.add(pathStack.pop())
                
        else:
            explored.add(pathStack.pop())
            
    return pathStack 

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    
    explored =set()
    visitedEd = list()
    curL = dict()
    chvList = list()
    nhvList = list()
    nextL = dict()
    combL = set()
    goalFound = start == goal
    
    if goalFound:
        return start
    
    curL[graph.get_heuristic(start, goal)] = [start]
    chvList.append(graph.get_heuristic(start, goal))
    
    while not goalFound and len(chvList)>0:
        
        for hv in chvList:
            
            for node in curL[hv]:
                
                explored.add(node)
                combL.add(node)
                
                for neib in graph.get_connected_nodes(node):
                    
                    if neib == goal:
                        edge = [node,neib]
                        visitedEd.append(edge)
                        goalFound = True
                        break
                    
                    elif neib not in combL:
                        combL.add(neib)
                        edge = [node,neib]
                        visitedEd.append(edge)
                        
                        if graph.get_heuristic(neib, goal) not in nhvList:
                            nhvList.append(graph.get_heuristic(neib, goal))
                            nextL[graph.get_heuristic(neib, goal)] = list([neib])
                        
                        else:
                            nextL[graph.get_heuristic(neib, goal)] += [neib]
        
                    else:
                        continue
                
                if goalFound:
                    break
                
            if goalFound:
                break
                
        entered = 0
        nhvList.sort()
        nhvList.reverse()
        chvList = list()
        curL = dict()
        combL = set(explored)
        
        while entered < beam_width and len(nhvList) > 0 :
            
            hv = nhvList.pop()
            
            if hv not in chvList:
                chvList.append(hv)
                curL[hv]= list()
                
            for newNode in nextL[hv]:
                curL[hv] += [newNode]
                combL.add(newNode)
                entered += 1
                    
                if entered >= beam_width:
                    break     
                 
        nhvList = list()
        nextL = dict()
            
    #backtracking the path
    endedge = visitedEd.pop()
    preNode = endedge[0]
    path = [endedge[0],endedge[1]]
          
    while len(visitedEd)>0:
                
        edge = visitedEd.pop()
                
        if edge[1] == preNode:
            path = [edge[0]]+ path
            preNode = edge[0]
  
    if goalFound:
        return path
    
    else:
        return []
    

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    
    sumLen = 0 
    
    if str(type(node_names)) == "<type 'NoneType'>":
        return 0
    
    elif len(node_names) <= 1:
        return 0
    
    else:
        
        for i in range(1,len(node_names)):
            edge = graph.get_edge(node_names[i-1],node_names[i])
            sumLen += edge.length
    
    return sumLen

def branch_and_bound(graph, start, goal):
    
    pathList = list([[start]])
    pdList = list([path_length(graph,[start])])
    endNodes = dict()
    endNodes[path_length(graph,[start])] = list([start])
    goalFound = start==goal
    temp_win_path = list()
    min_goal_len = -10
    
    if goalFound:
        return start
    
    while not goalFound and len(pdList)>0:
        
        pdList.sort()
        pdList.reverse()
        pl = pdList.pop()
        
        for toex in endNodes[pl]:
        
            pathToExtend = find_path(pathList,pl,graph,toex)
            #pathList = remove_path(pathList,pl,graph,toex)
            pathList.remove(pathToExtend)
            endNodes[pl].remove(toex)
            
            for neib in graph.get_connected_nodes(toex):
                
                if neib == goal:
                    goalFound = True
                    newPath = list(pathToExtend)
                    newPath.append(neib)
                    
                    if min_goal_len == -10:
                        temp_win_path = newPath
                        min_goal_len = path_length(graph,newPath)
                        
                    else:
                        
                        if min_goal_len > path_length(graph,newPath):
                            temp_win_path = newPath
                            min_goal_len = path_length(graph,newPath)
                    
                    break
                    
                else:
                    
                    if len(pathToExtend)<=1:
                        
                        newPath = list(pathToExtend)
                        newPath.append(neib)
                        newLen = path_length(graph,newPath)
                        pathList.append(newPath)
                            
                        if newLen in pdList:
                            pdList.append(newLen)
                            endNodes[newLen].append(neib)
                            
                        else:
                            pdList.append(newLen)
                            endNodes[newLen] = [neib]
                        
                    else:
                            
                        if neib != pathToExtend[len(pathToExtend)-2]:
                            newPath = list(pathToExtend)
                            newPath.append(neib)
                            newLen = path_length(graph,newPath)
                            pathList.append(newPath)
                            
                            if newLen in pdList:
                                pdList.append(newLen)
                                endNodes[newLen].append(neib)
                                    
                            else:
                                pdList.append(newLen)
                                endNodes[newLen] = [neib]
                                                             
    while len(pdList)>0:
    
        pdList.sort()
        pdList.reverse()
        pl = pdList.pop()
        
        if min_goal_len > pl:
        
            for toex in endNodes[pl]:
        
                pathToExtend = find_path(pathList,pl,graph,toex)
                pathList.remove(pathToExtend)
                endNodes[pl].remove(toex)
            
                for neib in graph.get_connected_nodes(toex):
                
                    if neib == goal:
                        goalFound = True
                        newPath = list(pathToExtend)
                        newPath.append(neib)
                    
                        if min_goal_len == -10:
                            temp_win_path = newPath
                            min_goal_len = path_length(graph,newPath)
                        
                        else:
                        
                            if min_goal_len > path_length(graph,newPath):
                                temp_win_path = newPath
                                min_goal_len = path_length(graph,newPath)
                    
                        break
                    
                    else:
                    
                        if len(pathToExtend)<=1:
                        
                            newPath = list(pathToExtend)
                            newPath.append(neib)
                            newLen = path_length(graph,newPath)
                            pathList.append(newPath)
                            
                            if newLen in pdList:
                                pdList.append(newLen)
                                endNodes[newLen].append(neib)
                                
                            else:
                                pdList.append(newLen)
                                endNodes[newLen] = [neib]
                        
                        else:
                            
                            if neib != pathToExtend[len(pathToExtend)-2]:
                                newPath = list(pathToExtend)
                                newPath.append(neib)
                                newLen = path_length(graph,newPath)
                                pathList.append(newPath)
                                
                                if newLen in pdList:
                                    pdList.append(newLen)
                                    endNodes[newLen].append(neib)
                                    
                                else:
                                    pdList.append(newLen)
                                    endNodes[newLen] = [neib]                            
    
        else: 
            return temp_win_path
        
def a_star(graph, start, goal):
 
    explored = set()
    endNodes = dict()
    path_cost_list = list([path_length(graph,[start])+graph.get_heuristic(start,goal)])
    path_list = list([[start]])
    goalFound = start == goal
    endNodes[path_length(graph,[start])+graph.get_heuristic(start,goal)] = [start]
    temp_goal_path = list()
    min_goal_cost = -1
    
    if goalFound:
        return start
    
    while not goalFound and len(path_cost_list) > 0:
        
        path_cost_list.sort()
        path_cost_list.reverse()
        cur_cost = path_cost_list.pop()
            
        for toex in endNodes[cur_cost]:
            toex_path = asfind_path(path_list, cur_cost,toex,graph,goal)
            path_list.remove(toex_path)
            endNodes[cur_cost].remove(toex)
            explored.add(toex)
            for neib in graph.get_connected_nodes(toex):
                if neib == goal:
                    goalFound = True
                    newPath = list(toex_path)
                    newPath.append(neib)
                    
                    if min_goal_cost == -1:
                        temp_goal_path = newPath
                        min_goal_cost = path_length(graph,newPath) 
                        
                    else:
                        
                        if min_goal_cost > path_length(graph,newPath):
                            temp_goal_path = newPath
                            min_goal_cost = path_length(graph,newPath)
                    
                    break
                                
                else:
                    
                    if neib not in explored:
                        
                        newPath = list(toex_path)
                        newPath.append(neib)
                        newCost = path_length(graph,newPath) + graph.get_heuristic(neib,goal)
                        path_list.append(newPath)
                            
                        if newCost in path_cost_list:
                            endNodes[newCost].append(neib)
                            
                        else:
                            endNodes[newCost] = [neib]
                        
                        path_cost_list.append(newCost)
                         
    while len(path_cost_list)>0:
    
        path_cost_list.sort()
        path_cost_list.reverse()
        cur_cost = path_cost_list.pop()
        
        if min_goal_cost > cur_cost:
        
            for toex in endNodes[cur_cost]:
                toex_path = asfind_path(path_list,cur_cost,toex,graph,goal)
                path_list.remove(toex_path)
                endNodes[cur_cost].remove(toex)
                explored.add(toex)
            
                for neib in graph.get_connected_nodes(toex):
                
                    if neib == goal:
                        goalFound = True
                        newPath = list(toex_path)
                        newPath.append(neib)
                    
                        if min_goal_cost == -1:
                            temp_goal_path = newPath
                            min_goal_cost = path_length(graph,newPath)
                        
                        else:
                        
                            if min_goal_cost > path_length(graph,newPath):
                                temp_goal_path = newPath
                                min_goal_cost = path_length(graph,newPath)
                    
                        break
                    
                    else:
                        
                        if neib not in explored:
                        
                            newPath = list(toex_path)
                            newPath.append(neib)
                            newCost = path_length(graph,newPath) + graph.get_heuristic(neib,goal)
                            path_list.append(newPath)
                            
                            if newCost in path_cost_list:
                                endNodes[newCost].append(neib)
                            
                            else:
                                endNodes[newCost] = [neib]
                        
                            path_cost_list.append(newCost)
                                                                         
        else: 
            break
        
    return temp_goal_path
              
def asfind_path(pathList,cost,endNode,graph,goal):
    
    found_path = list()

    for path in pathList:
        findcost = path_length(graph,path)+graph.get_heuristic(endNode,goal)
        
        if cost == findcost and path[len(path)-1]== endNode:
            found_path = path[:]
            break          
        
    return found_path            
        
def remove_path(pathList,pl,graph,endNode):
    
    for path in pathList:
        
        if pl == path_length(graph,path) and path[len(path)-1]== endNode:
            pathList.remove(path)
            break
        
    return pathList
        
def find_path(pathList,pl,graph,endNode):
    
    found_path = list()

    for path in pathList:
        
        if pl == path_length(graph,path) and path[len(path)-1]== endNode:
            found_path = path[:]
            break
            
    return found_path

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    
    nodes_to_check = list(graph.nodes)
    #nodes_to_check.remove(goal)
    
    for node in nodes_to_check:
        
        costs = list()    
        costs.append(path_length(graph,branch_and_bound(graph,node,goal)))
        costs.append(path_length(graph,a_star(graph,node,goal)))
        costs.append(path_length(graph,dfs(graph,node,goal)))
        costs.append(path_length(graph,bfs(graph,node,goal)))
        costs.append(path_length(graph,hill_climbing(graph,node,goal)))
        costs.append(path_length(graph,beam_search(graph,node,goal,5)))
        costs.sort()
        costs.reverse()
        min_cost = costs.pop()
        
        while min_cost == 0 and len(costs)>0:
            min_cost = costs.pop()
    
        if graph.get_heuristic(node,goal) > min_cost:
            return False
        
    return True

def is_consistent(graph, goal):
    
    for node in graph.nodes:
        for neib in graph.get_connected_nodes(node):
            
            node_h = graph.get_heuristic(node,goal)
            pl = path_length(graph,[node,neib])
            ph = graph.get_heuristic(neib,goal)
            
            if node_h > pl + ph:
                return False
            
    return True
    
HOW_MANY_HOURS_THIS_PSET_TOOK = 'less than 10 mins'
WHAT_I_FOUND_INTERESTING = 'all'
WHAT_I_FOUND_BORING = 'none'
