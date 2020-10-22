#from app import app
from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import random

app = Flask(__name__)
@app.route('/')
#@app.route('/home', methods=['GET','POST'])
#def index():
#	return render_template('index.html', text = "PRESS FOR NAME")


@app.route('/home', methods=['GET','POST'])
def home():
	chosen_pre = ''
	chosen_suf = ''
	suf_description = ''
	pre_description = ''

	if request.method == 'POST':
		def filter_names(fname):
			lines = open(fname, 'r').readlines()
			names = []
			for line in lines:
				#ls = line.decode('utf-8').strip().split(" ")
				ls = line.strip().split(" ")
				int_table = []
				name = ls[0]
				int_table.append(name)
				if (len(ls) > 1) :
					rarity = ls[1]
					if rarity == "RARE" :
						int_table.append("RARE")
						#print("updating with rare rarity")
						descriptions =' '.join(ls[2:])
					else :
						int_table.append("common")
						descriptions =' '.join(ls[1:])
				else :
					int_table.append("RARE")
				#descriptions =' '.join(ls[1:])
				#print(descriptions)
				int_table.append(descriptions)
				names.append(int_table)

			return names

		sunce_pre_names = filter_names("static/sunce_pre.txt")
		#print(sunce_pre_names)

		sunce_suf_names = filter_names("static/sunce_suf.txt")
		#print(sunce_suf_names)

		asra_pre_names = filter_names("static/asra_pre.txt")
		#print(asra_pre_names)

		asra_suf_names = filter_names("static/asra_suf.txt")
		#print(asra_suf_names)

		cansu_pre_names = filter_names("static/cansu_pre.txt")
		#print(cansu_pre_names)

		cansu_suf_names = filter_names("static/cansu_suf.txt")
		#print(asra_suf_names)

		misc_pre_names = filter_names("static/misc_pre.txt")
		#print(misc_pre_names)

		misc_suf_names = filter_names("static/misc_suf.txt")
		#print(misc_suf_names)

		fail_pre_names = filter_names("static/fail_pre.txt")
		#print(fail_pre_names)

		fail_suf_names = filter_names("static/fail_suf.txt")
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


		add_to_dict(d, sunce_pre_names, "sunce", 'prefix')
		add_to_dict(d, sunce_suf_names, "sunce", "suffix")

		add_to_dict(d, asra_pre_names, "sunce", 'prefix')
		add_to_dict(d, asra_suf_names, "sunce", "suffix")

		add_to_dict(d, cansu_pre_names, "sunce", 'prefix')
		add_to_dict(d, cansu_suf_names, "sunce", 'suffix')

		add_to_dict(d, misc_pre_names, "sunce", 'prefix')
		add_to_dict(d, misc_suf_names, "sunce", "suffix")


		add_to_dict(d, fail_pre_names, "sunce", 'prefix')
		add_to_dict(d, fail_suf_names, "sunce", "suffix")
		#print(d['Haze']['description'])
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
		rare_pre_names = []
		for name, c in pre_d.items():
			pre_names.append(name)
			pre_descriptions.append(c['description'])
			pre_rarities.append(c['rarity'])
			if c['rarity'] == "RARE":
				rare_pre_names.append(name)




		pre_prob = []
		for r in pre_rarities:
			if r == "RARE":
				pre_prob.append(1)
			else:
				pre_prob.append(20)


		#pre_id = np.array([-7 for r in pre_rarities if r == "RARE" else 0])
		#pre_prob = np.exp(pre_id) / np.exp(pre_id).sum() #normalize probabilities
		#chosen_pre = np.random.choice(pre_names, p=pre_prob)
		chosen_pre = random.choices(pre_names, pre_prob, k = 1)[0]
		pre_description = d[chosen_pre]['description']


		suf_names = []
		suf_rarities = []
		rare_suf_names = []
		for name, c in suf_d.items():
			if name != chosen_pre:
				suf_names.append(name)
				suf_rarities.append(c['rarity'])
				if c['rarity'] == "RARE":
					rare_suf_names.append(name)

		#print(len(suf_names))
		#print(len(suf_prob))
		suf_prob = []
		for r in suf_rarities:
			if r == "RARE":
				suf_prob.append(1)
			else:
				suf_prob.append(20)

		#suf_prob = np.exp(suf_id) / np.exp(suf_id).sum() #normalize probabilities
		#print(len(suf_names))
		#print(len(suf_prob))

		#chosen_suf = np.random.choice(suf_names, p=suf_prob)
		chosen_suf = random.choices(suf_names, suf_prob, k = 1)[0]
		suf_description = d[chosen_suf]['description']

		#print("YOU ARE {} {}".format(chosen_pre, chosen_suf))
		#print("The name " + chosen_pre + " means: " + pre_description)
		#print("The name " + chosen_suf + " means: " + suf_description)



		return render_template('home.html', pre_name = chosen_pre, suf_name = chosen_suf, s_desc =  chosen_suf + " " + suf_description, p_desc =  chosen_pre + " " + pre_description)
	else:
		return render_template('home.html')

if __name__ == '__main__':
	app.debug = True
	#app.run(host = '0.0.0.0', port = 5000)
