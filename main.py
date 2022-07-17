import poemthing
import threading



class myThread (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    
    def run(self):
      poemthing.generate_poem()
      if poemthing.generate_poem == True:
        print("Exiting " + self.name)
        threading.Thread.join()
      

thread1 = myThread("Thread-1")
thread1.start()


while True:
    

    topic = input("Enter topic phrase or word: ")

    if len(topic) >= 20:
        print("Topic is too long")
        
   

    
    poemthing.topicq.put(topic)

    

    if thread1.is_alive() == False:
        
        thread1 = myThread("Thread-" + str(threading.active_count() + 1))
        thread1.start()
    else:
        print("Thread is already running")
       
    