from bs4 import BeautifulSoup
from datetime import datetime


class Task:
    _module = ""
    _nameOfTask = ""
    _dtPosted = ""
    _status = ""

    def __init__(self):
        pass

    @property
    def module(self):  # this is getter for module
        return self._module

    @module.setter
    def module(self, m):
        self._module = m

    @property
    def nameOfTask(self):
        return self._nameOfTask

    @nameOfTask.setter
    def nameOfTask(self, n):
        self._nameOfTask = n

    @property
    def dtPosted(self):  # this is getter for module
        return self._dtPosted

    @dtPosted.setter
    def dtPosted(self, m):
        self._dtPosted = m

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, n):
        self._status = n


class Assignment(Task):
    _due = ""

    def __init__(self):
        pass

    @property
    def due(self):
        return self._due

    @due.setter
    def due(self, n):
        self._due = n


class Notification(Task):
    _notification = ""

    def __init__(self):
        pass

    @property
    def notification(self):
        return self._notification

    @notification.setter
    def notification(self, n):
        self._notification = n


class Announcement(Task):
    _summary = ""

    def __init__(self):
        pass

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, n):
        self._summary = n


class GradedTask(Task):
    _grade = 0
    _total = 100

    def __init__(self):
        pass

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, n):
        self._grade = n


if __name__ == '__main__':

    with open("a1.html") as fp:
      soup = BeautifulSoup(fp, 'html.parser')
      #lets start with what activity is happening
      totalItems = len(soup.select(".activity-stream li"))
      items = []
      status = []
      for string in soup.select(".activity-group-title"):
          status.append(repr(string.string))
      timeposted = []
      for string in soup.select("body li .date"):
          timeposted.append(repr(string.string))
      due = []
      for string in soup.select(".content bdi"):
          due.append(repr(string.string))
      module = []
      for string in soup.select('a[ng-switch-when="linkToCourse"]'):
          module.append(repr(string.string))
      title = []
      for string in soup.select(".name .js-title-link"):
          title.append(repr(string.string))
      summary = []
      for string in soup.select(".content .summary "):
          summary.append(repr(string.string))
      #Objects in important
      itemsImportant = soup.select('li[ng-repeat="item in important = baseStream.streamEntryLoader.buckets.important.view track by item.id"]')
      important = []
      for string in itemsImportant:
          important.append((repr(string)))
      for i in range(len(important)):
          for item in important:
              A = Assignment()
              A.status = "Upcoming"
              A.dtPosted = timeposted[i]
              A.due = due[i]
              A.module = module[i]
              A.nameOfTask = title[i]
              items.append(A)
              break
      itemsLeft = totalItems - len(important)
      filled = len(important)
      #gather objects in upcoming, always assignments
      itemsUpcoming = soup.select('li[ng-repeat="item in upcoming = baseStream.streamEntryLoader.buckets.upcoming.view track by item.id"]')
      upcoming = []
      for string in itemsUpcoming:
        upcoming.append((repr(string)))
      for i in range(len(upcoming)):
        for item in upcoming:
         A = Assignment()
         A.status = "Upcoming"
         A.dtPosted = timeposted[i+filled]
         A.due = due[i+filled]
         A.module = module[i+filled]
         A.nameOfTask = title[i+filled]
         items.append(A)
         break
      itemsLeft = totalItems - len(upcoming)
      filled += len(upcoming)
      # Items in Today
      itemsToday = soup.select('li[ng-repeat="item in today = baseStream.streamEntryLoader.buckets.today.view track by item.id"]')
      comparison1 = soup.select('li[ng-repeat="item in today = baseStream.streamEntryLoader.buckets.today.view track by item.id"] .date')
      comparison2 = soup.select('li[ng-repeat="item in upcoming = baseStream.streamEntryLoader.buckets.upcoming.view track by item.id"] .date')
      for i in comparison2:
          count = 0;
          count1 = 0;
          for j in comparison1:
              if j == i:
                  itemsToday.pop(count)
                  for obj in items:
                      count2 = 0
                      if count2 == count1:
                          obj.status = "Today"
                      count2 += 1
                  break
              count += 1
          count1 += 1
      today = []
      for string in itemsToday:
        today.append((repr(string)))
      for item in today:
          for i in range(len(today)):
              if("bb-ui-icon-grades" in item):
                  G = GradedTask()
                  G.status = "Today"
                  G.dtPosted = timeposted[i+filled]
                  G.due = due[i+filled]
                  G.module = module[i+filled]
                  G.nameOfTask = title[i+filled]
                  items.append(G)
                  break
              elif("bb-ui-icon-kudos" in item):
                  N = Notification()
                  N.status = "Today"
                  N.dtPosted = timeposted[i + filled]
                  N.module = module[i + filled]
                  N.nameOfTask = title[i+filled]
                  N.notification = summary[i]
                  items.append(N)
                  break
              elif("bb-ui-icon-assignment" or "bb-ui-icon-test" in item):
                  A = Assignment()
                  A.status = "Today"
                  A.dtPosted = timeposted[filled+i]
                  A.due = due[filled+i]
                  A.module = module[filled+i]
                  A.nameOfTask = title[filled+i]
                  items.append(A)
                  break
      print(len(items))
      for i in items:
          print(i)
      dates = []
      for i in items:
          dates.append(i.dtPosted)
      for i in items:
          print(i.status)

      def noOfObjectStatus(status):
          count = 0
          for i in items:
              if i.status == status:
                  count += 1
          return count


      print(noOfObjectStatus("Today"))
      def objectsAccordingStatus(status):
          objects = []
          for i in items:
              if i.status == status:
                  objects.append(i)
          return objects

      def objectsAccodringName(name):
          objects = []
          for i in items:
              if i.nameOfTask == name:
                  objects.append(i)
          return objects

      def objectsAccodringModule(module):
          objects = []
          for i in items:
              if module in i.module:
                  objects.append(i)
          return objects

      def objectsAccordingdtposted_sorted():
          dates = []
          for i in items:
              dates.append(i.dtPosted)
          dates.sort(key=lambda date: datetime.strptime(date, '%d %b %Y'))
          return dates

      def assiAccordingDue_sorted():
          dates = []
          for i in items:
              dates.append(i.dtPosted)
          dates.sort(key=lambda date: datetime.strptime(date, '%d %b %Y'))
          return dates
