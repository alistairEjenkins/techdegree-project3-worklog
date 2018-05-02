import csv
import re
import datetime
import os

class Entry():

    FILE = 'work_log.csv'

    def add_entry_to_file(self, *args):

        with open (self.FILE, 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter= ' ',
                                    lineterminator='\n')
            csv_writer.writerow(args)

    def search_by_date(self, date):

        matches = {}
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ',
                                  lineterminator='\n')
            for line_num, line in enumerate(csv_reader):
                if line:
                    if line[0] == date:
                        matches[line_num] = line

        return matches

    def search_by_range_of_dates(self,start_date, end_date):

        matched = {}
        for date in self.daterange(start_date, end_date):
            matched.update(self.search_by_date(date.strftime('%d/%m/%Y')))
        return matched

    def daterange(self, start_date, end_date):
        start_date = datetime.datetime.strptime(start_date,'%d/%m/%Y')
        end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
        for day in range(int((end_date - start_date).days + 1)):
            yield start_date + datetime.timedelta(day)


    def exact_search(self, entry):

        matches = {}
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ',
                                  lineterminator='\n')
            for line_num, line in enumerate(csv_reader):
                if line == entry:
                    matches[line_num] = line

        return matches

    def regex_search(self, pattern):

        matches = {}
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ',
                                  lineterminator='\n')
            for line_num, line in enumerate(csv_reader):
                if (re.search(r'{}'.format(pattern), line[1])
                    or re.search(r'{}'.format(pattern), line[3])):

                    matches[line_num] = line
        return matches

    def edit_file(self,action, n , entry):

        lines = {}
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ', lineterminator='\n')

            for line_num, line in enumerate(csv_reader):
                if line_num == n:
                    if action == 'edit':
                        lines[n] = entry
                    if action == 'delete':
                        continue
                else:
                    lines[line_num] = line

        with open(self.FILE, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter= ' ',
                                    lineterminator='\n')

            for num, line in lines.items():
                csv_writer.writerow(lines[num])


