class Schedule_Chart():

	def __init__(self, phrase):
		self.phrase = phrase
		self.perceptual_queue = []
		self.cognitive_queue = []
		self.motor_queue = []
		parsePhrase()

	def parsePhrase():
		uniq_num = 0
		percept_ind = 0
		cogn_ind = 0
		motor_ind = 0
		dependent = []
		endPhrase = False

		for word in self.phrase.split():
			#Add enitre word into perceptual, only dependent on previous perceptual if those exist
			if percept_ind != 0:
				dependent.append(self.perceptual_queue[percept_ind-1].uniq_num)
			self.perceptual_queue.append(Chart_Input(word, dependent, uniq_num, True))
			uniq_num += 1
			dependent = []
			percept_ind += 1

			#Add entire word into cognitive, dependent on the entire word just added to perceptual and previous cognitve
			if cogn_ind != 0:
				dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
			dependent.append(uniq_num - 1)
			self.cognitive_queue,append(Chart_Input(word, dependent, uniq_num, True))
			uniq_num += 1
			dependent = []
			cogn_ind += 1

			for letter in word:
				#If letter is uppercase have to add shift key
				if(letter.isupper()):
					#add shift key into cognitive, represents thinking about needing to type key
					#dependent only on previous cognitive
					dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
					self.cognitive_queue.append(Chart_Input("shift_key", dependent, uniq_num, False))
					uniq_num += 1
					dependent = []
					cogn_ind += 1

					#COULD ADD VISUAL SEARCH OF LOOKING FOR KEYS

					#Press key
                    #Dependent on thinking of typing the key and previous motor
                    if motor_ind != 0:
                    	dependent.append(self.motor_queue[motor_ind-1].uniq_num)
                    dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
                    self.motor_queue.append(Chart_Input("shift_key", dependent, uniq_num, False))
                    uniq_num += 1
                    dependent = []
                    motor_ind += 1
                letter = letter.lower()
				#add shift key into cognitive, represents thinking about needing to type key
				#dependent only on previous cognitive
				dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
				self.cognitive_queue.append(Chart_Input(letter, dependent, uniq_num, False))
				uniq_num += 1
				dependent = []
				cogn_ind += 1

				#COULD ADD VISUAL SEARCH OF LOOKING FOR KEYS

				#Press key
                #Dependent on thinking of typing the key and previous motor
                if motor_ind != 0:
                	dependent.append(self.motor_queue[motor_ind-1].uniq_num)
                dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
                self.motor_queue.append(Chart_Input(letter, dependent, uniq_num, False))
                uniq_num += 1
                dependent = []
                motor_ind += 1

                if letter == '.' or letter == '?' or letter == '!':
                	endPhrase = True
            if not endPhrase:
            	#add space key into cognitive, represents thinking about needing to type key
				#dependent only on previous cognitive
				dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
				self.cognitive_queue.append(Chart_Input("space_bar", dependent, uniq_num, False))
				uniq_num += 1
				dependent = []
				cogn_ind += 1

				#COULD ADD VISUAL SEARCH OF LOOKING FOR KEYS

				#Press key
                #Dependent on thinking of typing the key and previous motor
                if motor_ind != 0:
                	dependent.append(self.motor_queue[motor_ind-1].uniq_num)
                dependent.append(self.cognitive_queue[cogn_ind-1].uniq_num)
                self.motor_queue.append(Chart_Input("space_bar", dependent, uniq_num, False))
                uniq_num += 1
                dependent = []
                motor_ind += 1



class Chart_Input():

	def __init__(self, item, dependent, num, isWord=False, start=0, end=0):
		self.item = item
		self.dependent = dependent[:]
		self.uniq_num = num
		self.start = start
		self.end = end
		self.isWord = isWord
