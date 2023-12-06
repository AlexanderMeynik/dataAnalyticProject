import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from clientCode.dataRequestService import requestor
# Data
'''data = {
    'sets': ['scopus_id', 'creators', 'subjects', 'creators+scopus_id', 'subjects+scopus_id', 'subjects+creators', 'subjects+creators+scopus_id'],
    'counts': [324236, 321201, 306686, 257855, 257784, 306600, 404648]
}

# Create a DataFrame
df = pd.DataFrame(data)
print(df.loc[df['sets']=='scopus_id']['counts'])
set=(
df.loc[df['sets']=='scopus_id']['counts'].values[0],
df.loc[df['sets']=='creators']['counts'].values[0],
df.loc[df['sets']=='creators+scopus_id']['counts'].values[0],
df.loc[df['sets']=='subjects']['counts'].values[0],
df.loc[df['sets']=='subjects+scopus_id']['counts'].values[0],
df.loc[df['sets']=='subjects+creators']['counts'].values[0],
df.loc[df['sets']=='subjects+creators+scopus_id']['counts'].values[0],
)'''
rq=requestor()
df=rq.get_venn_diagram()
set=df[1]
fig=venn3(subsets = set, set_labels = ('scopus_id', 'creators', 'subjects'))
plt.show()