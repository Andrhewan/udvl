import io

class VariableMap(object):
    def __init__(self,variables=[]):
        self.map = {}
        self.max = 0
        for v in variables:
            self.addVar(v)

    def addVar(self, variable):
        if not variable in self.map:
            self.max += 1
            self.map[variable] = self.max
        return self

    def get(self, variable):
        return self.map[variable]

    def __getitem__ (self,variable):
        return self.get(variable)

    def keys(self):
        return self.map.keys()

    def toString(self):
        return str(self.map)

    def reverse(self):
        r = {}
        for k,v in self.map.items():
            r[v] = k
        return r

    def writeToFile(self,outFile):
        outFile.write(self.toString())
        outFile.write('0')


    @staticmethod
    def readFromFile(inFile):
        val = eval((inFile.getvalue()[:-1]))
        return val

class CnfLit:
    def __init__(self,name):
        self.name = name
        self.neg = False

    @staticmethod
    def Not(name):
        r = CnfLit(name)
        r.neg = True
        return r

    def __neg__(self):
        r = CnfLit(self.name)
        r.neg = not self.neg
        return r

    def toString(self):
        if self.neg:
            return "-"+self.name
        else:
            return self.name

    def eval(self, i):
        ret = i[self.name]
        if self.neg:
            ret = not ret
        return ret
        # return i[self.name]^sel.neg - XOR pouzity

    def extendVarMap(self,varMap):
        varMap.addVar(self.name)

    def writeToFile(self, outFile, varMap):
        if self.neg:
            outFile.write("-")
        outFile.write(str(varMap[self.name]))

class CnfClause(list):
    def __init__(self, literals):
        list.__init__(self, literals)

    def eval(self, i):
        for lit in self:
            if lit.eval(i):
                return True
        return False

    def extendVarMap(self, varMap):
        for lit in self:
            lit.extendVarMap(varMap)

    def writeToFile(self, outFile, varMap):
        for lit in self:
            lit.writeToFile(outFile, varMap)
            outFile.write(" ")
        outFile.write("0\n")

        @staticmethod
        def readFromFile(inFile,varMap):
            clause = CnfClause([])
            reverseMap = varMap.reverse()
            line = inFile.readline()
            numbers = [int(x) for x in line.split()]
            if len(numbers) == 0:
                raise IOError("Prazdny riadok")
            if numbers[-1] != 0:
                raise IOError("Zly riadok")
            for n in numbers[:-1]:
                name = reverseMap([abs(n)])
                lit = CnfLit(name)
                lit.neg = n < 0
                clause.append(lit)
            return clause

    def toString(self):
        return " ".join([lit.toString() for lit in self])

class Cnf(list):
    def __init__(self, clauses = []):
        list.__init__(self, clauses)
        self.clauses = clauses

    def toString(self):
        ret = ''
        for i in self:
            ret += i.toString()+'\n'
        return ret

    def eval(self, i):
        for clause in self.clauses:
            if clause.eval(i) == False:
                return False
        return True

    def extendVarMap(self, varMap):
        for lit in self:
            lit.extendVarMap(varMap)

    def writeToFile(self, outFile, varMap):
        outFile.write(self.toString())
        outFile.write('0')
        outFile.write('\n')
        

    @staticmethod
    def readFromFile(inFile,varMap):
        print(inFile.getvalue())
        val = inFile.getvalue()[:-1].split('\n')
        print(val)
        return Cnf([val])



# vim: set sw=4 ts=4 sts=4 et :
