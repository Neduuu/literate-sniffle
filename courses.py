import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


class Grades:
    def __init__(self,name):
        self.name = name
        self.assessments = {
            'Tests':[],
            'Quizzes': [],
            'Tutorials': [],
            'Assignments':[],
            'PP': [],
            'PS' : [],
            'SE' : []
        }
        self.weighed = 0
        self.ass_no = 0
        self.progress = 0
        self._pred = ''

    def add_assessments(self,key,score):
        self.score = score
        self.key = key #Assessment type
        self.assessments[key].append(score)
        return True

    def show(self,key = None):
        if key is None:
            return self.assessments
        else:
            return self.assessments[key]

    def average_score(self,key=None):
        score = 0
        if key is None:
            for assess in self.assessments:
                if self.assessments.get(assess) == []:
                    continue
                score = sum(self.assessments.get(assess))
                ave = score/len(self.assessments.get(assess))
                return f'The average of {assess} is {ave:.2f}'
        else:
            score = sum(self.assessments.get(key))
            ave = score/len(self.assessments[key])
            return f'Average: {ave:.2f}'
        
    def remove_assessments(self):
        '''Remove all irrelevat assessment for a course'''
        for i in list(self.assessments):
            if not self.assessments[i]:
                self.assessments.pop(i)
    def equal_lists(self):
        '''making all lists equal to be eventually used in array calculations '''
        row_lengths = []
        for v in self.assessments.values():
            row_lengths.append(len(v))
        max_length = max(row_lengths)
        for v in self.assessments.values():
            while len(v) < max_length:
                v.append(None)
            
                   
    def grade_predict(self,key):
        '''Using linear regression to predict future grades '''
        n = len(self.assessments[key])
        y = 0.01 * (np.array(self.assessments[key])).reshape(-1,1)
        X = np.array([i+1 for i in range(len(self.assessments[key]))]).reshape(-1,1)
        regressor = LinearRegression()  
        regressor.fit(X, y)
        y_pred = regressor.predict([[n+1]])
        self._pred = y_pred[0][0] * 100
        return f'The predicted score of the next {key[:-1]} is {(y_pred[0][0] * 100):.1f}%'
        
    def weighted_grade(self,weight_list):
        d  = self.assessments.copy()
        for lists in weight_list:
            if lists[0] not in self.assessments: #if an assessment in weigh_list has yet to be written/updated 
                d[lists[0]] = lists[1]
            x = np.array(d[lists[0]])
            weighted = lists[1] * x
            d[lists[0]] = weighted
        self.weighed = d
    
    def no_assessments(self,values):
        '''stores expected total number of assessments to be written per assessment type'''
        d = {}
        list1 = []
        for key in self.assessments: #Getting the assessment names AFTER the useless ones have been removed---(remove_assessments())
            list1.append(key)
        for ass,EN in zip(list1,values):#Looping through both lists to assign values
            d[ass] = EN
        self.ass_no = d
        
    def course_prog(self):
        k = {}
        '''returns how far youve gone in the course'''
        x = self.assessments
        y = self.ass_no
        #They both share keys so..
        for key in x:
            if key in y:
                done = len(x[key])
                total = y[key]
                prog = done/total * 100
                k[key] = f'{prog:.1f}%'
        self.progress = k
        return k
    
    def course_plots(self,key=None):
        a = self.assessments
        if key:#sending specific plots
            y = np.array(self.assessments[key])
            X = np.array([j+1 for j in range(len(y))])
            for_predic = np.array([len(y)+1])
            plt.title(f'Grades for {self.name}')
            plt.plot(X, y, marker = 'o',linestyle = 'dotted')
            plt.plot(for_predic ,self._pred, marker = 'x')
            plt.grid()
            plt.xlabel("Assessment number")
            plt.ylabel("Score in %")
            plt.legend([key,'predicted'])
            plt.savefig(f'{self.name}{key.upper()}_plots.png')
            plt.clf()
            
        else:
            #sending all the plots
            y_list = []
            k_list = []
            for k in list(self.assessments):
                k_list.append(k)
                ys = np.array(a[k])
                y_list.append(ys)
            for y in y_list:
                X = np.array([j+1 for j in range(len(y))])
                plt.title(f'Grades for {self.name}')
                plt.plot(X, y, marker = 'o',linestyle = 'dotted')
                plt.grid()
                plt.xlabel("Assessment number")
                plt.ylabel("Score in %")
                plt.legend( k_list)
                plt.savefig(f'{self.name}_plots.png')
            plt.clf()

        
stat = Grades('STAT2507')
comp = Grades('COMP1005')
l_prog = Grades('MATH3801')
calc = Grades('MATH3705')

grade_list = [stat,comp,l_prog,calc]

