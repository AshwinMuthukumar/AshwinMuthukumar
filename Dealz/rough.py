import re

x = "%206565/6565/aasd5575"
y = re.findall(r'\d+',x)
print(int(y[0]))