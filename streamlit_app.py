import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

DEV_MODE=False

@st.cache_data
def load_data():
	df_gender_neutral_names=pd.read_csv('data/gender_neutral_names.csv', index_col=0)
	return df_gender_neutral_names

def check_selected_names():
	tmp=[]
	has_illegal_name=False

	for name in st.session_state.selected_names:
		if name.isalpha():
			tmp.append(name)
		else:
			has_illegal_name=True

	if has_illegal_name:
		st.session_state.selected_names=tmp
	# if has_illegal_name:
	# 	st.sidebar.write("Please enter correct names.")

	# Capitalize the first letter
	return

def check_selected_years():
	if st.session_state.selected_years[1]==st.session_state.selected_years[0]:
		st.sidebar.error(f"You must select at least 2 years.")
		return False
	return True

def visualize(dataset):
	# Create a plot
	fig, ax = plt.subplots()

	sns.lineplot(data=dataset, x="Year", y="F_ratio", hue="Name", ax=ax)

	# Add a vertical span
	ax.axhspan(selected_f_ratio[0], selected_f_ratio[1], color='blue', alpha=0.1, label='Gender Neutral Range')

	# Add labels and title
	ax.set_xlabel('Year')
	ax.set_ylabel('Female /Female+Male (F_ratio)')
	ax.set_title('Trend of Gender Inclination')
	ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
	# ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
	# ax.yaxis.set_major_locator(ticker.MultipleLocator(0.1))
	# ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
	ax.set_xticklabels(ax.get_xticklabels(), rotation=90, size=4)

	# Add legend
	ax.legend()
	return fig

with st.sidebar:
	st.header('Search')

	selected_names = st.multiselect(
	    "What names do you have in mind? Up to 5 names.",
	    ["taylor", "morgan", "olivia", "michael"], # Use top 10 most used names
	    key="selected_names",
	    on_change=check_selected_names,
	    default=["taylor", "morgan"],
	    placeholder="Choose or type a name",
	    max_selections=5,
	    accept_new_options=True,
	    help="Choose at least 1 name to show the trend of its gender inclination."
	)

	selected_years = st.slider("Select a range of years", 1880, 2024, (1987, 2020), 
		help="Include at least 2 years to show the line chart.", 
		# on_change=check_selected_years,
		key="selected_years"
	)

	selected_f_ratio = st.slider("Select a range of female ratio of each name", 0.0004, 1.0, (0.3, 0.7), 
		format="%0.4f", 
		help="The larger the ratio, the more feminine the name is.",
		key="selected_f_ratio"
		)

	st.divider()

	st.header('About')
	txt_about='''
	About this app
	'''
	st.markdown(txt_about)

if DEV_MODE:
	st.sidebar.write(selected_names)
	st.sidebar.write(st.session_state)
	st.sidebar.write("Values:", selected_years)
	st.sidebar.write("Values:", selected_f_ratio)

st.title('Gender Neutral Names in the U.S. from 1880 to 2024')



Show_chart=True


# data_load_state = st.text('Loading data...')
df_gender_neutral_names = load_data()
# data_load_state.text('Loading data...done!')

if selected_years[1]==selected_years[0]:
	st.error(f"You must select at least 2 years.")
	Show_chart=False
else:
	df_gender_neutral_names=df_gender_neutral_names[(df_gender_neutral_names['Year'] >= selected_years[0]) & 
	    (df_gender_neutral_names['Year'] <= selected_years[1]) ]

if len(selected_names)<=0:
	st.error(f"You must select at least 1 name.")
	Show_chart=False
else:
	df_gender_neutral_names=df_gender_neutral_names[df_gender_neutral_names['Name'].isin(selected_names)]


if Show_chart:
	st.header('Change of gender neutrality')	
	st.pyplot(visualize(df_gender_neutral_names))


on = st.toggle("Show row data", value=True)

if on:
    st.write(df_gender_neutral_names)




#change of gender inclination, and the names that flipped gender inclination

