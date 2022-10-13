from __future__ import print_function
import pickle
import robot_movement as MOV

training_data=[
	['zold','szabad','kozep','uj',1],
	['zold','szabad','jobb','uj',2],
	['zold','szabad','bal','uj',3],
	['zold','szabad','forduljobb','uj',4],
	['zold','szabad','fordulbal','uj',5],
	['zold','szabad','kozep','volt',6]
]
print('sajt')
header=['color','diameter','label','hol']

def class_counts(rows):

	counts={}

	for row in rows:

		label=row[-1]
		if label not in counts:
			counts[label]=0
		counts[label]+=1
	return counts


def is_numeric(value):

	return isinstance(value,int) or isinstance(value,float)


class Question:

	def __init__(self,column,value):
		self.column=column
		self.value=value

	def match(self,example):

		val=example[self.column]
		if is_numeric(val):
			print(val,self.value)
			return val>self.value

		else:
			return val== self.value

	def __repr__(self):

		condition='=='
		if is_numeric(self.value):
			condition='>='
		return 'Is %s %s %s?' % (header[self.column],condition,str(self.value))




def partition(rows,question):

	true_rows,false_rows=[],[]
	for row in rows:
		if question.match(row):
			true_rows.append(row)
		else:
			false_rows.append(row)
	return true_rows,false_rows


def gini(rows):

	counts=class_counts(rows)
	impurity=1
	for lbl in counts:
		prob_of_lbl=counts[lbl]/float(len(rows))
		impurity -=prob_of_lbl**2
	return impurity


def info_gain(left,right,current_uncertainty):

	p=float(len(left))/(len(left)+len(right))
	return current_uncertainty-p*gini(left)-(1-p)*gini(right)


def find_best_split(rows):

	best_gain=0
	best_question=None
	current_uncertainty=gini(rows)
	n_features=len(rows[0])-1

	for col in range(n_features):

		values=set([row[col] for row in rows])

		for val in values:

			question=Question(col,val)
			true_rows,false_rows=partition(rows,question)

			if len(true_rows)==0 or len(false_rows)==0:
				continue

			gain=info_gain(true_rows,false_rows,current_uncertainty)

			if gain>=best_gain:
				best_gain,best_question=gain,question

	return best_gain,best_question


class Leaf:

	def __init__(self,rows):
		self.predictions=class_counts(rows)



class Decision_Node:

	def __init__(self,question,true_branch,false_branch):

		self.question=question
		self.true_branch=true_branch
		self.false_branch=false_branch



def build_tree(rows):

	gain,question=find_best_split(rows)

	if gain==0:
		return Leaf(rows)

	true_rows,false_rows=partition(rows,question)

	true_branch=build_tree(true_rows)
	false_branch=build_tree(false_rows)


	return Decision_Node(question,true_branch,false_branch)


def print_tree(node,spacing=''):

	if isinstance(node,Leaf):
		print(spacing+ 'Predict',node.predictions)
		return

	print(spacing+str(node.question))

	print(spacing +'--> True:')
	print_tree(node.true_branch,spacing+ " ")

	print(spacing + '--> False:')
	print_tree(node.false_branch,spacing+" ")



def classify(row,node):

	if isinstance(node,Leaf):
		return node.predictions

	if node.question.match(row):
		return classify(row,node.true_branch)
	else:
		return classify(row,node.false_branch)



def print_leaf(counts):

	total=sum(counts.values())*1.0
	probs=0

	for lbl in counts.keys():
		probs=lbl
	return probs




my_tree=build_tree(training_data)
#print_tree(my_tree)

testing_data=[
	#['zold','akadaly','jobb',-1],
	['zold','szabad','kozep','uj',1],
	#['mas','szabad','bal',-1],
	#['zold','akadaly','jobb',-1],
	#['mas','akadaly','kozep',-1],
	['zold','szabad','jobb','uj',2]
]


szin='zold'
path='szabad'

def decide(szin,path,irany,bejart):

	input_data=[
		[szin,path,irany,bejart]
	]

	for row in input_data:
		step=print_leaf(classify(row,my_tree))
		#print(step)

	if(step==1):
		MOV.frd(1,0,7)
		print('elore')
	elif(step==2):
		MOV.fordul(2,1)
		print('jobbkis')
	elif(step==3):
		MOV.fordul(3,1)
		print('balkis')
	elif(step==4):
		print('jobb')
		#MOV.frd(1,0,5)
		MOV.fordul(2,8)#bal 7
	elif(step==5):
		print('bal')
		MOV.frd(1,0,5)
		MOV.fordul(3,7)#jobb
	elif(step==6):
		MOV.fordul(3,7)
		#ha körbeért
	else:
		print("NO way!")
