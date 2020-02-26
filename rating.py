import requests, json, time, datetime, sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdt


def plotRating(*ls):
	
	mn = 9999
	mx = 0
	spacing = 1
	contests = requests.get('https://dmoj.ca/api/contest/list').json()
	
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
		plt.plot(x, y, label = name + ' (' + str(y[-1]) + ')', marker = 's', markerfacecolor = 'white')

	colors = ['#d2d2d3', '#a0ff8f', '#adb0ff', '#f399ff', '#ffd363', '#ff3729', '#a11b00']
	rng = [[0, 1000], [1001, 1200], [1201, 1500], [1501, 1800], [1801, 2200], [2201, 3000], [3001, 9999]]

	for i in range(7):
		if mn - 200 > rng[i][1]:
			continue
		elif mx + 200 < rng[i][0]:
			break
		plt.axhspan(max(mn - 200, rng[i][0]), min(mx + 200, rng[i][1]), facecolor = colors[i])

	plt.gca().set_ylim([mn - 200, mx + 200])
	plt.gca().xaxis.set_major_formatter(mdt.DateFormatter('%m/%d/%Y'))
	plt.gca().xaxis.set_major_locator(mdt.DayLocator(interval = spacing))	
	plt.gcf().autofmt_xdate()
	plt.legend(loc = "upper left", prop = {"size": 8})
	plt.xlabel('Date')
	plt.ylabel('Rating')
	plt.grid(color = 'white')

	plt.show()
		
if __name__ == '__main__':
	ls = sys.argv
	plotRating(*ls[1:])