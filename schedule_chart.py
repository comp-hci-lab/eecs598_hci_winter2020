class Schedule_Chart():

	def __init__(self, phrase, perceptTime):

		#Phrase to be parsed
		self.phrase = phrase
		#User given base time to perform perceptual operator
		self.perceptTime = perceptTime


		#Initialize empty queues for each operator type
		self.perceptual_queue = []
		self.cognitive_queue = []
		self.motor_queue = []

		#Index used for schedule chart generation
		self.percept_ind = 0
		self.cogn_ind = 0
		self.motor_ind = 0

		#Finished list of uniq indexes
		self.finished = []

		#Fitts Law previous letter; initialized to NOVALUE
		self.prev_letter = "NOVALUE"

		#Index used for critical path time finding
		self.percept_crit_ind = 0
		self.cogn_crit_ind = 0
		self.motor_crit_ind = 0
		parsePhrase()

	def parsePhrase(self):
		uniq_num = 0
		dependent = []
		endPhrase = False

		for word in self.phrase.split():
			#Add enitre word into perceptual, only dependent on previous perceptual if those exist
			if self.percept_ind != 0:
				dependent.append(self.perceptual_queue[self.percept_ind-1].uniq_num)
			self.perceptual_queue.append(Chart_Input(word, dependent, uniq_num, True))
			uniq_num += 1
			dependent = []
			self.percept_ind += 1

			#Add entire word into cognitive, dependent on the entire word just added to perceptual and previous cognitve
			if self.cogn_ind != 0:
				dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
			dependent.append(uniq_num - 1)
			self.cognitive_queue,append(Chart_Input(word, dependent, uniq_num, True))
			uniq_num += 1
			dependent = []
			self.cogn_ind += 1

			for letter in word:
				#If letter is uppercase have to add shift key
				if letter.isupper():
					#add shift key into cognitive, represents thinking about needing to type key
					#dependent only on previous cognitive
					dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
					self.cognitive_queue.append(Chart_Input("shift_key", dependent, uniq_num, False))
					uniq_num += 1
					dependent = []
					self.cogn_ind += 1

					#COULD ADD VISUAL SEARCH OF LOOKING FOR KEYS/THINKING ABOUT KEYS

					#Press key
                    #Dependent on thinking of typing the key and previous motor
                    if self.motor_ind != 0:
                    	dependent.append(self.motor_queue[self.motor_ind-1].uniq_num)
                    dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
                    self.motor_queue.append(Chart_Input("shift_key", dependent, uniq_num, False))
                    uniq_num += 1
                    dependent = []
                    self.motor_ind += 1
                letter = letter.lower()
				#add shift key into cognitive, represents thinking about needing to type key
				#dependent only on previous cognitive
				dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
				self.cognitive_queue.append(Chart_Input(letter, dependent, uniq_num, False))
				uniq_num += 1
				dependent = []
				self.cogn_ind += 1

				#COULD ADD VISUAL SEARCH OF LOOKING FOR KEYS/THINKING ABOUT KEYS

				#Press key
                #Dependent on thinking of typing the key and previous motor
                if self.motor_ind != 0:
                	dependent.append(self.motor_queue[self.motor_ind-1].uniq_num)
                dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
                self.motor_queue.append(Chart_Input(letter, dependent, uniq_num, False))
                uniq_num += 1
                dependent = []
                self.motor_ind += 1

                if letter == '.' or letter == '?' or letter == '!':
                	endPhrase = True
            if not endPhrase:
            	#add space key into cognitive, represents thinking about needing to type key
				#dependent only on previous cognitive
				dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
				self.cognitive_queue.append(Chart_Input("space_bar", dependent, uniq_num, False))
				uniq_num += 1
				dependent = []
				self.cogn_ind += 1

				#COULD ADD VISUAL SEARCH OF LOOKING FOR KEYS/THINKING ABOUT KEYS

				#Press key
                #Dependent on thinking of typing the key and previous motor
                if self.motor_ind != 0:
                	dependent.append(self.motor_queue[self.motor_ind-1].uniq_num)
                dependent.append(self.cognitive_queue[self.cogn_ind-1].uniq_num)
                self.motor_queue.append(Chart_Input("space_bar", dependent, uniq_num, False))
                uniq_num += 1
                dependent = []
                self.motor_ind += 1

    def get_crit_path_time(self):
    	#Use Breadth First Search to generate critical path time
    	while self.percept_crit_ind != self.percept_ind and canRun(self.perceptual_queue[self.percept_crit_ind].dependent):
    		perceptUpdate()

    	while self.cogn_crit_ind != self.cogn_ind and canRun(self.cognitive_queue[self.cogn_crit_ind].dependent):
    		cognUpdate()

    	while self.motor_crit_ind != self.motor_ind and canRun(self.motor_queue[self.motor_crit_ind].dependent):
    		motorUpdate()

    	if self.motor_crit_ind != self.motor_ind:
    		get_crit_path_time()

    def canRun(self, dependent):
    	amount = 0
    	for fin in self.finished:
    		for depend in dependent:
    			if fin == depend:
    				amt += 1

    	return amount == len(dependent)

   	def findStart(self, dependent):
   		#Find latest dependent end time to find where this next one can start
   		maxVal = -10
   		compare = 0
   		for depend in dependent:
   			compare = findCompare(depend)
   			if compare > maxVal:
   				maxVal = compVal

   		return maxVal

   	def findCompare(self, uniq_find):
   		for percept in self.perceptual_queue:
   			if percept.uniq_num == uniq_find:
   				return percept.end

   		for cogn in self.cognitive_queue:
   			if cogn.uniq_num == uniq_find:
   				return cogn.end

   		for motor in self.motor_queue:
   			if motor.uniq_num == uniq_find:
   				return motor.end

    def perceptUpdate(self):
    	if len(self.finished) == 0:
    		self.perceptual_queue[self.percept_crit_ind].start = 0
    		self.perceptual_queue[self.percept_crit_ind].end = self.perceptTime
    	else:
    		self.perceptual_queue[self.percept_crit_ind].start = findStart(self.perceptual_queue[self.percept_crit_ind].dependent)

    		if self.perceptual_queue[self.percept_crit_ind].isWord:
    			#Update end time for perceptual adding full word
    		else:
    			#Update perceptual for finding letter for each letter for visual search

    	finished.append(self.perceptual_queue[self.percept_crit_ind].uniq_num)
    	self.percept_crit_ind += 1


    def cognUpdate(self):
    	self.cognitive_queue[self.cogn_crit_ind].start = findStart(self.cognitive_queue[self.cogn_crit_ind].dependent)

    	if self.cognitive_queue[self.cogn_crit_ind].isWord:
    		#Increment end time by amount of time takes to take in full word
    	else:
    		#Increment end time by amount of time it takes to think of letter

    	finished.append(self.cognitive_queue[self.cogn_crit_ind].uniq_num)
    	self.cogn_crit_ind += 1


  	def motorUpdate(self):
  		self.motor_queue[self.motor_crit_ind].start = findStart(self.motor_queue[self.motor_crit_ind].dependent)

  		if self.prev_letter == "NOVALUE":
  			#Increment end time by base level for motor provided by user
  		else:
  			#Increment end time by Fitts law equation for moving finger from one letter to next

  		finished.append(self.motor_queue[self.motor_crit_ind].uniq_num)
  		self.motor_crit_ind += 1


class Chart_Input():

	def __init__(self, item, dependent, num, isWord=False, start=0, end=0):
		self.item = item
		self.dependent = dependent[:]
		self.uniq_num = num
		self.start = start
		self.end = end
		self.isWord = isWord
