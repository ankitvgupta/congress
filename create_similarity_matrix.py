import os
import json
from collections import defaultdict
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def get_votes_directory():
	return os.getcwd() + "/congress/data/114/votes/2015"

def get_vote_filenames():
	path = get_votes_directory()
	files_wanted = []
	for subdir, dirs, files in os.walk(path):
	    for filename in files:
	    	if filename.endswith(".json"):
	        	files_wanted.append(os.path.join(subdir, filename))
	return files_wanted

def keep_passage_votes(vote_filenames):
	passage_filenames = []
	for vote_filename in vote_filenames:
		with open(vote_filename) as vote_file:
			data = json.load(vote_file)
			if data['category'] != "passage":
				continue
			passage_filenames.append(vote_filename)
	return passage_filenames

# Input: A dict where each element has a field "id"
def congressman_ids_from_dict(vote_dict):
	ids = []
	for element in vote_dict:
		ids.append((element["id"], element["party"]))
	return ids

vote_filenames =  get_vote_filenames()
passage_filenames = keep_passage_votes(vote_filenames)

def get_party_affiliations(bioguide_ids, parties):
	affiliation = {}
	for congressman, party in zip(bioguide_ids, parties):
		affiliation[congressman] = party
	return affiliation

def convert_affiliation_to_color(affil):
	if affil == "R" or affil == "r" or affil == "Republican" or affil == "republican":
		return 'red'
	elif affil == "D" or affil == "d" or affil == "Democrat" or affil == "democrat":
		return 'blue'
	else:
		return 'green'

voting_record = defaultdict(lambda: defaultdict(int))
votes = []
for passage_filename in passage_filenames:
	with open(passage_filename) as vote_file:
		data = json.load(vote_file)
		vote_id = data["vote_id"]
		for vote_type in data["votes"].keys():
			if vote_type == "Aye":
				user_ids = congressman_ids_from_dict(data["votes"]["Aye"]) 
				votes_to_add = [(uid, vote_id, 1.0, party) for uid, party in user_ids]
				votes += votes_to_add
			elif vote_type == "Yea":
				user_ids = congressman_ids_from_dict(data["votes"]["Yea"]) 
				votes_to_add = [(uid, vote_id, 1.0, party) for uid, party in user_ids]
				votes += votes_to_add
			elif vote_type == "Nay":
				user_ids = congressman_ids_from_dict(data["votes"]["Nay"]) 
				votes_to_add = [(uid, vote_id, -1.0, party) for uid, party in user_ids]
				votes += votes_to_add
			elif vote_type == "No":
				user_ids = congressman_ids_from_dict(data["votes"]["No"]) 
				votes_to_add = [(uid, vote_id, -1.0, party) for uid, party in user_ids]
				votes += votes_to_add
			elif vote_type == "Not Voting": 
				user_ids = congressman_ids_from_dict(data["votes"]["Not Voting"]) 
				votes_to_add = [(uid, vote_id, 0.0, party) for uid, party in user_ids]
				votes += votes_to_add
			elif vote_type == "Present":
				continue
			else:
				continue
print "Counting the number of votes"
print "Number of votes is:"
print "", len(votes)
print "Creating vote dataframe"
vote_df = pd.pivot_table(pd.DataFrame(votes), index=0, columns=1, values=2).fillna(0.0)
print "Doing PCA"
pca = PCA(2)
two_d_view = pca.fit_transform(vote_df)
print "Explained variance ratios:"
print pca.explained_variance_ratio_

print "Getting party affiliations"
party_affiliations = get_party_affiliations([x[0] for x in votes], [x[3] for x in votes])
party_affil_colored = pd.Series(party_affiliations).apply(convert_affiliation_to_color)
colors = party_affil_colored[vote_df.index]
print "Colors"
print colors
#print party_affil_colored.head()
print "Plotting"

print two_d_view
plt.figure()
plt.scatter(two_d_view[:, 0], two_d_view[:, 1], c=colors)
plt.show()






