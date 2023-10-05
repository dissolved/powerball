import os
import csv
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = 'https://portalseven.com/lottery/powerball_jackpot_winners.jsp'
TABLE_ROW_CLASS_NAME = 'bg-light'
VALIDATING_DIRECTORY_STR = 'Validating directory...'
DIRECTORY_NOT_FOUND_STR = 'Directory not found. Please try again.'
CREATING_FILE_STR = 'Creating file in directory...'
WRITING_FILE_SUCCESS_STR = 'Successfully wrote to file: '


# Define functions

def get_html_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f'HTTP error occurred: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')
    else:
        return response.text

def get_table_rows_from_html(html_content):
    rows = []
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.select('div#myTabContent table')
    for table in tables:
        rows += table.find_all('tr')
    return rows

def parse_rows(rows, row_class_name=TABLE_ROW_CLASS_NAME):
    data = []

    for row in rows:
        if row.get('class') == [row_class_name]:
            drawing_data = parse_drawing_details(row)
            if drawing_data:
                data.append(drawing_data)
                # data_row = [cell.text.strip() for cell in cells]

                # try:
                #     following_row = rows[i + 1]
                #     following_cells = following_row.find_all('td')
                #     data_row.extend([cell.text.strip() for cell in following_cells])

                #     data.append(data_row)
                # except IndexError:
                #     data.append(data_row)
            else:
                next
    return data

def parse_drawing_details(row):
  try:
    draw_date, jackpot_amount, winning_numbers = [item.get_text() for item in row.select('td b')]
    draw_date = datetime.strptime(draw_date, "%B %d, %Y")
    jackpot_amount = parse_money(jackpot_amount)
    return [draw_date, jackpot_amount, winning_numbers]

  except Exception as e:
      print(f'Error occurred while parsing row: {row}', file=sys.stderr)
      return None

def parse_money(money_str):
    """
    Parses a string representation of money and returns it as an integer.

    Parameters
    ----------
    money_str : str
        The money string to be parsed. For example: "$94.8 Million".

    Returns
    -------
    int
        The integer value of the parsed money string.
        For example, an input of "$94.8 Million" will return 94800000.

    Raises
    ------
    ValueError
        If the input string cannot be parsed.

    Examples
    --------
    >>> parse_money("$94.8 Million")
    94800000
    >>> parse_money("$1.04 Billion")
    1040000000
    """

    # Removing commas, dollar signs and converting the string to lowercase
    money_str = money_str.replace(',', '').replace('$', '').lower()

    # Extract the numerical value from the string
    if 'million' in money_str:
        multiplier = 1000000
        money_str = money_str.replace('million', '')
    elif 'billion' in money_str:
        multiplier = 1000000000
        money_str = money_str.replace('billion', '')
    else:
        multiplier = 1

    try:
        value = float(money_str.strip())
        return int(value * multiplier)
    except ValueError:
        raise ValueError(f"Unable to parse the input: {money_str}")




def write_to_csv(data, directory='.'):
    csv_filepath = os.path.join(directory, 'scraped_data.csv')
    try:
        with open(csv_filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    except Exception as e:
        print(f'Error occurred while writing to file: {str(e)}', file=sys.stderr)
        return None

    return csv_filepath

def main(directory='.'):
    # Get HTML content from URL
    html_content = get_html_content(URL)

    # Parse HTML for the target table
    rows = get_table_rows_from_html(html_content)

    # Parse table for data
    data = parse_rows(rows)

    # Write data to CSV
    result = write_to_csv(data, directory)

    if result is not None:
        print(WRITING_FILE_SUCCESS_STR + str(result))


if __name__ == '__main__':
    main()
