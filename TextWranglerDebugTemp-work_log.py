import datetime
import os
import sys
import re

from entry import Entry

e = Entry()


class Work_log():

    '''Worklog class provides functionality for user interactivity with
    their work log entries.
    The class provides a series of menu for adding entries and searching for
    entries. Entries matching to a search can be viewed, edited and deleted.
    Searches can be conducted according to the exact date of a work log
    entry, a range of dates, the exact details of an entry, or by a user
    supplied regular expression pattern.
    Users are suitably prompted to make choices from menu, supply entry details
    as required. Each menu and input prompt are linked for logical navigation.
    There is also an option to end the program.
    '''

    def display_main_menu(self):

        self.clear_screen()
        main_menu_options = {'a': self.add_entry, 'b': self.search_entries,
                             'c': self.quit_program}
        print('WORK LOG')
        print('What would you like to do?')
        print('a) Add new entry')
        print('b) Search for existing entries')
        print('c) Quit program')

        try:
            main_menu_choice = main_menu_options[input('> ')]
        except KeyError:
            input('That is not a valid choice. Please enter to try again')
            self.display_main_menu()
        else:
            main_menu_choice()

    def add_entry(self):

        e.add_entry_to_file(*self.get_entry_details())
        input('The entry has been added. Please enter to return to the menu.')
        self.display_main_menu()

    def get_entry_details(self):

        date = self.get_date()
        title = self.get_title()
        time_spent = self.get_time_spent()
        notes = self.get_notes()
        return date, title, time_spent, notes

    def get_date(self):

        getting_date = True
        while getting_date:
            self.clear_screen()
            print('Enter date, (DD/MM/YYYY)')
            entry_date = input('> ').strip()
            try:
                entry_date = datetime.datetime.strptime(entry_date, "%d/%m/%Y")
            except ValueError:
                input('Sorry, not a valid date. Press enter to try again.')
            else:
                getting_date = False
        return entry_date.strftime("%d/%m/%Y")

    def get_title(self):

        getting_title = True
        while getting_title:
            self.clear_screen()
            print('Enter entry title')
            title = input('> ').strip()
            if not title:
                input('Sorry, no title entered. Press enter to try again.')
            else:
                getting_title = False

        return title

    def get_time_spent(self):

        getting_time_spent = True
        while getting_time_spent:
            self.clear_screen()
            print('Enter time spent (rounded to nearest minute)')
            time_spent = input('> ').strip()
            try:
                time_spent = int(time_spent)
            except ValueError:
                input('Sorry, not a valid amount. Press enter to try again.')
            else:
                getting_time_spent = False
        return time_spent

    def get_notes(self):

        self.clear_screen()
        print('Notes (Optional, leave blank if required)')
        return input('>')

    def search_entries(self):

        self.clear_screen()
        search_menu_options = {'a': self.exact_date,
                               'b': self.range_of_dates,
                               'c': self.exact_search,
                               'd': self.regex_search,
                               'e': self.time_spent,
                               'f': self.display_main_menu}
        print('Do you want to search by?')
        print('a) Exact date')
        print('b) Range of dates')
        print('c) Exact search')
        print('d) Regex search')
        print('e) Time spent')
        print('f) Return to menu')
        try:
            search_menu_choice = search_menu_options[input('> ')]
        except KeyError:
            input('That is not a valid choice. Press enter to try again.')
            self.search_entries()
        else:
            self.clear_screen()
            search_menu_choice()

    def exact_date(self):

        input('Search by exact date. Press any key to continue.')
        self.search_results(e.search_by_date(self.get_date()))

    def range_of_dates(self):

        input('Search by a range of dates.\nStart date.'
              'Press any key to continue')
        start_date = self.get_date()
        input('End date. Press any key to continue')
        end_date = self.get_date()

        self.search_results(e.search_by_range_of_dates(start_date, end_date))

    def exact_search(self):

        input('Search by exact entry details. Press any key to continue')
        entry = list(self.get_entry_details())
        self.search_results(e.exact_search(entry))

    def regex_search(self):

        try:
            pattern = re.compile(
                input("Enter a regex pattern (pattern will be applied to "
                      "entry title and notes): "))
        except re.error:
            input('Not a valid pattern. Press enter to try again.')
            self.clear_screen()
            self.regex_search()
        else:
            self.search_results(e.regex_search(pattern))

    def time_spent(self):

        input('Search by time spent date. Press any key to continue.')
        self.search_results(e.search_by_time_spent(self.get_time_spent()))

    def search_results(self, matches):

        if not matches:
            print('There were no matches')
            input('Press enter to return to the search menu.')
            self.search_entries()

        # keys to matches are stored in a list to allow matches to allow user
        #  to view the next or previous match
        index = []
        for i in matches.keys():
            index.append(i)
        count = 0

        options = {'n': '[N]ext, ', 'e': '[E]dit, ',
                   'p': '[P]revious ', 'd': '[D]elete, ',
                   'enter': '[enter] to return to search menu'}

        while True:
            self.clear_screen()
            print('Date : {}'.format(matches[index[count]][0]))
            print('Title : {}'.format(matches[index[count]][1]))
            print('Time Spent : {}'.format(matches[index[count]][2]))
            print('Notes : {}'.format(matches[index[count]][3]))
            print('Result {} of {}'.format(count+1, len(index)))
            if count == 0:
                print('{n}{e}{d}{enter}'.format(**options))
                search_result_options = 'ned'
            elif count >= 1 and count < len(index) - 1:
                print('{n}{p}{e}{d}{enter}'.format(**options))
                search_result_options = 'nped'
            else:
                print('{p}{e}{d}{enter}'.format(**options))
                search_result_options = 'ped'

            while True:
                choice = input('> ')
                if choice not in search_result_options:
                    input('Not a valid option. Press enter to try again.')
                else:
                    break
            if choice == 'n':
                count += 1
                continue
            elif choice == 'p':
                count -= 1
                continue
            elif choice == 'e':
                self.edit_entry(index[count])
            elif choice == 'd':
                self.delete_entry(index[count], matches[index[count]])
            break
        self.search_entries()

    def edit_entry(self, line_num):

        input('Edit entry. Press any key to enter edit')
        entry = list(self.get_entry_details())
        e.edit_file('edit', line_num, entry)
        input('Edit made. Press enter to return to search menu')
        self.search_entries()

    def delete_entry(self, line_num, match):

        input('Press any key to delete entry.')
        e.edit_file('delete', line_num, match)
        input('Entry deleted. Press enter to return to search menu')
        self.search_entries()

    def quit_program(self):

        self.clear_screen()
        print('Thank you and goodbye.')
        sys.exit()

    def clear_screen(self):

        os.system('cls' if os.name == 'nt' else 'clear')


def main():
    w = Work_log()
    w.display_main_menu()


if __name__ == '__main__':
    main()

