import pandas as pd

def load_data(path='./scraped_data.csv'):
    return pd.read_csv(path)

def analyze_data(data):
    # Define pattern
    pattern = r'(?P<numbers>[\d-]+)/(?P<powerball>\d{1,2})/(?P<multiplier>(?:NA|\d))'

    # Apply pattern
    winning_details = data['winning_numbers'].str.extract(pattern)

    # Split 'numbers' into individual numbers considering possible extra hyphens
    numbers_split = winning_details['numbers'].str.split(r'-+', expand=True)
    numbers_split.columns = ['number_'+str(i+1) for i in range(5)]

    # Join the dataframes
    parsed_data = pd.concat([data, winning_details, numbers_split], axis=1)

    # reformat numbers to int type
    number_cols = ['number_'+str(i+1) for i in range(5)]
    for col in number_cols:
      parsed_data[col] = pd.to_numeric(parsed_data[col], errors='coerce')

    # Calculate the 5 most and least frequent individual numbers
    most_common_numbers = parsed_data[number_cols].melt()['value'].value_counts().head(5)
    least_common_numbers = parsed_data[number_cols].melt()['value'].value_counts().tail(5)

    # Calculate the 5 most and least common powerball selections
    most_common_powerballs = parsed_data['powerball'].value_counts().head(5)
    least_common_powerballs = parsed_data['powerball'].value_counts().tail(5)

    return {'most_common_numbers': most_common_numbers, 'least_common_numbers': least_common_numbers, 'most_common_powerballs': most_common_powerballs, 'least_common_powerballs': least_common_powerballs}

def print_summary(results_dict):
   print("The five most frequent individual numbers are: ", end="")
   print(', '.join([str(i) for i in results_dict['most_common_numbers'].index.values]), end="")
   print(" (", ', '.join([str(i) for i in results_dict['most_common_numbers'].values]), "times each respectively).")

   print("The five least frequent individual numbers are: ", end="")
   print(', '.join([str(i) for i in results_dict['least_common_numbers'].index.values]), end="")
   print(" (", ', '.join([str(i) for i in results_dict['least_common_numbers'].values]), "occurrences each respectively).")

   print("The most frequent powerball numbers are: ", end="")
   print(', '.join([str(i) for i in results_dict['most_common_powerballs'].index.values]), end="")
   print(" (", ', '.join([str(i) for i in results_dict['most_common_powerballs'].values]), "times each respectively).")

   print("The least frequent powerball numbers are: ", end="")
   print(', '.join([str(i) for i in results_dict['least_common_powerballs'].index.values]), end="")
   print(" (", ', '.join([str(i) for i in results_dict['least_common_powerballs'].values]), "occurrences each respectively).")


def main():
    print_summary(analyze_data(load_data()))

if __name__ == '__main__':
    main()
