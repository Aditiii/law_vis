# Transpose the DataFrame
json_thingy = pd.read_excel('Naloxone Overdose Prevention Laws Data.xlsx')

json_thingy.replace(0, 0, inplace=True)
json_thingy = json_thingy.fillna(0)
json_thingy.replace('.', 0, inplace=True)
json_thingy = json_thingy.groupby('Jurisdictions', as_index=False).last()
json_thingy = json_thingy.drop(columns=['Effective Date', 'Valid Through Date'])
# json_thingy.columns = json_thingy.columns.map(cd7)
# json_thingy.columns = json_thingy.columns.map(lambda x: cd7[x] if x in cd7 else x)

json_thingy.head()

json_thingy = json_thingy.set_index('Jurisdictions').T

# og_transposed_df = og_transposed_df.iloc[:len(og_transposed_df)//2, :len(og_transposed_df.columns)//2]
# og_transposed_df = og_transposed_df.iloc[:len(og_transposed_df.columns)//2]

# Load the states.csv file into a DataFrame
states_df = pd.read_csv('states.csv')

# Create a dictionary mapping state names to abbreviations
state_to_abbr = dict(zip(states_df['State'], states_df['Abbreviation']))

# Map state names to abbreviations in transposed_df
json_thingy.columns = json_thingy.columns.map(state_to_abbr.get)
json_thingy.head()

json_thingy.to_json('DirOpioidLiti.json', orient='index')
