import csv
import re
import datetime
import os


class Entry():

    '''Entry class is responsible for handling individual work log entries
    stored in the accompanying .csv file for this project, work_log.csv
    Entry class has methods for adding an entry to this file, searching for
    entries within the file and editing entries within the
    file, including deletion.
    All matches to a search are stored in dictionaries, the key of each
    dictionary indexing a search match; the value details the work log entry
    details of the corresponding search match. Indexing entries within the
    file allows entries to be edited, deleted as required.
    '''

    FILE = 'work_log.csv'

    def add_entry_to_file(self, *args):
        # entries are added to .csv file line by line

        with open(self.FILE, 'a') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=' ',
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

    def search_by_range_of_dates(self, start_date, end_date):
        matched = {}
        for date in self.daterange(start_date, end_date):
            matched.update(self.search_by_date(date.strftime('%d/%m/%Y')))
        return matched

    def daterange(self, start_date, end_date):
        # generator function, yielding a range of dates to be searched over.
        start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
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
        # regex patterns are compared with the strings for entry titles and
        # notes
        matches = {}
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ',
                                    lineterminator='\n')
            for line_num, line in enumerate(csv_reader):
                if re.search(pattern, line[1]) or re.search(pattern, line[3]):
                    matches[line_num] = line
        return matches

    def search_by_time_spent(self, time):
        matches = {}
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ',
                                    lineterminator='\n')
            for line_num, line in enumerate(csv_reader):
                if line:
                    if line[2] == time:
                        matches[line_num] = line

        return matches

    def edit_file(self, action, n, entry):
        lines = {}
        # the lines of the file are read into a dictionary ...
        with open(self.FILE, 'r') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=' ',
                                    lineterminator='\n')

            for line_num, line in enumerate(csv_reader):
                if line_num == n:
                    if action == 'edit':  # ... a line is amended ...
                        lines[n] = entry
                    if action == 'delete':  # ... or, a line is not included,..
                        continue
                else:
                    lines[line_num] = line

        # ... the file is then rewritten
        with open(self.FILE, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=' ',
                                    lineterminator='\n')
            # ... using values of the new dictionary.
            for num, line in lines.items():
                csv_writer.writerow(lines[num])

