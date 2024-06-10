from Scheduler.task import *


class Scheduler:
    TICK = 1
    SCH_MAX_TASKS = 40
    SCH_tasks_G = []
    current_index_task = 0

    def __int__(self):
        return

    def SCH_Init(self):
        self.current_index_task = 0

    def SCH_Add_Task(self, pFunction, DELAY, PERIOD,AREA):
        if self.current_index_task < self.SCH_MAX_TASKS:
            aTask = Task(pFunction, DELAY / self.TICK, PERIOD / self.TICK)
            aTask.TaskID = self.current_index_task
            aTask.Area= AREA
            self.SCH_tasks_G.append(aTask)
            self.current_index_task += 1
        else:
            print("PrivateTasks are full!!!")

    def SCH_Update(self):
        for i in range(0, len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].Delay > 0:
                self.SCH_tasks_G[i].Delay -= 1
            elif self.SCH_tasks_G[i].Delay==0:
                if self.SCH_tasks_G[i].Period>0 :
                    self.SCH_tasks_G[i].Delay = self.SCH_tasks_G[i].Period
                    self.SCH_tasks_G[i].RunMe += 1
                else :
                    
                    self.SCH_tasks_G[i].Delay=-1
                    self.SCH_tasks_G[i].RunMe += 1

    def SCH_Dispatch_Tasks(self):
        for i in range(0, len(self.SCH_tasks_G)):
            if self.SCH_tasks_G[i].RunMe > 0:
                self.SCH_tasks_G[i].RunMe -= 1
                print("Phân khu ",self.SCH_tasks_G[i].Area)
                print("\n")
                self.SCH_tasks_G[i].pTask(i,self.SCH_tasks_G[i].Area)
                print("Kết thúc lịch tưới")

    def SCH_Delete(self):
        print("Xóa hết lịch tưới")
        for i in range(len(self.SCH_tasks_G)):
            del self.SCH_tasks_G[i]
        return
    

    def SCH_GenerateID(self):
        return -1
