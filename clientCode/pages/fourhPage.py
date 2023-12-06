import dash
from dash import html
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from dataRequestService import requestor
import base64
from io import BytesIO

rq=requestor()
#df=
set=rq.get_venn_diagram()[1]

fig = venn3(subsets = set, set_labels = ('scopus_id', 'creators', 'subjects'))


# Save it to a temporary buffer.
buf = BytesIO()
plt.savefig(buf, format="png")
# Embed the result in the html output.
fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
img_src = f'data:image/png;base64,{fig_data}'


dash.register_page(__name__)


layout = html.Div([
    html.H1('Это базовая страница'),
    html.Div('Здесь ничего не будет'),
    html.Img(id='bar-graph-matplotlib',src=img_src)
])