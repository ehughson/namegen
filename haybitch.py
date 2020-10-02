import numpy as np 
def filter_names(fname):
	lines = open(fname, 'r', encoding="utf8").readlines()
	names = []
	for line in lines:
		ls = line.strip().split(" ")
		int_table = []
		name = ls[0]
		int_table.append(name)
		if (len(ls) > 1) :
			rarity = ls[1]
			if rarity == "RARE" : 
				int_table.append("RARE")
			else : 
				int_table.append("common") 
		else : 
			int_table.append("RARE")
		descriptions =' '.join(ls[1:])
		#print(descriptions)
		int_table.append(descriptions)
		names.append(int_table)

	return names

sunce_pre_names = filter_names("sunce_pre.txt")
#print(sunce_pre_names)

sunce_suf_names = filter_names("sunce_suf.txt")
#print(sunce_suf_names)

asra_pre_names = filter_names("asra_pre.txt")
#print(asra_pre_names)

asra_suf_names = filter_names("asra_suf.txt")
#print(asra_suf_names)

cansu_pre_names = filter_names("cansu_pre.txt")
#print(cansu_pre_names)

cansu_suf_names = filter_names("cansu_suf.txt")
#print(asra_suf_names)

misc_pre_names = filter_names("misc_pre.txt")
#print(misc_pre_names)

misc_suf_names = filter_names("misc_suf.txt")
#print(misc_suf_names)

fail_pre_names = filter_names("fail_pre.txt")
#print(fail_pre_names)

fail_suf_names = filter_names("fail_suf.txt")
#print(fail_suf_names)


def add_to_dict(d, names_rarities, house, t):
	for name, rarity, desc in names_rarities:
		if name not in d:
			d[name] = {}
			d[name]['rarity'] = rarity
			d[name]['house'] = [house]
			d[name]['type'] = t
			d[name]['description'] = desc
		else:
			if house not in d[name]['house']:
				d[name]['house'].append(house)


d = {}


add_to_dict(d, sunce_pre_names, "sunce", 'suffix')
add_to_dict(d, sunce_suf_names, "sunce", "prefix")
print(d['Haze']['description'])
# add all the other files to this dictions using this function

# split into prefix and suffix dicts
pre_d = {}
suf_d = {}

for name, c in d.items():
	if c['type'] == "prefix":
		pre_d[name] = c
	else:
		suf_d[name] = c


#print(pre_d)
pre_names = []
pre_rarities = []
pre_descriptions = []
for name, c in pre_d.items():
	pre_names.append(name)
	pre_descriptions.append(c['description'])
	pre_rarities.append(c['rarity'])



pre_id = []
for r in pre_rarities:
	if r == "RARE":
		pre_id.append(-7)
	else:
		pre_id.append(0)


#pre_id = np.array([-7 for r in pre_rarities if r == "RARE" else 0])
pre_prob = np.exp(pre_id) / np.exp(pre_id).sum()
chosen_pre = np.random.choice(pre_names, p=pre_prob)
pre_description = d[chosen_pre]['description']


suf_names = []
suf_rarities = []
for name, c in suf_d.items():
	if name != chosen_pre:
		suf_names.append(name)
		suf_rarities.append(c['rarity'])
#print(len(suf_names))
#print(len(suf_prob))
suf_id = []
for r in suf_rarities:
	if r == "RARE":
		suf_id.append(-7)
	else:
		suf_id.append(0)

suf_prob = np.exp(suf_id) / np.exp(suf_id).sum()
print(len(suf_names))
print(len(suf_prob))

chosen_suf = np.random.choice(suf_names, p=suf_prob)
suf_description = d[chosen_suf]['description']

print("YOU ARE {} {}".format(chosen_pre, chosen_suf))
print("The name " + chosen_pre + " means: " + pre_description)
print("The name " + chosen_suf + " means: " + suf_description)



