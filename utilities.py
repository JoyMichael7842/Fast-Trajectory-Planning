#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:23:00 2022

@author: hiteshreddy
"""

#Grid Class
class Grid:
  #Initalizing grid with number of rows and number of columns
  def __init__(self,rows,cols,blocked):
    self.rows = rows
    self.cols = cols
    self.Uniblocked = blocked
    self.currblocked = []
  #Returns neighbors of given cell if they are not blocked in the current state
  def neighbors(self,id):
    (x,y) = id
    neighbors =  (x+1,y),(x-1,y),(x,y-1),(x,y+1)
    res = filter(self.inbound,neighbors)
    res = filter(self.passable,res)
    return res
  #checks if the cells are not crossing the limit of rows and columns
  def inbound(self,id):
    (x,y) = id
    return (0 <= x < self.rows) and (0 <= y < self.cols)
  #checks if cells are not blocked in the current state
  def passable(self,id):
    (x,y) = id
    return id not in self.currblocked
  #cost to move from one cell to another
  def cost(self,f,t):
    return 1

class PriorityQueueMaxG:
  def __init__(self):
    self.heapq = [0]
    self.priority = {}

  #inserts node into heap with priority given to min F value and max g-value
  def put(self,x,nodepriority):
    self.heapq.append(x)
    self.priority[x] = nodepriority
    index = len(self.heapq)-1
    #loop till you find min f-value and max g-value
    while((index//2)>=1 and self.priority[self.heapq[index]][0]<=self.priority[self.heapq[index//2]][0]):
      #if F-values are equal check g-values
      if self.priority[self.heapq[index]][0]==self.priority[self.heapq[index//2]][0]:
        #if g-value of parent is larger then child - swap
        if self.priority[self.heapq[index]][1]>self.priority[self.heapq[index//2]][1]:
          self.swap(index,index//2)    
      #if f-value of parent is smaller - swap
      else:
        self.swap(index,index//2)
      index = index//2
    return self.heapq

  #check if heap is empty
  def empty(self):
    return len(self.heapq) == 1

  #Returns minimum element
  def peek(self):
    return self.heapq[1]


  def get(self):
    max_ele = self.heapq[1]
    self.heapq[1] = self.heapq[-1]
    self.heapq = self.heapq[:-1]
    index = 1
    left_child = 2*index
    right_child = 2*index+1
    cond1 = right_child<len(self.heapq)
    cond2 = left_child<len(self.heapq)
    while cond1 or cond2:
      
      #both left_child and right_child
      if cond1:
        #parent F < left_child F and right_child F - done
        if self.priority[self.heapq[index]][0]<self.priority[self.heapq[left_child]][0] and self.priority[self.heapq[index]][0]<self.priority[self.heapq[right_child]][0]:
          return max_ele
        
        #parent F >left_child and right_child - check which is smaller
        elif self.priority[self.heapq[index]][0]>self.priority[self.heapq[left_child]][0] and self.priority[self.heapq[index]][0]>self.priority[self.heapq[right_child]][0]:
        #check which child has smaller F
            #left child has smaller F - swap with left child
            if self.priority[self.heapq[left_child]][0]< self.priority[self.heapq[right_child]][0]:
                self.swap(index,left_child)
                index = left_child
            #right child has smaller F -  swap with right_child        
            elif self.priority[self.heapq[left_child]][0]> self.priority[self.heapq[right_child]][0]:   
                self.swap(index,right_child)
                index = right_child
            #left child F = right child F - check g values
            else:
                #left_child G  > right child G - swap with left_child
                if self.priority[self.heapq[left_child]][1]>self.priority[self.heapq[right_child]][1]:
                    self.swap(index,left_child)
                    index = left_child
                #right_child G >= left child G - swap with right child
                else:
                    self.swap(index,right_child)
                    index = right_child

        #parent F == left_child F and parent F == right_child F - check g values
        elif self.priority[self.heapq[index]][0] == self.priority[self.heapq[left_child]][0] and self.priority[self.heapq[index]][0] == self.priority[self.heapq[right_child]][0]:
            #g_value of parent is larger than left_child and right_child - done
            if self.priority[self.heapq[index]][1]> self.priority[self.heapq[left_child]][1] and self.priority[self.heapq[index]][1]> self.priority[self.heapq[right_child]][1]:
                return max_ele
            #g_value of parent is equal to left and right child - done
            elif self.priority[self.heapq[index]][1] == self.priority[self.heapq[left_child]][1] and self.priority[self.heapq[index]][1] == self.priority[self.heapq[right_child]][1]:
                return max_ele
            #g_value of parent is smaller than left child and right child - check which is larger
            elif self.priority[self.heapq[index]][1]< self.priority[self.heapq[left_child]][1] and self.priority[self.heapq[index]][1]<self.priority[self.heapq[right_child]][1]:
                #g_value of left > g_value of right - swap parent with left
                if self.priority[self.heapq[left_child]][1]> self.priority[self.heapq[right_child]][1]:
                    self.swap(index,left_child)
                    index = left_child
                #g_value of right <= left_child - swap with right child
                else:
                    self.swap(index,right_child)
                    index = right_child
            
            #g_value of parent is smaller than left_child but not right_child - swap with left
            elif self.priority[self.heapq[left_child]][1]> self.priority[self.heapq[index]][1]:
                self.swap(left_child,index)
                index = left_child
            #g_value of parent is smaller than right_child but not left_child - swap with right
            elif self.priority[self.heapq[right_child]][1]> self.priority[self.heapq[index]][1]:
                self.swap(right_child,index)
                index = right_child
            #g_value of parent is equal to one of the child but other child is greater than parent-done
            else:
                return max_ele
        
        #parent F if greater than left child but not right child - swap with left
        elif self.priority[self.heapq[left_child]][0]< self.priority[self.heapq[index]][0]:
            self.swap(left_child,index)
            index = left_child
        
        #parent F is greater than right child but not left child - swap with right
        elif self.priority[self.heapq[right_child]][0]< self.priority[self.heapq[index]][0]:
            self.swap(right_child,index)
            index = right_child  
        
        #F-value of parent is equal to one of the children and other child is greater than parent - find equal and check g-values  
        else: 
            #F-value of left = F-value of parent - check G
            if self.priority[self.heapq[left_child]][0] == self.priority[self.heapq[index]][0]:
                #left child has larger G than parent - swap
                if self.priority[self.heapq[left_child]][1]>self.priority[self.heapq[index]][1]:
                    self.swap(left_child,index)
                    index = left_child
                #left_child G <= parent G
                else:
                    return max_ele
            #F-value of right = F-value of parent - check G
            elif self.priority[self.heapq[right_child]][0] == self.priority[self.heapq[index]][0]:
                #right child has larger G than parent - swap
                if self.priority[self.heapq[right_child]][1]>self.priority[self.heapq[index]][1]:
                    self.swap(right_child,index)
                    index = right_child
                #right_child G <= parent G
                else:
                    return max_ele
        
      else:#only left child
        
        #parent F < left_child F done
        if self.priority[self.heapq[index]][0]<self.priority[self.heapq[left_child]][0]:
          return max_ele

        #parent F > left_child F need to swap
        elif self.priority[self.heapq[index]][0]>self.priority[self.heapq[left_child]][0]:
            self.swap(left_child,index)
            index = left_child

        #parent F = left_child F check G
        elif self.priority[self.heapq[index]][0] == self.priority[self.heapq[left_child]][0]:
        #parent G >= left_child G done
          if self.priority[self.heapq[index]][1] >= self.priority[self.heapq[left_child]][1]:
            return max_ele
          #parent G < left_child G need to swap
          else: 
            self.swap(index,left_child)
            index = left_child
      
      #incerement child indexes
      left_child = 2*index
      right_child = 2*index+1
      cond1 = right_child<len(self.heapq)
      cond2 = left_child<len(self.heapq)
     

    return max_ele

  def swap(self,child,parent):
    self.heapq[child],self.heapq[parent] = self.heapq[parent],self.heapq[child]