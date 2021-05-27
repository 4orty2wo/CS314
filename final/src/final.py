from prolog_structures import Rule, RuleBody, Term, Function, Variable, Atom, Number
from typing import List
from functools import reduce

import sys
import random

class Not_unifiable(Exception):
	pass

'''
Please read prolog_structures.py for data structures
that represent Prolog terms, rules, and goals.
'''
class Interpreter:
	def __init__(self):
		pass

	'''
	Example
	occurs_check (v, t) where v is of type Variable, t is of type Term.
	occurs_check (v, t) returns true if the Prolog Variable v occurs in t.
	Please see the lecture note Control in Prolog to revisit the concept of
	occurs-check.
	'''
	def occurs_check (self, v : Variable, t : Term) -> bool:
		if isinstance(t, Variable):
			return v == t
		elif isinstance(t, Function):
			for t in t.terms:
				if self.occurs_check(v, t):
					return True
			return False
		return False


	'''
	Problem 1
	variables_of_term (t) where t is of type Term.
	variables_of_clause (c) where c is of type Rule.

	The function should return the Variables contained in a term or a rule
	using Python set.

	The result must be saved in a Python set. The type of each element (a Prolog Variable)
	in the set is Variable.
	'''
	def variables_of_term (self, t : Term) -> set :
		terms = set()
		for x in t.terms:
			if isinstance(x, Function):
				self.variables_of_term(x.terms)
			elif isinstance(x, Variable):
				terms.add(x)
		return terms

	def variables_of_clause (self, c : Rule) -> set :
		rules = set()
		for x in c.head.terms:
			if isinstance(x, Variable):
				rules.add(x)
		return rules


	'''
	Problem 2
	substitute_in_term (s, t) where s is of type dictionary and t is of type Term
	substitute_in_clause (s, t) where s is of type dictionary and c is of type Rule,

	The value of type dict should be a Python dictionary whose keys are of type Variable
	and values are of type Term. It is a map from variables to terms.

	The function should return t_ obtained by applying substitution s to t.

	Please use Python dictionary to represent a subsititution map.
	'''
	def substitute_in_term (self, s : dict, t : Term) -> Term:
		
		if not t:
			return
		if isinstance(t, Function):
			new_terms = []
			for term in t.terms:
				new_terms.append(self.substitute_in_term(s,term))
			return Function(t.relation,new_terms)
		else:
			"""
			t[0] = s.get(t[0], t[0])
			self.substitute_in_term(s, t[1:])
			"""
			if isinstance(t, Variable):
				try: return s[t]
				except: return t
			return t
			 
		"""
		for count, x in enumerate(t.terms):
			if isinstance(x, Function):
				self.substitute_in_term(x.terms)
			else:
				t.terms[count] = s.get(x,x)
		return t
		"""
	def substitute_in_clause (self, s : dict, c : Rule) -> Rule:
		for count, x in enumerate(c.head.terms):
			c.head.terms[count] = s.get(x,x)
		return c


	'''
	Problem 3
	unify (t1, t2) where t1 is of type term and t2 is of type Term.
	The function should return a substitution map of type dict,
	which is a unifier of the given terms. You may find the pseudocode
	of unify in the lecture note Control in Prolog useful.

	The function should raise the exception raise Not_unfifiable (),
	if the given terms are not unifiable.

	Please use Python dictionary to represent a subsititution map.
	'''
	def unify_helper(self, t1: Term, t2 : Term, theta : dict) -> dict:
		t1 = self.substitute_in_term(theta, t1)
		t2 = self.substitute_in_term(theta, t2)
		if (isinstance(t1, Variable)) and not self.occurs_check(t1, t2):
			theta[t1] = t2
			for k in theta.keys():
				if theta[k] == t1:
					#theta[k] = self.substitute_in_term(theta, {t1:t2})
					theta[k] = t2
			return theta
		elif (isinstance(t2, Variable)) and not self.occurs_check(t2, t1):
			theta[t2] = t1
			for k in theta.keys():
				if theta[k] == t2:
					#theta[k] = self.substitute_in_term(theta, {t2:t1})
					theta[k] = t1
			return theta
		elif t1 == t2: return theta
		elif isinstance(t1, Function) and isinstance(t2, Function):
			if t1.relation == t2.relation and len(t1.terms) == len(t2.terms):
				for x, y in zip(t1.terms, t2.terms):
					theta.update(self.unify_helper(x, y, theta))
				return theta
			else:
				raise Not_unifiable
		else:
			raise Not_unifiable

	def unify (self, tt1: Term, tt2: Term) -> dict:
		
		s = dict({})
		"""
		if type(tt1) is list: t1 = tt1[0]
		else: t1 = tt1
		if type(tt2) is list: t2 = tt2[0]
		else: t2 = tt2

		if isinstance(t1, Variable):
			if t1 != t2:
				s[t1] = t2
				return s
		elif isinstance(t2, Variable):
			if t2 != t1:
				s[t2] = t1
				return s
		elif ( isinstance(t1, Variable) and isinstance(t2, Variable) ) or ( isinstance(t2, Atom) and isinstance(t1, Atom) ) or ( isinstance(t1, Number) and isinstance(t2, Number) ):
			if t1 == t2:
				return s
			else: 
				raise Not_unifiable
		elif isinstance(t1, Function) and isinstance(t2, Function):
			s.update( self.unify( t1.terms[0:], t2.terms[0:] ))
			#reduce(f, self.unify( t1.terms[0:], t2.terms[0:] ))
			return s
		else:
			raise Not_unifiable
		"""

		"""
		if isinstance(t1, Variable) or isinstance(t2, Variable):
			if t1 != t2:
				if not isinstance(t2, Variable):
					s[t1] = t2
				else:
					s[t2] = t1
			return s
		elif t1 == t2 and isinstance(t1, Variable) and isinstance(t2, Variable):
			return {}
		elif t1 == t2 and isinstance(t1, Number) and isinstance(t2, Number):
			return {}
		elif t1 == t2 and isinstance(t1, Atom) and isinstance(t2, Atom):
			return {}
		elif isinstance(t1, Function) and isinstance(t2, Function):
			for i in range(len(t1.terms)):
				for j in range(len(t2.terms)):
					s.update(self.unify( t1.terms[i], t2.terms[j] ))
		else:
			raise Not_unifiable
		"""
		s.update(self.unify_helper(tt1, tt2, s))
		return s


	fresh_counter = 0
	def fresh(self) -> Variable:
		self.fresh_counter += 1
		return Variable("_G" + str(self.fresh_counter))
	def freshen(self, c: Rule) -> Rule:
		c_vars = self.variables_of_clause(c)
		theta = {}
		for c_var in c_vars:
			theta[c_var] = self.fresh()

		return self.substitute_in_clause(theta, c)


	'''
	Problem 4
	Following the Abstract interpreter pseudocode in the lecture note Control in Prolog to implement
	a nondeterministic Prolog interpreter.

	nondet_query (program, goal) where
		the first argument is a program which is a list of Rules.
		the second argument is a goal which is a list of Terms.

	The function returns a list of Terms (results), which is an instance of the original goal and is
	a logical consequence of the program. See the tests cases (in src/main.py) as examples.
	'''
	def nondet_query (self, program : List[Rule], pgoal : List[Term]) -> List[Term]:
		
		while(True):
			goal = pgoal.copy()
			resolvent = goal.copy()

			while resolvent:
				#chosen_goal = goal[random.randint(0, len(goal)-1)]
				#rand_rule = program[random.randint(0, len(program)-1)]
				chosen_goal = resolvent[random.randint(0, len(resolvent)-1)]
				rand_rule = program[random.randint(0, len(program)-1)]
				rand_rule = self.freshen(rand_rule)

				try: t = self.unify(chosen_goal, rand_rule.head)
				except: break

				resolvent.remove(chosen_goal)
				for term in rand_rule.body.terms: resolvent.append(term)
				"""
				for term in resolvent:
					resolvent.append( self.substitute_in_term(t,term) )
				for term in goal:
					goal.append( self.substitute_in_term(t,term) )
				"""
				tempR = []
				tempG = []
				for term in resolvent:
					tempR.append(self.substitute_in_term(t,term))
				for term in goal:
					tempG.append(self.substitute_in_term(t,term))
				resolvent = tempR.copy()
				goal = tempG.copy()
			if resolvent: continue
			else: break
		return goal

	'''
	Challenge Problem

	det_query (program, goal) where
		the first argument is a program which is a list of Rules.
		the second argument is a goal which is a list of Terms.

	The function returns a list of term lists (results). Each of these results is
	an instance of the original goal and is a logical consequence of the program.
	If the given goal is not a logical consequence of the program, then the result
	is an empty list. See the test cases (in src/main.py) as examples.
	'''
	def det_query (self, program : List[Rule], pgoal : List[Term]) -> List[List[Term]]:
		return [pgoal]