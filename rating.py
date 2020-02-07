import requests, json, time, datetime, sys
import matplotlib.pyplot as mpp
import matplotlib.dates as mdt

contests = requests.get('https://dmoj.ca/api/contest/list').json();
spacing = 1
ls = sys.argv
ls.pop(0)

mn = 9999
mx = 0

for name in ls:
	time.sleep(1)
	obj = requests.get('https://dmoj.ca/api/user/info/' + name).json();
	rtg = obj['contests']['history']
	x = []
	y = []
	for item in rtg:
		pt = str(rtg[item]['rating'])
		if pt.isdigit():
			x.append(contests[item]['start_time'])
			y.append(rtg[item]['rating'])
			mn = min(mn, rtg[item]['rating'])
			mx = max(mx, rtg[item]['rating'])
	x = [datetime.datetime.strptime(i,'%Y-%m-%dT%H:%M:%S+00:00') for i in x]
	spacing = max(spacing, int((x[-1] - x[0]).days / 10))
	mpp.plot(x, y, label = name + ' (' + str(y[-1]) + ')', marker = 's', markerfacecolor = 'white')

colors = ['#d2d2d3', '#a0ff8f', '#adb0ff', '#f399ff', '#ffd363', '#ff3729', '#a11b00']
rng = [[0, 1000], [1001, 1200], [1201, 1500], [1501, 1800], [1801, 2200], [2201, 3000], [3001, 9999]]

for i in range(7):
	if mn - 200 > rng[i][1]:
		continue
	elif mx + 200 < rng[i][0]:
		break
	mpp.axhspan(max(mn - 200, rng[i][0]), min(mx + 200, rng[i][1]), facecolor = colors[i])

mpp.gca().set_ylim([mn - 200, mx + 200])
mpp.gca().xaxis.set_major_formatter(mdt.DateFormatter('%m/%d/%Y'))
mpp.gca().xaxis.set_major_locator(mdt.DayLocator(interval = spacing))	
mpp.gcf().autofmt_xdate()
mpp.legend(loc = "upper left", prop = {"size": 8})
mpp.xlabel('Date')
mpp.ylabel('Rating')
mpp.grid(color = 'white')

mpp.show()
	
