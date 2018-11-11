import sys

class sysloganalyzer:

	def __init__(self, fn, *argv):
		self.argv = argv
		self.cargv = self.rlc(argv)
		self.largv = len(argv)
		self.file = fn
		self.lot = self.awk()
		self.llot = len(self.lot)
		self.vals = {}

	def awk(self):
		tmp = []
		result = []
		tpl = ()
		n = self.largv
		count = 0
		f = open(self.file, 'r')
		for line in f:
			for i in range(n):
				if self.argv[i] in line:
					count += 1
					if count == n:
						tmp = line.split()
						for j in range(len(tmp)):
							for k in range(n):
								if self.argv[k] in tmp[j]:
									tpl = tpl + (self.getAfterStr(tmp[j], self.argv[k]),)
						result.append(tpl)
						tpl = ()
			count = 0
		f.close()
		return result

	def rlc(self, lst):
		tmp = []
		for i in range(len(lst)):
			tmp.append(lst[i][:-1])
		return tmp

	def addTupleToDict(self, tpl):
		for i in range(self.largv-1):
			if tpl[0][0] in self.vals:
				self.vals[tpl[0][0]][i] += int(tpl[0][i+1])
			else:
				self.vals[tpl[0][0]] = self.setKeys()
				self.vals[tpl[0][0]][i] += int(tpl[0][i+1])

	def collect(self):
		for i in range(self.llot):
			self.addTupleToDict([self.lot[i]])

	def getIndex(self, lst, word):
		for i in range(len(lst)):
			if word == lst[i]:
				return i

	def setKeys(self):
		lot = self.lot
		lst = []
		for x in range(self.largv-1):
			lst.append(0)
		return lst

	def show(self):
		self.collect()
		for element in self.cargv:
			print "%20s\t" % element,

		print "\n"
		print "\t--------------------------------------------------------------"
		for key, value in sorted(self.vals.items()):
			print "%20s\t %20s\t %20s\t" % (key, value[0], value[1])

	def dicToLstOfTuple(self, dct):
		return [(k, v) for k, v in dct.iteritems()]

	def getAfterStr(self, s1, s2):
		return s1[s1.index(s2) + len(s2):]

def main():
	sla = sysloganalyzer("sys-log", "application=", "origsent=", "termsent=")
	sla.show()

if __name__ == '__main__':
    main()
