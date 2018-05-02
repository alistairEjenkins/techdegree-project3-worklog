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

		self.clear_screen()
		print('Date of task:')
		try:
			date = datetime.datetime.strptime(input('> '), '%d/%m/%Y')
		except ValueError:
			input('That is not a valid time. Press enter to try again.')
			self.get_date()
		else:
			return date.strftime('%d/%m/%Y')

	def get_title(self):

		self.clear_screen()
		print('Title of task:')

		title = input('> ')
		if title:
			return title
		else:
			input('You have not entered a title for the task. Press enter to '
				  'try again')
			self.get_title()

	def get_time_spent(self):

		self.clear_screen()
		print('Time spent (rounded to nearest minute)')

		try:
			time_spent = int(input('> '))
		except ValueError:
			input('That is not a valid input. Press enter to try again.')
			self.get_time_spent()
		else:
			return str(time_spent)

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
							   'e': self.display_main_menu}
		print('Do you want to search by?')
		print('a) Exact date')
		print('b) Range of dates')
		print('c) Exact search')
		print('d) Regex search')
		print('e) Return to menu')
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

		input('Search by a range of dates.\nPress enter to '
			  'continue and enter start date.')
		start_date = self.get_date()
		self.clear_screen()
		input('Press enter to continue and enter end date.')
		end_date = self.get_date()
		
		if end_date < start_date:
			input('End date has to be after start date. Press enter to try again.')
			self.range_of_dates()

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

	def search_results(self, matches):

		count = 0
		for line_num, match in matches.items():
			count += 1
			self.clear_screen()
			print('Date : {}'.format(match[0]))
			print('Title : {}'.format(match[1]))
			print('Time Spent : {}'.format(match[2]))
			print('Notes : {}'.format(match[3]))
			print('Result {} of {}'.format(count, len(matches)))

			if count == len(matches):
				print('[E]dit, [D]elete, [enter] to return to search menu')
				search_result_options = 'ed'
			else:
				print('[N]ext, [E]dit, [D]elete, '
					  '[enter] to return to search menu')
				search_result_options = 'ned'

			while True:
				choice = input('> ')
				if choice not in search_result_options:
					input('Not a valid option. Press enter to try again.')
				else:
					break
			if choice == 'n':
				continue
			elif choice == 'e':
				self.edit_entry(line_num)
			elif choice == 'd':
				self.delete_entry(line_num, match)
			else:
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

