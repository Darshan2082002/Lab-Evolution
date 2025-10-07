
from typing import List, Tuple, Dict, Any, Optional
import itertools








class Expr:
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __repr__(self):
        if self.op == 'atom': return self.args[0]
        if self.op == 'not': return f"~{self.args[0]}"
        if self.op == 'and': return '(' + ' & '.join(map(str, self.args)) + ')'
        if self.op == 'or':  return '(' + ' | '.join(map(str, self.args)) + ')'
        if self.op == 'imp': return f"({self.args[0]} -> {self.args[1]})"

def atom(a): return Expr('atom', a)
def neg(a): return Expr('not', a)
def imp(a,b): return Expr('imp', a,b)

class PropKB:
    def __init__(self):
        self.facts=set()
        self.neg_facts=set()
        self.imps=[]
        self.trace=[]

    def add(self, e):
        if e.op=='atom':
            self.facts.add(e.args[0])
            self.trace.append((e,'assertion',[]))
        elif e.op=='not' and e.args[0].op=='atom':
            self.neg_facts.add(e.args[0].args[0])
            self.trace.append((e,'assertion',[]))
        elif e.op=='imp':
            self.imps.append((e.args[0],e.args[1]))
            self.trace.append((e,'assertion',[]))

    def proved(self,e):
        if e.op=='atom': return e.args[0] in self.facts
        if e.op=='not' and e.args[0].op=='atom': return e.args[0].args[0] in self.neg_facts
        return False

    def apply_modus_ponens(self):
        changed=False
        for a,b in list(self.imps):
            if a.op=='atom' and a.args[0] in self.facts and b.op=='atom' and b.args[0] not in self.facts:
                self.facts.add(b.args[0])
                self.trace.append((b,'Modus Ponens',[a,imp(a,b)]))
                changed=True
        return changed

    def apply_modus_tollens(self):
        changed=False
        for a,b in self.imps:
            if b.op=='atom' and b.args[0] in self.neg_facts and a.args[0] not in self.neg_facts:
                self.neg_facts.add(a.args[0])
                self.trace.append((neg(a),'Modus Tollens',[imp(a,b),neg(b)]))
                changed=True
        return changed

    def infer(self,q):
        while True:
            if self.proved(q): return True
            changed=False
            changed|=self.apply_modus_ponens()
            changed|=self.apply_modus_tollens()
            if not changed: break
        return self.proved(q)

def parse_prop(statement):
    statement = statement.replace(" ", "")
    if "->" in statement:
        left, right = statement.split("->")
        return imp(parse_prop(left), parse_prop(right))
    elif statement.startswith("~"):
        return neg(parse_prop(statement[1:]))
    else:
        return atom(statement)

def propositional_user():
    print("=== PROPOSITIONAL LOGIC INFERENCE ===")
    kb = PropKB()
    n = int(input("Enter number of statements in KB: "))
    for i in range(n):
        s = input(f"Statement {i+1}: ")
        kb.add(parse_prop(s))
    query_str = input("Enter query to check: ")
    query = parse_prop(query_str)

    result = kb.infer(query)
    print("\nResult:", "Can be Inferred" if result else " Cannot be Inferred")

    print("\n--- Proof Trace ---")
    for e, r, p in kb.trace:
        print(f"{r}: {e}  from {p}")
    print("==============================\n")




class Term:
    def __init__(self,name,is_var=False): self.name=name; self.is_var=is_var
    def __repr__(self): return self.name
    def __eq__(self,o): return isinstance(o,Term) and self.name==o.name and self.is_var==o.is_var
    def __hash__(self): return hash((self.name,self.is_var))

class Predicate:
    def __init__(self,name,terms,neg=False):
        self.name=name; self.terms=terms; self.neg=neg
    def __repr__(self): return ("~" if self.neg else "")+f"{self.name}({', '.join(map(str,self.terms))})"
    def negate(self): return Predicate(self.name,self.terms,not self.neg)

class Clause:
    def __init__(self,preds): self.preds=frozenset(preds)
    def __repr__(self):
        if not self.preds: return "{} (empty)"
        return " | ".join(map(str,self.preds))
    def __eq__(self,o): return self.preds==o.preds
    def __hash__(self): return hash(self.preds)

def unify(x,y,theta):
    if theta is None: return None
    if x==y: return theta
    if isinstance(x,Term) and x.is_var:
        return unify_var(x,y,theta)
    if isinstance(y,Term) and y.is_var:
        return unify_var(y,x,theta)
    if isinstance(x,Predicate) and isinstance(y,Predicate):
        if x.name!=y.name or len(x.terms)!=len(y.terms): return None
        for a,b in zip(x.terms,y.terms):
            theta=unify(a,b,theta)
            if theta is None: return None
        return theta
    return None

def unify_var(var,x,theta):
    if var.name in theta: return unify(theta[var.name],x,theta)
    if isinstance(x,Term) and x.name in theta: return unify(var,theta[x.name],theta)
    new=theta.copy(); new[var.name]=x; return new

def substitute(pred,theta):
    new=[]
    for t in pred.terms:
        if t.is_var and t.name in theta: new.append(theta[t.name])
        else: new.append(t)
    return Predicate(pred.name,new,pred.neg)

def resolve(c1,c2):
    resolvents=[]
    for p in c1.preds:
        for q in c2.preds:
            if p.name==q.name and p.neg!=q.neg and len(p.terms)==len(q.terms):
                theta=unify(p,q,{})
                if theta is not None:
                    new_preds=[substitute(r,theta) for r in c1.preds if r!=p]+[substitute(r,theta) for r in c2.preds if r!=q]
                    resolvents.append(Clause(new_preds))
    return resolvents

def fol_resolution(kb,query):
    clauses=set(kb+[query])
    steps=[]
    while True:
        pairs=list(itertools.combinations(clauses,2))
        new=set()
        for (ci,cj) in pairs:
            resolvents=resolve(ci,cj)
            for r in resolvents:
                steps.append(f"{ci} + {cj} => {r}")
                if not r.preds:
                    print("\nEMPTY CLAUSE FOUND => Query is Entailed ✅")
                    return True,steps
                new.add(r)
        if new.issubset(clauses): return False,steps
        clauses|=new

def parse_predicate(pred_str):
    pred_str = pred_str.strip()
    neg = pred_str.startswith("~")
    if neg: pred_str = pred_str[1:]
    name, args = pred_str.split("(")
    args = args[:-1].split(",")
    terms = [Term(a.strip(), a.strip()[0].islower()) for a in args]
    return Predicate(name.strip(), terms, neg)

def fol_user():
    print("=== FIRST-ORDER LOGIC RESOLUTION ===")
    n = int(input("Enter number of clauses in KB: "))
    kb=[]
    for i in range(n):
        clause_str = input(f"Clause {i+1}: ")
        preds = [parse_predicate(p) for p in clause_str.split("|")]
        kb.append(Clause(preds))
    query_str = input("Enter query (will be negated internally): ")
    query_pred = parse_predicate(query_str)
    query = Clause([query_pred.negate()])
    res,trace = fol_resolution(kb,query)
    print("\n--- Resolution Steps ---")
    for t in trace: print(t)
    print("==============================\n")



if __name__ == "__main__":
    print(" AI Inference System")
    print("1. Propositional Logic")
    print("2. First-Order Logic (Resolution)")
    print("3. Both")
    ch = input("Choose option: ")

    if ch == '1':
        propositional_user()
    elif ch == '2':
        fol_user()
    else:
        propositional_user()
        fol_user()