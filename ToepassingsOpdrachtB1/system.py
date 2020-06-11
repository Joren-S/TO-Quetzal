import time
import math
import datetime
import random

from wrapper import *

from System import bestelling
from System import chili
from System import Chocolademelk
from System import Chocoladeshot
from System import Marshmallow
from System import Gebruiker
from System import honing
from System import stock
from System import Werknemer
from System import History

class Systeem:
    def __init__(self):
        self.Stock = stock.stock()
        self.Werknemers = Wrapper(ADT_TYPE.BinaireZoekboom)
        self.Gebruikers = Wrapper(ADT_TYPE.RoodZwartBoom)
        self.Chocolademelken = Wrapper(ADT_TYPE.TweeDrieBoom)
        self.Bestellingen = Queue.queue()
        self.Workloads = Stack.Stack()

    def init(self):
        cmds = []
        cur_timeid = 0
        initialized = False
        started = False
        nieuweBestelling = False
        with open('input.txt') as inputfile:
            cmds = inputfile.readlines()
        for line in cmds:
            line.rstrip()
            if (line[0] is not '#'):
                args = line.split()
                if (args):

                    # nothing will be interpreted if 'init' isn't called.
                    if (args[0] == 'init'):
                        initialized = True

                    if (args[0] == 'start'):
                        self.makeMoment(0)
                        started = True
                       

                    # this requires the 'start' command to be called, since these commands require the time id argument.
                    if (started and len(args) > 1):
                        
                        # if the current command is on the next time id, we can no longer go back to the previous one, we also handle our orders.
                        time_id = int(args[0])
                        if (time_id > cur_timeid):
                            diff = time_id - cur_timeid
                            cur_timeid = time_id
                            for i in range(diff):
                                self.doBestellingen()


                        # we make sure nothing can be done in the past.
                        if (time_id < cur_timeid) is False:

                            if (args[1] == 'gebruiker'):
                                self.addGebruiker(args[2], args[3], args[4], time_id)

                            elif (args[1] == 'werknemer'):
                                self.addWerknemer(args[2], args[3], int(args[4]), time_id)
                        
                            elif (args[1] == 'bestel'):
                                nieuweBestelling = True
                                email = args[2]
                                choc_id = self.addChocoladeMelk()
                                ingredients = args[3:]
                                for ingredient in ingredients:
                                    if (ingredient == "wit" or ingredient == "melk" or ingredient == "bruin" or ingredient == "zwart"):
                                        self.addIngredient(choc_id, "shot_" + ingredient)
                                    elif (ingredient == "chili" or ingredient == "marshmallow" or ingredient == "honing"):
                                        self.addIngredient(choc_id, ingredient)
                                self.addBestelling(email, choc_id, time_id)

                        
                            elif (args[1] == 'stock'):
                                if (args[2] == 'shot'):
                                    date = time.mktime(datetime.datetime(int(args[5]), int(args[6]), int(args[7])).timetuple())
                                    self.addItemsToStock(args[2] + '_' + args[3], date, int(args[4]))
                                elif (args[2] == 'honing') or (args[2] == 'marshmallow') or (args[2] == 'chili'):
                                    date = time.mktime(datetime.datetime(int(args[4]), int(args[5]), int(args[6])).timetuple())
                                    self.addItemsToStock(args[2], date, int(args[3]))
                        
                            elif (args[1] == 'log'):
                                print("\n\nBestellingen:")
                                self.logBestellingen()
                                print("\n\nGebruikers:")
                                self.logGebruikers()
                                print("\n\nWerknemers:")
                                self.logWerknemers()
                                print("\n\nStocks:")
                                self.logStocks()

                                self.makeLog()
                    
                    # this is for the stock, users and employees who are already present when the system is started.
                    if (initialized and not started and len(args) > 1):
                        if (args[0] == 'shot'):
                            date = time.mktime(datetime.datetime(int(args[3]), int(args[4]), int(args[5])).timetuple())
                            self.addItemsToStock(args[0] + '_' + args[1], date, int(args[2]))
                        elif (args[0] == 'honing') or (args[0] == 'marshmallow') or (args[0] == 'chili'):
                            date = time.mktime(datetime.datetime(int(args[2]), int(args[3]), int(args[4])).timetuple())
                            self.addItemsToStock(args[0], date, int(args[1]))
                        elif (args[0] == 'gebruiker'):
                            self.addGebruiker(args[1], args[2], args[3], 0)
                        elif (args[0] == 'werknemer'):
                            self.addWerknemer(args[1], args[2], int(args[3]), 0)

                    if (started and len(args) > 1):
                        self.makeMoment(time_id, email, nieuweBestelling)

    # Bestellingen:

    def doBestellingen(self):
        #Queued, Busy, Finished, Cancelled
        allBestellingen = self.Bestellingen.traverse()
        allWorkers = self.Werknemers.traverse()
        for worker in allWorkers:
            worker.restoreWorkload()
        for bestelling in allBestellingen:
            if bestelling.getStatusAsString() == "Queued":
                worker_tup = self.Workloads.pop()
                if (worker_tup[1] == True):
                    worker = self.retrieveWerknemer(worker_tup[0][1])
                    if (worker is not None):
                        bestelling.setWorker(worker_tup[0][1])
                        bestelling.setStatus(1) # processing/busy
                        wl = worker.getMaxWorkload()
                        if wl == 0: # we patch an exploit causing the system to crash if a worker with workload 0 is added (divide by 0)
                            wl += 1
                        tot_wl = self.retrieveChocoladeMelk(bestelling.getChocolademelk()).getWorkload()                       
                        bestelling.setTimeRemaining(math.ceil(tot_wl / wl)) # we use ceil because if i.e. tot_wl uneven and wl is even -> round up to the next whole number since half times don't exist.

            if bestelling.getStatusAsString() == "Busy":
                worker = self.retrieveWerknemer(bestelling.getWorker())
                if (worker is not None):
                    t_r = bestelling.getTimeRemaining()
                    wl = worker.getMaxWorkload()
                    tot_wl = self.retrieveChocoladeMelk(bestelling.getChocolademelk()).getWorkload()     
                    if (t_r > 0):
                        # worker is still busy
                        worker.doWork(tot_wl / math.ceil(tot_wl / wl))
                        bestelling.setTimeRemaining(bestelling.getTimeRemaining() - 1)
                        t_r -= 1
                    if (t_r == 0):
                        # worker is finished working on order
                        # we don't need to call setWorker and change the worker inside the order. By doing so, we can later retrieve who did a specific order (that is finished) since the field 'worker' inside the order is unchanged :-)
                        # i.e we want to know who did order 'order1', which was ordered x time ago. We can still do order1.getWorker() and get a correct result. (for example, for complaints)
                        bestelling.setStatus(2) # finished
                        worker.restoreWorkload()
                        self.Workloads.push((worker.getMaxWorkload(), worker.getID()))



        return True

    def addBestelling(self, email, chocolademelkID, time_id):
        user = self.retrieveGebruiker(email)
        if user is not None:
            order = bestelling.bestelling(email, chocolademelkID, time_id)
            last_order = self.Bestellingen.getLast()
            if last_order is not None:
                if (last_order.getTijd() >= order.getTijd()):
                    order.setTijd(last_order.getTijd() + 0.001)
            if self.Bestellingen.enqueue(order):
                user.addBestelling(order)
                return True
        return False

    def annuleerBestellingen(self, email):
        user = self.retrieveGebruiker(email)
        if user is not None:
            amount = user.getBestellingCount()
            for i in range(amount):
                user.getBestellingen()[i].setStatus(bestelling.ORDER_STATE.Aborted)
            user.annuleerBestellingen()
            return True
        return False

    def retrieveBestellingen(self, email):
        user = self.retrieveGebruiker(email)
        if user is not None:
            return user.getBestellingen()
        return []

    def logBestellingen(self):
        count = 0
        bestellingen = self.Bestellingen.traverse()
        for best in bestellingen:
            count = count + 1
            choc = self.retrieveChocoladeMelk(best.getChocolademelk()).getIngredients() #(obj, str)
            print("\nBestelling #", count, ":")
            print("\tTime ID: ", best.getTimeID())
            print("\tID: ", best.getTijd())
            print("\tGebruiker: ", best.getEmail())
            if self.retrieveWerknemer(best.getWorker()):
                print("\tWerknemer: ", self.retrieveWerknemer(best.getWorker()).getNaam())
            if choc:
                print("\tIngredienten: ")
                for tup in choc:
                    print("\t\t", tup[1])
            print("\tStatus: ", best.getStatusAsString())

    def getCurrentBestellingWorkload(self, bestelling_obj, cur_time):
        werkn = self.retrieveWerknemer(bestelling_obj.getWorker())
        choc = self.retrieveChocoladeMelk(bestelling_obj.getChocolademelk())
        if werkn is not None and choc is not None:
            status = bestelling_obj.getStatus()
            if status == 1:  # processing
                wl_per_tick = werkn.getMaxWorkload()
                timeLeft = choc.getWorkload() - (wl_per_tick * (cur_time - bestelling_obj.getTimeID()))
                if timeLeft > 0:
                    return timeLeft
                else:
                    return ""
            elif status == 0:  # idle
                return choc.getWorkload()
            else:  # finished or cancelled
                return 0
        return -1

    # Gebruikers:

    def addGebruiker(self, voornaam, naam, email, timeID):
        GB_Obj = Gebruiker.Gebruiker(voornaam, naam, email, timeID)
        inserted = self.Gebruikers.insert(GB_Obj.getEmail(), GB_Obj)
        if inserted:
            return GB_Obj.getID()
        return -1

    def removeGebruiker(self, email):
        if self.annuleerBestellingen(email) is True:
            return self.Gebruikers.delete(email)
        return False
    
    def retrieveGebruiker(self, email):
        retrieval = self.Gebruikers.retrieve(email)
        if retrieval[1] is True:
            return retrieval[0]
        return None

    def buildRekening(self, email):
        totPrijs = 0
        gebruiker = self.retrieveGebruiker(email)
        if gebruiker is not None:
            cnt = gebruiker.getBestellingCount()
            for i in range(cnt):
                melkid = gebruiker.getBestellingen()[i].getChocolademelk()
                choc = self.retrieveChocoladeMelk(melkid)
                totPrijs += choc.getPrijs()
        return totPrijs

    def logGebruikers(self):
        gebruikers = self.Gebruikers.traverse()
        if gebruikers is None:
            return False
        for i in gebruikers:
            print("Email: ", i.getEmail(), "\n\tNaam: ", i.getNaam(), "\n\tID: ", i.getID(), "\n\tTime ID: ", i.getTimeID())
        return True


    # Werknemers:

    def addWerknemer(self, voornaam, naam, maxWorkload, timeID):
        WN_Obj = Werknemer.Werknemer(voornaam, naam, maxWorkload, timeID)
        insertion = self.Werknemers.insert(WN_Obj.getID(), WN_Obj)
        if insertion is True:
            workloadTuple = (WN_Obj.getMaxWorkload(), WN_Obj.getID())
            self.Workloads.push(workloadTuple)
            return WN_Obj.getID()
        return -1

    def removeWerknemer(self, id):
        workloadbuffer = []
        if self.Werknemers.delete(id) is True:
            while self.Workloads.isEmpty() is False:
                pop = self.Workloads.pop()[0]
                if pop[1] == id:
                    for i in range(len(workloadbuffer)):
                        self.Workloads.push(workloadbuffer[i])
                    return True
                workloadbuffer.append(pop)
            for i in range(len(workloadbuffer)):
                self.Workloads.push(workloadbuffer[i])
        return False

    def retrieveWerknemer(self, id):
        retrieval = self.Werknemers.retrieve(id)
        if retrieval[1] is True:
            return retrieval[0]
        return None

    def getWerknemers(self):
        werknemers = self.Werknemers.traverse()
        if werknemers is None:
            return False
        else:
            return werknemers

    def logWerknemers(self):
        werknemers = self.Werknemers.traverse()
        if werknemers is None:
            return False
        for i in werknemers:
            print("ID: ", i.getID(), "\n\tNaam: ", i.getNaam(), "\n\tWorkload: ", i.getMaxWorkload(), "\n\tTime ID: ", i.getTimeID())
        return True


    # Stocks:

    def addItemsToStock(self, itemType, vervaldatum, amount = 1, prijs = -1):

        my_array = []

        ingredient = None
        for i in range(amount):
            if itemType == "shot_wit":
                ingredient = Chocoladeshot.Chocoladeshot("shot_wit", vervaldatum + (0.01 * i), 1.0 if prijs == -1 else prijs)
                self.Stock.addShotWit(ingredient)

            if itemType == "shot_melk":
                ingredient = Chocoladeshot.Chocoladeshot("shot_melk", vervaldatum + (0.01 * i), 1.0 if prijs == -1 else prijs)
                self.Stock.addShotMelk(ingredient)
                
            if itemType == "shot_bruin":
                ingredient = Chocoladeshot.Chocoladeshot("shot_bruin", vervaldatum + (0.01 * i), 1.0 if prijs == -1 else prijs)
                self.Stock.addShotBruin(ingredient)

            if itemType == "shot_zwart":
                ingredient = Chocoladeshot.Chocoladeshot("shot_zwart", vervaldatum + (0.01 * i), 1.0 if prijs == -1 else prijs)
                self.Stock.addShotZwart(ingredient)

            if itemType == 'honing':
                ingredient = honing.honing(vervaldatum + (0.01 * i), 0.5 if prijs == -1 else prijs) 
                self.Stock.addHoning(ingredient)

            if itemType == 'marshmallow':
                ingredient = Marshmallow.Marshmallow(vervaldatum + (0.01 * i), 0.75 if prijs == -1 else prijs)
                self.Stock.addMarshmallow(ingredient)

            if itemType == 'chili':
                ingredient = chili.chili(vervaldatum + (0.01 * i), 0.25 if prijs == -1 else prijs)
                self.Stock.addChili(ingredient)

    def changePrice(self, itemTyoe, price):
        '''
        placeholder
        '''
        self.Stock.setPrice(itemTyoe, price)

    def purgeStock(self):
        '''
        placeholder
        '''
        return self.Stock.purge()
                
    def logStocks(self):
        print("Wit: ", self.Stock.getStockCount('shot_wit'))
        print("Melk: ", self.Stock.getStockCount('shot_melk'))
        print("Bruin: ", self.Stock.getStockCount('shot_bruin'))
        print("Zwart: ", self.Stock.getStockCount('shot_zwart'))
        print("Honing: ", self.Stock.getStockCount('honing'))
        print("Marshmallow: ", self.Stock.getStockCount('marshmallow'))
        print("Chili: ", self.Stock.getStockCount('chili'))
        return False

    # Chocolademelk:

    def addChocoladeMelk(self, prijs = 2.0):
        melk = Chocolademelk.Chocolademelk(prijs)
        if self.Chocolademelken.insert(melk.getID(), melk) is True:
            return melk.getID()
        return -1

    def retrieveChocoladeMelk(self, id):
        retrieval = self.Chocolademelken.retrieve(id)
        if retrieval[1] is True:
            return retrieval[0]
        return None

    def addIngredient(self, melkID, str_ingredient):
        melk = self.retrieveChocoladeMelk(melkID)
        if melk is not None:
            if str_ingredient == "shot_wit":
                ingredient = self.Stock.removeShotWit()
                if ingredient[1] is True:
                    return melk.addShotWit(ingredient[0])

            if str_ingredient == "shot_melk":
                ingredient = self.Stock.removeShotMelk()
                if ingredient[1] is True:
                    return melk.addShotMelk(ingredient[0])

            if str_ingredient == "shot_bruin":
                ingredient = self.Stock.removeShotBruin()
                if ingredient[1] is True:
                    return melk.addShotBruin(ingredient[0])

            if str_ingredient == "shot_zwart":
                ingredient = self.Stock.removeShotZwart()
                if ingredient[1] is True:
                    return melk.addShotZwart(ingredient[0])

            if str_ingredient == 'honing':
                ingredient = self.Stock.removeHoning()
                if ingredient[1] is True:
                    return melk.addHoning(ingredient[0])

            if str_ingredient == 'marshmallow':
                ingredient = self.Stock.removeMarshmallow()
                if ingredient[1] is True:
                    return melk.addMarshmallow(ingredient[0])

            if str_ingredient == 'chili':
                ingredient = self.Stock.removeChili()
                if ingredient[1] is True:
                    return melk.addChili(ingredient[0])

        return False

    # Logs

    def makeMoment(self, time_id, email="", nieuweBestelling=False):

        # All current ingredients are as follows:
        ingredients = ["shot_melk", "shot_wit", "shot_zwart", "shot_bruin", "honing", "marshmallow", "chili"]

        # Make a dict, with the ingredient as key, and the stock amount as value. e.g. {'shot_melk': 29}
        stock = dict()
        for i in ingredients:
            stock[i] = self.Stock.getStockCount(i)

        # Get werknemers from system as a list
        werknemers = self.getWerknemers()

        # If system got a new Bestelling, the bool nieuweBestelling is true. Bestelling are ordered by date, so the last
        # one is the newest one. If the bool is false, pass an empty string to object
        if nieuweBestelling:
            nieuwebestelling = self.retrieveBestellingen(email)[-1]
        else:
            nieuwebestelling = ""

        # Get the current workload stack to pass to object
        stack = self.Workloads.traverse()

        # Get all bestellingen
        bestellingen = self.Bestellingen.traverse()

        # Make a list of all queued bestellingen to pass to object
        wachtendebestellingen = []
        for i in bestellingen:
            if i.getStatusAsString() == "Queued":
                wachtendebestellingen.append(i)

        # Make a list of all busy bestellingen to pass to object
        processingbestellingen = []
        for i in bestellingen:
            if i.getStatusAsString() == "Busy":
                processingbestellingen.append(i)

        # This dict gets the bestelling worker as Key, and the workload remainder for his bestelling as Value.
        processingTimeLeft = dict()
        for i in processingbestellingen:
            for j in werknemers:
                if i.getWorker() == j.getID():
                    processingTimeLeft[j.getID()] = self.getCurrentBestellingWorkload(i, time_id)

        # print("New Moment:")
        # print("time_id:", time_id)
        # print("stack:", stack)
        # print("nieuwebestelling:", nieuwebestelling)
        # print("wachtendebestellingen:", wachtendebestellingen)
        # print("workloads:", workloads)
        # print("stock:", stock)
        # print("process:", processingTimeLeft)

        # Get werknemers from system as a list to pass to history object
        werknemers = self.getWerknemers()


        # Make a new history object. This object is added into a registry in the class itself
        History.History(time_id, stack, nieuwebestelling, wachtendebestellingen, stock, processingTimeLeft, werknemers)

    def makeLog(self):
        # Read the template file and copy its content to string 'logfile'
        # This template file contains placeholders %WERKNEMERS%, %INGREDIENTS% and
        # %BESTELLINGTABEL%, which are all replaced during this function. Output goes into a different file!

        logfile = open("System/log_template.html", 'r').read()

        # The following lines make the table header bar. For this we need
        # the different werknemers and ingredients from the system, at current time

        # Get all current Werknemers and make a header cell for each of them
        werknemers = self.getWerknemers()
        t_werknemers = ""
        for persoon in werknemers:
            t_werknemers += "<th>\n"
            t_werknemers += persoon.getNaam() + "\n"
            t_werknemers += "</th>\n"
        logfile = logfile.replace("%WERKNEMERS%", t_werknemers)

        # list all current ingredients: If a new type of ingredient is made, add here too!
        ingredient = ["shot_wit", "shot_melk", "shot_bruin", "shot_zwart", "honing", "marshmallow", "chili"]
        # Make a cell for each ingredient
        t_ingredient = ""
        for ingr in ingredient:
            t_ingredient += "<th>\n"
            t_ingredient += ingr + "\n"
            t_ingredient += "</th>\n"
        logfile = logfile.replace("%INGREDIENTS%", t_ingredient)

        # The following lines make up the table body
        # Each history object is a moment, each moment is a new row in table. Append all data to string t_table.
        # t_table will replace %BESTELLINGTABEL% in logfile, which will be saved to another file.

        t_table = ""

        # Get every 'moment' (=History object) from the History registry.
        for moment in History.History.getRegistry():
            # Start a new line (or clear its contents on non-first iteration)
            t_newline = ""

            # Use moment.getTijdstip() to get time_id at the time the moment was created.
            # Be sure to convert to string
            t_newline += "<tr>\n"
            t_newline += "<td>"
            t_newline += str(moment.getTijdstip())
            t_newline += "</td>"

            # Use moment.getWorkloadstack() to get the workload stack at the time the moment was created.
            # Add a | in the beginning of the cell, to symbolise our stack bottom. Because the list traversing our stack
            # is given from top to bottom, reverse it first to get the actual order.
            t_newline += "<td> | "
            first = True
            for i in reversed(moment.getStack()):
                if not first:
                    t_newline += ", "
                t_newline += str(i[0])
                first = False
            t_newline += "</td>"

            # For each werknemer, check if their ID is in a processing bestelling. If so, print their workload remaining
            # If they're not in moment.getWerknemers(), they have not been added to the system at this moment.
            # If none apply; the werknemer is just not doing anything.
            time_remaining_per_employee = moment.getBestellingTimeRemaining()
            for i in werknemers:
                    w_id = i.getID()
                    if w_id in time_remaining_per_employee:
                        t_newline += "<td>"
                        t_newline += str(time_remaining_per_employee[w_id])
                        t_newline += "</td>"
                    elif i not in moment.getWerknemers():
                        t_newline += "<td>-\n</td>"
                    else:
                        t_newline += "<td>\n</td>"

            # If this moment brings a new bestelling, put it in next cell.
            # for this we need to get the object that's created during the bestelling, and get its workload
            t_newline += "<td>"
            if moment.getNieuweBestelling():
                choc = self.retrieveChocoladeMelk(moment.getNieuweBestelling().getChocolademelk())
                t_newline += str(choc.getWorkload())
            t_newline += "</td>"

            # Get all wachtende bestellingen with moment.getWachtendeBestelling()
            t_newline += "<td>"
            first = True
            for i in moment.getWachtendeBestellingen():
                if not first:
                    t_newline += ", "
                choc = self.retrieveChocoladeMelk(i.getChocolademelk())
                t_newline += str(choc.getWorkload())
                first = False
            t_newline += "</td>"

            # Get all the ingredients their stock count from the dictionary.
            for i in ingredient:
                t_newline += "<td>"
                t_newline += str(moment.getStockCount(i))
                t_newline += "</td> \n"

            # End the table row. Append it to the string t_table.
            t_newline += "</tr> \n"
            t_table += t_newline

        # Replace the %BESTELLINGTABLE% placeholder with t_table.
        logfile = logfile.replace("%BESTELLINGTABLE%", t_table)

        # And store it in the output file (will be created new, or overwrite previous versions)
        with open("output_log.html", "w") as target:
            target.write(logfile)


# init

quetzal = Systeem()

# lees input.txt in en zijn cmds
quetzal.init()
