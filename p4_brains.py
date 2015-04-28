
import random

# EXAMPLE STATE MACHINE
class MantisBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None

  def handle_event(self, message, details):

    if self.state is 'idle':

      if message == 'timer':
        # go to a random point, wake up sometime in the next 10 seconds
        world = self.body.world
        x, y = random.random()*world.width, random.random()*world.height
        self.body.go_to((x,y))
        self.body.set_alarm(random.random()*10)

      elif message == 'collide' and details['what'] == 'Slug':
        # a slug bumped into us; get curious
        self.state = 'curious'
        self.body.set_alarm(1) # think about this for a sec
        self.body.stop()
        self.target = details['who']

    elif self.state == 'curious':

      if message == 'timer':
        # chase down that slug who bumped into us
        if self.target:
          if random.random() < 0.5:
            self.body.stop()
            self.state = 'idle'
          else:
            self.body.follow(self.target)
          self.body.set_alarm(1)
      elif message == 'collide' and details['what'] == 'Slug':
        # we meet again!
        slug = details['who']
        slug.amount -= 0.01 # take a tiny little bite
    
class SlugBrain:

  def __init__(self, body):
    self.body = body
    self.state = 'idle'
    self.target = None
    self.hasResource = False
    self.body.amount = 0.5


  def handle_event(self, message, details):
    # TODO: IMPLEMENT THIS METHOD
    #  (Use helper methods and classes to keep your code organized where
    #  approprioate.)
    if self.state is 'idle':
      if self.body.amount <= 0.5:
	self.state = 'flee'
	self.body.set_alarm(0)
      if message == 'order':
        # go to a random point, wake up sometime in the next 10 seconds
	#self.state = 
        #else:
	if details == 'a':
	  self.body.stop()
	  self.state = 'attack'
	  self.body.set_alarm(0)
        elif details == 'h':
	  self.state = 'harvest'
	  self.body.set_alarm(0)
	elif isinstance(details, tuple):
	  self.state = 'move'
	  self.body.go_to(details)
	elif details == 'b':
	  self.state = 'build'
	  self.body.set_alarm(0)
    if self.state is 'move':
      if self.body.amount <= 0.5:
	self.state = 'flee'
	self.body.set_alarm(0)
      if message == 'order':
	if details == 'i':
	  self.body.stop()
        elif details == 'h':
	  self.state = 'harvest'
	  self.body.set_alarm(0)
	elif details == 'b':
	  self.body.set_alarm(0)
	  self.state = 'build'
	elif details == 'a':
	  self.body.stop()
	  self.state = 'attack'
	  self.body.set_alarm(0)
	if isinstance(details, tuple):
	  self.state = 'move'
	  self.body.go_to(details)
    if self.state == 'attack':
      if self.body.amount <= 0.5:
	self.state = 'flee'
	self.body.set_alarm(0)
      if message == 'order':
	if details == 'i':
	  self.body.stop()
	  self.state = 'idle'
        elif details == 'h':
	  self.state = 'harvest'
	  self.body.set_alarm(0)
	elif isinstance(details, tuple):
	  self.state = 'move'
	  self.body.go_to(details)
	elif details == 'b':
	  self.body.set_alarm(0)
	  self.state = 'build'
      if message == 'timer':
        try:
          nearest = self.body.find_nearest('Mantis')
	  self.body.follow(nearest)
	except ValueError:
	  nearest = None
	  print 'No more filthy Mantises'
	  self.state = 'idle'
	  self.body.stop()
	#print self.goal
	self.goal = nearest
	self.body.set_alarm(2)
      elif message == 'collide' and details['what'] == 'Mantis':
        # we meet again!
        mantis = details['who']
        mantis.amount -= 0.05 # take a tiny little bite
    if self.state == 'build':
      if self.body.amount <= 0.5:
	self.state = 'flee'
	self.body.set_alarm(0)
      if message == 'order':
	if details == 'i':
	  self.body.stop()
	  self.state = 'idle'
	elif details == 'a':
	  self.state = 'attack'
	  self.body.set_alarm(0)
        elif details == 'h':
	  self.state = 'harvest'
	  self.body.set_alarm(0)
        elif isinstance(details, tuple):
	  self.state = 'move'
	  self.body.go_to(details)
      if message == 'timer':
        try:
          nearest = self.body.find_nearest('Nest')
	  self.body.go_to(nearest)
	except ValueError:
	  nearest = None
	  print 'No more Nests'
	  self.state = 'idle'
	  self.body.stop()
	#print self.goal
	self.goal = nearest
	self.body.set_alarm(2)
      elif message == 'collide' and details['what'] == 'Nest':
        # we meet again!
        nest = details['who']
        nest.amount += 0.01
    if self.state == 'harvest':
      if self.body.amount <= 0.5:
	self.state = 'flee'
	self.body.set_alarm(0)
      if message == 'timer':
        if self.hasResource == True:
	  nearest = self.body.find_nearest('Nest')
	  self.body.go_to(nearest)
	else:
          try:
            nearest = self.body.find_nearest('Resource')
	    self.body.go_to(nearest)
	  except ValueError:
  	    nearest = None
	    print 'No more Resources'
	    self.state = 'idle'
	    self.body.stop()
	#print self.goal
	self.body.set_alarm(2)
      elif message == 'collide' and details['what'] == 'Resource' and self.hasResource == False:
        # we meet again!
	self.hasResource = True
        resource = details['who']
        resource.amount -= 0.25 # take a tiny little bite
	self.body.set_alarm(0)
      elif message == 'collide' and details['what'] == 'Nest' and self.hasResource == True:
        # we meet again!
	self.hasResource = False
        nest = details['who']
	self.body.set_alarm(0)
        #nest.amount += 0.01 # take a tiny little bite
      if message == 'order':
	if details == 'i':
	  self.body.stop()
	  self.state = 'idle'
	elif details == 'a':
	  self.state = 'attack'
	  self.body.set_alarm(0)
	elif isinstance(details, tuple):
	  self.state = 'move'
	  self.body.go_to(details)
    if self.state is 'flee':
      if self.body.amount >= 1.0:
	self.body.stop()
	self.state = 'idle'
      elif message == 'timer':
	nearest = self.body.find_nearest('Nest')
	self.body.go_to(nearest)
	self.body.set_alarm(2)
      elif message == 'collide' and details['what'] == 'Nest':
        nest = details['who']
	self.body.set_alarm(2)
        self.body.amount = 1.0
      elif message == 'order':
        # go to a random point, wake up sometime in the next 10 seconds
	#self.state = 
        #else:
	if details == 'a':
	  self.body.stop()
	  self.state = 'attack'
	  self.body.set_alarm(0)
        elif details == 'h':
	  self.state = 'harvest'
	  self.body.set_alarm(0)
	elif isinstance(details, tuple):
	  self.state = 'move'
	  self.body.go_to(details)
	elif details == 'b':
	  self.state = 'build'
	  self.body.set_alarm(0)


world_specification = {
  'worldgen_seed': 1222, # comment-out to randomize
  'nests': 2,
  'obstacles': 25,
  'resources': 5,
  'slugs': 5,
  'mantises': 5,
}

brain_classes = {
  'mantis': MantisBrain,
  'slug': SlugBrain,
}
