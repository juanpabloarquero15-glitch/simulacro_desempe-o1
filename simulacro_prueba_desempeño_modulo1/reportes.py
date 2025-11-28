import asyncio
class reports_and_time:
    __current_time : list[int, int, int]
    __current_date: list[int, int, int]
    __time_interval = 10 #Normal time interval, can be aumented
    __report:list
    __simulate:bool

    @classmethod
    async def run_time(cls):
        """
        starts the simulation time for the program
        executes async from the main flow each second
        MUST NOT be called befor set_date and set_time class methods
        """
        while cls.__simulate:
            await asyncio.sleep(1)
            cls.__current_time[2] += cls.__time_interval
            if cls.__current_time[2] > 60: # Seconds
                time_skip = cls.__current_time[2]%60
                cls.__current_time[2] += -time_skip*60
                cls.__current_time[1] += time_skip #A minute passed
            if cls.__current_time[1] > 60: # Minutes
                time_skip = cls.__current_time[1]%60
                cls.__current_time[1] += -time_skip*60
                cls.__current_time[0] += time_skip #An hour passed
            if cls.__current_time[0]>24: #Hours
                time_skip = cls.__current_time[0]%24
                cls.__current_time[0] += -time_skip*24
                cls.__current_date[0] += time_skip #A day passed
            if cls.__current_date[0] > 30: #Days (Only 30 days months)
                time_skip = cls.__current_date[2]%30 
                cls.__current_date[0] += -time_skip*30
                cls.__current_date[1] += time_skip #A month passed
            if cls.__current_date[1]>12: # Months
                time_skip = cls.__current_date[1]%12
                cls.__current_date[1] += -time_skip*12
                cls.__current_date[2] += time_skip #A year passed
    @classmethod
    def set_date(cls, day, month, year):
        """
        sets date on class attribute __current_date
        [day, month, year] -> all must be integers
        """
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except:
            print(f"All of the values must be an integer number, day: {day}, month: {month} oy year: {year} are/is an invalid value")
            return
        cls.__current_date = [day, month, year]
    @classmethod
    def set_time(cls, hour, minute, second):
        try:
            hour = int(hour)
            minute = int(minute)
            second = int(second)
        except:
            print(f"All of the values must be Integers, there's one or multiple invalid values in the entries: hour: {hour}, minute: {minute}, second: {second}")
            return
        cls.__current_time = [hour, minute, second]
    @classmethod
    def change_time_flow(cls, value):
        """
        Changes the time, the value represents the amount of seconds the simulated time moves forward each real time second
        """
        try:
            value = int(value)
        except:
            print(f"the value {value} is invalid, must be an integer number")
    @classmethod
    def stop_time(cls):
        cls.__simulate = False
    @classmethod
    def start_time(cls):
        cls.__simulate = True
        asyncio.run(cls.run_time)