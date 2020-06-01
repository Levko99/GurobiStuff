from gurobipy import *

# resouces and job sets
R = ['Carlos', 'Joe', 'Monika']
J = ['Tester', 'JavaDeveloper', 'Architect']

# matching score data
combinations, ms = multidict({
    ('Carlos', 'Tester'): 53,
    ('Carlos', 'JavaDeveloper'): 27,
    ('Carlos', 'Architect'): 13,
    ('Joe', 'Tester'): 80,
    ('Joe', 'JavaDeveloper'): 47,
    ('Joe', 'Architect'): 67,
    ('Monika', 'Tester'): 53,
    ('Monika', 'JavaDeveloper'): 73,
    ('Monika', 'Architect'): 47
})
#print(combinations[0][0])
m = Model('RAP')

x = m.addVars(combinations, name="assign")
print(x)

# create jobs constraints
jobs = m.addConstrs((x.sum('*', j) == 1 for j in J), 'job')
print(jobs)

#create resources constraints
resources = m.addConstrs((x.sum(r,'*') <= 1 for r in R), 'resource')

#obejctive function
m.setObjective(x.prod(ms), GRB.MAXIMIZE)


#save model for inspection
m.write('RAP.lp')

m.optimize()


#display optimal values of decision variables
for v in m.getVars():
    if(abs(v.x) > 1e-6):
        print(v.varName, v.x)


#display optimal total matching score
print('total matching scores', m.objVal)
