# -*- coding: utf-8 -*-
import random


class Hammurabi:
    '''Main game class - contains all needed methods and output'''
    def __init__(self):
        #set all the constant variables
        self.__gameRunning = True
        self.__maxTurns = 10
        self.__baseLandValue = 16
        self.__plagueProbability = 0.15
        self.__ratsProbability = 0.4
        self.__starvePercentUprising = 0.45
        self.__grainNeededPerAcre = 2
        self.__grainPersonRequires = 20
        self.__acresPersonFarms = 10
        #set initial game variables
        self.__turn = 1;
        self.__grain = 0
        self.__land = 1000
        self.__people = 95
        self.__grainRatsEaten = 200
        self.__peopleStarved = 0
        self.__peopleImmigrated = 5
        self.__peopleDiseased = 0
        self.__grainAcreGrown = 3
        self.__landValue = self.get_land_price()
        #create accumulation variables for game-end evaluation
        self.__totalStarved = 0
        self.__summedPopulation = 0
        self.__initialAcresPerson = round(self.__land / self.__people)
        #create prompt variables - used by Alexa to keep track of input
        self.grainFed = -1
        self.landSold = -1
        self.landBought = -1
        self.grainPlanted = -1
        
        
    """RULES
    - each person needs 20 bushels/year to survive
    - each person can farm a max of 10 acres of land
    - 2 bushels of grain plants 1 acre of land
    - each turn, 15% chance of plague that kills half of population
    - if more than 45% of people starve, uprising - you get overthrown and game ends
    - more people come if you feed more than needed:
        (20 * current_acres * grain_stored) / (100 * population) + 1
    - you harvest 1-6 grain per acre (randoom)
    - 40% chance that 10-30% of grain is eaten by rats
    - land value is 17 - 23 (16 + 1d7)
    - game lasts 10 years
    """
    
    def update_turn(self):
        #reset holder variables
        self.grainFed = -1
        self.landSold = -1
        self.landBought = -1
        self.grainPlanted = -1
        #by now, these variables have been updated or set for the next turn:
        #__grain, __land, __peopleStarved, __peopleImmigrated
        #check 1 - did you starve too many people?
        if self.check_for_uprising():
            self.__gameRunning = False
            return """You starved {} people in one year! Due to this extreme
                mismanagement, you have not only been impeached and thrown out of
                office, but you have also been declare National Fink!!!""".format(self.__peopleStarved)
        #check 2 - is term over? if so, evaluate performance
        if self.__turn >= self.__maxTurns:
            peopleLeft = self.__people + self.__peopleImmigrated - self.__peopleStarved
            finalAcresPerson = self.__land / peopleLeft
            avgPercentStarved = self.__totalStarved / self.__summedPopulation
            
            finalStr = """In your {} year term of office, {} percent of the population starved per 
                year on average, and a total of {} people starved. You started with {} 
                acres per person, and ended with {} acres per person.""".format(self.__maxTurns
                , avgPercentStarved, self.__totalStarved, self.__initialAcresPerson
                , finalAcresPerson)
            
            if avgPercentStarved > 0.33 or finalAcresPerson < 7:
                finalStr += """Due to this extreme mismanagement, you have not only been impeached and thrown out of
                    office, but you have also been declare National Fink!!!"""
            elif avgPercentStarved > 0.1 or finalAcresPerson < 9:
                finalStr += """Your heavy-handed performance smacks of Nero and Ivan IC. The remaining people find you an unpleasant
                    leader and, frankly, hate your guts!!!"""
            elif avgPercentStarved > 0.03 or finalAcresPerson < 10:
                finalStr +=  """Your performance could have been somewhat better, but really wasn't too bad at all."""
            else:
                finalStr += """A fantastic performance! Charlemagne, Disraeli, and Jefferson combined could not have done better!"""
                
            self.__gameRunning = False
            return finalStr
        #check 3 - did we get hit by a plague?
        if self.have_plague():
            peopleLeft = self.__people + self.__peopleImmigrated - self.__peopleStarved
            self.__totalDiseased = round(peopleLeft / 2)
        else:
            self.__totalDiseased = 0
        #check 4 - get rat damage (if any)
        self.__grainRatsEaten = self.get_rat_damage()
        
        
    def check_game_running(self):
        return self.__gameRunning
        
    def get_status_str(self):
        updatedPeople = self.__people + self.__peopleImmigrated - self.__peopleStarved - self.__peopleDiseased
        harvestedGrain = self.__grainAcreGrown * self.__land
        currentGrain = self.__grain + harvestedGrain - self.__grainRatsEaten
        
        statusStr = ""
        if self.__peopleDiseased > 0:
            statusStr += "Horrors! A plague killed half your people!"
        
        statusStr += """In Year {}, {} people starved and {} came to the city.
        The population is now {}.
        Your country controls {} acres.
        Your people harvested {} bushels per acre
        Rats ate {} bushels.
        You have {} bushels in store.
        Land is trading at {} bushels an acre.""".format(
            self.__turn, self.__peopleStarved, self.__peopleImmigrated
            , updatedPeople, self.__land, self.__grainAcreGrown
            , self.__grainRatsEaten, currentGrain, self.__landValue)
        
        self.__people = updatedPeople
        self.__grain = currentGrain
        
        
        return statusStr
    
    def get_current_grain(self):
        return "You currently have {} bushels of grain.".format(self.__grain)
    def get_current_land(self):
        return "You currently have {} acres of land.".format(self.__land)
    def get_current_people(self):
        return "Your kingdom currently has {} people.".format(self.__people)

    
    def get_short_status(self):
        return """You have {} bushels of grain, {} acres of land
            , and {} people.""".format(self.__grain, self.__land, self.__people)
    
    def get_land_price(self):
        return random.randrange(1, 7) + self.__baseLandValue
    
    def get_grain_per_acre_grown(self):
        return random.randrange(1, 6)
    
    def have_plague(self):
        if random.random() < self.__plagueProbability:
            return True
        else:
            return False
    
    def get_rat_damage(self):
        if random.random() < self.__ratsProbability:
            grainPercentEaten = random.uniform(0.10, 0.30)
            return round(self.__grain * grainPercentEaten)
        return 0
    
    def check_for_uprising(self):
        if self.__peopleStarved > 0 and self.__people / self.__peopleStarved >= self.__starvePercentUprising:
            return True
        else:
            return False
    
    def get_help(self):
        return """The only help I can give you is the fact that it takes 
            {} bushels of grain as seed to plant an acre.""".format(self.__grainNeededPerAcre)
    
    def prompt_acres_buy(self):
        return "How many acres of land to you wish to buy at {} an acre?".format(self.__landValue)
    def process_acres_buy(self, acres):
        if acres * self.__landValue > self.__grain:
            return "You don't have enough grain for that."
        else:
            self.__land += acres
            self.__grain -= acres * self.__landValue
            self.landBought = acres
            return "Done"
    
    def prompt_acres_sell(self):
        return "How many acres of land to you wish to sell for {} an acre?".format(self.__landValue)
    def process_acres_sell(self, acres):
        if acres > self.__land:
            return "You don't have that much land."
        else:
            self.__land -= acres
            self.__grain += acres * self.__landValue
            self.landSold = acres
            return "Done"
    
    def prompt_feed_grain(self):
        return "How many bushels do you wish to feed your people? You have {} bushels.".format(self.__grain)
    def process_feed_grain(self, bushels):
        if bushels > self.__grain:
            return "You don't have that much grain."
        else:
            self.__grain -= bushels
            self.__summedPopulation += self.__people
            newPopulation = round(bushels / 20.0)
            if newPopulation > self.__people:
                self.__peopleImmigrated = newPopulation - self.__people
                self.__peopleStarved = 0
            elif newPopulation < self.__people:
                self.__peopleImmigrated = 0
                self.__peopleStarved = self.__people - newPopulation
                self.__totalStarved += self.__peopleStarved
            else:
               self.__peopleImmigrated = 0
               self.__peopleStarved = 0
            self.grainFed = bushels
            return "Done"
    
    def prompt_plant_grain(self):
        return "How many acres will you plant? You have {} acres.".format(self.__land)
    def process_plant_grain(self, acres):
        bushelsNeeded = acres * self.__grainNeededPerAcre
        peopleNeeded = round(acres / self.__acresPersonFarms)
        if acres > self.__land:
            return "You don't have that much land."
        elif bushelsNeeded > self.__grain:
            return "You don't have enough grain for that."
        elif peopleNeeded > self.__people:
            return "You don't have enough people for that."
        else:
            self.__grain -= bushelsNeeded
            self.grainPlanted = bushelsNeeded
            return "Done"