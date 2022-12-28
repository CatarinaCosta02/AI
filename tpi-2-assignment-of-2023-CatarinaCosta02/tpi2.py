#encoding: utf8

# YOUR NAME: Catarina Costa
# YOUR NUMBER: 103696

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT:
# - João Monteiro - 102690
# - ...

from semantic_network import *
from bayes_net import *
from constraintsearch import *


class MySN(SemanticNetwork):

    def __init__(self):
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED
        pass

    def is_object(self,user,obj):
        # IMPLEMENT HERE
        #  checks if the object objexists in user declarations

        if (self.query_local(user = user,e1 = obj)+ self.query_local(user = user,e2 = obj)):
            for i in self.query_local(user = user,e1 = obj)+ self.query_local(user = user,e2 = obj):
                if isinstance(i.relation, Association):
                    return True
        return False

    def is_type(self,user,type):
        # IMPLEMENT HERE
        # checks if the type type exists in user declarations
        if (self.query_local(user = user,e2=type)):
            return True
        else:
            return False


    def infer_type(self, user, obj):

        # IMPLEMENT HERE
        # <tipo> - the type of the object, provided that it can be inferred;
        # None - if the type cannot be inferred;
        # __unknown__ - if the object is not declared in the user declarations.
        
        delc = [d for d in self.query_local(user=user, e1=obj) if isinstance(d.relation, Member)]
        if delc:
            return delc[0].relation.entity2

        for assoc in [d.relation.name for d in self.query_local(user=user, e1=obj) if isinstance(d.relation, Association)]:
            sign = self.infer_signature(user=user, assoc=assoc)
            if sign:
                if len(sign) == 2 and sign[0] != obj:
                    return sign[0]
                elif len(sign) == 1:
                    return sign[0] if sign[0] != obj else sign[1]
                else:
                    return None

        for assoc in [d.relation.name for d in self.query_local(user=user, e2=obj) if isinstance(d.relation, Association)]:
            sign = self.infer_signature(user=user, assoc=assoc)
            if sign:
                if len(sign) == 2 and sign[1] != obj:
                    return sign[1]
                elif len(sign) == 1:
                    return sign[0] if sign[0] != obj else sign[1]
                else:
                    return obj, 'unknown'


        if self.is_object(user, obj):
            return '__unknown__'
        return None
    
    def infer_signature(self,user,assoc):
        # IMPLEMENT HERE
        # (t1,t2) - where t1 and t2 are the types of the entities involved in the association;
        # None - if the association does not exist.

        delc = []
        sign = ()  

        for d in self.query_local(user=user, rel=assoc):
            delc.append(d)

        for d in delc:
            if d.relation.entity1 is None or d.relation.entity1 == "__unknown__":
                return None

            if d.relation.entity2 is None or d.relation.entity2 == "__unknown__":
                return None

            if isinstance(d.relation, Association) and d.relation.card == None:
                continue
            else:
                sign = (d.relation.entity1, d.relation.entity2)

        return sign



class MyBN(BayesNet):

    def __init__(self):
        BayesNet.__init__(self)
        

    def markov_blanket(self,var):
        # IMPLEMENT HERE
        
        markov_blanket = set()
        
        dependencies = self.dependencies[var]
        for (mt, mf, p) in dependencies:
            markov_blanket.update(mt)
            markov_blanket.update(mf)

        # se for parent adiciona ao markov blanket
        for v, dependencies in self.dependencies.items():
            for (mt, mf, p) in dependencies:
                if var in mt or var in mf:
                    markov_blanket.add(v)

        
        # copia do set para os children
        # para cada children, adiciona os seus parents
        children = markov_blanket.copy()
        for v in children:
            for (mt, mf, p) in self.dependencies[v]:
                markov_blanket.update(mt)
                markov_blanket.update(mf)
       
        markov_blanket.discard(var)
        
        # retorna a lista
        return list(markov_blanket)


class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        self.domains = domains
        self.constraints = constraints
        self.calls = 0
    
    # search dado no enunciado
    def search(self,domains=None):

        self.calls += 1 
        
        if domains==None:
            domains = self.domains

        if any([lv==[] for lv in domains.values()]):
            return None

        if all([len(lv)==1 for lv in list(domains.values())]):
            solution = { v:domains[v][0] for v in domains }
            if all( self.constraints[v1,v2](v1,solution[v1],v2,solution[v2])
                for (v1,v2) in self.constraints ): 
                return solution
 
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    self.propagate(newdomains,var)
                    solution = self.search(newdomains)
                    if solution != None:
                        return solution
        return None

    def propagate(self,domains,var):
        # IMPLEMENT HERE
        
        # Primeiro encontra todas as constraints que envolvem a variavel dada como a segunda variavel
        relevant_constraints = []
        for constraint in self.constraints:
            if constraint[1] == var:
                relevant_constraints.append(constraint)

        
        for var1, var2 in relevant_constraints:

            domain = []
            constraint = self.constraints[var1, var2]
            
            
            # Segundo encontra os valores do dominio de var1 que sao consistentes com a constraint
            for x in domains[var1]:
                for y in domains[var2]:
                    if constraint(var1, x, var2, y):
                        domain.append(x)
                        break

            if len(domain) < len(domains[var1]):
                updated_constraints = []
                domains[var1] = domain

                # Terceiro encontra todas as constraints que envolvem a variavel atualizada como a segunda variavel

                for constraint in self.constraints:
                    if constraint[1] == var1:
                        updated_constraints.append(constraint)
                
                # Adiciona as constraints altualizadas a lista de constraints relevantes
                relevant_constraints += updated_constraints



    def higherorder2binary(self,ho_c_vars,unary_c):
        # IMPLEMENT HERE
        pass


