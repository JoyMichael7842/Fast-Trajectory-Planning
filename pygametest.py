import pygame

from utilities import PriorityQueueMaxG,Grid

#Heuristic Function ->Manhattan distance between current and end
def heuristic(current,goal):
  return abs(goal[0]-current[0])+abs(goal[1]-current[1])

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 100*5
WINDOW_WIDTH = 100*5

grid = Grid(5,5,[(1,2),(2,2),(3,2),(2,3),(3,3),(4,3)])
start = (4,2)
goal = (4,4)
rows = 5
cols = 5

def drawGrid():
    blockSize = 100 #Set the size of the grid block
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 1)

    for blocked in grid.Uniblocked:
        pygame.draw.rect(SCREEN, WHITE, (blocked[0]*blockSize, blocked[1]*blockSize, blockSize, blockSize))
    #pygame.draw.rect(SCREEN, WHITE, (200, 100, blockSize, blockSize))

pygame.init()

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  
# set the pygame window name 
pygame.display.set_caption("Moving rectangle")
  
# object current co-ordinates 
x = 400
y = 400
  
# dimensions of the object 
width = 100
height = 100
  
  
# Indicates pygame is running
run = True
  
# infinite loop 
while run:
    # creates time delay of 10ms 
    pygame.time.delay(10)
      
    # iterate over the list of Event objects  
    # that was returned by pygame.event.get() method.  
    for event in pygame.event.get():
          
        if event.type == pygame.QUIT:
              
            # it will make exit the while loop 
            run = False
    
              
    # completely fill the surface object  
    # with black colour  
    SCREEN.fill((0, 0, 0))
    drawGrid()



    counter = 0
    search = {}

    for i in range(rows):
      for j in range(cols):
        search[(i,j)] = 0
    while start!=goal:
      g = {}
      h = {}
      came_from = {}
      counter = counter+1
      g[start] = 0
      search[start] = counter
      g[goal] = float('inf')
      search[goal] = counter
      Open = PriorityQueueMaxG()
      closed = []
      for node in grid.neighbors(start):
        if node in grid.Uniblocked:     
          grid.currblocked.append(node)
      f_value = g[start]+heuristic(start,goal)
      Open.put(start,(f_value,g[start]))
      
      
      while(g[goal]>g[Open.peek()]):
        current = Open.get()
        
        closed.append(current)
        next_list = []
        for node in grid.neighbors(current):
          if node not in closed:
            next_list.append(node)
       
        for next in next_list:
          if search[next]<counter:
            g[next] = float('inf')
            search[next] = counter
          if g[next] > g[current] + grid.cost(current,next):
            g[next] = g[current] + grid.cost(current,next)
            came_from[next] = current
            f_value = g[next]+heuristic(next,goal)
            Open.put(next,(f_value,g[next]))




      if Open.empty():
        print('I cannot reach the Target');
        break;
      temp = goal
      path = []
      
      while(temp!=start):
        path.append(temp)
        temp = came_from[temp]
      path.append(start)
      path.reverse()
      for node in path:
        
        if node in grid.Uniblocked:
            pygame.draw.rect(SCREEN, (0, 0, 255), (node[0]*100,node[1]*100 , width, height))
            pygame.time.delay(2000)
            # it refreshes the window
            pygame.display.update()    
            break
        pygame.draw.rect(SCREEN, (255, 0, 0), (node[0]*100,node[1]*100 , width, height))
        pygame.time.delay(1000)
        # it refreshes the window
        pygame.display.update()

        
      
      start = came_from[node]
      if node==goal:
        break
    


    # drawing object on screen which is rectangle here 
    pygame.draw.rect(SCREEN, (255, 0, 0), (x, y, width, height))
      
    # it refreshes the window
    pygame.display.update() 
  
# closes the pygame window 
pygame.quit()
